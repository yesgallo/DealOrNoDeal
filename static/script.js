let selectedCase = null;
let revealedCases = [];
let gameState = {
    selected: [],
    values: [],
    revealed: []
};

// Selección de un maletín
function selectPlayerCase(caseId) {
    const caseButton = document.getElementById(`case${caseId}`);
    const caseButtons = document.querySelectorAll('.case');

    // Deseleccionar el maletín previamente seleccionado
    caseButtons.forEach(button => button.classList.remove('selected'));

    // Seleccionar el maletín actual
    caseButton.classList.add('selected');
    selectedCase = caseId;

    // Opcionalmente, puedes ocultar el valor del maletín seleccionado
    // caseButton.querySelector('img').style.display = 'none';
}

// Función para hacer una oferta del banquero
function makeBankerOffer() {
    // Ejemplo de implementación, puedes modificar según tu lógica
    alert('El banquero hará una oferta.');
}

// Función para aceptar la oferta
function deal() {
    if (selectedCase === null) {
        alert('Por favor, selecciona un maletín primero.');
        return;
    }

    // Manejar la lógica para aceptar la oferta aquí
    alert('Has aceptado la oferta.');
}

// Función para rechazar la oferta
function noDeal() {
    if (selectedCase === null) {
        alert('Por favor, selecciona un maletín primero.');
        return;
    }

    // Manejar la lógica para rechazar la oferta aquí
    alert('Has rechazado la oferta.');
}

// Actualiza los valores visibles en la tabla después de abrir los maletines
function updateValues(value) {
    const valueItems = document.querySelectorAll('.value-item');

    valueItems.forEach(item => {
        if (item.getAttribute('data-value') === value) {
            item.classList.add('removed');
        }
    });
}

// Función para abrir un maletín y actualizar la tabla de valores
function revealCase(caseId) {
    if (!revealedCases.includes(caseId)) {
        const caseValue = document.querySelector(`#case${caseId} img`).getAttribute('data-value');
        updateValues(caseValue);
        revealedCases.push(caseId);

        // Actualizar el estado del juego
        gameState.revealed = revealedCases;
        saveGameState();
    }
}

// Guarda el estado del juego en el campo oculto
function saveGameState() {
    // Asume que `getGameState` es una función que obtiene el estado actual del juego
    const gameState = {
        selected: selectedCase,
        values: Array.from(document.querySelectorAll('.value-item')).map(item => item.dataset.value),
        revealed: revealedCases
    };
    const gameStateInput = document.getElementById('game-state-input');
    gameStateInput.value = JSON.stringify(gameState); // Convierte el estado del juego a JSON
}
// Agregar eventos para guardar el estado del juego
document.querySelectorAll('.case').forEach(button => {
    button.addEventListener('click', saveGameState);
});

document.querySelector('#buttons button').addEventListener('click', saveGameState);
