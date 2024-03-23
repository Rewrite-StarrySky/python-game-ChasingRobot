import random,sys
import os
# 設定初始常量constants
Width = 40
Height = 20
Num_Robots = 10
Num_teleports = 2 # 可傳送次數
Num_Dead_Robots = 2
Num_Walls = 100

Empty_Space = ' '
Player = '@'
Robot = 'R'
Dead_Robot = 'X'
Wall = chr(9617) # Character 9617 is '░'
def main():
    #print({}.format(Num_teleports))
    #input('Press Enter to begin ...')
    # 設定新遊戲
    board = getNewBoard()
    robots = addRobots(board)
    playerPosition = getRandomEmptySpace(board,robots)
    while True:
        displayBoard(board,robots,playerPosition)

        if len(robots) == 0: # 檢查玩家是否贏得勝利
            print ('All the robots have crashed into each other and you')
            print ('lived to tell the tale! Good job')
            sys.exit()
            # 移動玩家與機器人:
        playerPosition = askForPlayerMove(board,robots,playerPosition)
        robots = moveRobots(board,robots,playerPosition)

        for x,y in robots: # 檢查玩家是否輸掉
            if(x,y) == playerPosition:
                displayBoard(board,robots,playerPosition)
                print('You have been caught by a robot!')
                sys.exit()
def getNewBoard():
    """返回一個字典表示棋盤.The keys are 棋盤位置整數索引的(x,y)元組,
    the values are Wall,Empty_Space,or Dead_Robot. The dictionary also has the key
    'teleports'表示玩家剩餘的傳送次數.存活的機器人被單獨存儲於棋盤字典之外"""
    board = {'teleports':Num_teleports}

    # 創建空棋盤:
    for x in range(Width):
        for y in range(Height):
            board[(x,y)] = Empty_Space

    # 在棋盤邊緣加入牆壁
    for x in range(Width):
        board[(x,0)] = Wall #上方的牆
        board[(x,Height-1)] = Wall # 下方的牆
    for y in range(Height):
        board[(0,y)] = Wall #上方的牆
        board[(Width-1,y)] = Wall # 下方的牆

    # 加入隨機的牆(場地內障礙物)
    for i in range(Num_Walls):
        x,y = getRandomEmptySpace(board,[])
        board[(x,y)] = Wall
    
    # 加入起始死亡的機器人
    for i in range(Num_Dead_Robots):
        x,y = getRandomEmptySpace(board,[])
        board[(x,y)] = Dead_Robot
    return board

def getRandomEmptySpace(board,robots):
    """返回棋盤上的空白區域(x,y)的整數元組"""
    while True:
        randomX = random.randint(1,Width - 2)
        randomY = random.randint(1,Height - 2)
        if isEmpty(randomX,randomY,board,robots):
            break
    return (randomX,randomY)

def isEmpty(x,y,board,robots): # 檢查位置是否是空置的
    """如果(x,y)在棋盤上的位置是空的也沒有機器人在此位置上返回True"""
    return board[(x,y)] == Empty_Space and (x,y) not in robots

def addRobots(board):
    """增加Num_Robots數量的機器人到棋盤的空閒區域上同時return a list of there(x,y)space 為機器人現在的位置"""
    robots = []
    for i in range(Num_Robots):
        x,y = getRandomEmptySpace(board,robots)
        robots.append((x,y))
    return robots

def displayBoard(board,robots,playerPosition):
    """dispaly board,robots,playerPosition on the screen"""
    # loop over every space on the board:
    os.system("cls") # 畫面刷新
    for y in range(Height):
        for x in range(Width):
            # 畫出所有board上的物件
            if board[(x,y)] == Wall:
                print(Wall,end='')
            elif board[(x,y)] == Dead_Robot:
                print(Dead_Robot,end='')
            elif (x,y) == playerPosition:
                print(Player,end='')
            elif (x,y) in robots:
                print(Robot,end='')
            else:
                print(Empty_Space,end='')
        print() # Print a newline.

def askForPlayerMove(board,robots,playerPosition):
    """返回玩家移動至(x,y)地方的整數元組,給玩家他們目前的位置與牆的位置""" 
    playerX,playerY = playerPosition

    # Find which directions aren't blocked by a wall:
    q = 'Q' if isEmpty(playerX - 1,playerY - 1,board,robots) else ' '
    w = 'W' if isEmpty(playerX + 0,playerY - 1,board,robots) else ' '
    e = 'E' if isEmpty(playerX + 1,playerY - 1,board,robots) else ' '
    d = 'D' if isEmpty(playerX + 1,playerY + 0,board,robots) else ' '
    c = 'C' if isEmpty(playerX + 1,playerY + 1,board,robots) else ' '
    x = 'X' if isEmpty(playerX + 0,playerY + 1,board,robots) else ' '
    z = 'Z' if isEmpty(playerX - 1,playerY + 1,board,robots) else ' '
    a = 'A' if isEmpty(playerX - 1,playerY + 0,board,robots) else ' '
    allMoves = (q + w + e + d + c + x + z + a + 'S')

    while True:
        # Get player's move:
        print('(T)eleports remaining:{}'.format(board["teleports"]))
        print('                   ({}) ({}) ({})'.format(q,w,e))
        print('                   ({}) (S) ({})'.format(a,d))
        print('Enter move or QUIT:({}) ({}) ({})'.format(z,x,c))
        print('')
        move = input('>').upper()
        if move == 'QUIT':
            print('Thanks for playing!')
            sys.exit()
        elif move == 'T' and board['teleports'] > 0:
            # 傳送玩家到隨機的空白位置
            board['teleports'] -= 1
            return getRandomEmptySpace(board,robots)
        elif move != 8 and move in allMoves:
            # Return the new player position based on their move:
            return {'Q':(playerX - 1,playerY - 1),
                    'W':(playerX + 0,playerY - 1),
                    'E':(playerX + 1,playerY - 1),
                    'D':(playerX + 1,playerY + 0),
                    'C':(playerX + 1,playerY + 1),
                    'X':(playerX + 0,playerY + 1),
                    'Z':(playerX - 1,playerY + 1),
                    'A':(playerX - 1,playerY + 0),
                    'S':(playerX,playerY)}[move]

def moveRobots(board,robotPositions,playerPosition):
    """Return a list of (x,y) tuple of new robots position 
    after they have tried to move toward the player"""        
    playerx,playery = playerPosition
    nextRobotPositions = []

    while len(robotPositions) > 0:
        robotx,roboty = robotPositions[0]

        #決定機器人的移動方向
        if robotx < playerx:
            movex = 1 # move right
        elif robotx > playerx:
            movex = -1 # move left
        elif robotx == playerx:
            movex = 0 # Don't move horizontally.

        if roboty < playery:
            movey = 1 # move up
        elif roboty > playery:
            movey = -1 # move down
        elif roboty == playery:
            movey = 0 #  don't move vertically.
        # 檢查機器人是否會撞到牆壁,然後調整行進方向:
        if board[(robotx + movex,roboty + movey)] == Wall:
            # 機器人碰撞到牆,所以產生一個new move:
            if board[(robotx + movex,roboty)] == Empty_Space:
                movey = 0 # Robot can't move horizontally.
            elif board[(robotx ,roboty + movey)] == Empty_Space:
                movex = 0 # Robot can't move vertically.
            else:
                # robot can't move.
                movex = 0
                movey = 0
        newRobotx = robotx + movex
        newRoboty = roboty + movey

        if(board[(robotx,roboty)] == Dead_Robot or board[(newRobotx,newRoboty)] == Dead_Robot):
            # 機器人被破壞在當前位置,將其移除
            del robotPositions[0]
            continue

            # 檢查兩個機器人是否移動(碰撞)至一起,然後如果是則摧毀他們
        if (newRobotx,newRoboty) in nextRobotPositions:
            board[(newRobotx,newRoboty)] = Dead_Robot
            nextRobotPositions.remove((newRobotx,newRoboty))
        else:
            nextRobotPositions.append((newRobotx,newRoboty))

            # remove robots from robotPositions as they move.
        del robotPositions[0]
    return nextRobotPositions

# 
if __name__ == '__main__':
    main()

    
