document.addEventListener("DOMContentLoaded", () => {
  document.querySelector(".msger-inputarea").addEventListener("submit", function(e) {
      e.preventDefault();
      let input = document.querySelector(".msger-input").value;
      document.querySelector(".msger-input").value = "";
      if (input.trim()) {
          addChatEntry(input, "user");
          output(input);
      }
  });

  document.querySelector("#openChatBtn").addEventListener("click", openChat);
  document.querySelector("#closeChatBtn").addEventListener("click", closeChat);
  startIdleTimer();
});

let idleTimer;

function startIdleTimer() {
  idleTimer = setTimeout(() => {
      addChatEntry("Are you there?", "bot");
  }, 180000); // 3 minutes
}

function resetIdleTimer() {
  clearTimeout(idleTimer);
  startIdleTimer();
}

function openChat() {
  document.querySelector("#chatbox").classList.add("open");
  document.querySelector("#openChatBtn").style.display = "none";
}

function closeChat() {
  document.querySelector("#chatbox").classList.remove("open");
  document.querySelector("#openChatBtn").style.display = "block";
}

const utterances = [ 
  ["how are you", "how was your day", "what is good", "are you alright?"],        
  ["hello", "hey", "hi", "good morning", "good afternoon"],      
  ["visa type", "consultation type", "family visa", "visitor visa", "student visa", "business visa", "temporal visa", "skilled work visa", "settlement visa"],      
  ["service type", "standard", "premium", "diplomats"], 
  ["what is your name"],
  ["i want to make an enquiry about the post graduate study visa. i want to know if i have to pay for my baby born in the uk"],
];

const answers = [
  ["I am fine, thank you."],
  ["Hello! How can I assist you today?", "Hey there! Are you looking for guidance on your visa processing?", "Welcome back! How can I help you with your visa application? Need assistance navigating the process?", "Hi! Did you know we provide comprehensive assistance with visa processing for various countries?", "Hi! Ready to start your visa application journey? Let's dive into the intricacies of the process together!", "Hello! I’m here to guide you through the visa processing steps. Need assistance with documentation or requirements?", "Welcome! You can ask me about visa requirements, application forms, or any other visa-related queries you may have.", "Hi! What brings you in today? Need help with your visa application or clarifying any doubts?", "Hey there! Let’s make your visa application process smooth and hassle-free. How can I assist you in this journey?", "Welcome back! Have you explored our latest visa processing services? I'm here to walk you through them?", "Hello! Need assistance navigating the visa application process? Let's simplify it together!", "Hi! Want to stay updated on the latest developments in visa processing? I've got you covered!", "Hey! Let’s make your visa application experience easy and stress-free. Where would you like to begin?", "Welcome! I can assist you with visa appointments, document preparation, or any other visa-related tasks you need help with.", "Hi! Shall we pick up where we left off in your visa application process?", "Hey there! Ready to explore the latest updates in visa regulations and processing? Let's stay informed!", "Hello! Let’s find the perfect visa solution tailored to your travel plans and requirements.", "Welcome back! Let’s continue shaping your visa application for your dream destination. How can I assist you further?", "Hi! Need some expert guidance on visa options and requirements? Feel free to ask!", "Hey! Let’s get you started on your visa application journey. It’s simpler than you might think!", "Hello! Ready to proceed with your visa application or need more information before you take the next step?"],
  ["I'm sorry, I couldn't understand your question. Please contact our office for assistance."],
  ["My name is UVCLegal ChatBot. How can I help you?"],
  ["Please contact our office for more information on: Tel - +441332316601, WhatsApp - +447404700760, Email - uvcteamb2@gmail.com"],
];

const alternatives = ["Go on...", "Try again", "I'm not sure I understand. Please contact our office on: Tel - +441332316601, WhatsApp - +447404700760, Email - uvcteamb2@gmail.com"];

function output(input) {
  let product;
  let text = input.toLowerCase().replace(/[^\w\s\d]/gi, "");

  text = text
      .replace(/ a /g, " ")
      .replace(/whats/g, "what is")
      .replace(/please /g, "")
      .replace(/ please/g, "");

  let found = false;
  for (let i = 0; i < utterances.length; i++) {
      for (let j = 0; j < utterances[i].length; j++) {
          if (text.includes(utterances[i][j])) {
              product = answers[i][Math.floor(Math.random() * answers[i].length)];
              found = true;
              break;
          }
      }
      if (found) break;
  }

  if (!found) {
      product = alternatives[Math.floor(Math.random() * alternatives.length)];
  }

  setTimeout(() => {
      addChatEntry(product, "bot");
  }, 1000);
}

function addChatEntry(text, sender) {
  const messagesContainer = document.getElementById("messages");

  let msgDiv = document.createElement("div");
  msgDiv.className = sender === "user" ? "msg right-msg" : "msg left-msg";

  let msgImg = document.createElement("div");
  msgImg.className = "msg-img";
  msgImg.style.backgroundImage = sender === "user" ? "url('./img/chatbot-2.png')" : "url('./img/chatbot-1.png')";

  let msgBubble = document.createElement("div");
  msgBubble.className = "msg-bubble";

  let msgInfo = document.createElement("div");
  msgInfo.className = "msg-info";

  let msgInfoName = document.createElement("div");
  msgInfoName.className = "msg-info-name";
  msgInfoName.innerText = sender === "user" ? "Client" : "BOT";

  let msgInfoTime = document.createElement("div");
  msgInfoTime.className = "msg-info-time";
  msgInfoTime.innerText = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  let msgText = document.createElement("div");
  msgText.className = "msg-text";
  msgText.innerText = text;

  msgInfo.appendChild(msgInfoName);
  msgInfo.appendChild(msgInfoTime);
  msgBubble.appendChild(msgInfo);
  msgBubble.appendChild(msgText);
  msgDiv.appendChild(msgImg);
  msgDiv.appendChild(msgBubble);
  messagesContainer.appendChild(msgDiv);

  messagesContainer.scrollTop = messagesContainer.scrollHeight;

  if (sender === "user") {
      resetIdleTimer();
  }
}
