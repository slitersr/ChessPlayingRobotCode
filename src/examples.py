import chess
import chess.engine


board = chess.Board()

#example API uses

#the following command returns false, board.legal_moves checks legal moves for given piece
chess.Move.from_uci("a8a1") in board.legal_moves


#example of moving a piece once you know it is a legal move
board.push_san("Qxf7")


#example initialization of the stockfish engine
engine = chess.engine.SimpleEngine.popen_uci(r"C:/Users/seans/Desktop/SeniorDesignI/ProjectCode/src/stockfish_14_win_x64_avx2/stockfish_14_win_x64_avx2.exe")

#example game loop
#board = chess.Board()
while not board.is_game_over():
    result = engine.play(board, chess.engine.Limit(time=0.1))
    board.push(result.move)

engine.quit()

#code for analyzing the score of a position
with engine.analysis(chess.Board()) as analysis:
    for info in analysis:
        print(info.get("score"), info.get("pv"))

        # Arbitrary stop condition.
        if info.get("seldepth", 0) > 20:
            break

#check if it is checkmate on each move
board.is_checkmate()