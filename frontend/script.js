console.log("Script loaded");

const chatWindow = document.getElementById("chatWindow");
const promptInput = document.getElementById("promptInput");
const sendBtn = document.getElementById("sendBtn");
const fileInput = document.getElementById("fileInput");
const docStatus = document.getElementById("docStatus");
const quickBtns = document.querySelectorAll(".prompt-btn");

let extractedText = null;
let chatHistory = [];

/* Medical terms to highlight */
const medicalTerms = ["hypertension", "diabetes", "cholesterol", "tumor", "MRI", "CT", "blood pressure", "proteins"];

/* Highlight terms */
function highlightMedical(text) {

  if (!text) return "";

  medicalTerms.forEach(term => {
    const regex = new RegExp(`\\b${term}\\b`, "gi");
    text = text.replace(regex, `<span class="highlight">${term}</span>`);
  });

  return text;
}

/* Add message */
function addMessage(role, text) {
  const row = document.createElement("div");
  row.className = "msg-row";

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.innerText = role === "user" ? "🧑" : "🤖";

  const bubble = document.createElement("div");
  bubble.className = `message ${role === "user" ? "user-bubble" : "assistant-bubble"}`;
  if (role === "assistant") {
    bubble.innerHTML = highlightMedical(text).replace(/\n/g, "<br>");
} else {
    bubble.textContent = text;
}

  if (role === "user") row.style.justifyContent = "flex-end";

  row.appendChild(role === "user" ? bubble : avatar);
  row.appendChild(role === "user" ? avatar : bubble);

  chatWindow.appendChild(row);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

/* Typing animation */
let typingRow;
function showTyping() {
  typingRow = document.createElement("div");
  typingRow.className = "msg-row";

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.innerText = "🤖";

  const bubble = document.createElement("div");
  bubble.className = "message assistant-bubble typing";
  bubble.innerHTML = "AI is typing<span>.</span><span>.</span><span>.</span>";

  typingRow.appendChild(avatar);
  typingRow.appendChild(bubble);
  chatWindow.appendChild(typingRow);
}

function hideTyping() {
  if (typingRow) typingRow.remove();
}

/* Quick prompt buttons */
quickBtns.forEach(btn => {
  btn.onclick = () => {
    promptInput.value = btn.innerText;
    sendMessage();
  };
});

/* Send message */
sendBtn.onclick = sendMessage;
promptInput.onkeydown = (e) => { if (e.key === "Enter") sendMessage(); };

/* Upload file (backend placeholder) */
fileInput.onchange = async () => {
  const file = fileInput.files[0];
  if (!file) return;

  docStatus.innerText = "Uploading...";
  addMessage("assistant", "Uploading and extracting document...");

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("/extract-text", {
      method: "POST",
      body: formData
    });

const data = await res.json();

console.log("Upload successful!");
console.log(data);

extractedText = data.text;
window.currentSessionId = data.session_id;

addMessage(
    "assistant",
    `✅ Your report has been processed successfully.

You can now ask questions such as:

• Summarize my report.
• What are the abnormal values?
• Explain this report in simple language.
• What does my cholesterol level mean?
• Are there any concerning findings?`
);
  } catch(err) {
    console.error(err);
    hideTyping();

    addMessage(
        "assistant",
        err.toString()
    );
}
};



async function sendMessage() {
  const text = promptInput.value.trim();
  if (!text) return;

  addMessage("user", text);
  promptInput.value = "";
  showTyping();

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        session_id: window.currentSessionId,
        message: text
      })
    });

    const data = await res.json();

    hideTyping();

    if (!res.ok) {
      addMessage("assistant", data.error || "Unknown error");
      return;
    }

    addMessage("assistant", data.reply);

  } catch (err) {
    hideTyping();
    console.error(err);
    addMessage("assistant", err.toString());
  }
}