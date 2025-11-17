import json
import os
import streamlit as st
from pathlib import Path

# --- Data (categories, estimates, messages) ---
categories = [
    "Apostleship", "Prophecy", "Evangelism", "Shepherding", "Teaching",
    "Serving", "Exhortation", "Giving", "Giving Aid", "Compassion",
    "Healing", "Working Miracles", "Tongues", "Interpretation of Tongues",
    "Wisdom", "Knowledge", "Faith", "Discernment", "Helps", "Administration"
]

percent_estimates = {
    "Apostleship": 2, "Prophecy": 3, "Evangelism": 4, "Shepherding": 2,
    "Teaching": 9, "Serving": 8, "Exhortation": 5, "Giving": 3,
    "Giving Aid": 5, "Compassion": 4, "Healing": 4, "Working Miracles": 1,
    "Tongues": 3, "Interpretation of Tongues": 1, "Wisdom": 4,
    "Knowledge": 4, "Faith": 7, "Discernment": 5, "Helps": 9,
    "Administration": 3
}

encouragement_messages = {
    "Apostleship": "You're a trailblazer! With Apostleship as your top gift, you're called to pioneer new paths and build foundations for others. **Embrace this rare calling**—it's a foundational gift that changes lives and expands God's kingdom!",
    "Prophecy": "What a powerful voice! Prophecy means you're tuned into God's messages for today. Speak boldly and watch how your words inspire transformation. You have a **distinct and vital role** in the body.",
    "Evangelism": "You're a natural sharer of good news! Evangelism lights up the world, and with this gift, you're equipped to draw others closer to faith in exciting ways. **Your passion is contagious!**",
    "Shepherding": "A heart for guiding others! Shepherding means nurturing and leading with care. **Your unique ability** to provide empathy and direction will help many find their way and feel deeply supported.",
    "Teaching": "Knowledge unlocked! Your Teaching gift makes complex truths accessible and life-changing. **Your wisdom is needed**—keep sharing what you know; the world needs more accessible insight like yours.",
    "Serving": "The ultimate helper! Serving brings joy through action, and your willingness to step up makes every community stronger and brighter. **Your actions are the foundation** of ministry success.",
    "Exhortation": "Encourager extraordinaire! Exhortation lifts spirits and motivates growth. **Your uplifting words** can turn challenges into triumphs and help others see their full potential.",
    "Giving": "Generosity flows from you! With Giving, you bless others abundantly, creating ripples of provision and hope wherever you go. **You are a crucial source of provision** for God's work.",
    "Giving Aid": "A true supporter! Giving Aid means you're there in practical ways, easing burdens and showing love through deeds that matter. **Your hands-on support** provides stability and strength.",
    "Compassion": "Heart of mercy! Compassion drives you to comfort and heal emotionally. **Your empathy is a powerful gift** that mends broken spirits and connects people to God's love.",
    "Healing": "Restorer of wholeness! Healing brings renewal, and your gift can touch lives in profound, miraculous ways. **Expect the impossible** and step out in faith to see renewal.",
    "Working Miracles": "Wonder-worker! Working Miracles means stepping into the extraordinary. **As a member of a very small group** of believers with this gift, expect the impossible and watch faith soar.",
    "Tongues": "Bridge-builder across languages! Tongues opens doors for deeper connection and worship in diverse ways. **Your gift fosters intimacy** with God and unity in the church.",
    "Interpretation of Tongues": "Decoder of mysteries! Your Interpretation gift brings clarity and unity, turning unknowns into shared revelations. **You are uniquely gifted to bring understanding** and build up the body.",
    "Wisdom": "Sage advisor! Wisdom guides decisions with divine insight. **Your counsel is a beacon** for those seeking direction; people trust your deep, spiritual discernment.",
    "Knowledge": "Seeker of truths! Knowledge uncovers depths that enlighten and empower. **Keep exploring and sharing** what you find; you are called to bring clarity to complex truths.",
    "Faith": "Unshakable believer! Faith moves mountains, and yours inspires others to trust in the unseen with bold confidence. **Your unwavering trust** encourages everyone around you to dream bigger.",
    "Discernment": "Sharp perceiver! Discernment protects and directs, helping navigate truth from deception with clarity. **Your insight is essential** for guiding others away from harm.",
    "Helps": "Behind-the-scenes hero! Helps makes everything run smoothly. **Your support amplifies** everyone's efforts, making you invaluable to the church's operation and success.",
    "Administration": "Master organizer! Administration brings order to chaos, turning visions into reality with efficiency and grace. **Your ability to organize** ensures long-term fruitfulness and growth."
}

# Initialize session state
if 'answers' not in st.session_state:
    st.session_state.answers = [None] * 201
if 'current_question' not in st.session_state:
    st.session_state.current_question = 1
if 'answered_count' not in st.session_state:
    st.session_state.answered_count = 0
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

def compute_row_sums():
    row_sums = [0] * 20
    for row in range(20):
        start = row + 1
        for col in range(10):
            q_num = start + col * 20
            row_sums[row] += st.session_state.answers[q_num] if st.session_state.answers[q_num] is not None else 0
    return row_sums

def get_sorted_gifts(row_sums):
    return sorted([(row_sums[i], categories[i]) for i in range(20)], reverse=True)

def save_progress():
    answered_data = {str(i): st.session_state.answers[i] for i in range(1, 201) if st.session_state.answers[i] is not None}
    st.download_button(label="Download Progress", data=json.dumps(answered_data), file_name="progress.json", mime="application/json")

def load_progress(uploaded_file):
    if uploaded_file is not None:
        saved_data = json.load(uploaded_file)
        for q, ans in saved_data.items():
            q_num = int(q)
            st.session_state.answers[q_num] = int(ans)
        st.session_state.answered_count = sum(1 for a in st.session_state.answers[1:] if a is not None)
        st.session_state.current_question = 1
        st.success(f"Loaded {st.session_state.answered_count} answers!")

# Main App
st.title("Spiritual Gifts Assessment")

if not st.session_state.show_results:
    # Welcome/Start
    st.subheader("Answer 200 questions (0-5) from your book.")
    
    # Load Progress
    uploaded_file = st.file_uploader("Load Progress (JSON)", type="json")
    if uploaded_file:
        load_progress(uploaded_file)

    # Question Input
    while st.session_state.current_question <= 200 and st.session_state.answers[st.session_state.current_question] is not None:
        st.session_state.current_question += 1

    if st.session_state.current_question <= 200:
        st.write(f"Question {st.session_state.current_question}/200")
        ans = st.number_input("Enter score (0-5)", min_value=0, max_value=5, step=1)
        if st.button("Submit"):
            st.session_state.answers[st.session_state.current_question] = ans
            st.session_state.answered_count += 1
            st.session_state.current_question += 1
            st.rerun()  # Refresh to next question

        # Progress
        st.progress(st.session_state.answered_count / 200)
        st.write(f"Progress: {st.session_state.answered_count}/200")

        # Save Button
        if st.button("Save Progress"):
            save_progress()
    else:
        st.session_state.show_results = True
        st.rerun()

else:
    # Results
    row_sums = compute_row_sums()
    sorted_gifts = get_sorted_gifts(row_sums)
    top_score, top_gift = sorted_gifts[0]
    percent = percent_estimates[top_gift]
    message = encouragement_messages[top_gift]

    st.header("Your Results")
    st.subheader("Top 4 Gifts")
    for rank in range(4):
        score, gift = sorted_gifts[rank]
        st.write(f"{rank+1}. {gift}: {score}")

    st.subheader("Encouragement")
    st.write(message)
    st.write(f"Estimated rarity: {percent}%")

    # Export (as text)
    if st.button("Export Results"):
        export_content = "Spiritual Gifts Assessment Results\n\nTop 4 Gifts:\n"
        for rank in range(4):
            score, gift = sorted_gifts[rank]
            export_content += f"{rank+1}. {gift}: {score}\n"
        export_content += f"\nEncouragement: {message} (Rarity: {percent}%)\n"
        st.download_button("Download Results", data=export_content, file_name="results.txt")

    # Edit Answer
    q = st.number_input("Edit Question (1-200)", 1, 200)
    new_ans = st.number_input("New Score (0-5)", 0, 5)
    if st.button("Update"):
        st.session_state.answers[q] = new_ans
        st.session_state.show_results = False  # Recalculate
        st.rerun()

    if st.button("Restart"):
        st.session_state.clear()
        st.rerun()