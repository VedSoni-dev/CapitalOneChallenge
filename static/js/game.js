class FinancialGame {
    constructor() {
        this.balance = 0;
        this.day = 0;
        this.gameHistory = [];
        this.currentScenario = null;
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
            this.showError('');
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
        let rewardImage = '';
        let rewardText = '';
        if (summary.final_balance >= 3250) {
            rewardImage = '/static/assets/images/gold-reward.png';
            rewardText = 'Gold Reward: 10% off at participating restaurants!';
        } else if (summary.final_balance >= 3000) {
            rewardImage = '/static/assets/images/silver-reward.png';
            rewardText = 'Silver Reward: 7.5% off at participating restaurants!';
        } else if (summary.final_balance >= 2750) {
            rewardImage = '/static/assets/images/bronze-reward.png';
            rewardText = 'Bronze Reward: 5% off at participating restaurants!';
        }
    
        const modalContent = `
            <h2 class="modal-title">Game Over</h2>
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
            ${rewardImage ? `
                <div class="reward-container">
                    <img src="${rewardImage}" alt="Reward" class="reward-image" />
                    <p class="reward-text">${rewardText}</p>
                </div>` : ''}
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
        
        // Add CSS for reward styling
        const style = document.createElement('style');
        style.textContent = `
            .reward-container {
                text-align: center;
                margin: 20px 0;
                padding: 20px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                animation: fadeIn 0.5s ease-out;
            }

            .reward-image {
                max-width: 200px;
                height: auto;
                margin-bottom: 10px;
                animation: scaleIn 0.5s ease-out;
            }

            .reward-text {
                color: #ffd700;
                font-size: 1.2rem;
                font-weight: bold;
                margin: 10px 0;
                animation: slideIn 0.5s ease-out;
            }

            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }

            @keyframes scaleIn {
                from { transform: scale(0); }
                to { transform: scale(1); }
            }

            @keyframes slideIn {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }

            .modal {
                background: var(--card-bg);
                padding: 2rem;
                border-radius: 1rem;
                max-width: 500px;
                width: 90%;
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                z-index: 1000;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                opacity: 0;
                transition: opacity 0.3s ease;
            }

            .overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.7);
                z-index: 999;
                opacity: 0;
                transition: opacity 0.3s ease;
            }

            .modal.active,
            .overlay.active {
                opacity: 1;
            }
        `;
        document.head.appendChild(style);
        
        // Trigger reflow before adding active class
        modal.offsetHeight;
        
        overlay.classList.add('active');
        modal.classList.add('active');
    }
}

// Initialize the game when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.game = new FinancialGame();
});

export default FinancialGame;