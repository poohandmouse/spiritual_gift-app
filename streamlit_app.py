import json
import streamlit as st

# --- Data ---
categories = [ "Apostleship", "Prophecy", "Evangelism", "Shepherding", "Teaching",
    "Serving", "Exhortation", "Giving", "Giving Aid", "Compassion",
    "Healing", "Working Miracles", "Tongues", "Interpretation of Tongues",
    "Wisdom", "Knowledge", "Faith", "Discernment", "Helps", "Administration" ]

percent_estimates = { "Apostleship": 2, "Prophecy": 3, "Evangelism": 4, "Shepherding": 2,
    "Teaching": 9, "Serving": 8, "Exhortation": 5, "Giving": 3, "Giving Aid": 5,
    "Compassion": 4, "Healing": 4, "Working Miracles": 1, "Tongues": 3,
    "Interpretation of Tongues": 1, "Wisdom": 4, "Knowledge": 4, "Faith": 7,
    "Discernment": 5, "Helps": 9, "Administration": 3 }

encouragement_messages = {
    "Apostleship": "You're a trailblazer! With Apostleship as your top gift, you're called to pioneer new paths and build foundations for others. **Embrace this rare calling**—it's a foundational gift that changes lives and expands God's kingdom!",
    "Prophecy": "What a powerful voice! Prophecy means you're tuned into God's messages for today. Speak boldly and watch how your words inspire transformation. You have a **distinct and vital role** in the body.",
    # ... (keep the rest exactly as you had them)
    "Administration": "Master organizer! Administration brings order to chaos, turning visions into reality with efficiency and grace. **Your ability to organize** ensures long-term fruitfulness and growth."
}

# --- Session State ---
if 'answers' not in st.session_state:
    st.session_state.answers = [None] * 201
if 'current_question' not in st.session_state:
    st.session_state.current_question = 1
if 'answered_count' not in st.session_state:
    st.session_state.answered_count = 0
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

# --- Core Functions ---
def compute_row_sums():
    row_sums = [0] * 20
    for row in range(20):
        start = row + 1
        for col in range(10):
            q_num = start + col * 20
            row_sums[row] += st.session_state.answers[q_num] or 0
    return row_sums

def get_sorted_gifts(row_sums):
    return sorted([(row_sums[i], categories[i]) for i in range(20)], reverse=True)

# --- Main App ---
st.title("Spiritual Gifts Assessment")

# Sidebar
with st.sidebar:
    st.header("Controls")
    uploaded = st.file_uploader("Load Progress (.json)", type="json")
    if uploaded:
        data = json.load(uploaded)
        for q, v in data.items():
            qn = int(q)
            if 1 <= qn <= 200 and 0 <= int(v) <= 5:
                st.session_state.answers[qn] = int(v)
        st.session_state.answered_count = sum(1 for a in st.session_state.answers[1:] if a is not None)
        st.success("Progress loaded!")
        st.rerun()

    if st.button("Download Progress"):
        data = {str(i): v for i, v in enumerate(st.session_state.answers[1:], 1) if v is not None}
        st.download_button("Save as JSON", json.dumps(data, indent=2), "progress.json", "application/json")

    if st.button("Start Over"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- Assessment Mode ---
if not st.session_state.show_results:
    st.subheader("Answer 200 questions (0–5) from your book")
    st.info("Just type a number 0–5 and press **Enter** — no clicking needed!")

    # Find next unanswered question
    while (st.session_state.current_question <= 200 and
           st.session_state.answers[st.session_state.current_question] is not None):
        st.session_state.current_question += 1

    if st.session_state.current_question <= 200:
        q = st.session_state.current_question

        # Form + number input with unique key
        with st.form(key=f"form_q{q}", clear_on_submit=True):
            st.write(f"### Question {q} / 200")
            score = st.number_input(
                "Score (0–5)",
                min_value=0,
                max_value=5,
                value=st.session_state.answers[q] or 0,
                step=1,
                key=f"input_q{q}",
                label_visibility="collapsed"
            )
            submitted = st.form_submit_button("Submit →")

        if submitted:
            if 0 <= score <= 5:
                if st.session_state.answers[q] is None:
                    st.session_state.answered_count += 1
                st.session_state.answers[q] = score
                st.session_state.current_question += 1
                st.rerun()
            else:
                st.error("Score must be 0–5")

        # Auto-focus + select the number input (works perfectly now)
        st.components.v1.html(
            f"""
            <script>
                const input = document.querySelector('input[type="number"][data-testid="stNumberInput"]');
                if (input) {{
                    input.focus();
                    input.select();
                }}
            </script>
            """,
            height=0
        )

        # Progress
        st.progress(st.session_state.answered_count / 200)
        st.write(f"**{st.session_state.answered_count}/200** answered")

    else:
        st.success
