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
        
    ####PLAYER WILL ALWAYS PLAY AS WHITE

    #while game is not over, keep looping
    while (not board.is_game_over()):

        #reset these indicators on each move
        capture = False
        queenSideCastling = False
        kingSideCastling = False

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
            

            #store current move in move variable to check conditions
            move = board.push_san(playerMoveTextEdited) # if not working change parse_san() to push_san()

            #determine if it is a capturing move, need arm to remove captured piece
            if(board.is_capture(move)):
                capture = True
            else:
                capture = False

            #determine if it is a castling move, need arm to handle this special case (move both king and rook)
            if(board.is_kingside_castling(move)):
                kingSideCastling = True
            elif (board.is_queenside_castling(move)):
                queenSideCastling = True
            else:
                kingSideCastling = False
                queenSideCastling = False
            
            #determine if it is a en passant move, need arm to handle this special case
            if(board.is_en_passant(move)):
                enPassant = True
            else:
                enPassant = False

                
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

            #handle special cases of captures, castling, and en passant
            if (capture):
                arm.remove() #remove piece at toSquare
                arm.move(fromSquare, toSquare, currentPiece) # move piece at fromSquare to toSquare
            elif(kingSideCastling):
                arm.move('e1', 'g1', 'k') # move king
                arm.move('h1', 'f1', 'r') # move rook
            elif(queenSideCastling):
                arm.move('e1', 'c1', 'k') # move king
                arm.move('a1', 'd1', 'r') # move rook
            elif(enPassant):
                tempSplit = [char for char in toSquare]
                removeSquare = str(tempSplit[0]) + str(int(tempSplit[1]) + 1) 
                arm.remove() #remove piece at removeSquare
                arm.move(fromSquare, toSquare, currentPiece) # move piece at fromSquare to toSquare
            else:
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

            #determine if it is a capturing move, need arm to remove captured piece
            if(board.is_capture(engineResult.move)):
                capture = True
            else:
                capture = False

            #determine if it is a castling move, need arm to handle this special case (move both king and rook)
            if(board.is_kingside_castling(engineResult.move)):
                kingSideCastling = True
            elif (board.is_queenside_castling(engineResult.move)):
                queenSideCastling = True
            else:
                kingSideCastling = False
                queenSideCastling = False
            
            # #determine if it is a en passant move, need arm to handle this special case
            # if(board.is_en_passant(engineResult.move)):
            #     enPassant = True
            # else:
            #     enPassant = False


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


            #handle special cases of captures, castling, and en passant
            if (capture):
                arm.remove() #remove piece at toSquare
                arm.move(fromSquare, toSquare, currentPiece) # move piece at fromSquare to toSquare
            elif(kingSideCastling):
                arm.move('e8', 'g8', 'k') # move king 
                arm.move('h8', 'f8', 'r') # move rook
            elif(queenSideCastling):
                arm.move('e8', 'c8', 'k') # move king
                arm.move('a8', 'd8', 'r') # move rook 
            elif(enPassant):
                tempSplit = [char for char in toSquare]
                removeSquare = str(tempSplit[0]) + str(int(tempSplit[1]) - 1) 
                arm.remove() #remove piece at removeSquare
                arm.move(fromSquare, toSquare, currentPiece) # move piece at fromSquare to toSquare
            else:
                # Send in move to movement engine
                arm.move(fromSquare, toSquare, currentPiece)

            # Give time to finish any movements before returning to home
            sleep(2)
            arm.returnHome()

            print("\nCOMPUTER MOVE\n")
            print(board)

            playerTurn = True


    #ending game message
    if (board.is_checkmate()):
        print("Checkmate!")
    elif (board.is_stalemate()):
        print("Draw, stalemate!")
    elif (board.is_insufficient_material()):
        print("Draw, insufficeint material!")
    elif (board.is_fivefold_repetition()):
        print("Draw, repetition of moves!")
    elif (board.is_seventyfive_moves()):
        print("Draw, 75 move rule!")


    gripper.cleanup()
    arm.shutdown()
    #end of the game
    engine.quit()



main()