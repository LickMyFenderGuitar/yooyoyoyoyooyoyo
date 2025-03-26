let lastUserMessage = '';
let currentRoom = 'New Chat';

async function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (!userInput) return;

    appendMessage(userInput, 'user');
    document.getElementById('user-input').value = '';
    lastUserMessage = userInput;

    const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userInput })
    });

    const data = await response.json();
    handleBotResponse(data.response);
    document.getElementById('continue-btn').style.display = 'inline-block';
}

function appendMessage(message, sender) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.innerText = message;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function handleBotResponse(response) {
    console.log('Before cleaning:', response);

    // Check if there's content inside <think>
    if (response.includes("<think>")) {
        response = response.replace(/<think>[\s\S]*?<\/think>/g, '').trim();
    }

    console.log('After cleaning:', response);

    if (response.includes("```")) {
        const parts = response.split(/```/); // Split on code delimiters
        const messagesDiv = document.getElementById('messages');
        let languageName = parts[0].trim(); // Extract first line as language name

        parts.forEach((part, index) => {
            if (index % 2 === 0) {
                if (part.trim()) {
                    appendMessage(part.trim(), 'bot');
                }
            } else {
                const codeDiv = document.createElement('div');
                codeDiv.classList.add('code');
                codeDiv.innerHTML = `
                    <div class="code-header">
                        <span>${languageName}</span>
                        <button class="copy-button" onclick="copyCode(this)">Copy</button>
                    </div>
                    <div class="code-content">${part.trim()}</div>
                `;
                messagesDiv.appendChild(codeDiv);
            }
        });
    } else if (response.trim()) {
        appendMessage(response.trim(), 'bot');
    }
}

function copyCode(button) {
    const codeContent = button.parentElement.nextElementSibling.innerText;
    navigator.clipboard.writeText(codeContent).then(() => {
        alert("Code copied to clipboard!");
    }).catch(() => {
        alert("Failed to copy code.");
    });
}

function continueGeneration() {
    if (!lastUserMessage) return;

    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: lastUserMessage })
    }).then(resp => resp.json()).then(data => {
        handleBotResponse(data.response);
    });
}

function changeRoom(room) {
    currentRoom = room;
    document.getElementById('messages').innerHTML = '';
    document.getElementById('continue-btn').style.display = 'none';
    appendMessage(`Switched to ${room} chat! Feel free to ask anything.`, 'bot');
}

function createNewRoom() {
    const roomName = prompt("Enter the name of the new chat room:");
    if (roomName) {
        const roomDiv = document.createElement('div');
        roomDiv.classList.add('room');
        roomDiv.textContent = roomName;
        roomDiv.onclick = () => changeRoom(roomName);
        document.getElementById('sidebar').insertBefore(roomDiv, document.getElementById('create-room-btn'));
    }
}
