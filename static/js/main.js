document.addEventListener('DOMContentLoaded', () => {
    const codeForm = document.getElementById('codeForm');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const spinner = submitBtn.querySelector('.spinner');
    const outputSection = document.querySelector('.output-section');
    const resultsContainer = document.querySelector('.results-container');

    codeForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Show loading state
        btnText.textContent = 'Analyzing...';
        spinner.classList.remove('hidden');
        submitBtn.disabled = true;

        const code = document.getElementById('codeInput').value;
        const language = document.getElementById('language').value;

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code, language }),
            });

            const data = await response.json();

            // Display results
            outputSection.classList.remove('hidden');
            resultsContainer.innerHTML = generateResultsHTML(data);
        } catch (error) {
            console.error('Error:', error);
            resultsContainer.innerHTML = `
                <div class="error-card">
                    <h3>Error</h3>
                    <p>An error occurred while analyzing the code. Please try again.</p>
                </div>
            `;
        } finally {
            // Reset button state
            btnText.textContent = 'Analyze Code';
            spinner.classList.add('hidden');
            submitBtn.disabled = false;
        }
    });

    function generateResultsHTML(data) {
        return `
            <div class="analysis-card">
                <h3>Code Complexity</h3>
                <p>Cyclomatic Complexity: ${data.complexity}</p>
            </div>
            <div class="analysis-card">
                <h3>Issues Found</h3>
                <ul>
                    ${data.issues.map(issue => `
                        <li>
                            <strong>Line ${issue.line}:</strong> ${issue.message}
                        </li>
                    `).join('')}
                </ul>
            </div>
            <div class="analysis-card">
                <h3>Suggestions</h3>
                <ul>
                    ${data.suggestions.map(suggestion => `
                        <li>${suggestion}</li>
                    `).join('')}
                </ul>
            </div>
        `;
    }
}); 