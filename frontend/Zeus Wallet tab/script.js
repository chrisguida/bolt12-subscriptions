const app = document.getElementById('app');
const content = document.getElementById('content');
const buttonsContainer = document.getElementById('buttons');

const mainMenuButtons = [
    { icon: '⚡', text: 'Lightning', amount: '0 sats' },
    { icon: '💼', text: 'On-chain', amount: '0 sats' },
    { icon: '📃', text: 'Subscriptions/Bills', amount: '0 sats' },
];

const subscriptionsButtons = [
    { icon: '⚡', text: 'CFE', amount: '0 sats' },
    { icon: '📞', text: 'Telmex', amount: '0 sats' },
    { icon: '💧', text: 'Siapa', amount: '0 sats' },
    { icon: '🛒', text: 'Amazon Prime', amount: '0 sats' },
];

const cfeButtons = [
    { icon: '💳', text: 'Manual Payment' },
    { icon: '❌', text: 'Unsubscribe' },
];

function createButton(button, onClick) {
    const btn = document.createElement('button');
    btn.className = 'button';
    btn.innerHTML = `
        <div class="button-left">
            <span class="button-icon">${button.icon}</span>
            ${button.text}
        </div>
        ${button.amount ? `<span>${button.amount}</span>` : ''}
    `;
    btn.onclick = onClick;
    return btn;
}

function showMainMenu() {
    buttonsContainer.innerHTML = '';
    mainMenuButtons.forEach(button => {
        const btn = createButton(button, () => {
            if (button.text === 'Subscriptions/Bills') {
                showSubscriptionsMenu();
            }
        });
        buttonsContainer.appendChild(btn);
    });
}

function showSubscriptionsMenu() {
    buttonsContainer.innerHTML = '';
    subscriptionsButtons.forEach(button => {
        const btn = createButton(button, () => {
            if (button.text === 'CFE') {
                showCFEMenu();
            }
        });
        buttonsContainer.appendChild(btn);
    });
    const backButton = createButton({ icon: '⬅️', text: 'Back' }, showMainMenu);
    buttonsContainer.appendChild(backButton);
}

function showCFEMenu() {
    buttonsContainer.innerHTML = '';
    const balanceText = document.createElement('p');
    balanceText.textContent = 'Pending Balance: $0.00';
    balanceText.style.textAlign = 'center';
    balanceText.style.marginBottom = '20px';
    buttonsContainer.appendChild(balanceText);

    cfeButtons.forEach(button => {
        const btn = createButton(button, () => {
            // Handle button click (e.g., manual payment or unsubscribe)
        });
        buttonsContainer.appendChild(btn);
    });
    const backButton = createButton({ icon: '⬅️', text: 'Back' }, showSubscriptionsMenu);
    buttonsContainer.appendChild(backButton);
}

// Initialize the app
showMainMenu();

