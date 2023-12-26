document.addEventListener('DOMContentLoaded', () => {
  const socket = io();

  // Join the game
  socket.emit('join', { team: 'team1' });

  // Handle join success event
  socket.on('join_success', (data) => {
    console.log(`Joined team: ${data.team}`);
  });

  // Handle clue submitted event
  socket.on('clue_submitted', (data) => {
    const { team } = data;
    const clueElement = document.getElementById(`${team}-clue`);
    clueElement.textContent = `Clue: ${data.clue}`;
  });

  // Handle guess submitted event
  socket.on('guess_submitted', (data) => {
    const { team } = data;
    const guessElement = document.getElementById(`${team}-guess`);
    guessElement.textContent = `Guess: ${data.guess}`;
  });

  // Handle game state updated event
  socket.on('game_state_updated', (data) => {
    const { teams } = data;

    for (const [team, teamData] of Object.entries(teams)) {
      const scoreElement = document.getElementById(`${team}-score`);
      scoreElement.textContent = `Score: ${teamData.score}`;
    }
  });

  // Handle clue form submission
  const clueForm = document.getElementById('clue-form');
  clueForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const clueInput = document.getElementById('clue-input');
    const clueCountInput = document.getElementById('clue-count-input');
    const clue = clueInput.value;
    const clueCount = parseInt(clueCountInput.value);

    socket.emit('submit_clue', { team: 'team1', clue, clue_count: clueCount });

    clueInput.value = '';
    clueCountInput.value = '';
  });

  // Handle guess form submission
  const guessForm = document.getElementById('guess-form');
  guessForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const guessInput = document.getElementById('guess-input');
    const guess = guessInput.value;

    socket.emit('submit_guess', { team: 'team1', guess });

    guessInput.value = '';
  });
});
