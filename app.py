from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
socketio = SocketIO(app)

class Game:
    def __init__(self):
        self.players = []
        self.clues = []
        self.code_words = []
        self.current_turn = 0

    def add_player(self, player_name):
        self.players.append(player_name)

    def generate_clues(self):
        # Generate random clues for each player
        self.clues = [str(random.randint(1000, 9999)) for _ in range(len(self.players))]

    def generate_code_words(self):
        # Generate random code words
        words = ['apple', 'banana', 'cherry', 'date', 'elderberry']
        self.code_words = random.sample(words, 4)

    def update_game_state(self):
        self.current_turn = (self.current_turn + 1) % len(self.players)

game = Game()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/new_game', methods=['POST'])
def new_game():
    game.add_player(request.form.get('player_name'))
    return render_template('game.html', game=game)

@app.route('/join_game', methods=['POST'])
def join_game():
    game.add_player(request.form.get('player_name'))
    return render_template('game.html', game=game)

@app.route('/start_game', methods=['POST'])
def start_game():
    game.generate_clues()
    game.generate_code_words()
    return render_template('game.html', game=game)

@socketio.on('submit_clue')
def submit_clue(clue):
    game.clues[game.current_turn] = clue
    game.update_game_state()
    emit('game_state', {'clues': game.clues, 'current_turn': game.current_turn}, broadcast=True)

@socketio.on('guess_code_word')
def guess_code_word(guess):
    correct = guess == game.code_words[game.current_turn]
    game.update_game_state()
    emit('game_state', {'clues': game.clues, 'current_turn': game.current_turn, 'correct': correct}, broadcast=True)

@socketio.on('chat_message')
def chat_message(message):
    emit('chat_message', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
