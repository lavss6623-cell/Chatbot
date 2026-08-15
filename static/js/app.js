/* =====================================================
TNEA CHATBOT FRONTEND
===================================================== */

document.addEventListener("DOMContentLoaded", () => {

    /* =====================================================
       DOM ELEMENTS
       ===================================================== */

    const chatForm =
        document.getElementById("chatForm");
    const messageInput =
        document.getElementById("messageInput");
    const sendButton =
        document.getElementById("sendButton");
    const chatMessages =
        document.getElementById("chatMessages");


    /* =====================================================
       CONTROLS
       ===================================================== */

    const resetButton =
        document.getElementById("resetButton");

    const themeButton =
        document.getElementById("themeButton");


    /* =====================================================
   SIDEBAR ROBIN
===================================================== */

    const robinCharacter =
        document.getElementById("robinCharacter");

    const robinStatus =
        document.querySelector(
            ".robin-status-message span"
        );


    /* =====================================================
       PROFILE
       ===================================================== */

    const profileCutoff =
        document.getElementById("profileCutoff");

    const profileCommunity =
        document.getElementById("profileCommunity");

    const profileBranch =
        document.getElementById("profileBranch");


    /* =====================================================
       PROGRESS
       ===================================================== */

    const progressCutoff =
        document.getElementById("progressCutoff");

    const progressCommunity =
        document.getElementById("progressCommunity");

    const progressBranch =
        document.getElementById("progressBranch");

    const progressResults =
        document.getElementById("progressResults");


    /* =====================================================
       APPLICATION STATE
       ===================================================== */

    let isProcessing = false;

    let robinState = "idle";


    /* =====================================================
       ROBIN STATE SYSTEM
       ===================================================== */
    /*
     * -----------------------------------------------------
     * ROBIN MESSAGES
     * -----------------------------------------------------
     */

    const robinMessages = {

        idle:
            "I'm listening...",

        thinking:
            "Let me check the TNEA data..."

    };


    /*
     * -----------------------------------------------------
     * ROBIN IMAGES
     * -----------------------------------------------------
     *
     * IMPORTANT:
     *
     * These images control ONLY the large Robin character
     * in the sidebar.
     *
     * Other Robin images used inside chat messages are
     * NOT controlled by this state system.
     * -----------------------------------------------------
     */

    /*
     * -----------------------------------------------------
     * SET ROBIN STATE
     * -----------------------------------------------------
     */

    function setRobinState(state) {

    robinState = state;

    const robinMessages = {
        idle: "I'm listening...",
        thinking: "Let me check the TNEA data...",
        happy: "I found some useful information.",
        error: "Something went wrong. Let's try again."
    };


    /*
     * ---------------------------------------------
     * Robin ALWAYS uses robin-main.png
     * ---------------------------------------------
     */

    if (robinCharacter) {

        robinCharacter.src =
            "/static/images/robin-main.png";


        /*
         * Remove previous animation states.
         */

        robinCharacter.classList.remove(
            "robin-idle",
            "robin-thinking",
            "robin-happy",
            "robin-error"
        );


        /*
         * Apply the new visual state.
         */

        robinCharacter.classList.add(
            `robin-${state}`
        );

    }


    /*
     * ---------------------------------------------
     * Change speech bubble
     * ---------------------------------------------
     */

    if (robinStatus) {

        robinStatus.textContent =
            robinMessages[state] ||
            robinMessages.idle;

    }

}

    /*
     * -----------------------------------------------------
     * WAIT HELPER
     * -----------------------------------------------------
     */

    function wait(milliseconds) {

        return new Promise(resolve => {

            setTimeout(
                resolve,
                milliseconds
            );

        });

    }


    /* =====================================================
ESCAPE HTML
===================================================== */

    function escapeHTML(text) {

        const element =
            document.createElement("div");

        element.textContent =
            String(text ?? "");

        return element.innerHTML;

    }


    /* =====================================================
       FORMAT BOT RESPONSE
    ===================================================== */

    function formatBotResponse(text) {

        if (!text) {

            return "";

        }


        return escapeHTML(text)
            .replace(/\n/g, "<br>");

    }


    /* =====================================================
       CURRENT TIME
    ===================================================== */

    function getCurrentTime() {

        return new Date().toLocaleTimeString(
            [],
            {
                hour: "2-digit",
                minute: "2-digit"
            }
        );

    }


    /* =====================================================
       ADD USER MESSAGE
    ===================================================== */

    function addUserMessage(message) {

        const wrapper =
            document.createElement("div");


        wrapper.className =
            "message user-message";


        wrapper.innerHTML = `

            <div class="message-content">

                <div class="message-bubble">

                    <p>
                        ${escapeHTML(message)}
                    </p>

                </div>

                <span class="message-time">
                    ${getCurrentTime()}
                </span>

            </div>

        `;


        chatMessages.appendChild(
            wrapper
        );


        scrollToBottom();

    }


    /* =====================================================
       ADD ASSISTANT MESSAGE
    ===================================================== */

    function addAssistantMessage(message) {

        const wrapper =
            document.createElement("div");


        wrapper.className =
            "message assistant-message";


        /*
         * This is ONLY the small avatar beside
         * the chatbot message.
         *
         * It does NOT use robinCharacter.
         */

        wrapper.innerHTML = `

            <div class="message-avatar">

                <img
                    src="/static/images/robin-main.png"
                    alt="Robin"
                    loading="eager"
                >

            </div>


            <div class="message-content">

                <div class="message-bubble">

                    <p>
                        ${formatBotResponse(message)}
                    </p>

                </div>

                <span class="message-time">
                    ${getCurrentTime()}
                </span>

            </div>

        `;


        chatMessages.appendChild(
            wrapper
        );


        scrollToBottom();

    }

    /* =====================================================
   SHOW TYPING INDICATOR
===================================================== */

    function showTypingIndicator() {

        removeTypingIndicator();


        const wrapper =
            document.createElement("div");


        wrapper.id =
            "typingIndicator";


        wrapper.className =
            "message assistant-message";


        wrapper.innerHTML = `

            <div class="message-avatar">

                <img
                    src="/static/images/robin-main.png"
                    alt="Robin"
                >

            </div>


            <div class="message-content">

                <div class="typing-indicator">

                    <span></span>
                    <span></span>
                    <span></span>

                </div>

            </div>

        `;


        chatMessages.appendChild(
            wrapper
        );


        scrollToBottom();

    }


    /* =====================================================
       REMOVE TYPING INDICATOR
    ===================================================== */

    function removeTypingIndicator() {

        const indicator =
            document.getElementById(
                "typingIndicator"
            );


        if (indicator) {

            indicator.remove();

        }

    }


    /* =====================================================
       SCROLL CHAT
    ===================================================== */

    function scrollToBottom() {

        if (!chatMessages) {

            return;

        }


        chatMessages.scrollTo({

            top:
                chatMessages.scrollHeight,

            behavior:
                "smooth"

        });

    }

    /* =====================================================
   SEND MESSAGE
===================================================== */

    async function sendMessage(message) {

        /*
         * Clean message.
         */

        message =
            String(message ?? "").trim();


        /*
         * Ignore empty messages.
         */

        if (!message) {

            return;

        }


        /*
         * Prevent duplicate requests.
         */

        if (isProcessing) {

            return;

        }


        /*
         * Start processing.
         */

        isProcessing = true;


        /*
         * Disable input.
         */

        setInputState(true);


        /*
         * Show user's message.
         */

        addUserMessage(
            message
        );


        /*
         * Clear input.
         */

        messageInput.value = "";


        /*
         * -------------------------------------------------
         * ROBIN STARTS THINKING
         * -------------------------------------------------
         */

        const thinkingStartedAt =
            Date.now();


        setRobinState(
            "thinking"
        );


        /*
         * Show chat typing indicator.
         */

        showTypingIndicator();


        try {

            /*
             * -------------------------------------------------
             * SEND REQUEST TO FLASK
             * -------------------------------------------------
             */

            const response =
                await fetch(
                    "/chat",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            message:
                                message
                        })
                    }
                );


            /*
             * Parse JSON.
             */

            const data =
                await response.json();


            /*
             * Remove typing indicator.
             */

            removeTypingIndicator();


            /*
             * -------------------------------------------------
             * HTTP ERROR
             * -------------------------------------------------
             */

            if (!response.ok) {

                throw new Error(

                    data.error ||
                    "Unable to process your request."

                );

            }


            /*
             * -------------------------------------------------
             * BACKEND ERROR
             * -------------------------------------------------
             */

            if (data.error) {

                throw new Error(
                    data.error
                );

            }


            /*
             * -------------------------------------------------
             * UPDATE PROFILE
             * -------------------------------------------------
             */

            if (data.state) {

                updateProfile(
                    data.state
                );


                updateProgress(
                    data.state
                );

            }


            /*
             * -------------------------------------------------
             * ENSURE THINKING IS VISIBLE
             * -------------------------------------------------
             */

            const thinkingDuration =
                Date.now() -
                thinkingStartedAt;


            const minimumThinkingTime =
                1200;


            if (
                thinkingDuration <
                minimumThinkingTime
            ) {

                await wait(

                    minimumThinkingTime -
                    thinkingDuration

                );

            }


            /*
             * -------------------------------------------------
             * SHOW BOT RESPONSE
             * -------------------------------------------------
             */

            addAssistantMessage(

                data.response ||
                "I couldn't generate a response."

            );


            /*
             * -------------------------------------------------
             * RETURN SIDEBAR ROBIN TO MAIN IMAGE
             * -------------------------------------------------
             */

            setRobinState(
                "idle"
            );


        } catch (error) {

            console.error(
                "Chat error:",
                error
            );


            /*
             * Remove typing indicator.
             */

            removeTypingIndicator();


            /*
             * Return sidebar Robin to main image.
             */

            setRobinState(
                "idle"
            );


            /*
             * Show error.
             */

            addAssistantMessage(

                error.message ||
                "Something went wrong while contacting the server."

            );


        } finally {

            /*
             * Finish processing.
             */

            isProcessing =
                false;


            /*
             * Re-enable input.
             */

            setInputState(
                false
            );


            /*
             * Return focus to input.
             */

            messageInput.focus();

        }

    }

    /* =====================================================
   INPUT STATE
===================================================== */

    function setInputState(disabled) {

        if (messageInput) {

            messageInput.disabled =
                disabled;

        }


        if (sendButton) {

            sendButton.disabled =
                disabled;


            if (disabled) {

                sendButton.style.opacity =
                    "0.5";

                sendButton.style.cursor =
                    "not-allowed";

            } else {

                sendButton.style.opacity =
                    "";

                sendButton.style.cursor =
                    "";

            }

        }

    }


    /* =====================================================
       USER TYPING
    ===================================================== */

    if (messageInput) {

        messageInput.addEventListener(
            "input",
            () => {

                /*
                 * Typing does NOT activate thinking.
                 *
                 * Robin stays on robin-main.png.
                 */

                if (!isProcessing) {

                    setRobinState(
                        "idle"
                    );

                }

            }
        );

    }


    /* =====================================================
       FORM SUBMISSION
    ===================================================== */

    if (chatForm) {

        chatForm.addEventListener(
            "submit",
            event => {

                event.preventDefault();


                if (isProcessing) {

                    return;

                }


                sendMessage(
                    messageInput.value
                );

            }
        );

    }


    /* =====================================================
       ENTER KEY
    ===================================================== */

    if (messageInput) {

        messageInput.addEventListener(
            "keydown",
            event => {

                if (
                    event.key === "Enter" &&
                    !event.shiftKey
                ) {

                    event.preventDefault();


                    if (isProcessing) {

                        return;

                    }


                    sendMessage(
                        messageInput.value
                    );

                }

            }
        );

    }


    /* =====================================================
       QUICK PROMPTS
    ===================================================== */

    const quickPromptButtons =
        document.querySelectorAll(
            ".quick-prompt"
        );


    quickPromptButtons.forEach(
        button => {

            button.addEventListener(
                "click",
                () => {

                    if (isProcessing) {

                        return;

                    }


                    const message =
                        button.dataset.message ||
                        button.textContent.trim();


                    if (!message) {

                        return;

                    }


                    sendMessage(
                        message
                    );

                }
            );

        }
    );

    /* =====================================================
   RESET CHAT
===================================================== */

function resetFrontend() {

    /*
     * ---------------------------------------------
     * Remove conversation messages
     * ---------------------------------------------
     */

    if (chatMessages) {

        const dynamicMessages =
            chatMessages.querySelectorAll(
                ".user-message, .assistant-message, #typingIndicator"
            );

        dynamicMessages.forEach(
            element => {
                element.remove();
            }
        );

    }


    /*
     * ---------------------------------------------
     * Restore initial Robin welcome message
     * ---------------------------------------------
     */

    const welcomeMessage = document.createElement(
        "div"
    );

    welcomeMessage.className =
        "message assistant-message";

    welcomeMessage.innerHTML = `
        <div class="message-avatar">
            <img
                src="/static/images/robin-main.png"
                alt="Robin"
            />
        </div>

        <div class="message-content">

            <div class="message-bubble">

                <p>Hello! I'm Robin.</p>

                <p>Your TNEA AI Assistant.</p>

            </div>

            <span class="message-time">
                Now
            </span>

        </div>
    `;


    /*
     * Insert the welcome message
     * before the static welcome section.
     */

    if (chatMessages) {

        const welcomeBlock =
            chatMessages.querySelector(
                ".welcome-block"
            );

        if (welcomeBlock) {

            chatMessages.insertBefore(
                welcomeMessage,
                welcomeBlock
            );

        } else {

            chatMessages.appendChild(
                welcomeMessage
            );

        }

    }


    /*
     * ---------------------------------------------
     * Reset profile
     * ---------------------------------------------
     */

    if (profileCutoff) {

        profileCutoff.textContent =
            "—";

    }


    if (profileCommunity) {

        profileCommunity.textContent =
            "—";

    }


    if (profileBranch) {

        profileBranch.textContent =
            "—";

    }


    /*
     * ---------------------------------------------
     * Reset counselling progress
     * ---------------------------------------------
     */

    [
        progressCutoff,
        progressCommunity,
        progressBranch,
        progressResults

    ].forEach(
        step => {

            step?.classList.remove(
                "completed",
                "current"
            );

        }
    );


    /*
     * ---------------------------------------------
     * Reset Robin
     * ---------------------------------------------
     */

    setRobinState(
        "idle"
    );


    /*
     * ---------------------------------------------
     * Clear input
     * ---------------------------------------------
     */

    if (messageInput) {

        messageInput.value = "";
        messageInput.focus();

    }

}
    
    /* =====================================================
   RESET BUTTON
===================================================== */

if (resetButton) {

    resetButton.addEventListener(
        "click",
        async () => {

            /*
             * Don't reset while a message is
             * currently being processed.
             */

            if (isProcessing) {
                return;
            }


            /*
             * Confirm reset.
             */

            const confirmed =
                window.confirm(
                    "Reset your TNEA conversation?"
                );


            if (!confirmed) {
                return;
            }


            try {

                /*
                 * Reset BACKEND conversation state.
                 */

                const response =
                    await fetch(
                        "/reset",
                        {
                            method: "POST"
                        }
                    );


                /*
                 * Read backend response.
                 */

                const data =
                    await response.json();


                /*
                 * Backend reset failed.
                 */

                if (!response.ok) {

                    throw new Error(
                        data.error ||
                        "Unable to reset the conversation."
                    );

                }


                /*
                 * Reset FRONTEND state
                 * only after backend reset succeeds.
                 */

                resetFrontend();


                /*
                 * Keep the frontend profile
                 * synchronized with backend.
                 */

                if (data.state) {

                    updateProfile(
                        data.state
                    );

                    updateProgress(
                        data.state
                    );

                }


                console.log(
                    "TNEA conversation reset successfully."
                );


            } catch (error) {

                console.error(
                    "Reset error:",
                    error
                );

                alert(
                    "Unable to reset the conversation. Please try again."
                );

            }

        }
    );

}

    /* =====================================================
       UPDATE PROFILE
    ===================================================== */

    function updateProfile(state) {

        if (!state) {

            return;

        }


        if (
            state.cutoff !== null &&
            state.cutoff !== undefined
        ) {

            profileCutoff.textContent =
                state.cutoff;

        }


        if (state.community) {

            profileCommunity.textContent =
                state.community;

        }


        if (state.branch) {

            profileBranch.textContent =
                formatBranchName(
                    state.branch
                );

        }

    }


    /* =====================================================
       FORMAT BRANCH NAME
    ===================================================== */

    function formatBranchName(branch) {

        if (!branch) {

            return "—";

        }


        const branchNames = {

            cse:
                "CSE",

            ece:
                "ECE",

            eee:
                "EEE",

            it:
                "IT",

            mechanical:
                "Mechanical",

            civil:
                "Civil",

            "computer science and engineering":
                "CSE",

            "electronics and communication engineering":
                "ECE",

            "electrical and electronics engineering":
                "EEE"

        };


        const normalized =
            branch
                .toString()
                .trim()
                .toLowerCase();


        return (
            branchNames[normalized] ||
            branch
        );

    }

    /* =====================================================
   UPDATE PROGRESS
===================================================== */

    function updateProgress(state) {

        if (!state) {

            return;

        }


        /*
         * Determine completed information.
         */

        const hasCutoff =
            state.cutoff !== null &&
            state.cutoff !== undefined;


        const hasCommunity =
            Boolean(
                state.community
            );


        const hasBranch =
            Boolean(
                state.branch
            );


        const recommendationReady =
            hasCutoff &&
            hasCommunity &&
            hasBranch;


        /*
         * Cutoff.
         */

        if (progressCutoff) {

            progressCutoff.classList.toggle(
                "completed",
                hasCutoff
            );

        }


        /*
         * Community.
         */

        if (progressCommunity) {

            progressCommunity.classList.toggle(
                "completed",
                hasCommunity
            );

        }


        /*
         * Branch.
         */

        if (progressBranch) {

            progressBranch.classList.toggle(
                "completed",
                hasBranch
            );

        }


        /*
         * Recommendations.
         */

        if (progressResults) {

            progressResults.classList.toggle(
                "completed",
                recommendationReady
            );

        }

    }
    /* =====================================================
   THEME TOGGLE
===================================================== */

    if (themeButton) {

        themeButton.addEventListener(
            "click",
            () => {

                document.body.classList.toggle(
                    "light-theme"
                );


                const isLight =
                    document.body.classList.contains(
                        "light-theme"
                    );


                localStorage.setItem(
                    "tnea-theme",
                    isLight
                        ? "light"
                        : "dark"
                );

            }
        );

    }


    /* =====================================================
       LOAD SAVED THEME
    ===================================================== */

    const savedTheme =
        localStorage.getItem(
            "tnea-theme"
        );


    if (savedTheme === "light") {

        document.body.classList.add(
            "light-theme"
        );

    }


    /* =====================================================
       SIDEBAR NAVIGATION
    ===================================================== */

    const navigationItems =
        document.querySelectorAll(
            "[data-section]"
        );


    navigationItems.forEach(
        item => {

            item.addEventListener(
                "click",
                event => {

                    event.preventDefault();


                    const section =
                        item.dataset.section;


                    if (!section) {

                        return;

                    }


                    navigationItems.forEach(
                        navItem => {

                            navItem.classList.remove(
                                "active"
                            );

                        }
                    );


                    item.classList.add(
                        "active"
                    );


                    const target =
                        document.getElementById(
                            section
                        );


                    if (target) {

                        target.scrollIntoView({

                            behavior:
                                "smooth",

                            block:
                                "start"

                        });

                    }

                }
            );

        }
    );


    /* =====================================================
       QUICK PROMPT KEYBOARD ACCESSIBILITY
    ===================================================== */

    quickPromptButtons.forEach(
        button => {

            button.setAttribute(
                "role",
                "button"
            );


            button.setAttribute(
                "tabindex",
                "0"
            );


            button.addEventListener(
                "keydown",
                event => {

                    if (
                        event.key === "Enter" ||
                        event.key === " "
                    ) {

                        event.preventDefault();

                        button.click();

                    }

                }
            );

        }
    );


    /* =====================================================
       INITIAL ROBIN
    ===================================================== */

    setRobinState(
        "idle"
    );


    /* =====================================================
       INITIAL PROFILE
    ===================================================== */

    updateProfile({

        cutoff:
            null,

        community:
            null,

        branch:
            null

    });


    /* =====================================================
       INITIAL PROGRESS
    ===================================================== */

    updateProgress({

        cutoff:
            null,

        community:
            null,

        branch:
            null

    });


    /* =====================================================
       INITIAL INPUT
    ===================================================== */

    setInputState(
        false
    );


    /*
     * Focus input.
     */

    if (messageInput) {

        messageInput.focus();

    }


    /* =====================================================
       DEBUG INFORMATION
    ===================================================== */

    console.log(
        "TNEA AI frontend initialized."
    );


    console.log(
        "Robin state:",
        robinState
    );


    console.log(
        "Robin character:",
        robinCharacter
    );



    /* =====================================================
       END DOMContentLoaded
    ===================================================== */

});