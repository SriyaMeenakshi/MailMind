import pandas as pd
import re
import math
#from transformers import pipeline

# --- 1. Summarization Pipeline (CPU-Friendly) ---
# Use a small model like 'sshleifer/distilbart-cnn-12-6' or 't5-small' for CPU.
#try:
    # Use 't5-small' if distilbart is too large/slow. device=-1 uses CPU.
#    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", device=-1) 
#    print("Summarizer pipeline loaded successfully.")
#except Exception as e:
summarizer = None
    # print(f"Warning: Summarizer pipeline not loaded ({e}). Using extractive fallback.") # Commented out for cleaner console

def generate_summary(text, max_length=60):
    """Generates a summary or returns a simple extractive fallback."""
    if not text or len(text.split()) < 20:
        return text.strip().replace("\n", " ")[:120] + "..."

    if summarizer:
        try:
            out = summarizer(text, max_length=max_length, min_length=15, do_sample=False)
            return out[0]['summary_text']
        except Exception:
            # Fallback if generation fails
            return text.strip().replace("\n", " ")[:150] + "..."
    else:
        # Extractive fallback
        sentences = re.split(r'(?<=[.!?]) +', text.strip())
        return sentences[0] if sentences else text.strip().replace("\n", " ")[:120] + "..."

# --- 2. Base Classifier & Keywords ---
PROMO_KEYWORDS = ["sale", "discount", "offer", "promo", "unsubscribe", "deal", "coupon"]
NOTIF_KEYWORDS = ["reminder", "alert", "notification", "update", "delivery", "receipt"]
URGENT_KEYWORDS = ["urgent", "asap", "important", "interview", "password", "login", "suspicious", "deadline", "overdue"]

def classify_label(subject, body, sender):
    """Assigns a simple label based on keywords and sender heuristics."""
    text = (subject + " " + body + " " + sender).lower()

    if any(k in text for k in URGENT_KEYWORDS):
        return "Important"
    if "no-reply" in sender.lower() and any(k in text for k in PROMO_KEYWORDS):
        return "Promotional"
    if any(k in text for k in PROMO_KEYWORDS) or "newsletter" in subject.lower():
        return "Promotional"
    if any(k in text for k in NOTIF_KEYWORDS):
        return "Notification"
    
    return "Personal"

# --- 3. CORE ORIGINALITY: Priority Score and Frequency ---

def calculate_sender_frequency(emails):
    """Calculates how often each sender appears."""
    if not emails:
        return {}
    df = pd.DataFrame(emails)
    return df['sender'].value_counts().to_dict()

def calculate_priority_score(email, sender_freq_map):
    """
    Calculates a custom weighted priority score (0.0 to 1.0) based on:
    W1: Keyword Importance
    W2: Sender Rarity (Boost for less frequent senders)
    """
    text = (email['subject'] + " " + email['body']).lower()

    # FIX: Explicitly define 'label' with a fallback to satisfy Pylance
    # The 'label' key is added in app.py before this function is called, but this
    # satisfies the Pylance linter and makes the code safer.
    label = email.get('label', 'Personal') 

    # W1: Keyword-based Score (Weight: 0.7)
    score_map = {"Important": 0.8, "Notification": 0.5, "Personal": 0.4, "Promotional": 0.1}
    w1_score = score_map.get(label, 0.1)

    # W2: Sender Frequency Score (Weight: 0.3)
    frequency = sender_freq_map.get(email['sender'], 1)
    
    # Rarity-boost: Use a log scale to penalize high frequency.
    freq_penalty = math.log1p(frequency) / 3 
    w2_score = max(0.0, 1.0 - freq_penalty) 

    # Combine the scores (70% keywords, 30% rarity)
    final_score = (w1_score * 0.7) + (w2_score * 0.3)
    
    # Final check: Max boost for critical security/financial terms
    if any(k in text for k in ["password reset", "unauthorized transaction", "critical error"]):
        final_score = 1.0 
        
    return round(min(1.0, final_score), 2)

# --- 4. HIGH-VALUE FEATURE: Clutter Suggestions ---

def calculate_clutter_suggestions(df):
    """Identifies high-frequency, low-value senders for unsubscribing/muting."""
    if df.empty:
        return pd.DataFrame()
        
    # Group by sender, count total, and count low-priority
    clutter_df = df.groupby('sender').agg(
        total_emails=('id', 'count'),
        low_priority_count=('label', lambda x: ((x == 'Promotional') | (x == 'Notification')).sum()),
    ).reset_index()
    
    # Calculate percentage of low-priority emails from this sender
    clutter_df['low_priority_percentage'] = (clutter_df['low_priority_count'] / clutter_df['total_emails']) * 100
    
    # ORIGINAL LOGIC: Suggestion Condition
    # More than 3 emails in the window AND > 70% are low priority
    clutter_df['suggestion'] = clutter_df.apply(lambda row: 
        "✅ Unsubscribe/Mute Suggested" if row['total_emails'] >= 3 and row['low_priority_percentage'] >= 70 else "Keep", axis=1)
        
    return clutter_df.sort_values(by=['total_emails', 'low_priority_percentage'], ascending=False)