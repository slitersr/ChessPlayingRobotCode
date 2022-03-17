from distutils.errors import UnknownFileError
from boardTracker import BoardTracker
from robot import Robot
import chess
import chess.engine
import time
import waitForInput

def main():

    #SimpleEngine spawns event loop and creates engine instance using stockfish.exe

    engine = chess.engine.SimpleEngine.popen_uci(r"../data/stockfish_14_win_x64_avx2/stockfish_14_x64_avx2.exe")

    #create board
    board = chess.Board()

    #player will always play as white for now, will start with first move
    playerTurn = True

    robot = Robot()
    robot.initRobot()

    boardTracker = BoardTracker()

    #while game is not over, keep looping
    while (not board.is_game_over()) and (not board.is_checkmate()) and (not board.is_stalemate()):

        # players turn: enter move and it will be played by arm
        if(playerTurn):
            input("Press enter to start recording...")

            #read input from user
            playerMoveText = waitForInput.microphoneReady()
            #make lowercase text
            playerMoveTextEdited = playerMoveText.lower()
            #get rid of any whitespace in voice inputted string
            playerMoveTextEdited = playerMoveTextEdited.replace(' ', '')

            #while loop below handles incorrect input
            legalPlayerInput = False
            while(not legalPlayerInput):
                try:
                    #if player inputted move is not legal then loop back and ask for move again
                    if(chess.Move.from_uci(playerMoveTextEdited) not in board.legal_moves):
                        input("Illegal move, press enter to start recording again...")
                        playerMoveText = waitForInput.microphoneReady()
                        playerMoveTextEdited = playerMoveText.lower()
                        playerMoveTextEdited = playerMoveTextEdited.replace(' ', '')
                    else:
                        legalPlayerInput = True
                except BaseException as e:
                    input("Incorrect input, press enter to start recording again...")
                    playerMoveText = waitForInput.microphoneReady()
                    playerMoveTextEdited = playerMoveText.lower()
                    playerMoveTextEdited = playerMoveTextEdited.replace(' ', '')
                    continue
                break
                
            # perform players move on stockfish
            board.push_san(playerMoveTextEdited)

            # here is where we would move the physical board peice
            fromSquare = playerMoveText.split(' ')[0]
            toSquare = playerMoveText.split(' ')[1]

            # Checks if the board is occupied by opposing team and 
            if BoardTracker.checkIfOccupied(toSquare) == 'b':
                robot.remove(toSquare, 'b')
            elif BoardTracker.checkIfOccupied(toSquare) == 'w':
                ValueError("This square is already occupied by same team. Check if stockfish is working correctly")
            
            # Update board tracker with new move
            BoardTracker.addMove(fromSquare, toSquare, 'w')

            # Send in move to movement engine
            robot.move(fromSquare, toSquare)

            # give time to finish any movements before returning to home
            time.sleep(2)
            robot.returnHome()

            print("\nPLAYER MOVE\n")

            print(board)

            playerTurn = False

        # robots turn: calculate engineResult and perform move with robot
        else:   
            # evaluate best move
            engineResult = engine.play(board, chess.engine.Limit(time=0.1))
            # perform computers move on stockfish
            board.push(engineResult.move)

            # Get the substring of return from engine of move
            fromSquare = str(engineResult.move.uci)[41:43].upper()
            toSquare = str(engineResult.move.uci)[43:45].upper()

            # Checks if the board is occupied by opposing team and 
            if BoardTracker.checkIfOccupied(toSquare) == 'w':
                robot.remove(toSquare, 'w')
            elif BoardTracker.checkIfOccupied(toSquare) == 'b':
                ValueError("This square is already occupied by same team. Check if stockfish is working correctly")
            
            # Update board tracker with new move
            BoardTracker.addMove(fromSquare, toSquare, 'b')

            # Send in move to movement engine
            robot.move(fromSquare, toSquare)

            # Give time to finish any movements before returning to home
            time.sleep(2)
            robot.returnHome()

            print("\nCOMPUTER MOVE\n")
            print(board)

            playerTurn = True


    #ending game message
    if (board.is_game_over()):
        print("Game is a draw!")
    elif (board.is_checkmate()):
        print("Checkmate!")
    elif (board.is_stalemate()):
        print("Stalemate, game is a draw!")


    robot.shutdown()
    #end of the game
    engine.quit()



main()