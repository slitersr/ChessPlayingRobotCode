from distutils.errors import UnknownFileError
from robot import Arm
from robot import Gripper
from time import sleep
import chess
import chess.engine
import waitForInput

def main():

    #SimpleEngine spawns event loop and creates engine instance using stockfish.exe

    # WINDOWS:
    # engine = chess.engine.SimpleEngine.popen_uci(r"../data/stockfish_14_win_x64_avx2/stockfish_14_x64_avx2.exe")
    
    # LINUX:
    engine = chess.engine.SimpleEngine.popen_uci(r"/home/pi/.local/share/Trash/files/stockfish_14.1_linux_x64/Stockfish/src/stockfish")

    #create board
    board = chess.Board()

    #player will always play as white for now, will start with first move
    playerTurn = True
    
    gripper = Gripper()
    gripper.init()
    gripper.calibrate()
    
    arm = Arm()
    arm.init(gripper)
    arm.calibrate()
        

    #while game is not over, keep looping
    while (not board.is_game_over()) and (not board.is_checkmate()) and (not board.is_stalemate()):

        # players turn: enter move and it will be played by arm
        if(playerTurn):
            
            invalidInput = True
            
            while(invalidInput):
                try:
                    response = input("Press enter to start recording...")
                    
                    #dev tool for inputting move through keyboard by inputting '1'
                    if response == 1:
                        playerMoveText = input("Enter move: ")                       
                    else:
                        playerMoveText = waitForInput.microphoneReady()
                        
                    playerMoveTextEdited = playerMoveText.lower()
                    playerMoveTextEdited = playerMoveTextEdited.replace(' ', '')
                        
                    if chess.Move.from_uci(playerMoveTextEdited) not in board.legal_moves:
                        print("Illegal move. Try again.")
                    else:
                        invalidInput = False
                except BaseException as e:
                    print("Incorrect input. Try again.")
                continue

                
            # perform players move on stockfish
            board.push_san(playerMoveTextEdited)

            #Get the substrings for player move
            fromSquare = playerMoveText.split(' ')[0]
            fromSquare = fromSquare.lower()
            toSquare = playerMoveText.split(' ')[1]
            toSquare = toSquare.lower()

            #get current piece
            currentPiece = board.piece_at(chess.parse_square(toSquare))
            currentPiece = str(currentPiece)
            currentPiece = currentPiece.lower()

            # Send in move to movement engine
            arm.move(fromSquare, toSquare, currentPiece)

            # give time to finish any movements before returning to home
            sleep(2)
            arm.returnHome()

            print("\nPLAYER MOVE\n")

            print(board)

            playerTurn = False

        # AI turn: calculate engineResult and perform move with AI
        else:   
            # evaluate best move
            engineResult = engine.play(board, chess.engine.Limit(time=0.1))

            # perform computers move on stockfish
            board.push(engineResult.move)

            # Get the substring of return from engine of move
            fromSquare = str(engineResult.move.uci)[41:43].upper()
            fromSquare = fromSquare.lower()
            toSquare = str(engineResult.move.uci)[43:45].upper()
            toSquare = toSquare.lower()

            #get current piece
            currentPiece = board.piece_at(chess.parse_square(toSquare))
            currentPiece = str(currentPiece)
            currentPiece = currentPiece.lower()

            # Send in move to movement engine
            arm.move(fromSquare, toSquare, currentPiece)

            # Give time to finish any movements before returning to home
            sleep(2)
            arm.returnHome()

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


    gripper.cleanup()
    arm.shutdown()
    #end of the game
    engine.quit()



main()