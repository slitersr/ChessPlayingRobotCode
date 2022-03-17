class Board:

    board = [10][10]
    
    def Board():
        Board.board = [['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
                ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b']
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
                ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']
                ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']]

    def addMove(fromSquare, toSquare, team):
        col_start = ord(fromSquare[0]) - 64 - 1
        row_start = int(fromSquare[1]) - 1

        col_end = ord(toSquare[0]) - 64 - 1
        row_end = int(toSquare[1]) - 1

        Board.board[row_start][col_start] = '0'

        if team == 'b':
            Board.board[row_end][col_end] = 'b'
        else:
            Board.board[row_end][col_end] = 'w'

    def checkIfOccupied(fromSquare, toSquare):
        col_start = ord(fromSquare[0]) - 64 - 1
        row_start = int(fromSquare[1]) - 1

        col_end = ord(toSquare[0]) - 64 - 1
        row_end = int(toSquare[1]) - 1

        if Board.board[row_end][col_end] == '0':
            return '0'
        elif Board.board[row_end][row_end] == 'w':
            return 'w'
        elif Board.board[row_end][row_end] == 'b':
            return 'b'

        ValueError("No sqaure type found. Check board setup.")