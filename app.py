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

@socketio.on('submit_guess')
def handle_submit_guess(data):
    team = data['team']
    guess = data['guess']
    
    # Validate guess
    if not validate_guess(guess):
        emit('guess_error', {'message': 'Invalid guess'})
        return
    
    teams[team]['guess'] = guess
    emit('guess_submitted', {'team': team}, room=team)
    
    # Check if both teams have submitted their guesses
    if teams['team1']['guess'] and teams['team2']['guess']:
        # Update game state and calculate scores
        update_game_state()
        emit('game_state_updated', {'teams': teams}, broadcast=True)

def validate_clue(clue):
    # Add your validation logic here
    if len(clue) < 3:
        return False
    return True

def validate_clue_count(clue_count):
    # Add your validation logic here
    if not isinstance(clue_count, int) or clue_count < 1 or clue_count > 4:
        return False
    return True

def validate_guess(guess):
    # Add your validation logic here
    if len(guess) < 3:
        return False
    return True

def update_game_state():
    # Add your game logic here
    # Update the scores, check for correct guesses, etc.
    for team in teams.values():
        secret_words = team['secret_words']
        guess = team['guess']
        score = 0

        # Check if the guess matches any of the secret words
        for word in secret_words:
            if word == guess:
                score += 1

        # Update the team's score
        team['score'] += score

        # Reset the guess for the next round
        team['guess'] = ''

        # Add any additional game logic here

        # Emit an event to update the team's score on the client-side
        emit('score_updated', {'team': team, 'score': team['score']}, room=team)

        # Reset the game state for the next round
        team['clue'] = ''
        team['clue_count'] = 0

    # Add any additional game logic here

    # Emit an event to update the game state on the client-side
    emit('game_state_updated', {'teams': teams}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
