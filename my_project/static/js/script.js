// Wait until the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {

    // Handle Quiz Start button click
    const startQuizButtons = document.querySelectorAll('.start-quiz');

    startQuizButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            
            // Get the quiz title and show a confirmation message
            const quizTitle = this.closest('.quiz-card').querySelector('h2').textContent;
            const confirmation = confirm(`Do you want to start the quiz: "${quizTitle}"?`);

            if (confirmation) {
                // Redirect to the quiz page (replace 'all_quiz' with the actual quiz URL if needed)
                window.location.href = this.getAttribute('href');
            }
        });
    });

    // Optional: Add some behavior when clicking a quiz card (just for example)
    const quizCards = document.querySelectorAll('.quiz-card');
    quizCards.forEach(function(card) {
        card.addEventListener('click', function() {
            this.classList.toggle('highlight');
        });
    });

});
