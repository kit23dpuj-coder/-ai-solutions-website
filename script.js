// AI Chatbot - Floating Button with Chat Window
document.addEventListener('DOMContentLoaded', function() {
    // Chatbot HTML structure
    const chatbotHTML = `
        <div id="chatbot-toggle" style="position: fixed; bottom: 20px; right: 20px; background: #0d6efd; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 1000; box-shadow: 0 0 15px rgba(13,110,253,0.5);">
            <i class="fas fa-comment-dots fa-2x"></i>
        </div>
        <div id="chatbot-window" style="position: fixed; bottom: 90px; right: 20px; width: 350px; background: #1e1e1e; border-radius: 15px; box-shadow: 0 0 20px rgba(0,0,0,0.5); display: none; flex-direction: column; z-index: 1000; border: 1px solid #0d6efd;">
            <div style="background: #0d6efd; padding: 12px; border-radius: 15px 15px 0 0; color: white; font-weight: bold;">
                AI Assistant <i class="fas fa-robot"></i>
                <span id="close-chat" style="float: right; cursor: pointer;">&times;</span>
            </div>
            <div id="chat-messages" style="height: 300px; overflow-y: auto; padding: 10px; background: #111; color: white;">
                <div class="bot-msg" style="margin-bottom: 10px;"><strong>AI:</strong> Hello! How can I help you today?</div>
            </div>
            <div style="padding: 10px; display: flex; border-top: 1px solid #333;">
                <input type="text" id="chat-input" placeholder="Type your message..." style="flex: 1; padding: 8px; border-radius: 20px; border: none; background: #333; color: white;">
                <button id="chat-send" style="margin-left: 8px; background: #0d6efd; border: none; border-radius: 50%; width: 35px; height: 35px; color: white;">➤</button>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', chatbotHTML);

    const toggle = document.getElementById('chatbot-toggle');
    const windowDiv = document.getElementById('chatbot-window');
    const closeBtn = document.getElementById('close-chat');
    const sendBtn = document.getElementById('chat-send');
    const input = document.getElementById('chat-input');
    const messagesDiv = document.getElementById('chat-messages');

    toggle.addEventListener('click', () => {
        windowDiv.style.display = windowDiv.style.display === 'none' ? 'flex' : 'none';
    });
    closeBtn.addEventListener('click', () => {
        windowDiv.style.display = 'none';
    });

    function addMessage(sender, text) {
        const msgDiv = document.createElement('div');
        msgDiv.style.marginBottom = '10px';
        msgDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
        messagesDiv.appendChild(msgDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    async function sendMessage() {
        const message = input.value.trim();
        if (!message) return;
        addMessage('You', message);
        input.value = '';

        try {
            const response = await fetch('/chatbot', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            });
            const data = await response.json();
            addMessage('AI', data.response);
        } catch (error) {
            addMessage('AI', 'Sorry, I am having trouble. Please try again.');
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});