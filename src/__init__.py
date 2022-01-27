from distutils.errors import UnknownFileError
import chess
import chess.engine
import waitForInput


def main():

    #SimpleEngine spawns event loop and creates engine instance using stockfish.exe
    engine = chess.engine.SimpleEngine.popen_uci(r"C:/Users/seans/Desktop/SeniorDesignI/ProjectCode/src/stockfish_14_win_x64_avx2/stockfish_14_x64_avx2.exe")

    #create board
    board = chess.Board()

    #player will always play as white for now, will start with first move
    playerTurn = True

    # robot.reset()

    #while game is not over, keep looping
    while (not board.is_game_over()) and (not board.is_checkmate()) and (not board.is_stalemate()):

        #if it is players turn have player enter move/ move will be played by arm
        if(playerTurn):
            input("Press enter to start recording...")

            #read input from user
            playerMoveText = waitForInput.microphoneReady()

            #make lowercase text
            playerMoveText = playerMoveText.lower()
            #get rid of any whitespace in voice inputted string
            playerMoveText = playerMoveText.replace(' ', '')

            #while loop below handles incorrect input
            condition = False
            while(not condition):
                try:
                    #if player inputted move is not legal then loop back and ask for move again
                    if(chess.Move.from_uci(playerMoveText) not in board.legal_moves):
                        input("Illegal move, press enter to start recording again...")
                        playerMoveText = waitForInput.microphoneReady()
                        playerMoveText = playerMoveText.lower()
                        playerMoveText = playerMoveText.replace(' ', '')
                    else:
                        condition = True
                except BaseException as e:
                    input("Illegal move, press enter to start recording again...")
                    playerMoveText = waitForInput.microphoneReady()
                    playerMoveText = playerMoveText.lower()
                    playerMoveText = playerMoveText.replace(' ', '')
                    continue
                break
                

            
            # make sure move satisfies mate condition. If not pick new move
            board.push_san(playerMoveText)

            # here is where we would move the physical board peice
            # firstHalfplayerMoveText = playerMoveText.split(' ')[0]
            # secondHalfplayerMoveText = playerMoveText.split(' ')[1]
            #robot.move(firstHalfplayerMoveText, secondHalfplayerMoveText)

            print("\nPLAYER MOVE\n")

            print(board)

            #make it the engine's turn after the player has gone
            playerTurn = False

        #if it's the robots turn, calculate engineResult.move and perform move with robot
        else:   
            # evaluate best move
            engineResult = engine.play(board, chess.engine.Limit(time=0.1))
            # perform move
            board.push(engineResult.move)

            print("\nCOMPUTER MOVE\n")
            print(board)

            #make it the players move again
            playerTurn = True


    #ending game message
    if (board.is_game_over()):
        print("Game is a draw!")
    elif (board.is_checkmate()):
        print("Checkmate!")
    elif (board.is_stalemate()):
        print("Stalemate, game is a draw!")


    #end of the game
    engine.quit()







main()