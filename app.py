import streamlit as st
import json
import pandas as pd
from model import classify_label, generate_summary, calculate_sender_frequency, calculate_priority_score, calculate_clutter_suggestions
from PIL import Image
st.set_page_config(page_title="MailMind - AI Email Cleaner", layout="wide")
# 🌟 BACKGROUND THEME (soft gradient)
st.markdown("""
    <style>
        /* 🌌 Dynamic Dark Animated Background */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(-45deg, #1a1a2e, #16213e, #0f3460, #533483);
            background-size: 400% 400%;
            animation: gradientFlow 15s ease infinite;
            color: #f5f5f5 !important;
        }

        @keyframes gradientFlow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* 🪞 Transparent, glass-like header */
        [data-testid="stHeader"] {
            background: rgba(20, 20, 40, 0.4);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* ✨ Text Visibility */
        h1, h2, h3, h4, h5, h6, p, li, span, div {
            color: #f0f0f0 !important;
        }

        /* 📦 Card/Expander Glass Effect */
        .stExpander {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        }

        /* 🧮 Metrics Styling */
        [data-testid="stMetricValue"] {
            color: #00e6ff !important;
            font-weight: 700 !important;
            text-shadow: 0 0 8px #00e6ff;
        }

        /* 🧠 Sidebar Styling */
        section[data-testid="stSidebar"] {
            background: rgba(10, 10, 30, 0.8);
            color: #e0e0e0;
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* 🎨 Main Buttons */
        div.stButton > button {
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            color: white !important;
            border: none;
            border-radius: 10px;
            font-weight: bold;
            padding: 0.6em 1.6em;
            transition: all 0.3s ease;
            box-shadow: 0 0 12px rgba(0, 114, 255, 0.6);
        }

        div.stButton > button:hover {
            background: linear-gradient(90deg, #3a7bd5, #00d2ff);
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(0, 214, 255, 0.8);
        }

        /* 🪶 Download Button */
        div[data-testid="stDownloadButton"] > button {
            background: linear-gradient(90deg, #8e2de2, #4a00e0);
            color: white !important;
            border: none;
            border-radius: 10px;
            font-weight: bold;
            padding: 0.6em 1.8em;
            box-shadow: 0 0 10px rgba(138, 43, 226, 0.6);
            transition: all 0.3s ease;
        }

        div[data-testid="stDownloadButton"] > button:hover {
            background: linear-gradient(90deg, #6a11cb, #2575fc);
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(90, 90, 255, 0.8);
        }

        /* 🧊 DataFrame Style */
        .stDataFrame {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
        }

        /* 💫 Scrollbar Styling */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(#00e6ff, #7a00ff);
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

logo=Image.open("assets/mailmind_logo.png")
st.image(logo,width=120)
st.title("📧 MailMind — AI Email Cleaner & Summarizer 📥")
st.markdown("---")
hero=Image.open("assets/herorobo1.jpg")
st.image(hero,use_container_width=True)

st.markdown("""
Welcome to MailMind! This AI analyzes your last 24 hours 🕰️ of email (using sample data for the demo)
and uses a **Custom Priority Score** to clean the clutter and highlight what matters.
""")

# --- Data Loading ---
uploaded = st.file_uploader("Upload emails.json (or CSV)", type=["json", "csv"])

if uploaded:
    try:
        if uploaded.type == "application/json" or uploaded.name.endswith(".json"):
            emails = json.load(uploaded)
        else:
            df_upload = pd.read_csv(uploaded)
            emails = df_upload.to_dict(orient="records")
    except Exception as e:
        st.error(f"Error loading file: {e}. Please ensure the JSON/CSV format is correct.")
        st.stop()
else:
    st.info("Using sample dataset. Upload your own `emails.json` to see the logic in action!")
    # Load sample data (Ensure you have sample_emails.json ready)
    try:
        with open("sample_emails.json", "r", encoding="utf-8") as f:
            emails = json.load(f)
    except FileNotFoundError:
        st.error("Error: 'sample_emails.json' not found. Please create it or upload a file.")
        st.stop()

# --- Processing Pipeline ---
processed = []
# Pre-calculate sender frequency map once
sender_freq_map = calculate_sender_frequency(emails)

# Run classification and summarization
with st.spinner(f"Analyzing {len(emails)} emails..."):
    for e in emails:
        sender = e.get("sender", "")
        subject = e.get("subject", "")
        body = e.get("body", "")
        
        # 1. Base Classification
        label = classify_label(subject, body, sender)
        
        # 2. Priority Score (Original Logic)
        score = calculate_priority_score(e, sender_freq_map)
        
        # 3. Summarization (CPU-friendly model)
        summary = generate_summary(body)
        
        processed.append({
            "id": e.get("id",""),
            "sender": sender,
            "subject": subject,
            "body_preview": body[:400] + "...",
            "date": e.get("date",""),
            "label": label,
            "priority_score": score, # The original feature
            "summary": summary,
        })

df = pd.DataFrame(processed)

# --- Tabs for different views ---
tab_clean, tab_all, tab_clutter = st.tabs(["✨ Clean Inbox (Prioritized)", "📦 All Emails", "🗑️ Clutter Report"])

# --- TAB 1: Clean Inbox (Prioritized) ---
with tab_clean:
    st.header("Filtered & Prioritized View")
    organize_img = Image.open("assets/emailrobosummarizer.png")
    st.image(organize_img, width=400, caption="MailMind sorts and prioritizes your emails automatically.")
    st.markdown("Emails are sorted by the **Custom Priority Score** (0.0 to 1.0). Promotional and Low-Value Notifications are hidden.")

    # Filter out the lowest priority labels (Promotional)
    show_df = df[df.label != "Promotional"].sort_values(by="priority_score", ascending=False)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Emails", len(df))
    col2.metric("Clean View Count", len(show_df))
    col3.metric("Highest Priority Score", f"{show_df['priority_score'].max():.2f}" if not show_df.empty else "N/A")
    col4.metric("Promotional Count", int((df.label=="Promotional").sum()))

    if show_df.empty:
        empty_img = Image.open("assets/footer.png")
        st.image(empty_img, width=300)
        st.info("🎉 Your inbox is perfectly clean!")
    else:
        # Display results with expanders
        for _, row in show_df.iterrows():
            color = {"Important":"red", "Notification":"orange", "Personal":"green"}.get(row['label'], "blue")
            
            with st.expander(f"**[{row['priority_score']:.2f}]** {row['subject']} — {row['sender']} ({row['label']})"):
                st.markdown(f"**Date:** {row['date']} | **Label:** :{color}[**{row['label']}**]")
                st.subheader("💡 AI Summary")
                brain_img = Image.open("assets/summarize_brain.jpg")
                st.image(brain_img, width=300)
                st.write(f"> {row['summary']}")
                st.markdown("---")
                st.caption(f"Full Body Preview:\n {row['body_preview']}")
                
# --- TAB 2: All Emails ---
with tab_all:
    st.header("Raw Inbox View")
    st.dataframe(df[['date', 'sender', 'subject', 'label', 'priority_score', 'summary']], use_container_width=True)

# --- TAB 3: Clutter Report (Original Feature) ---
with tab_clutter:
    st.header("Sender Clutter & Unsubscribe Report")
    clutter_img = Image.open("assets/herorobo2.png")
    st.image(clutter_img, width=400, caption="Detecting senders who clutter your inbox.")
    st.markdown("Analyzes high-volume senders with low-priority content and suggests muting or unsubscribing.")
    
    clutter_suggestions_df = calculate_clutter_suggestions(df)
    
    suggested_df = clutter_suggestions_df[clutter_suggestions_df['suggestion'] == "✅ Unsubscribe/Mute Suggested"]
    
    st.metric("Senders Suggested for Cleanup", len(suggested_df))
    
    if suggested_df.empty:
        st.success("Great job! No high-volume, low-value senders detected in the current batch.")
    else:
        st.subheader("High-Frequency, Low-Value Senders")
        st.dataframe(
            suggested_df[['sender', 'total_emails', 'low_priority_percentage', 'suggestion']],
            column_config={
                "total_emails": "Total Emails (7 Days)",
                "low_priority_percentage": st.column_config.ProgressColumn("Low-Priority %", format="%f%%", min_value=0, max_value=100),
                "suggestion": "Action"
            },
            use_container_width=True,
            hide_index=True
        )

# --- Download Button (Final Polish) ---
st.sidebar.markdown("---")
st.sidebar.subheader("Export")
csv = df.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="Download Processed CSV",
    data=csv,
    file_name='inboxzen_processed_emails.csv',
    mime='text/csv',
)