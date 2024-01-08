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
    board = chess.Board(fen)
    # extract fixed depth value
    fixed_depth = request.form.get('fixed_depth')
    # search for best move
    

    result = engine.analyse(board, chess.engine.Limit(depth=int(fixed_depth)))
    board.push(result.move)
    
    


    # update internal python chess board state
    
    # get best score
    try:
        # extract best move from PV
        best_move = result['pv'][0]
        
        
        
        # get best score
        try:
            score = -int(str(result['score'])) / 100
        
        except:
            score = str(result['score'])
            
            # inverse score
            if '+' in score:
                score = score.replace('+', '-')
            
            elif '-' in score:
                score = score.replace('-', '+')
          
        return {
            'fen': board.fen(),
            'best_move': str(best_move),
            'score': score,
            'depth': result['depth'],
            'pv': ' '.join([str(move) for move in result['pv']]),
            'nodes': result['nodes'],
            'time': result['time']
        }
    
    except:
        return {
            'fen': board.fen(),
            'score': '#+1'
        }

# main driver
if __name__ == '__main__':
    # start HTTP server
    app.run(debug=True, threaded=True)