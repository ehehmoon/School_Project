import random

def flip():
    wl = random.choice(['player', 'com'])

    return wl

w_player = flip()
print(f'{w_player}이/가 선공입니다.')

game_board = [' ', ' ', ' ',
              ' ', ' ', ' ',
              ' ', ' ', ' ',]

def empty_spots(board):
    spots = []
    for x, spot in enumerate(board):
        if spot == ' ':
            spots.append(x)

    return spots

def valid_move(x):
    return x in empty_spots(game_board)

def move(x, player):
    if valid_move(x):
        game_board[x] = player
        return True
    return False

def draw(board):
    for i, spot in enumerate(board):
        if i % 3 == 0:
            print(f'\n---------------')
        print('|', spot, '|', end='')
    print(f'\n---------------')

def check_win(board, player):
    win_config = [
        [board[0], board[1], board[2]],
        [board[3], board[4], board[5]],
        [board[6], board[7], board[8]],
        [board[0], board[3], board[6]],
        [board[1], board[4], board[7]],
        [board[2], board[5], board[8]],
        [board[0], board[4], board[8]],
        [board[2], board[4], board[6]],
    ]
    return [player, player, player] in win_config

def evaluate(board):
    if check_win(board, 'X'):
        score = 1
    elif check_win(board, 'O'):
        score = -1
    else:
        score = 0
    return score

def game_over(board):
    return check_win(board, 'X') or check_win(board ,'O') or len(empty_spots(board)) == 0

def minimax(board, depth, maxPlayer):
    pos = -1
    if depth == 0 or len(empty_spots(board)) == 0 or game_over(board):
        return -1, evaluate(board)
    
    if maxPlayer:
        value = -99999
        for point in empty_spots(board):
            board[point] = 'X'

            x, score = minimax(board, depth - 1, False)
            board[point] = ' '
            if score > value:
                value = score
                pos = point

    else:
        value = 99999
        for point in empty_spots(board):
            board[point] = 'O'

            x, score = minimax(board, depth - 1, True)
            board[point] = ' '
            if score < value:
                value = score
                pos = point
            
    return pos, value


if w_player == 'com':
    player = 'O'
    com = 'X'
    draw(game_board)
    print('COM 차례입니다')
    i, _ =minimax(game_board, 9, com == 'X')
    move(i, com)
    draw(game_board)

else:
    player = 'X'
    com = 'O'


while True:
    if len(empty_spots(game_board)) == 0 or game_over(game_board):
        print('경기가 종료되었습니다\n')
        break

    while True:
        player_move = int(input('당신의 차례입니다. 0 ~ 8 중 하나의 위치를 선택하세요: '))

        if valid_move(player_move):
            move(player_move, player)
            draw(game_board)
            break

        else:
            print('유효하지 않은 위치입니다')

    print('COM 차례입니다')
    i, _ =minimax(game_board, 9, com == 'X')
    move(i, com)
    draw(game_board)

if check_win(game_board, 'X'):
    print('X 승리')

elif check_win(game_board, 'O'):
    print('O 승리')

else:
    print('비겼습니다!')

