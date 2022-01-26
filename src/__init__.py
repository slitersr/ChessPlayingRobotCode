import chess
import chess.engine
import waitForInput


def main():

    #SimpleEngine spawns event loop and creates engine instance using stockfish.exe
    engine = chess.engine.SimpleEngine.popen_uci(r"C:/Users/seans/Desktop/SeniorDesignI/ProjectCode/src/stockfish_14_win_x64_avx2/stockfish_14_win_x64_avx2.exe")

    #create board
    board = chess.Board()

    #player will always play as white for now, will start with first move
    playerTurn = True

    #while game is not over, keep looping
    while (not board.is_game_over()) and (not board.is_checkmate()) and (not board.is_stalemate()):

        #if it is players turn have player enter move/ move will be played by arm
        if(playerTurn):
            #read input from user
            playerMoveText = waitForInput.microphoneReady()

            #get rid of any whitespace in voice inputted string
            playerMoveText.replace(" ", "")

            #if player inputted move is not legal then loop back and ask for move again
            while(not chess.Move.from_uci(player_move) in board.legal_moves):
                player_move = input("Enter move")

            # make sure move satisfies mate condition. If not pick new move
            board.push(player_move)

            #make it the engine's turn after the player has gone
            playerTurn = False

        #if it's the robots turn, calculate engineResult.move and perform move with robot
        else:   
            # evaluate best move
            engineResult = engine.play(board, chess.engine.Limit(time=0.1))
            # perform move
            board.push(engineResult.move)

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

