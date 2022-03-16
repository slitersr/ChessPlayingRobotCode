class BoardTracker:

    # Note that this board is flipped with stockfish. That is because of the way python indexes.
    board = [['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
             ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
             ['0', '0', '0', '0', '0', '0', '0', '0'],
             ['0', '0', '0', '0', '0', '0', '0', '0'],
             ['0', '0', '0', '0', '0', '0', '0', '0'],
             ['0', '0', '0', '0', '0', '0', '0', '0'],
             ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
             ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],]

    def addMove(fromSquare, toSquare, team):
        col_start = ord(fromSquare[0]) - 64 - 1
        row_start = int(fromSquare[1]) - 1

        col_end = ord(toSquare[0]) - 64 - 1
        row_end = int(toSquare[1]) - 1

        BoardTracker.board[row_start][col_start] = '0'

        if team == 'b':
            BoardTracker.board[row_end][col_end] = 'b'
        else:
            BoardTracker.board[row_end][col_end] = 'w'

    def checkIfOccupied(toSquare):
        col_end = ord(toSquare[0]) - 64 - 1
        row_end = int(toSquare[1]) - 1

        if BoardTracker.board[row_end][col_end] == '0':
            return '0'
        elif BoardTracker.board[row_end][row_end] == 'w':
            return 'w'
        elif BoardTracker.board[row_end][row_end] == 'b':
            return 'b'

        ValueError("No sqaure type found. Check board setup.")