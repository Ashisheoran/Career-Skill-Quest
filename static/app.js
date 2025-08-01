
// Global variables to store parsed resume data and generated questions
let parsedResumeData = null;
let generatedTestQuestions = [];
let lastTestWeaknesses = []; // Store weaknesses for retry test

// Multi-step form variables
let currentStep = 0;
const formSteps = document.querySelectorAll('.form-step');
const progressBar = document.getElementById('progress-bar');
const progressDots = document.querySelectorAll('.dot');
const totalSteps = formSteps.length;

// --- Utility Functions ---

function showSection(sectionId) {
    // Hide all sections with a fade-out effect first
    document.querySelectorAll('.section.visible').forEach(section => {
        section.classList.remove('visible');
    });

    // After a short delay, show the target section with fade-in
    setTimeout(() => {
        document.querySelectorAll('.section').forEach(section => {
            section.classList.add('hidden');
        });
        const targetSection = document.getElementById(sectionId);
        targetSection.classList.remove('hidden');
        // Force reflow to ensure transition plays
        void targetSection.offsetWidth;
        targetSection.classList.add('visible');
    }, 300); // Small delay to allow fade-out to start
}

function showMessage(message, type) {
    const msgBox = document.getElementById('message-box');
    let iconClass = '';
    if (type === 'success') {
        iconClass = 'fas fa-check-circle';
    } else if (type === 'error') {
        iconClass = 'fas fa-times-circle';
    } else if (type === 'info') {
        iconClass = 'fas fa-info-circle';
    }
    msgBox.innerHTML = `<i class="${iconClass}"></i> ${message}`;
    msgBox.className = `message-box ${type} visible`;
    setTimeout(() => {
        msgBox.classList.remove('visible');
        msgBox.classList.add('hidden');
    }, 5000); // Hide after 5 seconds
}

function showLoading(text = "Processing...") {
    document.getElementById('loading-text').textContent = text;
    document.getElementById('loading-overlay').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading-overlay').classList.add('hidden');
}

function updateProgressBar() {
    const progress = (currentStep / (totalSteps - 1)) * 100;
    progressBar.style.width = `${progress}%`;

    progressDots.forEach((dot, index) => {
        if (index <= currentStep) {
            dot.classList.add('active');
        } else {
            dot.classList.remove('active');
        }
    });
}

function showStep(stepIndex) {
    formSteps.forEach((step, index) => {
        if (index === stepIndex) {
            step.classList.add('active');
        } else {
            step.classList.remove('active');
        }
    });
    currentStep = stepIndex;
    updateProgressBar();
}

function validateStep(stepIndex) {
    let isValid = true;
    const currentFormStep = formSteps[stepIndex];
    const inputs = currentFormStep.querySelectorAll('input[required], textarea[required]');

    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.style.borderColor = 'red'; // Simple visual feedback
        } else {
            input.style.borderColor = ''; // Reset border color
        }
    });

    // Specific validation for email
    if (stepIndex === 0) { // Step 1 contains email
        const emailInput = document.getElementById('input-email');
        if (emailInput && !/\S+@\S+\.\S+/.test(emailInput.value)) {
            isValid = false;
            emailInput.style.borderColor = 'red';
            showMessage('Please enter a valid email address.', 'error');
        }
    }

    // Specific validation for skills (ensure at least one skill)
    if (stepIndex === 3) { // Step 4 contains skills
        const skillsInput = document.getElementById('input-skills');
        const skills = skillsInput.value.trim().split(',').map(s => s.trim()).filter(s => s.length > 0);
        if (skills.length === 0) {
            isValid = false;
            skillsInput.style.borderColor = 'red';
            showMessage('Please enter at least one skill.', 'error');
        }
    }

    if (!isValid) {
        showMessage('Please fill in all required fields for this step.', 'error');
    }
    return isValid;
}

function displayParsedResume(data) {
    document.getElementById('parsed-name').textContent = data.name;
    document.getElementById('parsed-email').textContent = data.email;
    document.getElementById('parsed-experience-years').textContent = data.experience_years;
    document.getElementById('parsed-experience-summary').textContent = data.experience;
    document.getElementById('parsed-education').textContent = data.education;

    const skillsList = document.getElementById('parsed-skills');
    skillsList.innerHTML = '';
    data.skills.forEach(skill => {
        const li = document.createElement('li');
        li.textContent = skill;
        skillsList.appendChild(li);
    });
}

function displayTestQuestions(questions, questionType) {
    const container = document.getElementById('test-questions-container');
    container.innerHTML = ''; // Clear previous questions

    questions.forEach((q, index) => {
        const questionCard = document.createElement('div');
        questionCard.className = 'question-card';

        const questionText = document.createElement('p');
        questionText.textContent = `${index + 1}. ${q.question}`;
        questionCard.appendChild(questionText);

        if (questionType === 'mcq' && q.options) {
            const optionsDiv = document.createElement('div');
            optionsDiv.className = 'question-options';
            q.options.forEach(option => {
                const label = document.createElement('label');
                const input = document.createElement('input');
                input.type = 'radio';
                input.name = `question-${index}`;
                input.value = option.charAt(0); // Assuming option starts with A, B, C, D
                label.appendChild(input);
                label.appendChild(document.createTextNode(option));
                optionsDiv.appendChild(label);
            });
            questionCard.appendChild(optionsDiv);
        } else if (questionType === 'coding') {
            const codeInputDiv = document.createElement('div');
            codeInputDiv.className = 'coding-question-input';
            const textarea = document.createElement('textarea');
            textarea.name = `question-${index}`;
            textarea.rows = 10;
            textarea.placeholder = "Write your code here...";
            if (q.code_template) {
                textarea.value = q.code_template;
            }
            codeInputDiv.appendChild(textarea);
            questionCard.appendChild(codeInputDiv);

            if (q.expected_output_example) {
                const example = document.createElement('p');
                example.innerHTML = `<strong>Example:</strong> <pre>${q.expected_output_example}</pre>`;
                questionCard.appendChild(example);
            }
        }
        container.appendChild(questionCard);
    });
}

function displayTestResults(results) {
    document.getElementById('overall-feedback-text').textContent = results.overall_feedback;

    const strengthsList = document.getElementById('strengths-list');
    strengthsList.innerHTML = '';
    results.strengths.forEach(s => {
        const li = document.createElement('li');
        li.textContent = s;
        strengthsList.appendChild(li);
    });

    const weaknessesList = document.getElementById('weaknesses-list');
    weaknessesList.innerHTML = '';
    results.weaknesses.forEach(w => {
        const li = document.createElement('li');
        li.textContent = w;
        weaknessesList.appendChild(li);
    });
    lastTestWeaknesses = results.weaknesses; // Store for retry button

    const detailedFeedbackList = document.getElementById('detailed-feedback-list');
    detailedFeedbackList.innerHTML = '';
    results.detailed_feedback.forEach(df => {
        const li = document.createElement('li');
        li.textContent = df;
        detailedFeedbackList.appendChild(li);
    });

    const learningResourcesList = document.getElementById('learning-resources-list');
    learningResourcesList.innerHTML = '';
    if (results.general_learning_resources && results.general_learning_resources.length > 0) {
        results.general_learning_resources.forEach(lr => {
            const li = document.createElement('li');
            li.innerHTML = `<a href="${lr.link}" target="_blank" rel="noopener noreferrer">${lr.title}</a>: ${lr.description}`;
            learningResourcesList.appendChild(li);
        });
    } else {
        learningResourcesList.innerHTML = '<li>No general learning resources provided.</li>';
    }


    const learningPathsContainer = document.getElementById('learning-paths-container');
    learningPathsContainer.innerHTML = '';
    if (results.specific_learning_paths && results.specific_learning_paths.length > 0) {
        results.specific_learning_paths.forEach(lp => {
            const pathCard = document.createElement('div');
            pathCard.className = 'learning-path-card';
            pathCard.innerHTML = `
                <h4>${lp.topic}</h4>
                <p><strong>Reason:</strong> ${lp.reason}</p>
                <p><strong>Path:</strong> ${lp.path}</p>
                ${lp.resources.map(res => `<p><a href="${res.link}" target="_blank" rel="noopener noreferrer">${res.title}</a></p>`).join('')}
            `;
            learningPathsContainer.appendChild(pathCard);
        });
    } else {
        learningPathsContainer.innerHTML = '<p>No specific learning paths recommended at this time.</p>';
    }
}

function displayJobRecommendations(jobs) {
    const jobListContainer = document.getElementById('job-recommendations-list');
    jobListContainer.innerHTML = ''; // Clear previous jobs

    if (jobs.length === 0) {
        jobListContainer.innerHTML = '<p>No job recommendations found based on your profile and the current search criteria. Try updating your skills or experience.</p>';
        return;
    }

    jobs.forEach(job => {
        const jobCard = document.createElement('div');
        jobCard.className = 'job-card';
        jobCard.innerHTML = `
            <h3>${job.title}</h3>
            <p><strong>Company:</strong> ${job.company}</p>
            <p><strong>Location:</strong> ${job.location}</p>
            <div class="job-description">${job.description}</div>
            <a href="${job.apply_link}" target="_blank" rel="noopener noreferrer" class="apply-link-btn">
                Apply Directly <i class="fas fa-external-link-alt"></i>
            </a>
        `;
        jobListContainer.appendChild(jobCard);
    });
}


// --- Event Listeners ---

// Multi-step form navigation
document.querySelectorAll('.next-step-btn').forEach(button => {
    button.addEventListener('click', () => {
        if (validateStep(currentStep)) {
            if (currentStep < totalSteps - 1) {
                showStep(currentStep + 1);
            }
        }
    });
});

document.querySelectorAll('.prev-step-btn').forEach(button => {
    button.addEventListener('click', () => {
        if (currentStep > 0) {
            showStep(currentStep - 1);
        }
    });
});

// Initial step display
showStep(0);

document.getElementById('manual-input-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!validateStep(currentStep)) { // Validate the final step before submission
        return;
    }

    const name = document.getElementById('input-name').value.trim();
    const email = document.getElementById('input-email').value.trim();
    const experienceYears = parseInt(document.getElementById('input-experience-years').value);
    const experienceSummary = document.getElementById('input-experience-summary').value.trim();
    const education = document.getElementById('input-education').value.trim();
    const skillsRaw = document.getElementById('input-skills').value.trim();
    const skills = skillsRaw.split(',').map(s => s.trim()).filter(s => s.length > 0);

    showLoading('Submitting your details...');

    const resumeData = {
        name: name,
        email: email,
        experience_years: experienceYears,
        experience: experienceSummary,
        education: education,
        skills: skills
    };

    try {
        const response = await fetch('/submit-resume-details', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(resumeData),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to submit resume details.');
        }

        parsedResumeData = await response.json();
        displayParsedResume(parsedResumeData);
        showSection('parsed-resume-section');
        showMessage('Details submitted successfully!', 'success');

    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
});

document.getElementById('generate-test-btn').addEventListener('click', () => {
    if (parsedResumeData && parsedResumeData.skills && parsedResumeData.skills.length > 0) {
        showSection('test-generation-section');
    } else {
        showMessage('Please enter your resume details first to extract skills.', 'error');
    }
});

document.getElementById('start-test-generation-btn').addEventListener('click', async () => {
    if (!parsedResumeData || !parsedResumeData.skills || parsedResumeData.skills.length === 0) {
        showMessage('No skills found in your details to generate a test. Please go back and add some skills.', 'error');
        return;
    }

    const testType = document.querySelector('input[name="testType"]:checked').value;
    const numQuestions = parseInt(document.getElementById('num-questions-input').value);

    if (isNaN(numQuestions) || numQuestions <= 0) {
        showMessage('Please enter a valid number of questions.', 'error');
        return;
    }

    showLoading('Generating your test...');

    try {
        const response = await fetch('/generate-test', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                skills: parsedResumeData.skills,
                experience_years: parsedResumeData.experience_years,
                num_questions: numQuestions,
                question_type: testType
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to generate test.');
        }

        generatedTestQuestions = await response.json();
        displayTestQuestions(generatedTestQuestions, testType);
        showSection('test-taking-section');
        showMessage('Test generated successfully!', 'success');

    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
});

document.getElementById('test-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    if (generatedTestQuestions.length === 0) {
        showMessage('No test questions to submit.', 'error');
        return;
    }

    const answers = {};
    const testType = document.querySelector('input[name="testType"]:checked').value;

    generatedTestQuestions.forEach((q, index) => {
        if (testType === 'mcq') {
            const selectedOption = document.querySelector(`input[name="question-${index}"]:checked`);
            if (selectedOption) {
                answers[index] = selectedOption.value;
            } else {
                answers[index] = 'No answer provided.';
            }
        } else if (testType === 'coding') {
            const codeAnswer = document.querySelector(`textarea[name="question-${index}"]`);
            if (codeAnswer) {
                answers[index] = codeAnswer.value;
            } else {
                answers[index] = 'No code provided.';
            }
        }
    });

    showLoading('Submitting your answers and evaluating test...');

    try {
        const response = await fetch('/evaluate-test', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                questions: generatedTestQuestions,
                answers: answers
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to evaluate test.');
        }

        const testResults = await response.json();
        displayTestResults(testResults);
        showSection('test-results-section');
        showMessage('Test evaluated successfully!', 'success');

    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
});

document.getElementById('retry-test-btn').addEventListener('click', async () => {
    if (lastTestWeaknesses.length > 0) {
        showLoading('Generating a new test focusing on your weaknesses...');
        try {
            const testType = document.querySelector('input[name="testType"]:checked').value; // Keep current test type
            const numQuestions = parseInt(document.getElementById('num-questions-input').value); // Keep current number of questions

            const response = await fetch('/generate-test', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    skills: lastTestWeaknesses, // Use weaknesses as skills
                    experience_years: parsedResumeData.experience_years, // Use original experience
                    num_questions: numQuestions,
                    question_type: testType
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to generate retry test.');
            }

            generatedTestQuestions = await response.json();
            displayTestQuestions(generatedTestQuestions, testType);
            showSection('test-taking-section');
            showMessage('Retry test generated successfully!', 'success');

        } catch (error) {
            showMessage(`Error generating retry test: ${error.message}`, 'error');
        } finally {
            hideLoading();
        }
    } else {
        showMessage('No specific weaknesses identified for a retry test, or please take the initial test first.', 'info');
    }
});


// New Job Recommendation Button Event Listener
document.getElementById('recommend-jobs-btn').addEventListener('click', async () => {
    if (!parsedResumeData || !parsedResumeData.skills || parsedResumeData.skills.length === 0) {
        showMessage('Please enter your resume details first to get job recommendations.', 'error');
        return;
    }

    showLoading('Finding job recommendations...');

    try {
        const response = await fetch('/recommend-jobs', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(parsedResumeData), // Pass the entire parsedResumeData object
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to fetch job recommendations.');
        }

        const jobs = await response.json();
        displayJobRecommendations(jobs);
        showSection('job-recommendation-section');
        showMessage('Job recommendations loaded!', 'success');

    } catch (error) {
        showMessage(`Error: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
});

// Go back buttons
document.getElementById('go-back-from-parsed-btn').addEventListener('click', () => {
    showSection('manual-resume-input-section');
    showStep(currentStep); // Go back to the last step of the form
});

document.getElementById('go-back-from-test-gen-btn').addEventListener('click', () => {
    showSection('parsed-resume-section');
});

document.getElementById('go-back-from-test-taking-btn').addEventListener('click', () => {
    showSection('test-generation-section');
});

document.getElementById('go-back-from-test-results-btn').addEventListener('click', () => {
    showSection('test-taking-section');
});

document.getElementById('go-back-from-jobs-btn').addEventListener('click', () => {
    showSection('test-results-section');
});
document.getElementById('return-to-start-btn').addEventListener('click', () => {
    showSection('manual-resume-input-section');
    showStep(0); // Go back to the very first step of the form
});
document.getElementById('return-to-start').addEventListener('click', () => {
    showSection('manual-resume-input-section');
    showStep(0); 
});

