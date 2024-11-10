class GameAnimations {
    static async animateScenarioTransition(oldContent, newContent, container) {
        // Fade out old content
        container.style.opacity = '0';
        container.style.transform = 'translateY(20px)';
        
        // Wait for fade out
        await new Promise(resolve => setTimeout(resolve, 300));
        
        // Update content
        container.innerHTML = newContent;
        
        // Fade in new content
        container.style.opacity = '1';
        container.style.transform = 'translateY(0)';
    }

    static createConfetti() {
        for (let i = 0; i < 100; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.setProperty('--delay', `${Math.random() * 5}s`);
            confetti.style.setProperty('--rotation', `${Math.random() * 360}deg`);
            confetti.style.setProperty('--position', `${Math.random() * 100}%`);
            document.body.appendChild(confetti);
            
            // Remove after animation
            setTimeout(() => confetti.remove(), 5000);
        }
    }

    static pulseElement(element) {
        element.classList.add('pulse');
        setTimeout(() => element.classList.remove('pulse'), 1000);
    }

    static async typeWriter(element, text, speed = 50) {
        element.textContent = '';
        for (let i = 0; i < text.length; i++) {
            element.textContent += text.charAt(i);
            await new Promise(resolve => setTimeout(resolve, speed));
        }
    }

    static animateNumber(element, start, end, duration = 1000) {
        const startTime = performance.now();
        const updateNumber = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const value = start + (end - start) * this.easeOutQuad(progress);
            element.textContent = Math.round(value).toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(updateNumber);
            }
        };
        
        requestAnimationFrame(updateNumber);
    }

    static easeOutQuad(t) {
        return t * (2 - t);
    }

    static shake(element) {
        element.classList.add('shake');
        setTimeout(() => element.classList.remove('shake'), 500);
    }

    static async highlightChoice(element) {
        element.classList.add('highlight');
        await new Promise(resolve => setTimeout(resolve, 300));
        element.classList.remove('highlight');
    }

    static async showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        
        document.body.appendChild(toast);
        
        // Trigger reflow
        toast.offsetHeight;
        
        // Show toast
        toast.classList.add('show');
        
        // Remove after 3 seconds
        await new Promise(resolve => setTimeout(resolve, 3000));
        toast.classList.remove('show');
        
        // Wait for fade out animation
        await new Promise(resolve => setTimeout(resolve, 300));
        toast.remove();
    }
}

// Export for use in other files
export default GameAnimations;