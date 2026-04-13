const chatLog = document.getElementById("chat-log");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");
const clearButton = document.getElementById("clear-button");
const stopButton = document.getElementById("stop-button");
const popup = document.getElementById("popup");
const chatContainer = document.querySelector(".chat-container");
let chatHistory = [];

window.addEventListener("DOMContentLoaded", () => {
  chatContainer.classList.add("fade-in");
  appendMessage("bot", "How are you feeling today?");
});

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;
  appendMessage("user", message);
  userInput.value = "";

  const loadingDots = createLoadingDots();
  chatLog.appendChild(loadingDots);
  chatLog.scrollTop = chatLog.scrollHeight;

  try {
    const response = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: message, history: chatHistory })
    });

    const data = await response.json();
    const { reply, emotion, medicine, dosage } = data;
    chatLog.removeChild(loadingDots);

    const illnessKeywords = ["fever", "headache", "cold", "cough", "sore throat", "pain", "tired", "fatigue", "nausea", "vomit", "dizzy", "chills"];
    const lowerMessage = message.toLowerCase();
    const isIllnessMentioned = illnessKeywords.some(keyword => lowerMessage.includes(keyword));

    if (isIllnessMentioned) {
      appendMessage("bot", "🩺 I'm really sorry to hear that you're not feeling well.");
    }

    appendMessage("bot", `🧠 Detected Emotion: ${emotion}`);
    if (medicine) appendMessage("bot", `💊 Recommended Medicine: ${medicine}`);
    if (dosage) appendMessage("bot", `📋 Suggested Dosage: ${dosage}`);
    appendMessage("bot", reply);

    chatHistory.push({ user: message, bot: reply });
  } catch (error) {
    chatLog.removeChild(loadingDots);
    appendMessage("bot", "Sorry, something went wrong.");
  }
}

function appendMessage(sender, text) {
  const messageDiv = document.createElement("div");
  messageDiv.className = sender === "user" ? "user-message" : "bot-message";
  messageDiv.innerText = text;
  chatLog.appendChild(messageDiv);
  chatLog.scrollTop = chatLog.scrollHeight;
}

function createLoadingDots() {
  const dots = document.createElement("div");
  dots.className = "bot-message loading-dots";
  dots.innerHTML = `<span>.</span><span>.</span><span>.</span>`;
  return dots;
}

clearButton.addEventListener("click", () => {
  chatLog.innerHTML = "";
  chatHistory = [];
});

stopButton.addEventListener("click", () => {
  appendMessage("bot", "Hope you are feeling better now.");
  popup.style.display = "block";
});

document.getElementById("new-chat").addEventListener("click", () => {
  chatLog.innerHTML = "";
  chatHistory = [];
  appendMessage("bot", "How are you feeling today?");
  popup.style.display = "none";
});

userInput.addEventListener("keypress", function (event) {
  if (event.key === "Enter") {
    event.preventDefault();
    sendButton.click();
  }
});
