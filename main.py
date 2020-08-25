from flask import Flask
from flask import render_template, redirect, request
from chess import WebInterface, Board
import random

app = Flask(__name__)
ui = WebInterface()
game = Board()

class Stack:
    def __init__(self):
        self.data = []
    def push(self, value):
        self.data.append(value)
    def pop(self):
        return self.data.pop(len(self.data) - 1)
    def top(self):
        return self.data[-1]
    def length(self):
        return len(self.data)

movstack = Stack()

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
    ui.errmsg = ""
    ui.btnlabel = 'Move'
    return redirect('/play')

@app.route('/play')
def play():
    # TODO: get player move from GET request object
    # TODO: if there is no player move, render the page template
    pinput = request.args.get('player_input', None)
    if pinput != None:
        if pinput == "undo":
            if movstack.length() == 0:
                print('no more undos so go suck it')
                ui.errmsg = random.choice(['No more undos for you','HoW bOuT nO?','What you gona do? Cry?','Make me','Undo what?'])
                ui.errmsg += " (Nothing to undo)"
            else:
                end, start = movstack.pop()
                print(end, start)
                game.move(start, end)
                ui.board = game.display()
                game.next_turn()
        elif game.valinput(pinput) != 69:
            ui.errmsg = game.valinput(pinput) 
            pinput = "-"
        else:
            ui.errmsg = ""
            start, end = pinput.split(' ')
            start = (int(start[0]), int(start[1]))
            end = (int(end[0]), int(end[1]))
            game.update(start, end)
            movstack.push((start, end))
            ui.board = game.display()
            if game.pawnscanpromote():
                return redirect('/promote')
            game.next_turn()


    return render_template('chess.html', ui=ui, pin=pinput)
    # TODO: Validate move, redirect player back to /play again if move is invalid
    # If move is valid, check for pawns to promote
    # Redirect to /promote if there are pawns to promote, otherwise 

@app.route('/promote')
def promote():
    pinput = request.args.get('promo', None)
    if pinput != None:
        game.promotepawns(PieceClass=pinput)
        ui.board = game.display()
        game.next_turn()
        return redirect('/play')
    return render_template('promote.html')

app.run('0.0.0.0')