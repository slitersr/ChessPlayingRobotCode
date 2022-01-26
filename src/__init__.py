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

    #while the players have not agreed to a draw
    while not board.is_game_over():

        # check if checkmate. if not continue game

        #if it is players turn have player enter move/ move will be played by arm
        if(playerTurn):
            #read input from user
            player_move = waitForInput.microphoneReady()

            #convert player move

            #if player inputted move is not legal then loop back and ask for move again
            while(not chess.Move.from_uci(player_move) in board.legal_moves):
                player_move = input("Enter move")

            # make sure move satisfies mate condition. If not pick new move

            board.push_san(player_move)

            # commit move on robot

            #read user inputted move
            # with open('C:/Users/seans/Desktop/SeniorDesignI/ProjectCode/' + 'playerInput.txt') as f:
            #     playerInput = f.read()
            #     f.close

            #make it the engine's turn after the player has gone
            playerTurn = False

        #if it's the robots turn, calculate engineResult.move and perform move with robot
        else:   
            # evaluate best move
            engineResult = engine.play(board, chess.engine.Limit(time=0.1))
            # perform move
            board.push(engineResult.move)

            # do game checks (checkmate/mate)


            #make it the players move again
            playerTurn = True





        ####do stuff with player input
        






        #if it is not stalemate or checkmate end the game with proper result
        if(not board.is_stalemate and not board.is_checkmate):
            #play move inputted by player
            #push structured player input string into result structure and push onto board

            #the bottom two lines currently play stockfish against itself/// find how to input player move?
            result = engine.play(board, chess.engine.Limit(time=0.1))
            board.push(result.move)
        else:
            #if its stalemate print it
            if(board.is_stalemate):
                print("Stalemate...")
            
            #if its checkmate print it 
            if(board.is_checkmate):
                print("Checkmate...")
            
            return

    engine.quit()


    












