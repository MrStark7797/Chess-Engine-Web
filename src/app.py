#
# Web based GUI for BBC chess engine
#

# packages
from flask import Flask
from flask import render_template
from flask import request
import chess
import chess.engine
import chess.pgn
import io
import random
from flask import jsonify
from flask import Response
from flask_pymongo import PyMongo
from datetime import datetime
import json
import asyncio
import re


engine = chess.engine.SimpleEngine.popen_uci('./engine/slice.exe')
# create web app instance
app = Flask(__name__)

# define root(index) route
@app.route('/')
def root():
    return render_template('Analysis.html')
# make move API
@app.route('/make_move', methods=['POST'])
def make_move():
    # extract FEN string from HTTP POST request body
    fen = request.form.get('fen')

    # init python chess board instance
    analysboard = chess.Board(fen)
    board = chess.Board(fen)
    # search for best move
    
    fixed_depth = request.form.get('fixed_depth')
    
    result = engine.play(board, chess.engine.Limit(depth=fixed_depth))


    

    info = engine.analyse(analysboard, chess.engine.Limit(depth=6))
    # update internal python chess board state
    board.push(result.move)
    
    # extract FEN from current board state
    fen = board.fen()
    old_score = str(info['score'])
    
    
    score = re.sub('[PovScore(Cp(), BLACK) WHITE]', '', old_score)
    
    
    try:
            score = -int(str(score)) / 100
        
    except:
        score = str(score) + 'Centi-Pawns'
        if '+' in score:
                score = score.replace('+', '-')
            
        elif '-' in score:
            score = score.replace('-', '+')
         

    
    return {
        'fen': fen,
        'best_move': str(result.move),
        'score': score,

        'nodes': info['nodes'],
        'time': info['time']
    }
    
@app.route('/play')
def analytics():
    return render_template('Play.html')

# main driver
if __name__ == '__main__':
    # start HTTP server
    app.run(debug=True, threaded=True)