from flask import Flask
from flask import render_template, redirect, request
from chess import WebInterface, Board

app = Flask(__name__)
ui = WebInterface()
game = Board()

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/newgame')
def newgame():
    # Note that in Python, objects and variables
    # in the global space are available to
    # top-level functions
    game.start()
    ui.board = game.display()
    ui.inputlabel = f'{game.turn} player: '
    ui.errmsg = "No Errors Here"
    ui.btnlabel = 'Move'
    return redirect('/play')

@app.route('/play')
def play():
    # TODO: get player move from GET request object
    # TODO: if there is no player move, render the page template
    pinput = request.args.get('player_input', None)
    if pinput != None:
        if game.valinput(pinput) != 69:
            ui.errmsg = game.valinput(pinput) 
            pinput = "-"
        else:
            ui.errmsg = ""
            start, end = pinput.split(' ')
            start = (int(start[0]), int(start[1]))
            end = (int(end[0]), int(end[1]))
            game.update(start, end)
            ui.board = game.display()
            game.next_turn()


    return render_template('chess.html', ui=ui, pin=pinput)
    # TODO: Validate move, redirect player back to /play again if move is invalid
    # If move is valid, check for pawns to promote
    # Redirect to /promote if there are pawns to promote, otherwise 

@app.route('/promote')
def promote():
    pass

app.run('0.0.0.0')