document.addEventListener('DOMContentLoaded', () => {
    const socket = io();

    // Handle form submission for submitting a clue
    const clueForm = document.getElementById('clue-form');
    const clueInput = document.getElementById('clue-input');
    clueForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const clue = clueInput.value;
        socket.emit('submit_clue', clue);
        clueInput.value = '';
    });

    // Handle form submission for guessing a code word
    const guessForm = document.getElementById('guess-form');
    const guessInput = document.getElementById('guess-input');
    guessForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const guess = guessInput.value;
        socket.emit('guess_code_word', guess);
        guessInput.value = '';
    });

    // Handle form submission for sending a chat message
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const message = chatInput.value;
        socket.emit('chat_message', message);
        chatInput.value = '';
    });

    // Handle receiving game state updates
    socket.on('game_state', (data) => {
        const cluesList = document.getElementById('clues-list');
        cluesList.innerHTML = '';
        data.clues.forEach((clue) => {
            const li = document.createElement('li');
            li.textContent = clue;
            cluesList.appendChild(li);
        });

        const turnMessage = document.getElementById('turn-message');
        turnMessage.textContent = `It's ${data.players[data.current_turn]}'s turn`;

        if (data.correct) {
            alert('Correct guess!');
        }
    });

    // Handle receiving chat messages
    socket.on('chat_message', (message) => {
        const chatMessages = document.getElementById('chat-messages');
        const li = document.createElement('li');
        li.textContent = message;
        chatMessages.appendChild(li);
    });
});
