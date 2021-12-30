import chess
import chess.engine
import waitForInput


def main():

    #SimpleEngine spawns event loop and creates engine instance using stockfish.exe
    engine = chess.engine.SimpleEngine.popen_uci(r"C:/Users/seans/Desktop/SeniorDesignI/ProjectCode/src/stockfish_14_win_x64_avx2/stockfish_14_win_x64_avx2.exe")

    #create board
    board = chess.Board()

    #while the players have not agreed to a draw
    while not board.is_game_over():

        #read input from user
        waitForInput.microphoneReady()
        #read user inputted move
        with open('C:/Users/seans/Desktop/SeniorDesignI/ProjectCode/' + 'playerInput.txt') as f:
            sk1Key = f.read()
            f.close
        
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


    












