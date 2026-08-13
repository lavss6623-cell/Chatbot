/* ============================================================
   TNEA COUNSELLING ASSISTANT
   FRONTEND JAVASCRIPT
============================================================ */


/* ============================================================
   DOM ELEMENTS
============================================================ */

const chatForm = document.getElementById("chatForm");

const messageInput = document.getElementById("messageInput");

const chatMessages = document.getElementById("chatMessages");

const mascot = document.getElementById("mascot");

const assistantBubble =
    document.getElementById("assistantBubble");

const profileCutoff =
    document.getElementById("profileCutoff");

const profileCommunity =
    document.getElementById("profileCommunity");

const profileBranch =
    document.getElementById("profileBranch");

const progressPercent =
    document.getElementById("progressPercent");

const progressFill =
    document.getElementById("progressFill");


/* ============================================================
   APPLICATION STATE
============================================================ */

let isProcessing = false;


/* ============================================================
   SEND MESSAGE
============================================================ */

async function sendMessage(message) {

    /*
        Prevent empty messages
    */

    if (!message || !message.trim()) {
        return;
    }


    /*
        Prevent multiple requests at the same time
    */

    if (isProcessing) {
        return;
    }


    message = message.trim();


    /*
        Remove welcome suggestions after first message
    */

    removeWelcomeMessage();


    /*
        Add user's message
    */

    addUserMessage(message);


    /*
        Clear input box
    */

    messageInput.value = "";


    /*
        Start assistant thinking state
    */

    setAssistantState("thinking");


    /*
        Add typing indicator
    */

    const typingMessage = addTypingMessage();


    isProcessing = true;


    try {

        /*
            Send request to Flask
        */

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });


        /*
            Convert response to JSON
        */

        const data = await response.json();


        /*
            Remove typing indicator
        */

        removeTypingMessage(typingMessage);


        /*
            Handle backend errors
        */

        if (!response.ok || data.error) {

            addBotMessage(
                data.error ||
                "Something went wrong while processing your message."
            );

            setAssistantState("error");

            return;
        }


        /*
            Display bot response
        */

        addBotMessage(data.response);


        /*
            Update profile information
        */

        if (data.state) {

            updateProfile(data.state);

            updateProgress(data.state);

        }


        /*
            Assistant finished successfully
        */

        setAssistantState("happy");


    } catch (error) {

        console.error("Chat error:", error);


        removeTypingMessage(typingMessage);


        addBotMessage(
            "I couldn't connect to the TNEA server. Please make sure Flask is running."
        );


        setAssistantState("error");


    } finally {

        isProcessing = false;

        messageInput.focus();

    }

}


/* ============================================================
   FORM SUBMISSION
============================================================ */

if (chatForm) {

    chatForm.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();

            sendMessage(messageInput.value);

        }
    );

}


/* ============================================================
   ENTER KEY
============================================================ */

if (messageInput) {

    messageInput.addEventListener(
        "keydown",
        function (event) {

            /*
                Enter sends the message.
            */

            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {

                event.preventDefault();

                sendMessage(messageInput.value);

            }

        }
    );

}


/* ============================================================
   ADD USER MESSAGE
============================================================ */

function addUserMessage(message) {

    const row = document.createElement("div");

    row.className =
        "message-row user-row";


    const bubble = document.createElement("div");

    bubble.className =
        "message user-message";


    /*
        textContent prevents HTML injection.
    */

    bubble.textContent = message;


    row.appendChild(bubble);


    chatMessages.appendChild(row);


    scrollToBottom();

}


/* ============================================================
   ADD BOT MESSAGE
============================================================ */

function addBotMessage(message) {

    const row = document.createElement("div");

    row.className =
        "message-row bot-row";


    /*
        Avatar
    */

    const avatarContainer =
        document.createElement("div");

    avatarContainer.className =
        "message-avatar";


    const avatar =
        document.createElement("div");

    avatar.className =
        "mini-avatar";

    avatar.textContent = "◉";


    avatarContainer.appendChild(avatar);


    /*
        Message bubble
    */

    const bubble =
        document.createElement("div");

    bubble.className =
        "message bot-message";


    /*
        Preserve line breaks
    */

    bubble.style.whiteSpace =
        "pre-wrap";


    bubble.textContent = message;


    /*
        Build row
    */

    row.appendChild(avatarContainer);

    row.appendChild(bubble);


    chatMessages.appendChild(row);


    scrollToBottom();

}


/* ============================================================
   TYPING INDICATOR
============================================================ */

function addTypingMessage() {

    const row =
        document.createElement("div");

    row.className =
        "message-row bot-row";


    row.dataset.typing =
        "true";


    /*
        Avatar
    */

    const avatarContainer =
        document.createElement("div");

    avatarContainer.className =
        "message-avatar";


    const avatar =
        document.createElement("div");

    avatar.className =
        "mini-avatar";

    avatar.textContent =
        "◉";


    avatarContainer.appendChild(avatar);


    /*
        Bubble
    */

    const bubble =
        document.createElement("div");

    bubble.className =
        "message bot-message";


    /*
        Typing animation
    */

    const indicator =
        document.createElement("div");

    indicator.className =
        "typing-indicator";


    for (let i = 0; i < 3; i++) {

        const dot =
            document.createElement("span");

        indicator.appendChild(dot);

    }


    bubble.appendChild(indicator);


    row.appendChild(avatarContainer);

    row.appendChild(bubble);


    chatMessages.appendChild(row);


    scrollToBottom();


    return row;

}


/* ============================================================
   REMOVE TYPING MESSAGE
============================================================ */

function removeTypingMessage(element) {

    if (!element) {
        return;
    }


    if (element.parentNode) {

        element.parentNode.removeChild(element);

    }

}


/* ============================================================
   REMOVE WELCOME MESSAGE
============================================================ */

function removeWelcomeMessage() {

    const welcome =
        document.querySelector(
            ".welcome-message"
        );


    if (welcome) {

        const row =
            welcome.closest(
                ".message-row"
            );


        if (row) {

            row.remove();

        } else {

            welcome.remove();

        }

    }

}


/* ============================================================
   SCROLL CHAT TO BOTTOM
============================================================ */

function scrollToBottom() {

    if (!chatMessages) {
        return;
    }


    setTimeout(
        function () {

            chatMessages.scrollTop =
                chatMessages.scrollHeight;

        },
        50
    );

}


/* ============================================================
   UPDATE PROFILE
============================================================ */

function updateProfile(state) {

    if (!state) {
        return;
    }


    /*
        Cutoff
    */

    if (
        state.cutoff !== null &&
        state.cutoff !== undefined
    ) {

        profileCutoff.textContent =
            state.cutoff;

    } else {

        profileCutoff.textContent =
            "Not set";

    }


    /*
        Community
    */

    if (
        state.community !== null &&
        state.community !== undefined
    ) {

        profileCommunity.textContent =
            state.community.toUpperCase();

    } else {

        profileCommunity.textContent =
            "Not set";

    }


    /*
        Branch
    */

    if (
        state.branch !== null &&
        state.branch !== undefined
    ) {

        profileBranch.textContent =
            formatBranch(state.branch);

    } else {

        profileBranch.textContent =
            "Not set";

    }

}


/* ============================================================
   FORMAT BRANCH NAME
============================================================ */

function formatBranch(branch) {

    if (!branch) {
        return "Not set";
    }


    const branchMap = {

        "cse":
            "CSE",

        "ece":
            "ECE",

        "eee":
            "EEE",

        "mech":
            "Mechanical",

        "civil":
            "Civil",

        "it":
            "IT"

    };


    const normalized =
        branch.toLowerCase().trim();


    if (branchMap[normalized]) {

        return branchMap[normalized];

    }


    /*
        If backend sends a full branch name,
        keep it readable.
    */

    return branch
        .toLowerCase()
        .replace(/\b\w/g, function (letter) {

            return letter.toUpperCase();

        });

}


/* ============================================================
   UPDATE COUNSELLING PROGRESS
============================================================ */

function updateProgress(state) {

    if (!state) {
        return;
    }


    let completed = 0;


    /*
        Cutoff
    */

    const cutoffStep =
        document.getElementById(
            "stepCutoff"
        );


    if (
        state.cutoff !== null &&
        state.cutoff !== undefined
    ) {

        completed++;

        cutoffStep.classList.add(
            "completed"
        );

    } else {

        cutoffStep.classList.remove(
            "completed"
        );

    }


    /*
        Community
    */

    const communityStep =
        document.getElementById(
            "stepCommunity"
        );


    if (
        state.community !== null &&
        state.community !== undefined
    ) {

        completed++;

        communityStep.classList.add(
            "completed"
        );

    } else {

        communityStep.classList.remove(
            "completed"
        );

    }


    /*
        Branch
    */

    const branchStep =
        document.getElementById(
            "stepBranch"
        );


    if (
        state.branch !== null &&
        state.branch !== undefined
    ) {

        completed++;

        branchStep.classList.add(
            "completed"
        );

    } else {

        branchStep.classList.remove(
            "completed"
        );

    }


    /*
        Recommendation

        We consider the recommendation
        stage complete when all three
        profile values exist.
    */

    const recommendationStep =
        document.getElementById(
            "stepRecommendation"
        );


    if (
        state.cutoff !== null &&
        state.community !== null &&
        state.branch !== null
    ) {

        completed++;

        recommendationStep.classList.add(
            "completed"
        );

    } else {

        recommendationStep.classList.remove(
            "completed"
        );

    }


    /*
        Calculate percentage
    */

    const percentage =
        Math.round(
            (completed / 4) * 100
        );


    progressPercent.textContent =
        `${percentage}%`;


    progressFill.style.width =
        `${percentage}%`;

}


/* ============================================================
   ASSISTANT STATES
============================================================ */

function setAssistantState(state) {

    if (!mascot) {
        return;
    }


    /*
        Remove previous states
    */

    mascot.classList.remove(
        "thinking",
        "happy",
        "error"
    );


    if (state === "thinking") {

        mascot.classList.add(
            "thinking"
        );


        assistantBubble.textContent =
            "Hmm... let me check the TNEA data.";

    }


    else if (state === "happy") {

        mascot.classList.add(
            "happy"
        );


        assistantBubble.textContent =
            "Done! I found something useful for you.";

    }


    else if (state === "error") {

        mascot.classList.add(
            "error"
        );


        assistantBubble.textContent =
            "Something went wrong. Let's try again.";

    }


    else {

        assistantBubble.innerHTML =
            "Hi! I'm your TNEA assistant.<br>Let's find the right college for you.";

    }

}


/* ============================================================
   MASCOT INTERACTION
============================================================ */

if (mascot) {

    mascot.addEventListener(
        "click",
        function () {

            mascot.classList.add(
                "happy"
            );


            assistantBubble.textContent =
                "I'm ready! Ask me about TNEA.";

        }
    );

}


/* ============================================================
   RESET CONVERSATION
============================================================ */

async function resetChat() {

    /*
        Confirm reset
    */

    const confirmed =
        window.confirm(
            "Reset your TNEA counselling conversation?"
        );


    if (!confirmed) {
        return;
    }


    try {

        /*
            Call Flask reset endpoint.
        */

        const response =
            await fetch(
                "/reset",
                {
                    method: "POST"
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Reset failed"
            );

        }


        /*
            Clear messages
        */

        chatMessages.innerHTML = "";


        /*
            Reset profile
        */

        profileCutoff.textContent =
            "Not set";

        profileCommunity.textContent =
            "Not set";

        profileBranch.textContent =
            "Not set";


        /*
            Reset progress
        */

        progressPercent.textContent =
            "0%";

        progressFill.style.width =
            "0%";


        document
            .querySelectorAll(
                ".progress-step"
            )
            .forEach(
                function (step) {

                    step.classList.remove(
                        "completed"
                    );

                }
            );


        /*
            Reset mascot
        */

        setAssistantState(
            "idle"
        );


        /*
            Add welcome screen again
        */

        addWelcomeMessage();


        messageInput.focus();


    } catch (error) {

        console.error(
            "Reset error:",
            error
        );


        /*
            Even if the backend reset
            fails, don't silently pretend
            everything worked.
        */

        addBotMessage(
            "I couldn't reset the conversation. Please try again."
        );

    }

}


/* ============================================================
   RESTORE WELCOME MESSAGE
============================================================ */

function addWelcomeMessage() {

    const row =
        document.createElement(
            "div"
        );

    row.className =
        "message-row bot-row";


    const avatarContainer =
        document.createElement(
            "div"
        );

    avatarContainer.className =
        "message-avatar";


    const avatar =
        document.createElement(
            "div"
        );

    avatar.className =
        "mini-avatar";

    avatar.textContent =
        "◉";


    avatarContainer.appendChild(
        avatar
    );


    const bubble =
        document.createElement(
            "div"
        );

    bubble.className =
        "message bot-message welcome-message";


    bubble.innerHTML = `

        <h3>Hello!</h3>

        <p>
            I can help you explore TNEA
            counselling using the 2025
            cutoff dataset.
        </p>

        <p>
            Find colleges, branches and
            cutoff information based on
            your cutoff and community.
        </p>

        <div class="message-divider"></div>

        <h4>✦ Try asking:</h4>

        <div class="suggestions">

            <button
                type="button"
                class="suggestion-button"
                onclick="sendMessage('I want CSE colleges')"
            >
                🎓
                <span>I want CSE colleges</span>
                <strong>→</strong>
            </button>

            <button
                type="button"
                class="suggestion-button"
                onclick="sendMessage('What is the cutoff for CSE?')"
            >
                ▥
                <span>What is the cutoff for CSE?</span>
                <strong>→</strong>
            </button>

            <button
                type="button"
                class="suggestion-button"
                onclick="sendMessage('What branches are available?')"
            >
                ⌘
                <span>What branches are available?</span>
                <strong>→</strong>
            </button>

            <button
                type="button"
                class="suggestion-button"
                onclick="sendMessage('Tell me about Anna University')"
            >
                ⌂
                <span>Tell me about Anna University</span>
                <strong>→</strong>
            </button>

        </div>

    `;


    row.appendChild(
        avatarContainer
    );

    row.appendChild(
        bubble
    );


    chatMessages.appendChild(
        row
    );


    scrollToBottom();

}


/* ============================================================
   INITIALIZE
============================================================ */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        messageInput.focus();

        updateProgress({
            cutoff: null,
            community: null,
            branch: null
        });

    }
);