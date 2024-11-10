class GameUtils {
    static formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    }

    static formatPercentage(value) {
        return new Intl.NumberFormat('en-US', {
            style: 'percent',
            minimumFractionDigits: 1,
            maximumFractionDigits: 1
        }).format(value / 100);
    }

    static getRandomElement(array) {
        return array[Math.floor(Math.random() * array.length)];
    }

    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    static throttle(func, limit) {
        let inThrottle;
        return function executedFunction(...args) {
            if (!inThrottle) {
                func(...args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    static calculateStats(gameHistory) {
        return {
            totalGain: gameHistory.reduce((sum, record) => sum + record.outcome, 0),
            bestDecision: gameHistory.reduce((best, current) => 
                current.outcome > best.outcome ? current : best
            ),
            worstDecision: gameHistory.reduce((worst, current) => 
                current.outcome < worst.outcome ? current : worst
            ),
            averageOutcome: gameHistory.reduce((sum, record) => 
                sum + record.outcome, 0) / gameHistory.length
        };
    }

    static generateAchievement(action, value) {
        const achievements = {
            highBalance: [
                { threshold: 5000, title: "Financial Novice", message: "Reached $5,000 in balance" },
                { threshold: 10000, title: "Money Master", message: "Reached $10,000 in balance" },
                { threshold: 20000, title: "Wealth Wizard", message: "Reached $20,000 in balance" }
            ],
            goodDecisions: [
                { threshold: 3, title: "Sharp Mind", message: "Made 3 profitable decisions in a row" },
                { threshold: 5, title: "Strategic Thinker", message: "Made 5 profitable decisions in a row" },
                { threshold: 10, title: "Financial Genius", message: "Made 10 profitable decisions in a row" }
            ]
        };

        const category = achievements[action];
        if (!category) return null;

        return category.find(achievement => value >= achievement.threshold);
    }

    static getSkillDescription(skillLevel) {
        if (skillLevel >= 90) return "Expert";
        if (skillLevel >= 75) return "Advanced";
        if (skillLevel >= 60) return "Intermediate";
        if (skillLevel >= 40) return "Basic";
        return "Novice";
    }

    static validateChoice(choice, scenario) {
        return choice >= 0 && choice < scenario.choices.length;
    }

    static localStorage = {
        save(key, data) {
            try {
                localStorage.setItem(key, JSON.stringify(data));
                return true;
            } catch (error) {
                console.error('Error saving to localStorage:', error);
                return false;
            }
        },

        load(key) {
            try {
                const data = localStorage.getItem(key);
                return data ? JSON.parse(data) : null;
            } catch (error) {
                console.error('Error loading from localStorage:', error);
                return null;
            }
        },

        clear(key) {
            try {
                localStorage.removeItem(key);
                return true;
            } catch (error) {
                console.error('Error clearing localStorage:', error);
                return false;
            }
        }
    };
}

// Export for use in other files
export default GameUtils;