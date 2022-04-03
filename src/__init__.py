from distutils.errors import UnknownFileError
from boardTracker import BoardTracker
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
        
    boardTracker = BoardTracker()

    #while game is not over, keep looping
    while (not board.is_game_over()) and (not board.is_checkmate()) and (not board.is_stalemate()):

        # players turn: enter move and it will be played by arm
        if(playerTurn):
            
            invalidInput = True
            
            while(invalidInput):
                try:
                    response = input("Press enter to start recording...")
                    
                    if response == 1:
                        playerMoveText = input("Enter move: ")                       
                    else:
                        playerMoveText = waitForInput.microphoneReady()
                        
                    playerMoveTextEdited = playerMoveText.lower()
                    playerMoveTextEdited = playerMoveTextEdited.replace(' ', '')
                        
#                     if len(playerMoveText) > 5 or len(playerMoveText) < 5:
#                         print("Incorrect input. Try again.")
                    if chess.Move.from_uci(playerMoveTextEdited) not in board.legal_moves:
                        print("Illegal move. Try again.")
                    else:
                        invalidInput = False
                except BaseException as e:
                    print("Incorrect input. Try again.")
                continue

                
#             response = input("Press enter to start recording...")
#             
#             if response == 1:
#                 #read input from user
#                 playerMoveText = input("Enter move: ")                       
#             else:
#                 playerMoveText = waitForInput.microphoneReady()
#                 
#             #make lowercase text
#             playerMoveTextEdited = playerMoveText.lower()
#             #get rid of any whitespace in voice inputted string
#             playerMoveTextEdited = playerMoveTextEdited.replace(' ', '')
# 
#             #while loop below handles incorrect input
#             legalPlayerInput = False
#             while(not legalPlayerInput):
#                 try:
#                     #if player inputted move is not legal then loop back and ask for move again
#                     if(chess.Move.from_uci(playerMoveTextEdited) not in board.legal_moves):
#                         response = input("Illegal move, press enter to start recording again...")
#                         if response == 1:
#                             #read input from user
#                             playerMoveText = input("Enter move: ")                       
#                         else:
#                             playerMoveText = waitForInput.microphoneReady()
#                         playerMoveTextEdited = playerMoveText.lower()
#                         playerMoveTextEdited = playerMoveTextEdited.replace(' ', '')
#                     else:
#                         legalPlayerInput = True
#                 except BaseException as e:
#                     response = input("Incorrect input, press enter to start recording again...")
#                     if response == 1:
#                         #read input from user
#                         playerMoveText = input("Enter move: ")                       
#                     else:
#                         playerMoveText = waitForInput.microphoneReady()
#                     playerMoveTextEdited = playerMoveText.lower()
#                     playerMoveTextEdited = playerMoveTextEdited.replace(' ', '')
#                     continue
#                 break
                
            # perform players move on stockfish
            board.push_san(playerMoveTextEdited)

            # here is where we would move the physical board peice
            fromSquare = playerMoveText.split(' ')[0]
            toSquare = playerMoveText.split(' ')[1]

            # Checks if the board is occupied by opposing team and 
            if BoardTracker.checkIfOccupied(toSquare) == 'b':
                arm.remove(toSquare, 'b')
            elif BoardTracker.checkIfOccupied(toSquare) == 'w':
                ValueError("This square is already occupied by same team. Check if stockfish is working correctly")
            
            # Update board tracker with new move
            piece = BoardTracker.addMove(fromSquare, toSquare, 'w')

            # Send in move to movement engine
            arm.move(fromSquare, toSquare, piece)

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
            toSquare = str(engineResult.move.uci)[43:45].upper()

            # Checks if the board is occupied by opposing team and 
            if BoardTracker.checkIfOccupied(toSquare) == 'w':
                arm.remove(toSquare, 'w')
            elif BoardTracker.checkIfOccupied(toSquare) == 'b':
                ValueError("This square is already occupied by same team. Check if stockfish is working correctly")
            
            # Update board tracker with new move
            piece = BoardTracker.addMove(fromSquare, toSquare, 'b')

            # Send in move to movement engine
            arm.move(fromSquare, toSquare, piece)

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