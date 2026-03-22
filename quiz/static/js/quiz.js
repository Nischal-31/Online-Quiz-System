document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('quizForm');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            submitQuiz();
        });
    }
});

async function submitQuiz() {
    const formData = new FormData(document.getElementById('quizForm'));
    const submitBtn = document.querySelector('button[type="submit"]');
    
    submitBtn.innerHTML = 'Submitting...';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch('/submit/', {
            method: 'POST',
            body: new URLSearchParams(formData),
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            showResults(result);
        }
    } catch (error) {
        alert('Error submitting quiz. Please try again.');
    } finally {
        submitBtn.innerHTML = 'Submit Quiz';
        submitBtn.disabled = false;
    }
}

function showResults(result) {
    const scoreDisplay = document.getElementById('scoreDisplay');
    const progressBar = document.getElementById('progressBar');
    const percentageEl = document.getElementById('percentage');
    
    scoreDisplay.textContent = `${result.score}/${result.total}`;
    percentageEl.textContent = `${result.percentage}%`;
    
    // Update progress bar
    progressBar.style.width = `${result.percentage}%`;
    progressBar.setAttribute('aria-valuenow', result.percentage);
    
    // Color coding
    if (result.percentage >= 80) {
        scoreDisplay.className = 'score-excellent';
        scoreDisplay.innerHTML += ' <span class="badge bg-success">Excellent!</span>';
    } else if (result.percentage >= 60) {
        scoreDisplay.className = 'score-good';
        scoreDisplay.innerHTML += ' <span class="badge bg-warning">Good!</span>';
    } else {
        scoreDisplay.className = 'score-poor';
        scoreDisplay.innerHTML += ' <span class="badge bg-danger">Keep Practicing!</span>';
    }
    
    new bootstrap.Modal(document.getElementById('resultsModal')).show();
}