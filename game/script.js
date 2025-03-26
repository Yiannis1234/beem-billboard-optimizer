const dogResponses = {
    happy: [
        "That's wonderful! Your happiness makes my tail wag! 🐕 What's making you feel so good today?",
        "I'm so glad you're feeling good! Want to share what's bringing you joy? It might help others too! 🎾",
        "Your positive energy is contagious! Let's celebrate! 🎉 Have you tried writing down these happy moments? It can help on tougher days."
    ],
    sad: [
        "I'm here for you! Would you like to talk about what's making you feel this way? Sometimes sharing helps lighten the load. 🤗",
        "It's okay to feel sad. I'm here to listen. Would you like to try a quick exercise? Take three deep breaths with me... 💕",
        "Remember, every cloud has a silver lining. Let's find something to smile about! 🌈 Would you like to try listing three things you're grateful for, even if they're small?"
    ],
    anxious: [
        "Take a deep breath with me... In... Out... 🧘‍♂️ Let's try the 5-4-3-2-1 technique: Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste.",
        "I'm right here with you. You're safe. Want to try some grounding exercises? 🌟 Let's focus on your feet touching the ground...",
        "Let's focus on the present moment together. What do you see around you? 👀 Sometimes focusing on the here and now can help calm anxious thoughts."
    ],
    angry: [
        "I understand you're upset. Want to take a walk together? 🚶‍♂️ Physical movement can help release tension. Or we could try some quick breathing exercises.",
        "It's okay to feel angry. Let's talk it out. I'm here to listen. 🐾 Would you like to try writing down your feelings? Sometimes putting it on paper helps.",
        "Take a moment to breathe. I'll stay right here with you. 💫 Would you like to try counting to 10 slowly? It can help create space between feeling and reacting."
    ]
};

const meditationPrompts = [
    "Let's take a deep breath together... In for 4 counts, hold for 4, out for 4. Repeat with me...",
    "Imagine a peaceful garden... What do you see? What colors are there? What sounds do you hear?",
    "Feel the gentle breeze... Notice how it cools your skin. Let your thoughts float away like leaves in the wind...",
    "Listen to the calming sounds... Focus on one sound at a time. Let other thoughts drift away...",
    "Let your thoughts float away... Imagine they're clouds in the sky, passing by without judgment..."
];

const followUpQuestions = {
    happy: [
        "What made you smile today?",
        "Who shared in your happiness?",
        "How can you carry this feeling forward?",
        "What's one thing you're looking forward to?"
    ],
    sad: [
        "When did you start feeling this way?",
        "Is there someone you can talk to about this?",
        "What usually helps you feel better?",
        "Would you like to try a quick mood-lifting activity?"
    ],
    anxious: [
        "What's the worst that could happen?",
        "What's the best that could happen?",
        "What's most likely to happen?",
        "What's one small step you can take right now?"
    ],
    angry: [
        "What triggered this feeling?",
        "What do you need right now?",
        "What would help you feel calmer?",
        "Would you like to try a quick anger management technique?"
    ]
};

const copingStrategies = {
    happy: [
        "Share your joy with others - happiness grows when shared!",
        "Write down what's making you happy - it's great to look back on later",
        "Take a moment to fully appreciate this feeling",
        "Think about how you can spread this positivity"
    ],
    sad: [
        "Try the 3-3-3 rule: Name 3 things you see, 3 things you hear, and 3 things you can touch",
        "Write down your feelings in a journal",
        "Call or text a friend or family member",
        "Take a short walk outside"
    ],
    anxious: [
        "Try the box breathing technique: Inhale for 4, hold for 4, exhale for 4, hold for 4",
        "Practice the 5-4-3-2-1 grounding technique",
        "Take a cold shower or splash cold water on your face",
        "Write down your worries and then tear up the paper"
    ],
    angry: [
        "Try the STOP technique: Stop, Take a step back, Observe, Proceed mindfully",
        "Squeeze a stress ball or pillow",
        "Write down your anger and then tear it up",
        "Take a short walk or do some jumping jacks"
    ]
};

let currentMood = null;
let meditationMode = false;
let conversationContext = {
    lastMood: null,
    lastResponse: null,
    followUpCount: 0
};

// Add inappropriate words filter
const inappropriateWords = [
    // Add inappropriate words here
    "badword1",
    "badword2",
    // etc...
];

function containsInappropriateContent(message) {
    const lowerMessage = message.toLowerCase();
    return inappropriateWords.some(word => lowerMessage.includes(word));
}

function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim().toLowerCase();
    
    if (message) {
        if (containsInappropriateContent(message)) {
            addMessage("I understand you might be upset, but let's keep our conversation respectful. How can I help you express your feelings in a constructive way? 🐕", 'dog');
            input.value = '';
            return;
        }
        
        addMessage(message, 'user');
        input.value = '';
        
        if (message.includes('yes')) {
            setTimeout(() => {
                startVirtualWalk();
            }, 1000);
        } else {
            setTimeout(() => {
                addMessage("That's okay! Let me know if you change your mind! 🐕", 'dog');
            }, 1000);
        }
    }
}

function addMessage(text, sender) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function generateDogResponse(message) {
    const lowerMessage = message.toLowerCase();
    
    // Check for inappropriate content in user's message
    if (containsInappropriateContent(message)) {
        return "I understand you might be upset, but let's keep our conversation respectful. How can I help you express your feelings in a constructive way? 🐕";
    }
    
    // Check for meditation-related keywords
    if (lowerMessage.includes('meditation') || lowerMessage.includes('calm')) {
        meditationMode = true;
        return meditationPrompts[Math.floor(Math.random() * meditationPrompts.length)];
    }
    
    // Check for mood-related keywords
    for (const mood in dogResponses) {
        if (lowerMessage.includes(mood)) {
            currentMood = mood;
            conversationContext.lastMood = mood;
            conversationContext.followUpCount = 0;
            return dogResponses[mood][Math.floor(Math.random() * dogResponses[mood].length)];
        }
    }
    
    // Handle follow-up responses
    if (conversationContext.lastMood && conversationContext.followUpCount < 2) {
        conversationContext.followUpCount++;
        const followUp = followUpQuestions[conversationContext.lastMood][Math.floor(Math.random() * followUpQuestions[conversationContext.lastMood].length)];
        return followUp;
    }
    
    // Check for yes/no responses to follow-up questions
    if (conversationContext.lastMood && (lowerMessage.includes('yes') || lowerMessage.includes('yeah'))) {
        const strategy = copingStrategies[conversationContext.lastMood][Math.floor(Math.random() * copingStrategies[conversationContext.lastMood].length)];
        return `Great! Let's try this: ${strategy} Would you like to try it now?`;
    }
    
    // Default responses
    return "I'm here to listen and help! Would you like to tell me more about how you're feeling? 🐕";
}

function selectMood(mood) {
    currentMood = mood;
    conversationContext.lastMood = mood;
    conversationContext.followUpCount = 0;
    const response = dogResponses[mood][Math.floor(Math.random() * dogResponses[mood].length)];
    addMessage(response, 'dog');
    
    // Animate the dog based on mood
    animateDog(mood);
}

function animateDog(mood) {
    const dog = document.querySelector('.dog');
    dog.style.animation = 'none';
    dog.offsetHeight; // Trigger reflow
    
    switch(mood) {
        case 'happy':
            dog.style.animation = 'bounce 0.5s infinite';
            break;
        case 'sad':
            dog.style.animation = 'tilt 2s infinite';
            break;
        case 'anxious':
            dog.style.animation = 'bounce 0.3s infinite';
            break;
        case 'angry':
            dog.style.animation = 'tilt 0.5s infinite';
            break;
    }
}

const environments = [
    {
        name: 'forest',
        background: 'linear-gradient(180deg, #87CEEB 0%, #90EE90 100%)',
        elements: ['tree', 'cloud']
    },
    {
        name: 'beach',
        background: 'linear-gradient(180deg, #87CEEB 0%, #FFD700 100%)',
        elements: ['cloud', 'palm']
    },
    {
        name: 'park',
        background: 'linear-gradient(180deg, #87CEEB 0%, #98FB98 100%)',
        elements: ['tree', 'cloud', 'bench']
    }
];

let isWalking = false;
let walkInterval;
let currentEnvironment = 0;

function startVirtualWalk() {
    document.getElementById('chatScreen').classList.add('hidden');
    document.getElementById('walkScreen').classList.remove('hidden');
    setupEnvironment();
}

function setupEnvironment() {
    const environment = document.getElementById('environment');
    const elementsContainer = environment.querySelector('.environment-elements');
    elementsContainer.innerHTML = '';
    
    // Set background
    environment.style.background = environments[currentEnvironment].background;
    
    // Add environment elements
    environments[currentEnvironment].elements.forEach(element => {
        if (element === 'tree') {
            addTree(elementsContainer);
        } else if (element === 'cloud') {
            addCloud(elementsContainer);
        }
    });
}

function addTree(container) {
    const tree = document.createElement('div');
    tree.className = 'tree';
    tree.style.left = Math.random() * 80 + 10 + '%';
    tree.style.bottom = '10%';
    container.appendChild(tree);
}

function addCloud(container) {
    const cloud = document.createElement('div');
    cloud.className = 'cloud';
    cloud.style.top = Math.random() * 40 + 10 + '%';
    container.appendChild(cloud);
}

function startWalk() {
    if (!isWalking) {
        isWalking = true;
        const dog = document.querySelector('.dog-walk');
        dog.classList.add('walking');
        
        let position = 20; // Starting position
        walkInterval = setInterval(() => {
            position += 0.5;
            dog.style.left = position + '%';
            
            if (position >= 80) {
                stopWalk();
            }
        }, 50);
    }
}

function stopWalk() {
    if (isWalking) {
        isWalking = false;
        const dog = document.querySelector('.dog-walk');
        dog.classList.remove('walking');
        clearInterval(walkInterval);
    }
}

function changeEnvironment() {
    currentEnvironment = (currentEnvironment + 1) % environments.length;
    setupEnvironment();
    stopWalk();
    const dog = document.querySelector('.dog-walk');
    dog.style.left = '20%';
}

// Add event listener for Enter key
document.getElementById('userInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function analyzeText() {
    const text = document.getElementById('textInput').value;
    if (!text.trim()) {
        alert('Please enter some text to analyze');
        return;
    }

    // Calculate various metrics
    const metrics = calculateMetrics(text);
    
    // Update UI with results
    updateResults(metrics);
}

function humanizeText() {
    const text = document.getElementById('textInput').value;
    if (!text.trim()) {
        alert('Please enter some text to humanize');
        return;
    }
    
    // Clean input text of any previous processing markers
    const cleanText = text.replace(/__humanized__/g, '').trim();
    
    // Apply a simple, coherent humanization
    const humanizedText = basicHumanization(cleanText);
    
    // Update the text input with humanized version
    document.getElementById('textInput').value = humanizedText;
    
    // Re-analyze to show improvement
    analyzeText();
}

function basicHumanization(text) {
    // Process text paragraph by paragraph
    const paragraphs = text.split(/\n+/);
    const humanizedParagraphs = paragraphs.map(paragraph => {
        if (!paragraph.trim()) return paragraph;
        
        // Apply only safe transformations that preserve meaning
        return applySafeTransformations(paragraph);
    });
    
    return humanizedParagraphs.join('\n\n');
}

function applySafeTransformations(paragraph) {
    // Split into sentences
    const sentences = paragraph.split(/(?<=[.!?])\s+/);
    if (sentences.length === 0) return paragraph;
    
    // Process each sentence with controlled transformations
    const processedSentences = [];
    
    for (let i = 0; i < sentences.length; i++) {
        let sentence = sentences[i].trim();
        if (!sentence) continue;
        
        // Step 1: Apply contractions (safe transformation that preserves meaning)
        sentence = applyBasicContractions(sentence);
        
        // Step 2: Very selectively vary vocabulary (only for common words)
        sentence = varyCommonWords(sentence);
        
        // Step 3: Add minimal transitions between sentences
        if (i > 0 && i % 3 === 0 && sentence.length > 10) {
            const previousSentence = processedSentences[processedSentences.length - 1];
            sentence = addSimpleTransition(sentence, previousSentence);
        }
        
        processedSentences.push(sentence);
    }
    
    return processedSentences.join(' ');
}

function applyBasicContractions(text) {
    // Apply only the most common contractions
    return text
        .replace(/\bit is\b/g, "it's")
        .replace(/\bthat is\b/g, "that's")
        .replace(/\byou are\b/g, "you're")
        .replace(/\bthey are\b/g, "they're")
        .replace(/\bwe are\b/g, "we're")
        .replace(/\bdo not\b/g, "don't")
        .replace(/\bdoes not\b/g, "doesn't")
        .replace(/\bdid not\b/g, "didn't")
        .replace(/\bcannot\b/g, "can't")
        .replace(/\bI am\b/g, "I'm")
        .replace(/\bwill not\b/g, "won't");
}

function varyCommonWords(text) {
    // Only replace a few very common words with safe alternatives
    const commonReplacements = [
        { word: /\bvery\b/g, replacements: ["really", "quite"] },
        { word: /\bmany\b/g, replacements: ["several", "numerous"] },
        { word: /\bgood\b/g, replacements: ["great", "excellent"] },
        { word: /\bbad\b/g, replacements: ["poor", "terrible"] },
        { word: /\bbig\b/g, replacements: ["large", "substantial"] },
        { word: /\bsmall\b/g, replacements: ["little", "minor"] }
    ];
    
    let result = text;
    
    // Only apply one or two replacements per sentence to avoid over-processing
    let replacementCount = 0;
    const maxReplacements = 2;
    
    for (const { word, replacements } of commonReplacements) {
        if (replacementCount >= maxReplacements) break;
        
        if (word.test(result) && Math.random() < 0.7) {
            const replacement = replacements[Math.floor(Math.random() * replacements.length)];
            // Only replace the first occurrence
            result = result.replace(word, replacement);
            replacementCount++;
        }
    }
    
    return result;
}

function addSimpleTransition(sentence, previousSentence) {
    // Only add simple transitions that won't change meaning
    const simpleTransitions = [
        "Also, ", 
        "Additionally, ", 
        "Furthermore, ", 
        "Moreover, "
    ];
    
    // Skip if the sentence already starts with a transition
    const firstWord = sentence.split(' ')[0].toLowerCase();
    if (["also", "additionally", "furthermore", "moreover", "however", "nevertheless"].includes(firstWord)) {
        return sentence;
    }
    
    // Only add transition if it makes sense (we're adding information)
    if (!sentence.toLowerCase().includes("but") && 
        !sentence.toLowerCase().includes("however") && 
        !sentence.toLowerCase().includes("instead")) {
        
        const transition = simpleTransitions[Math.floor(Math.random() * simpleTransitions.length)];
        return transition + sentence.charAt(0).toLowerCase() + sentence.slice(1);
    }
    
    return sentence;
}

function calculateMetrics(text) {
    // Split text into words and sentences
    const words = text.split(/\s+/);
    const sentences = text.split(/[.!?]+/);
    
    // Calculate perplexity (simplified version)
    const perplexity = calculatePerplexity(words);
    
    // Calculate vocabulary diversity
    const vocabulary = calculateVocabularyDiversity(words);
    
    // Analyze sentence structure
    const sentenceStructure = analyzeSentenceStructure(sentences);
    
    // Check for pattern consistency
    const patternConsistency = checkPatternConsistency(text);
    
    // Calculate overall AI detection score
    const aiScore = calculateAIScore(perplexity, vocabulary, sentenceStructure, patternConsistency);
    
    return {
        perplexity,
        vocabulary,
        sentenceStructure,
        patternConsistency,
        aiScore
    };
}

function calculatePerplexity(words) {
    // Simplified perplexity calculation
    const wordFrequency = {};
    words.forEach(word => {
        wordFrequency[word] = (wordFrequency[word] || 0) + 1;
    });
    
    let totalProbability = 0;
    Object.values(wordFrequency).forEach(freq => {
        totalProbability += Math.log(freq / words.length);
    });
    
    return Math.exp(-totalProbability / words.length);
}

function calculateVocabularyDiversity(words) {
    const uniqueWords = new Set(words.map(word => word.toLowerCase()));
    return (uniqueWords.size / words.length) * 100;
}

function analyzeSentenceStructure(sentences) {
    // Remove empty sentences
    sentences = sentences.filter(s => s.trim().length > 0);
    
    // Calculate average sentence length
    const avgLength = sentences.reduce((acc, sent) => acc + sent.trim().split(/\s+/).length, 0) / sentences.length;
    
    // Calculate sentence length variance
    const lengths = sentences.map(sent => sent.trim().split(/\s+/).length);
    const variance = calculateVariance(lengths);
    
    return {
        averageLength: avgLength,
        variance: variance
    };
}

function checkPatternConsistency(text) {
    // Check for repetitive patterns
    const patterns = {
        similarStarts: checkSimilarSentenceStarts(text),
        wordRepetition: checkWordRepetition(text),
        structureRepetition: checkStructureRepetition(text)
    };
    
    return patterns;
}

function calculateAIScore(perplexity, vocabulary, sentenceStructure, patternConsistency) {
    // Weight different factors
    const weights = {
        perplexity: 0.3,
        vocabulary: 0.2,
        sentenceStructure: 0.3,
        patternConsistency: 0.2
    };
    
    // Normalize scores
    const normalizedPerplexity = Math.min(perplexity / 100, 1);
    const normalizedVocabulary = vocabulary / 100;
    const normalizedSentenceVariance = Math.min(sentenceStructure.variance / 10, 1);
    const normalizedPatterns = (patternConsistency.similarStarts + 
                               patternConsistency.wordRepetition + 
                               patternConsistency.structureRepetition) / 3;
    
    // Calculate weighted score
    const score = (
        normalizedPerplexity * weights.perplexity +
        normalizedVocabulary * weights.vocabulary +
        normalizedSentenceVariance * weights.sentenceStructure +
        normalizedPatterns * weights.patternConsistency
    ) * 100;
    
    return Math.min(Math.round(score), 100);
}

function updateResults(metrics) {
    // Update AI Score
    const aiScoreElement = document.getElementById('aiScore');
    aiScoreElement.textContent = metrics.aiScore + '%';
    aiScoreElement.className = 'score ' + getScoreClass(metrics.aiScore);
    
    // Update metrics
    document.getElementById('perplexityScore').textContent = 
        Math.round(metrics.perplexity) + ' (Lower is more human-like)';
    document.getElementById('vocabularyScore').textContent = 
        Math.round(metrics.vocabulary) + '% (Higher is more human-like)';
    document.getElementById('sentenceScore').textContent = 
        Math.round(metrics.sentenceStructure.variance) + ' (Higher is more human-like)';
    document.getElementById('patternScore').textContent = 
        Math.round((metrics.patternConsistency.similarStarts + 
                   metrics.patternConsistency.wordRepetition + 
                   metrics.patternConsistency.structureRepetition) / 3) + '% (Lower is more human-like)';
    
    // Generate suggestions
    generateSuggestions(metrics);
}

function getScoreClass(score) {
    if (score < 30) return 'low';
    if (score < 70) return 'medium';
    return 'high';
}

function generateSuggestions(metrics) {
    const suggestions = [];
    
    if (metrics.perplexity > 50) {
        suggestions.push('Add more natural variations in word choice and phrasing');
    }
    
    if (metrics.vocabulary < 40) {
        suggestions.push('Expand your vocabulary to include more diverse word choices');
    }
    
    if (metrics.sentenceStructure.variance < 5) {
        suggestions.push('Vary your sentence lengths and structures more naturally');
    }
    
    if (metrics.patternConsistency.similarStarts > 0.7) {
        suggestions.push('Avoid starting sentences with the same words or phrases');
    }
    
    if (metrics.patternConsistency.wordRepetition > 0.7) {
        suggestions.push('Reduce repetitive word usage and find synonyms');
    }
    
    if (metrics.patternConsistency.structureRepetition > 0.7) {
        suggestions.push('Mix up your sentence structures to sound more natural');
    }
    
    const suggestionsList = document.getElementById('suggestionsList');
    suggestionsList.innerHTML = suggestions.map(s => `<li>${s}</li>`).join('');
}

// Helper functions
function calculateVariance(numbers) {
    const mean = numbers.reduce((acc, val) => acc + val, 0) / numbers.length;
    const squareDiffs = numbers.map(value => {
        const diff = value - mean;
        return diff * diff;
    });
    return squareDiffs.reduce((acc, val) => acc + val, 0) / numbers.length;
}

function checkSimilarSentenceStarts(text) {
    const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
    const starts = sentences.map(s => s.trim().split(/\s+/)[0].toLowerCase());
    const uniqueStarts = new Set(starts);
    return 1 - (uniqueStarts.size / starts.length);
}

function checkWordRepetition(text) {
    const words = text.toLowerCase().split(/\s+/);
    const wordFrequency = {};
    words.forEach(word => {
        wordFrequency[word] = (wordFrequency[word] || 0) + 1;
    });
    
    const maxFrequency = Math.max(...Object.values(wordFrequency));
    return maxFrequency / words.length;
}

function checkStructureRepetition(text) {
    const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
    const structures = sentences.map(s => {
        const words = s.trim().split(/\s+/);
        return words.map(w => w.length).join(',');
    });
    
    const uniqueStructures = new Set(structures);
    return 1 - (uniqueStructures.size / structures.length);
}

// Add event listeners when the document is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add event listener for the analyze button
    const analyzeBtn = document.querySelector('.primary-btn');
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', analyzeText);
    }
    
    // Add event listener for the humanize button
    const humanizeBtn = document.querySelector('.secondary-btn');
    if (humanizeBtn) {
        humanizeBtn.addEventListener('click', humanizeText);
    }
}); 