// =====================================================
// GET HTML ELEMENTS
// =====================================================

const chatMessages = document.getElementById("chatArea");
const userInput = document.getElementById("messageInput");


// =====================================================
// STUDENT DATA
// =====================================================

const students = {

    ashwikha: {
        name: "Ashwikha",
        rollNo: "23CSE001",
        branch: "CSE",
        cgpa: 8.8,
        backlogs: 0,
        gradYear: 2029
    },

    danish: {
        name: "Danish",
        rollNo: "23CSE002",
        branch: "CSE",
        cgpa: 7.2,
        backlogs: 1,
        gradYear: 2029
    },

    rahul: {
        name: "Rahul",
        rollNo: "23ECE001",
        branch: "ECE",
        cgpa: 8.5,
        backlogs: 0,
        gradYear: 2029
    }

};


// =====================================================
// COMPANY DATA
// =====================================================

const companies = {

    tcs: {
        name: "TCS",
        role: "Software Engineer",
        ctc: 7.5,
        deadline: "2026-10-15",
        minCgpa: 7.5,
        maxBacklogs: 0,
        allowedBranches: ["CSE", "IT"],
        gradYear: 2029
    },

    infosys: {
        name: "Infosys",
        role: "Systems Engineer",
        ctc: 6.0,
        deadline: "2026-10-20",
        minCgpa: 7.0,
        maxBacklogs: 1,
        allowedBranches: ["CSE", "IT", "ECE"],
        gradYear: 2029
    }

};


// =====================================================
// SEND MESSAGE
// =====================================================

function sendMessage() {

    const message = userInput.value.trim();

    // Do nothing if input is empty

    if (!message) {
        return;
    }


    // Hide welcome screen

    const welcomeScreen =
        document.getElementById("welcomeScreen");

    if (welcomeScreen) {
        welcomeScreen.style.display = "none";
    }


    // Show user message

    addUserMessage(message);


    // Clear input

    userInput.value = "";

    userInput.style.height = "auto";


    // Start agent processing

    showAgentProcessing(message);

}


// =====================================================
// ADD USER MESSAGE
// =====================================================

function addUserMessage(message) {

    const messageDiv =
        document.createElement("div");


    messageDiv.className =
        "message user-message";


    messageDiv.innerHTML = `

        <div class="message-content">

            ${escapeHTML(message)}

        </div>

    `;


    chatMessages.appendChild(messageDiv);


    scrollToBottom();

}


// =====================================================
// SHOW AGENT PROCESSING
// =====================================================

function showAgentProcessing(question) {

    const processingDiv =
        document.createElement("div");


    processingDiv.className =
        "agent-processing";


    processingDiv.innerHTML = `

        <div class="processing-title">

            <span class="processing-dot"></span>

            Agent is working...

        </div>


        <div class="tool-status">

            ✓ Understanding student name

        </div>


        <div class="tool-status">

            ✓ Checking placement drive

        </div>


        <div class="tool-status">

            ✓ Checking eligibility requirements

        </div>

    `;


    chatMessages.appendChild(processingDiv);


    scrollToBottom();


    // Wait for 1 second

    setTimeout(function () {

        processingDiv.remove();

        generateResponse(question);

    }, 1000);

}


// =====================================================
// GENERATE RESPONSE
// =====================================================

function generateResponse(question) {

    const lowerQuestion =
        question.toLowerCase();


    let student = null;

    let company = null;


    // =================================================
    // FIND STUDENT
    // =================================================

    for (const key in students) {

        if (lowerQuestion.includes(key)) {

            student = students[key];

            break;
        }

    }


    // =================================================
    // FIND COMPANY
    // =================================================

    for (const key in companies) {

        if (lowerQuestion.includes(key)) {

            company = companies[key];

            break;
        }

    }


    // =================================================
    // STUDENT NOT FOUND
    // =================================================

    if (!student) {

        addAgentMessage(`

            <p>
                I couldn't identify the student.
            </p>

            <p>
                Try:
                <b>Danish</b>,
                <b>Rahul</b>,
                or
                <b>Ashwikha</b>.
            </p>

        `);

        return;

    }


    // =================================================
    // COMPANY NOT FOUND
    // =================================================

    if (!company) {

        addAgentMessage(`

            <p>
                I found the student
                <b>${student.name}</b>.
            </p>

            <p>
                Please mention a company such as
                <b>TCS</b> or
                <b>Infosys</b>.
            </p>

        `);

        return;

    }


    // =================================================
    // CHECK REQUIREMENTS
    // =================================================


    // CGPA

    const cgpaPassed =
        student.cgpa >= company.minCgpa;


    // Backlogs

    const backlogPassed =
        student.backlogs <= company.maxBacklogs;


    // Branch

    const branchPassed =
        company.allowedBranches.includes(
            student.branch
        );


    // Graduation year

    const gradYearPassed =
        student.gradYear === company.gradYear;


    // Overall eligibility

    const eligible =
        cgpaPassed &&
        backlogPassed &&
        branchPassed &&
        gradYearPassed;


    // =================================================
    // SHOW RESULT
    // =================================================

    addEligibilityResponse(

        student,

        company,

        cgpaPassed,

        backlogPassed,

        branchPassed,

        gradYearPassed,

        eligible

    );

}


// =====================================================
// ELIGIBILITY RESULT
// =====================================================

function addEligibilityResponse(

    student,

    company,

    cgpaPassed,

    backlogPassed,

    branchPassed,

    gradYearPassed,

    eligible

) {


    const resultDiv =
        document.createElement("div");


    resultDiv.className =
        "agent-message";


    resultDiv.innerHTML = `

        <div class="result-card">


            <!-- RESULT HEADER -->

            <div class="result-header">


                <div>

                    <h3>
                        ${student.name}
                    </h3>

                    <p>
                        ${student.rollNo}
                    </p>

                </div>


                <div
                    class="${eligible
                        ? "eligible"
                        : "not-eligible"}"
                >

                    ${
                        eligible
                            ? "Eligible"
                            : "Not Eligible"
                    }

                </div>

            </div>


            <!-- STUDENT DETAILS -->

            <div class="student-details">


                <div class="detail">

                    <span>
                        Branch
                    </span>

                    <strong>
                        ${student.branch}
                    </strong>

                </div>


                <div class="detail">

                    <span>
                        CGPA
                    </span>

                    <strong>
                        ${student.cgpa}
                    </strong>

                </div>


                <div class="detail">

                    <span>
                        Backlogs
                    </span>

                    <strong>
                        ${student.backlogs}
                    </strong>

                </div>


                <div class="detail">

                    <span>
                        Graduation Year
                    </span>

                    <strong>
                        ${student.gradYear}
                    </strong>

                </div>


            </div>


            <!-- COMPANY -->

            <div class="company-section">

                <h4>
                    ${company.name}
                </h4>

                <p>
                    ${company.role}
                    •
                    ${company.ctc} LPA
                </p>

            </div>


            <!-- REQUIREMENTS -->

            <div class="requirements">


                <div
                    class="${cgpaPassed
                        ? "passed"
                        : "failed"}"
                >

                    ${cgpaPassed ? "✓" : "✗"}

                    CGPA ≥ ${company.minCgpa}

                </div>


                <div
                    class="${backlogPassed
                        ? "passed"
                        : "failed"}"
                >

                    ${backlogPassed ? "✓" : "✗"}

                    Backlogs ≤ ${company.maxBacklogs}

                </div>


                <div
                    class="${branchPassed
                        ? "passed"
                        : "failed"}"
                >

                    ${branchPassed ? "✓" : "✗"}

                    Branch:
                    ${company.allowedBranches.join(", ")}

                </div>


                <div
                    class="${gradYearPassed
                        ? "passed"
                        : "failed"}"
                >

                    ${gradYearPassed ? "✓" : "✗"}

                    Graduation Year:
                    ${company.gradYear}

                </div>


            </div>


            <!-- SUMMARY -->

            <div class="result-summary">

                ${
                    eligible

                    ? `
                        <strong>
                            ${student.name}
                            is eligible for
                            ${company.name}.
                        </strong>
                    `

                    : `
                        <strong>
                            ${student.name}
                            is not eligible for
                            ${company.name}.
                        </strong>
                    `
                }

            </div>


        </div>

    `;


    chatMessages.appendChild(resultDiv);


    scrollToBottom();

}


// =====================================================
// NORMAL AGENT MESSAGE
// =====================================================

function addAgentMessage(message) {

    const messageDiv =
        document.createElement("div");


    messageDiv.className =
        "agent-message";


    messageDiv.innerHTML = `

        <div class="agent-avatar">
            PA
        </div>

        <div class="message-content">

            ${message}

        </div>

    `;


    chatMessages.appendChild(messageDiv);


    scrollToBottom();

}


// =====================================================
// EXAMPLE QUESTIONS
// =====================================================

function useExample(question) {

    userInput.value = question;

    sendMessage();

}


// =====================================================
// NEW CHAT
// =====================================================

function newChat() {

    chatMessages.innerHTML = `

        <div
            class="welcome"
            id="welcomeScreen"
        >

            <div class="welcome-icon">
                ✦
            </div>


            <h2>
                How can I help you?
            </h2>


            <p>
                Ask me about student eligibility,
                placement drives, or eligibility requirements.
            </p>


            <div class="example-grid">


                <button
                    onclick="useExample('Is Danish eligible for TCS?')"
                >

                    <span>🎓</span>

                    <div>

                        <strong>
                            Check eligibility
                        </strong>

                        <small>
                            Is Danish eligible for TCS?
                        </small>

                    </div>

                </button>


                <button
                    onclick="useExample('What is the TCS placement drive?')"
                >

                    <span>🏢</span>

                    <div>

                        <strong>
                            Company information
                        </strong>

                        <small>
                            What is the TCS placement drive?
                        </small>

                    </div>

                </button>


                <button
                    onclick="useExample('What are the TCS eligibility requirements?')"
                >

                    <span>📋</span>

                    <div>

                        <strong>
                            Requirements
                        </strong>

                        <small>
                            What are the TCS requirements?
                        </small>

                    </div>

                </button>


            </div>

        </div>

    `;


    scrollToBottom();

}


// =====================================================
// ENTER KEY
// =====================================================

function handleKeyDown(event) {

    if (
        event.key === "Enter" &&
        !event.shiftKey
    ) {

        event.preventDefault();

        sendMessage();

    }

}


// =====================================================
// TEXTAREA AUTO RESIZE
// =====================================================

userInput.addEventListener(
    "input",
    function () {

        this.style.height = "auto";

        this.style.height =
            this.scrollHeight + "px";

    }
);


// =====================================================
// SCROLL TO BOTTOM
// =====================================================

function scrollToBottom() {

    chatMessages.scrollTop =
        chatMessages.scrollHeight;

}


// =====================================================
// ESCAPE HTML
// =====================================================

function escapeHTML(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;

}


// =====================================================
// MOBILE SIDEBAR
// =====================================================

function toggleSidebar() {

    const sidebar =
        document.querySelector(".sidebar");

    if (sidebar) {

        sidebar.classList.toggle("open");

    }

}