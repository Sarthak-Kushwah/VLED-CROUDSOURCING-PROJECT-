// Main JavaScript file
document.addEventListener('DOMContentLoaded', function () {
    generateTOC();
    initFAQ();
    initSearch();
    initChatWidget();
});

function setFaqExpanded(item, expanded) {
    const button = item.querySelector('.faq-question');
    if (button) {
        button.setAttribute('aria-expanded', expanded ? 'true' : 'false');
    }
}

// ==================== TABLE OF CONTENTS ====================
function generateTOC() {
    const tocContainer = document.getElementById('tableOfContents');
    const sections = document.querySelectorAll('.faq-section');

    let tocHTML = '';

    sections.forEach((section) => {
        const sectionTitle = section.querySelector('.section-title');
        const titleText = sectionTitle.textContent;

        tocHTML += `<div class="toc-section-title">${titleText}</div>`;

        const items = section.querySelectorAll('.faq-item');
        items.forEach((item) => {
            const questionText = item.querySelector('.question-text').textContent;
            const questionId = item.dataset.question;
            tocHTML += `<div class="toc-item"><a href="#" data-target="${questionId}">${questionText}</a></div>`;
        });
    });

    tocContainer.innerHTML = tocHTML;

    tocContainer.querySelectorAll('.toc-item a').forEach((link) => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.dataset.target;
            const targetItem = document.querySelector(`.faq-item[data-question="${targetId}"]`);
            if (targetItem) {
                targetItem.classList.add('active');
                setFaqExpanded(targetItem, true);
                targetItem.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    });
}

// ==================== FAQ EXPAND/COLLAPSE ====================
function initFAQ() {
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach((item) => {
        const question = item.querySelector('.faq-question');
        const answer = item.querySelector('.faq-answer');
        const questionId = item.dataset.question;

        if (answer && questionId) {
            answer.id = `answer-${questionId.replace(/\./g, '-')}`;
        }

        if (question && answer) {
            question.setAttribute('aria-controls', answer.id);
            question.setAttribute('aria-expanded', 'false');
        }

        question.addEventListener('click', function () {
            const isOpen = item.classList.toggle('active');
            setFaqExpanded(item, isOpen);
        });
    });

    document.getElementById('expandAll').addEventListener('click', function () {
        document.querySelectorAll('.faq-item').forEach((item) => {
            if (!item.classList.contains('hidden')) {
                item.classList.add('active');
                setFaqExpanded(item, true);
            }
        });
    });

    document.getElementById('collapseAll').addEventListener('click', function () {
        document.querySelectorAll('.faq-item').forEach((item) => {
            item.classList.remove('active');
            setFaqExpanded(item, false);
        });
    });
}

// ==================== SEARCH ====================
function initSearch() {
    const searchInput = document.getElementById('searchInput');
    let debounceTimer;

    searchInput.addEventListener('input', function () {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            performSearch(this.value.trim().toLowerCase());
        }, 200);
    });
}

function performSearch(query) {
    const faqItems = document.querySelectorAll('.faq-item');
    const sections = document.querySelectorAll('.faq-section');
    const searchStatus = document.getElementById('searchStatus');
    const existingNoResults = document.querySelector('.no-results');
    let firstVisible = null;

    if (existingNoResults) {
        existingNoResults.remove();
    }

    if (searchStatus) {
        searchStatus.textContent = '';
    }

    document.querySelectorAll('.highlight').forEach((el) => {
        el.replaceWith(el.textContent);
    });

    faqItems.forEach((item) => {
        item.classList.remove('search-match');
    });

    if (!query) {
        faqItems.forEach((item) => {
            item.classList.remove('hidden');
        });
        sections.forEach((section) => {
            section.style.display = '';
        });
        if (searchStatus) {
            searchStatus.textContent = 'Showing all FAQ entries';
        }
        return;
    }

    let visibleCount = 0;

    sections.forEach((section) => {
        const items = section.querySelectorAll('.faq-item');
        let sectionHasVisible = false;

        items.forEach((item) => {
            const questionText = item.querySelector('.question-text').textContent.toLowerCase();
            const answerText = item.querySelector('.faq-answer').textContent.toLowerCase();

            if (questionText.includes(query) || answerText.includes(query)) {
                item.classList.remove('hidden');
                item.classList.add('search-match');
                if (!firstVisible) {
                    firstVisible = item;
                }
                sectionHasVisible = true;
                visibleCount++;
                highlightText(item.querySelector('.question-text'), query);
            } else {
                item.classList.add('hidden');
                item.classList.remove('active');
                setFaqExpanded(item, false);
            }
        });

        section.style.display = sectionHasVisible ? '' : 'none';
    });

    if (visibleCount === 0) {
        const noResults = document.createElement('div');
        noResults.className = 'no-results';
        noResults.textContent = `No results found for "${query}"`;
        document.getElementById('faqContainer').appendChild(noResults);
        if (searchStatus) {
            searchStatus.textContent = `No matches found for "${query}"`;
        }
        return;
    }

    if (searchStatus) {
        searchStatus.textContent = `${visibleCount} matching FAQ${visibleCount === 1 ? '' : 's'} found for "${query}"`;
    }

    if (firstVisible) {
        firstVisible.classList.add('active');
        setFaqExpanded(firstVisible, true);
        firstVisible.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

function highlightText(element, query) {
    const text = element.textContent;
    const lowerText = text.toLowerCase();
    const index = lowerText.indexOf(query);

    if (index !== -1) {
        const before = text.substring(0, index);
        const match = text.substring(index, index + query.length);
        const after = text.substring(index + query.length);
        element.innerHTML = `${before}<span class="highlight">${match}</span>${after}`;
    }
}

// ==================== CHAT WIDGET ====================
function initChatWidget() {
    const chatWidget = document.getElementById('chatWidget');
    const chatToggle = document.getElementById('chatToggle');
    const chatClose = document.getElementById('chatClose');
    const chatInput = document.getElementById('chatInput');
    const chatSend = document.getElementById('chatSend');
    const chatMessages = document.getElementById('chatMessages');

    chatToggle.classList.add('hidden');

    chatClose.addEventListener('click', function () {
        chatWidget.classList.add('hidden');
        chatToggle.classList.remove('hidden');
    });

    chatToggle.addEventListener('click', function () {
        chatWidget.classList.remove('hidden');
        chatToggle.classList.add('hidden');
    });

    function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;

        addMessage(message, 'user');
        chatInput.value = '';

        setTimeout(() => {
            const response = getBotResponse(message);
            addMessage(response, 'bot');
        }, 800);
    }

    chatSend.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    function addMessage(text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${type}-message`;
        messageDiv.innerHTML = `<p>${text}</p>`;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function getBotResponse(query) {
        const lowerQuery = query.toLowerCase();

        if (lowerQuery.includes('noc') || lowerQuery.includes('no objection')) {
            return 'NOC (No Objection Certificate) must be signed by your HOD/Dean and uploaded through your dashboard. Check section 3 for detailed NOC guidelines including format, deadlines, and who can sign it.';
        }
        if (lowerQuery.includes('stipend') || lowerQuery.includes('payment') || lowerQuery.includes('paid')) {
            return 'Stipend availability varies by cohort and track. Check your offer letter or the Overview page for specific details about compensation for your cycle. See section 5.4.';
        }
        if (lowerQuery.includes('certificate')) {
            return 'Yes, you will receive a completion certificate if you successfully complete all requirements. It is issued as a digital e-certificate. See section 8 for details.';
        }
        if (lowerQuery.includes('rosetta') || lowerQuery.includes('journal')) {
            return 'Rosetta is your daily internship journal for structured reflection. Write authentically in your own words — AI tools are not allowed. See section 9 for complete Rosetta guidelines.';
        }
        if (lowerQuery.includes('vibe') || lowerQuery.includes('course') || lowerQuery.includes('video')) {
            return 'ViBe is the learning platform for coursework. Use Chrome for best experience. For technical issues, try clearing cache first. See section 13 for detailed ViBe troubleshooting.';
        }
        if (lowerQuery.includes('team') || lowerQuery.includes('teammate')) {
            return 'Teams are formed during a structured activity in the internship. Team sizes are typically 3-5 members. See section 14 for all team formation details.';
        }
        if (lowerQuery.includes('spurti') || lowerQuery.includes('sp') || lowerQuery.includes('points')) {
            return 'Spurti Points (SP) measure your participation and engagement. They are calculated from attendance, coursework, journal entries, and contributions. See section 11 for details.';
        }
        if (lowerQuery.includes('zoom') || lowerQuery.includes('standup') || lowerQuery.includes('live session')) {
            return 'Zoom links for sessions are shared on your dashboard. Provide your Zoom ID in profile settings for attendance tracking. See section 10 for live session details.';
        }
        if (lowerQuery.includes('start') || lowerQuery.includes('begin') || lowerQuery.includes('date')) {
            return 'Your start date is in your offer letter. You\'ll receive access to materials on or before day 1. See section 2 for timing and dates information.';
        }
        if (lowerQuery.includes('mentor')) {
            return 'Your mentor is assigned after team formation and communicated via dashboard and email. If not assigned within the first week, contact the programme team. See section 5.3.';
        }
        if (lowerQuery.includes('hello') || lowerQuery.includes('hi') || lowerQuery.includes('hey')) {
            return 'Hello! I can help with questions about the Vicharanashala Internship. Ask about NOC, dates, Rosetta, ViBe, teams, Spurti Points, or anything else!';
        }
        if (lowerQuery.includes('vins') || lowerQuery.includes('vise') || lowerQuery.includes('online') || lowerQuery.includes('offline')) {
            return 'VINS is the online/self-paced track, VISE is the offline track. You choose during the selection process. Switching after selection is generally not permitted. See sections 1.2 and 4.11.';
        }

        return 'I can help with questions about the Vicharanashala Internship. Try asking about: NOC, dates, Rosetta journal, ViBe platform, teams, Spurti Points, certificates, or mentors. For specific cases, log in at samagama.in and ask Yaksha.';
    }
}
