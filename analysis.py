import chess
import chess.pgn
import chess.engine
import pandas as pd
import numpy as np
import statistics

board = chess.Board()
stockfish = chess.engine.SimpleEngine.popen_uci('/usr/games/stockfish')
MATE_EVAL = 100000
CP_THRESHOLD = 1000
SHORT_GAME_THRESHOLD = 5
DEPTH = 10

def compute_evals(board, game, engine, depth):
    limit = chess.engine.Limit(depth=depth)
    evals = [engine.analyse(board, limit)['score'].white()]

    for move in game.mainline_moves():
        if board.is_game_over():
            break

        board.push(move)
        eval = engine.analyse(board, limit)['score'].white()
        evals.append(eval)
    return evals

def compute_cpl(evals, mate_eval, cp_threshold):
    white_cpl = []
    black_cpl = []
    from itertools import pairwise
    for i, eval in enumerate(pairwise(evals)):
        diff = eval[0].score(mate_score=mate_eval) - eval[1].score(mate_score=mate_eval)
        if abs(diff) > cp_threshold:
            continue
        if i % 2 == 0:
            white_cpl.append(max(diff, 0))
        else:
            black_cpl.append(max(-diff, 0)) 
    
    return white_cpl, black_cpl

def process_pgn(file, df):
    game_num = 0
    year = None
    while True:
        game = chess.pgn.read_game(file)
        game_num += 1
        if game is None:
            break
        
        output = {}
        headers = game.headers
        # ensure each championship has one year
        if year is None:
            year = int(headers['Date'][:4])
        output['white'] = headers['White']
        output['black'] = headers['Black']
        output['ECO'] = headers['ECO']
        output['opening'] = headers['Opening']

        board.reset()
        evals = compute_evals(board, game, stockfish, DEPTH)
        white_cpl, black_cpl = compute_cpl(evals, MATE_EVAL, CP_THRESHOLD)

        # ignore short games
        if len(white_cpl) < SHORT_GAME_THRESHOLD or len(black_cpl) < SHORT_GAME_THRESHOLD:
            continue
        output['white ACPL'] = statistics.mean(white_cpl)
        output['black ACPL'] = statistics.mean(black_cpl)
        output['combined ACPL'] = output['white ACPL'] + output['black ACPL']
        output['white num moves'] = len(white_cpl)
        output['black num moves'] = len(black_cpl)

        df.loc[(year, game_num), :] = output

columns = ['year', 'game number', 'white', 'black', 'white num moves', 'black num moves', 'white ACPL', 'black ACPL', 'combined ACPL', 'ECO', 'opening']
data = pd.DataFrame(columns=columns)
data.set_index(['year', 'game number'], inplace=True)

rel_path = 'project/pgns/'
output_path = 'project/analysis.csv'
champs_path = 'project/champs.csv'
nstudies = 47
nbroadcasts = 2
for i in range(nstudies):
    path = f'{rel_path}study{i}.pgn'
    with open(path, 'r') as f:
        process_pgn(f, data)

for i in range(nbroadcasts):
    path = f'{rel_path}broadcast{i}.pgn'
    with open(path, 'r') as f:
        process_pgn(f, data)

champs = pd.read_csv(champs_path) 
champs.columns = ['year', 'WC']
champs.set_index('year', inplace=True)
data = data.join(champs)
data.to_csv(output_path)