document.getElementById("send-button").addEventListener("click", function() {
    const userMessage = document.getElementById("user-message").value;
    
    if (userMessage.trim() === "") return; // Prevent sending empty messages

    // Display the user's message
    displayMessage("user", userMessage);

    // Send the message to FastAPI backend
    fetch(`http://127.0.0.1:8000/ask?query=${encodeURIComponent(userMessage)}`)
        .then(response => response.json())
        .then(data => {
            const botMessage = data.response;
            displayMessage("bot", botMessage);
        })
        .catch(error => {
            console.error("Error:", error);
            displayMessage("bot", "Sorry, I encountered an error while processing your message.");
        });

    document.getElementById("user-message").value = ""; // Clear input field
});

// Handle Enter key press for sending messages
document.getElementById("user-message").addEventListener("keypress", function(event) {
    if (event.key === "Enter" && event.target.value.trim() !== "") {
        document.getElementById("send-button").click();
    }
});

// Function to display messages
function displayMessage(type, message) {
    const chatLog = document.getElementById("chat-log");
    const messageDiv = document.createElement("div");
    messageDiv.classList.add(type + "-message");
    messageDiv.innerHTML = `
        <div class="message-content">
            <img src="images/${type}-avatar.png" alt="${type} Avatar" class="avatar">
            <span class="message-text">${message}</span>
        </div>`;
    chatLog.appendChild(messageDiv);
    chatLog.scrollTop = chatLog.scrollHeight; // Scroll to the latest message
}
