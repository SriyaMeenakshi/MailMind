<p align="center">
  <img src="assets/mailmind_logo.png" alt="MailMind Logo" width="120"/>
</p>

# 📧 MailMind — AI Email Cleaner & Summarizer

<p align="center">
  <em>Clean Inbox. Clear Mind. ✨</em>
</p>

<p align="center">
  🌐 <strong><a href="https://mailmindai.streamlit.app" target="_blank">Live Demo</a></strong> • 
  🧠 Built with <strong>Python + Streamlit</strong> • 
  🚀 <strong>ByteWars Hackathon 2025</strong>
</p>

---

## 🚀 Overview

**MailMind** is an AI-powered inbox manager that helps you declutter your emails, summarize messages, and highlight what matters most — all in one click.  

The app mimics a real-world productivity assistant and was built for **ByteWars Hackathon 2025** to address the problem of information overload caused by excessive emails.

---

## ✨ Features

- ✉️ **Smart Email Categorization** — Automatically classifies emails into Important, Personal, Notifications, or Promotions.  
- 🧠 **AI Summarization** — Generates concise one-line summaries of lengthy emails.  
- 💡 **Priority Scoring** — Scores emails based on urgency, sender frequency, and content type.  
- 🧹 **Clutter Report** — Detects repetitive low-value senders and suggests unsubscribe/mute actions.  
- 📊 **Visual Dashboard** — Tabs for Clean Inbox, All Emails, and Clutter Report with metrics.  
- 📥 **Export as CSV** — Download your cleaned inbox data instantly.

---

## 🧩 Tech Stack

| Tool / Library | Purpose |
|----------------|----------|
| **Streamlit** | Front-end framework |
| **Pandas** | Data processing |
| **NumPy** | Calculations & scoring |
| **Pillow (PIL)** | Image handling |

---

## 📂 Folder Structure

# MailMind/
# ├── app.py
# ├── model.py
# ├── sample_emails.json
# ├── requirements.txt
# ├── assets/
# │ ├── mailmind_logo.png
# │ └── (other illustrations)
# └── README.md


## ⚙️ Setup & Run Locally

# 1️⃣ Clone the repository
git clone https://github.com/SriyaMeenakshi/MailMind.git

cd MailMind

# 2️⃣ Create and activate virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Run the app
streamlit run app.py
Once launched, your default browser will open:
http://localhost:8501
# 🧪 Sample Dataset
For testing, sample_emails.json contains 50 mock emails (work, promotions, alerts, and personal).
You can upload your own email export in JSON/CSV format to see live analysis.

# 🧠 Future Enhancements
Gmail/Outlook API integration

Voice-based email summaries

Smart Unsubscribe automation

Multi-user login & saved preferences

Analytics Dashboard (daily/weekly email insights)

# 👩🏻‍💻 Author
Sriya Meenakshi Chalamalasetty
🎓 B.Tech CSE (AI & ML) | Passionate about building intelligent, human-centered products
🔗 LinkedIn https://www.linkedin.com/in/sriya-meenakshi-chalamalasetty/
🌐 MailMind Live App https://mailmindai.streamlit.app/

# 🏆 Hackathon Credit
This project was created as part of ByteWars Hackathon 2025, organized by the
Department of Commerce, Delhi School of Economics (DSE), New Delhi.

# “Innovation begins when you solve your own pain — MailMind was born from an inbox with 2000+ unread mails.”
