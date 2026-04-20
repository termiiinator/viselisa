const wordDisplay = document.getElementById('wordDisplay');
const letterInput = document.getElementById('letterInput');
const guessButton = document.getElementById('guessButton');
const newGameButton = document.getElementById('newGameButton');
const hintsList = document.getElementById('hintsList');
const message = document.getElementById('message');
const usedLetters = document.getElementById('usedLetters');

function getCookie(name) {
    const cookieValue = document.cookie
        .split('; ')
        .find((row) => row.startsWith(`${name}=`));
    return cookieValue ? decodeURIComponent(cookieValue.split('=')[1]) : null;
}

function setHangmanLevel(mistakes, maxMistakes) {
    for (let i = 1; i <= maxMistakes; i += 1) {
        const part = document.getElementById(`hangman-${i}`);
        if (part) {
            part.classList.toggle('visible', i <= mistakes);
        }
    }
}

function lockControls(isLocked) {
    guessButton.disabled = isLocked;
    letterInput.disabled = isLocked;
}

function renderState(data) {
    wordDisplay.textContent = data.masked_word;
    usedLetters.textContent = `Ошибки: ${data.wrong_letters.join(', ') || '—'}`;
    setHangmanLevel(data.mistakes, data.max_mistakes);

    hintsList.innerHTML = '';
    data.hints.forEach((hint) => {
        const li = document.createElement('li');
        li.textContent = `${hint.label}: ${hint.value}`;
        hintsList.appendChild(li);
    });

    if (data.status === 'won') {
        message.textContent = `Победа! Слово: ${data.word}`;
        lockControls(true);
    } else if (data.status === 'lost') {
        message.textContent = `Поражение! Слово: ${data.word}`;
        lockControls(true);
    } else if (data.repeated) {
        message.textContent = 'Эта буква уже была.';
    } else {
        message.textContent = '';
        lockControls(false);
    }
}

async function startNewGame() {
    const response = await fetch('/api/game/new/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken') || '',
            'Content-Type': 'application/json',
        },
    });

    const data = await response.json();
    if (!response.ok) {
        message.textContent = data.detail || 'Ошибка запуска игры.';
        return;
    }

    letterInput.value = '';
    renderState(data);
}

async function guessLetter() {
    const raw = letterInput.value.trim().toLowerCase();
    if (!/^[a-z]$/.test(raw)) {
        message.textContent = 'Введите одну латинскую букву (a-z).';
        return;
    }

    const response = await fetch('/api/game/guess/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken') || '',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ letter: raw }),
    });
    const data = await response.json();

    if (!response.ok) {
        message.textContent = data.detail || 'Ошибка проверки буквы.';
        return;
    }

    letterInput.value = '';
    renderState(data);
}

guessButton.addEventListener('click', guessLetter);
newGameButton.addEventListener('click', startNewGame);
letterInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        guessLetter();
    }
});

// Start first game automatically when page opens.
startNewGame();
