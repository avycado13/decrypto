from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app)

# Game state variables
teams = {
    'team1': {
        'secret_words': ['apple', 'banana', 'cherry', 'date'],
        'clue': '',
        'clue_count': 0,
        'guess': '',
        'score': 0
    },
    'team2': {
        'secret_words': ['elephant', 'giraffe', 'hippo', 'jaguar'],
        'clue': '',
        'clue_count': 0,
        'guess': '',
        'score': 0
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    team = data['team']
    join_room(team)
    emit('join_success', {'team': team})

@socketio.on('submit_clue')
def handle_submit_clue(data):
    team = data['team']
    clue = data['clue']
    clue_count = data['clue_count']
    
    # Validate clue and clue count
    if not validate_clue(clue):
        emit('clue_error', {'message': 'Invalid clue'})
        return
    
    if not validate_clue_count(clue_count):
        emit('clue_error', {'message': 'Invalid clue count'})
        return
    
    teams[team]['clue'] = clue
    teams[team]['clue_count'] = clue_count
    emit('clue_submitted', {'team': team}, room=team)

@socketio.on('guess_code_word')
def guess_code_word(guess):
    correct = guess == game.code_words[game.current_turn]
    game.update_game_state()
    emit('game_state', {'clues': game.clues, 'current_turn': game.current_turn, 'correct': correct}, broadcast=True)

@socketio.on('chat_message')
def chat_message(message):
    emit('chat_message', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
