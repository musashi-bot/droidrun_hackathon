# 🚀 ChatPilot – AI WhatsApp Productivity Agent

[![Watch the video](https://img.youtube.com/vi/I8JkN32J-5I/0.jpg)](https://www.youtube.com/watch?v=I8JkN32J-5I)

ChatPilot is an **agentic mobile AI assistant** built using the **Droidrun framework** that automatically reads WhatsApp messages, understands their intent, prioritizes them, and takes productivity actions such as creating reminders, calendar events, notes, and drafting replies — all on a **real Android device**.

This project was built as part of a **hackathon (Droidrun DevSprint)** to demonstrate **mobile-native AI automation with agentic behavior**.

---

## ✨ What Problem Does It Solve?

WhatsApp is overloaded with:

* Important deadlines hidden in chats
* Missed follow-ups
* Repetitive replies
* No task or priority management

ChatPilot turns **messages into actions**, helping users focus on what actually matters.

---

## 🧠 Key Features

* 📩 **Reads WhatsApp messages autonomously**
* 🧠 **Classifies messages** by intent, urgency, and importance
* ⏰ **Creates reminders & calendar events** automatically
* 📝 **Saves important information** as notes
* 💬 **Drafts smart replies** (manual approval or auto-send)
* 📊 **Daily productivity summary**
* 🤖 Fully **agentic** (observe → reason → act)

---

## 🤖 Agentic Workflow

```
WhatsApp Message
      ↓
Message Reader Agent
      ↓
Classification & Priority Agent
      ↓
Decision Engine
      ↓
Calendar / Notes / Reply / Ignore
```

This is **not rule-based automation** — the agent reasons about each message before acting.

---

## 📌 Message Classification Logic

Each message is analyzed on four dimensions:

1. **Intent** – deadline, meeting, question, info, casual
2. **Urgency** – high / medium / low (based on time expressions)
3. **Importance** – sender-based (professor, manager, family, etc.)
4. **Actionability** – does it require an action?


---

## 🛠️ Tech Stack

* **Droidrun Framework** (mobile agent execution)
* **Mobilerun Cloud** (cloud-based Android devices)
* **Python**
* **LLM (for NLP & reasoning)**

---

## 📁 Project Structure

```
DROIDRUN_HACKATHON/
│
├── .venv/ # Python virtual environment
│
├── chatPilot/
│ ├── agent/
│ │ ├── prompts/
│ │ │ ├── __init__.py
│ │ │ └── whatsapp_prompts.py # All Droidrun goal prompts
│ │ │
│ │ ├── __init__.py
│ │ ├── act_on_messages.py # Executes actions (calendar, reply, notes)
│ │ ├── classify_messages.py # Message intent & priority classification
│ │ └── read_messages.py # Reads WhatsApp messages using Droidrun
│ │
│ ├── schemas/
│ │ ├── __init__.py
│ │ ├── decision_schema.py # Agent decision
│ │ └── message_schema.py # WhatsApp message structure
│ │
│ └── main.py # Entry point for ChatCopilot agent
│
├── data/ # Logs / extracted message data
├── trajectories/ # Droidrun execution traces
├── .env # Environment variables
├── .gitignore
└── requirements.txt
```

---

## 🎥 Demo Flow (1–2 Minutes)

1. New WhatsApp message arrives
2. ChatPilot reads the message
3. Classifies intent & urgency
4. Automatically creates a reminder / event
5. Drafts a smart reply
6. Shows calendar or notes update

---

## 🏆 Why This Project Stands Out

* ✅ Real mobile automation (not a simulation)
* ✅ Strong agentic behavior
* ✅ High real-world usefulness
* ✅ Easy to demo & understand
* ✅ High potential for virality

---

## 🚀 Future Improvements

* Multi-language support (English + Hindi)
* Learning user preferences over time
* WhatsApp Business integration
* Payment & invoice follow-ups

---

## 🧑‍💻 Built By

**Vansh Toshniwal** **Pradeep Sagitra** **Abhrajit Chowdhury**
IIT Patna

---

## 📢 Hackathon Note

This project was built as part of a hackathon to showcase **mobile AI agents using Droidrun**. All actions are demonstrated in a controlled environment for educational purposes.

---

> *“Read less. Do more. Let ChatCopilot handle your chats.”* 🚀
