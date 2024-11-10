


class FinancialGame {
    constructor() {
        this.balance = 0;
        this.day = 0;
        this.gameHistory = [];
        this.currentScenario = null;
        this.decisionsMade = 0;
        this.setupEventListeners();
    }

    setupEventListeners() {
        document.getElementById('startBtn')?.addEventListener('click', () => this.startGame());
    }

    async startGame() {
        try {
            const response = await fetch('/start_game');
            const data = await response.json();
            
            this.balance = data.initial_balance;
            this.updateUI('startScreen', 'none');
            this.updateUI('gameScreen', 'block');
            this.updateBalance(this.balance);
            this.updateDay(1);
            await this.getNextScenario();
            
            // Add initial animations
            document.querySelector('.status-bar').classList.add('slide-in');
            document.querySelector('.scenario').classList.add('fade-in');
        } catch (error) {
            this.showError('Failed to start game');
        }
    }

    async getNextScenario() {
        try {
            const response = await fetch('/get_scenario');
            const scenario = await response.json();
            this.currentScenario = scenario;
            
            this.updateScenario(scenario);
            this.animateScenarioTransition();
        } catch (error) {
            this.showError('Failed to get next scenario');
        }
    }

    updateScenario(scenario) {
        const scenarioElement = document.getElementById('scenarioText');
        const choicesContainer = document.getElementById('choicesContainer');
        
        // Clear previous content with fade-out
        scenarioElement.classList.add('fade-out');
        choicesContainer.classList.add('fade-out');
        
        setTimeout(() => {
            scenarioElement.textContent = scenario.question;
            choicesContainer.innerHTML = '';
            
            scenario.choices.forEach((choice, index) => {
                const button = this.createChoiceButton(choice, index, scenario.scenario_index);
                choicesContainer.appendChild(button);
            });
            
            // Fade in new content
            scenarioElement.classList.remove('fade-out');
            scenarioElement.classList.add('fade-in');
            choicesContainer.classList.remove('fade-out');
            choicesContainer.classList.add('fade-in');
        }, 300);
    }

    updateDecisionsCounter() {
        const decisionsDisplay = document.getElementById('decisionsDisplay');
        if (decisionsDisplay) {
            decisionsDisplay.textContent = this.decisionsMade;
            
            // Optional: Add animation for visual feedback
            decisionsDisplay.classList.add('counter-update');
            setTimeout(() => {
                decisionsDisplay.classList.remove('counter-update');
            }, 500);
        }
    }


    createChoiceButton(choice, index, scenarioIndex) {
        const button = document.createElement('button');
        button.textContent = choice;
        button.classList.add('choice-btn', 'choice-hover');
        button.addEventListener('click', () => this.makeChoice(scenarioIndex, index));
        return button;
    }

    async makeChoice(scenarioIndex, choiceIndex) {
        try {
            const response = await fetch('/play_scenario', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    scenario_index: scenarioIndex,
                    choice_index: choiceIndex
                })
            });
            
            const result = await response.json();

            this.decisionsMade++;
            this.updateDecisionsCounter();
            
            if (result.game_over) {
                this.endGame(result);
            } else {
                this.updateBalance(result.balance);
                this.updateDay(this.day + 1);
                await this.getNextScenario();
            }
        } catch (error) {
            this.showError('Failed to process choice');
        }
    }

    updateBalance(newBalance) {
        const balanceDisplay = document.getElementById('balanceDisplay');
        const oldBalance = parseFloat(balanceDisplay.textContent);
        
        // Add animation class based on balance change
        if (newBalance > oldBalance) {
            balanceDisplay.classList.add('balance-increase');
        } else if (newBalance < oldBalance) {
            balanceDisplay.classList.add('balance-decrease');
        }
        
        // Animate the number change
        this.animateNumber(balanceDisplay, oldBalance, newBalance, 1000);
        
        setTimeout(() => {
            balanceDisplay.classList.remove('balance-increase', 'balance-decrease');
        }, 1000);
    }

    animateNumber(element, start, end, duration) {
        const startTime = performance.now();
        const updateNumber = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const current = start + (end - start) * progress;
            element.textContent = Math.round(current).toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(updateNumber);
            }
        };
        
        requestAnimationFrame(updateNumber);
    }

    updateDay(newDay) {
        this.day = newDay;
        const dayDisplay = document.getElementById('dayDisplay');
        dayDisplay.textContent = `Day ${newDay}`;
        dayDisplay.classList.add('day-update');
        
        setTimeout(() => {
            dayDisplay.classList.remove('day-update');
        }, 1000);
    }

    updateUI(elementId, display) {
        const element = document.getElementById(elementId);
        if (element) {
            element.style.display = display;
        }
    }

    animateScenarioTransition() {
        const scenarioContainer = document.querySelector('.scenario-container');
        scenarioContainer.classList.add('scenario-transition');
        
        setTimeout(() => {
            scenarioContainer.classList.remove('scenario-transition');
        }, 500);
    }

    endGame(summary) {
        const modalContent = `
            <h2>Game Over</h2>
            <div class="summary-stats">
                <div class="stat">
                    <span class="stat-label">Final Balance</span>
                    <span class="stat-value">$${summary.final_balance.toLocaleString()}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Performance</span>
                    <span class="stat-value">${summary.performance_score.toFixed(1)}%</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Days Survived</span>
                    <span class="stat-value">${summary.day}</span>
                </div>
            </div>
            <button class="restart-btn" onclick="location.reload()">Play Again</button>
        `;
        
        this.showModal(modalContent);
    }

    showModal(content) {
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = content;
        
        const overlay = document.createElement('div');
        overlay.className = 'overlay';
        
        document.body.appendChild(overlay);
        document.body.appendChild(modal);
        
        // Trigger reflow before adding active class
        modal.offsetHeight;
        
        overlay.classList.add('active');
        modal.classList.add('active');
    }

    showError(message) {
        const errorToast = document.createElement('div');
        errorToast.className = 'error-toast';
        errorToast.textContent = message;
        document.body.appendChild(errorToast);
        
        // Add active class after a brief delay to trigger animation
        setTimeout(() => {
            errorToast.classList.add('active');
        }, 10);
        
        // Remove the toast after 3 seconds
        setTimeout(() => {
            errorToast.classList.remove('active');
            setTimeout(() => {
                errorToast.remove();
            }, 300); // Wait for fade-out animation to complete
        }, 3000);
    }
}

// Initialize the game when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.game = new FinancialGame();
});

export default FinancialGame;