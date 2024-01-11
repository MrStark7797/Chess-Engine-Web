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
import werkzeug
import os


engine = chess.engine.SimpleEngine.popen_uci('./engine/slice.exe')
png_path = "static/pngstore/"
scoreArr = []
moveArr = []
best_scoreArr = []
best_moveArr = []


ALLOWED_EXTENSIONS = {'pgn'}
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



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/upload_PGN', methods=['POST'])
def upload_PGN():
    # gets file
    if 'file' in request.files:
        file = request.files['file']
        # checks if file is pgn
        if file and allowed_file(file.filename):
            filename = werkzeug.utils.secure_filename(file.filename)
            file.save(os.path.join(png_path, file.filename))  
            pgn = open(os.path.join(png_path, file.filename))
            
            # gets pgn
            gamePGN = chess.pgn.read_game(pgn)
        else:
            return 'Not Valid PGN'
    else:
        return 'No File'
    print("Pass: File Save and get PGN \n")
    # init python chess board instance
    board = gamePGN.board()
    for move in gamePGN.mainline_moves():
        # push move
        board.push(move)
        # init python chess board instance with best move for analysis
        analysboard = board

        print("Pass: push move \nMove:", len(moveArr), "\n")
        
        if (board.is_game_over() == True):
            outcome = board.outcome()
            if(outcome.result() == '1-0'):
                scoreArr.append(300) 
                best_moveArr.append(move)
                best_scoreArr.append(300) 
            elif (outcome.result() == '0-1'):
                scoreArr.append(-300)
                best_moveArr.append(move)
                best_scoreArr.append(-300) 

            else:
                scoreArr.append(0)
                board.pop()
                if (len(moveArr) != 1):
        
                    analysboard = board
                    playboard = board
                else:
                    analysboard = chess.Board()
                    playboard = chess.Board()
                    check = 1
        
                print("Boards Set\n")
                # init python chess board instance with best move
        
                # gets best move and best score
                best_result = engine.play(playboard, chess.engine.Limit(depth=6))
                best_info = engine.analyse(analysboard, chess.engine.Limit(depth=6))
                print("Best Score Got\n")
                # remove extras
                best_old_score = str(best_info['score'])    
                best_score = re.sub('[PovScore(Cp(), BLACK) WHITE]', '', best_old_score)
                if (chess.Color() == True):

                    best_score = int(str(best_score)) / 100
                else:
                    best_score = -int(str(best_score)) / 100
                    
                # update arrays
                best_scoreArr.append(best_score)
                best_moveArr.append(str(best_result.move))
                print("Best Score added\n")
                # add played move back on to board so next move can be analysed
        
                board.push(move)            
            moveArr.append(move)
            print("Game Over")
            break
        print('Pass: Check\n')
        fixed_depth = request.form.get('fixed_depth')
        info = engine.analyse(analysboard, chess.engine.Limit(depth=6))

        print("Score Got\n")
        # remove extras
        old_score = str(info['score'])    
        score = re.sub('[PovScore(Cp(), BLACK) WHITE]', '', old_score)
        if (chess.Color() == True):

            score = int(str(score)) / 100
        else:
            best_score = -int(str(score)) / 100
                  

        # update arrays
        scoreArr.append(score)
        moveArr.append(move)
        print("Score added\n")
        # pop to check best move
        board.pop()
        if (len(moveArr) != 1):
        
            analysboard = board
            playboard = board
        else:
            analysboard = chess.Board()
            playboard = chess.Board()
            check = 1
        
        print("Boards Set\n")
        # init python chess board instance with best move
        
        # gets best move and best score
        best_result = engine.play(playboard, chess.engine.Limit(depth=6))
        best_info = engine.analyse(analysboard, chess.engine.Limit(depth=6))
        print("Best Score Got\n")
        # remove extras
        best_old_score = str(best_info['score'])    
        best_score = re.sub('[PovScore(Cp(), BLACK) WHITE]', '', best_old_score)
        if (chess.Color() == True):

            best_score = int(str(best_score)) / 100
        else:
            best_score = -int(str(best_score)) / 100
                  

        # update arrays
        best_scoreArr.append(best_score)
        best_moveArr.append(str(best_result.move))
        print("Best Score added\n")
        # add played move back on to board so next move can be analysed
        
        board.push(move)

    print("Score:\n")
    for x in scoreArr:
         print(x)
    print("Move:\n")
    for x in moveArr:
         print(x)
    print("Best Score:\n")
    for x in best_scoreArr:
         print(x)
    print("Best Move:\n")
    for x in best_moveArr:
         print(x)
    return ''


        
    
@app.route('/next_move', methods=['POST'])
def next_move():
    fen = request.form.get('fen')
    board = chess.Board(fen)
    movePly = board.ply()
    if(movePly > len(scoreArr)):
         return ''
    
    score = scoreArr[movePly]
    move = moveArr[movePly]
    best_score = best_scoreArr[movePly]
    best_move = best_moveArr[movePly]
    print("Score:", score,"\n")

    print("Move:", move,"\n")

    print("Best Score:", best_score,"\n")
  
    print("Best Move:", best_move,"\n")
    
    
    board.push(move)
    fen = board.fen()
    movePly =+ 1
    return {
        'fen': fen,
        'move': str(move),
        'score': score,
        'best_move': str(best_move),
        'best_score': best_score,  
    }
    
@app.route('/prev_move', methods=['POST'])
def prev_move():
    fen = request.form.get('fen')
    board = chess.Board(fen)
    movePly = board.ply()
    board.reset()
    
    if(movePly > len(scoreArr) + 1):
         return ''
    nPly = 0
    while nPly < movePly - 1:
        board.push(moveArr[nPly])
        nPly += 1
        print(board.fen())
    
    
    
    score = scoreArr[movePly - 2]
    move = moveArr[movePly - 2]
    best_score = best_scoreArr[movePly - 2]
    best_move = best_moveArr[movePly - 2]
    print("Score:", score,"\n")

    print("Move:", move,"\n")

    print("Best Score:", best_score,"\n")
  
    print("Best Move:", best_move,"\n")
    
    
    fen = board.fen()
    movePly =- 1
    return {
        'fen': fen,
        'move': str(move),
        'score': score,
        'best_move': str(best_move),
        'best_score': best_score,  
    }
    

    
    
# main driver
if __name__ == '__main__':
    # start HTTP server
    app.run(debug=True, threaded=True)