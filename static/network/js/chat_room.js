const userId = other_user_id;
const selfId = "{{ request.user.id }}";
const protocol = window.location.protocol === "https:" ? "wss" : "ws";
const chatSocket = new WebSocket(
  `${protocol}://${window.location.host}/ws/chat/${userId}/`
);

const chatBox = document.getElementById("chat-box");
const input = document.getElementById("chat-message-input");
const sendButton = document.getElementById("chat-message-submit");

// Utility: format date (e.g., 2025-05-05) to readable string
function formatDate(dateString) {
  const options = { year: "numeric", month: "short", day: "numeric" };
  const dateObj = new Date(dateString);
  return dateObj.toLocaleDateString(undefined, options);
}

// Utility: format time (hh:mm)
function formatTime(timestamp) {
  const dateObj = new Date(timestamp);
  return dateObj.toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
}

let lastMessageDate = null;

const appendMessage = (message, senderId, timestamp) => {
  const messageDate = new Date(timestamp).toISOString().split("T")[0];

  if (lastMessageDate !== messageDate) {
    lastMessageDate = messageDate;
    const dateLabel = document.createElement("div");
    dateLabel.className = "text-center text-sm text-black/50 my-2";
    dateLabel.innerText = formatDate(messageDate);
    chatBox.appendChild(dateLabel);
  }

  const wrapper = document.createElement("div");
  wrapper.className = senderId == selfId ? "text-right" : "text-left";

  const messageDiv = document.createElement("div");
  messageDiv.className =
    "inline-block bg-white/20 text-black px-4 py-2 rounded-lg max-w-xs break-words";

  messageDiv.innerHTML = `
      <div>${message}</div>
      <div class="text-xs text-black/50 mt-1">${formatTime(timestamp)}</div>
    `;

  wrapper.appendChild(messageDiv);
  chatBox.appendChild(wrapper);
  chatBox.scrollTop = chatBox.scrollHeight;
};

// Receiving message
chatSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  console.log(data);
  appendMessage(data.message, data.sender_id, data.timestamp);
};

// Sending message
sendButton.onclick = function () {
  const message = input.value.trim();
  if (!message) return;

  const timestamp = new Date().toISOString();
  chatSocket.send(JSON.stringify({ message, timestamp }));
  appendMessage(message, selfId, timestamp);
  input.value = "";
};

// Load previous messages
window.addEventListener("DOMContentLoaded", () => {
  fetch(`/network/fetch_messages/${userId}/`)
    .then((res) => res.json())
    .then((data) => {
      data.messages.forEach((msg) => {
        appendMessage(msg.message, msg.sender, msg.timestamp);
      });
    });
});
