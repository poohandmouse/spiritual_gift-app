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
    # The scoring system is: Q(row_index + 1) is the first question, then + 20 for each subsequent.
    for row in range(20):
        start = row + 1
        for col in range(10): # 10 questions per gift
            q_num = start + col * 20
            row_sums[row] += st.session_state.answers[q_num] if st.session_state.answers[q_num] is not None else 0
    return row_sums

def get_sorted_gifts(row_sums):
    return sorted([(row_sums[i], categories[i]) for i in range(20)], reverse=True)

def save_progress():
    answered_data = {str(i): st.session_state.answers[i] for i in range(1, 201) if st.session_state.answers[i] is not None}
    # This button triggers the download of the file created from the dictionary
    st.download_button(
        label="Download Progress (Save File)",
        data=json.dumps(answered_data, indent=4),
        file_name="progress.json",
        mime="application/json"
    )

def load_progress(uploaded_file):
    if uploaded_file is not None:
        try:
            saved_data = json.load(uploaded_file)
            newly_answered = 0
            
            # Reset answers based on the loaded data
            new_answers = [None] * 201
            for q, ans in saved_data.items():
                q_num = int(q)
                # Validation check upon loading data
                if 1 <= q_num <= 200 and 0 <= int(ans) <= 5:
                    new_answers[q_num] = int(ans)
                    newly_answered += 1
                else:
                    st.warning(f"Skipped invalid score '{ans}' for question {q_num}.")
            
            st.session_state.answers = new_answers
            st.session_state.answered_count = newly_answered
            
            # Find the next unanswered question
            st.session_state.current_question = 1
            while st.session_state.current_question <= 200 and st.session_state.answers[st.session_state.current_question] is not None:
                st.session_state.current_question += 1
                
            st.success(f"Loaded {st.session_state.answered_count} answers! Ready for Question {st.session_state.current_question}.")
            st.session_state.show_results = (st.session_state.current_question > 200)
            st.rerun()

        except json.JSONDecodeError:
            st.error("Error loading file. Please ensure it is a valid JSON file.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# Main App Layout
st.title("Spiritual Gifts Assessment")
st.markdown("---")

if 'show_all' not in st.session_state:
    st.session_state.show_all = False

# --- Sidebar Controls ---
with st.sidebar:
    st.header("App Controls")

    # Load Progress
    st.subheader("Load/Save")
    uploaded_file = st.file_uploader("Upload Progress (.json file)", type="json")
    if uploaded_file:
        load_progress(uploaded_file)
    
    # Save Progress Button
    save_progress()
    
    st.markdown("---")

    # Restart Button
    if st.button("Start Over (Clear All Answers)"):
        st.session_state.clear()
        st.session_state.answers = [None] * 201
        st.session_state.current_question = 1
        st.session_state.answered_count = 0
        st.session_state.show_results = False
        st.success("Assessment cleared. Starting from Question 1.")
        st.rerun()

# --- Assessment or Results View ---

if not st.session_state.show_results:
    # --- ASSESSMENT INPUT VIEW ---
    st.subheader("Answer 200 questions (0-5) based on your assessment book.")
    st.info("Scores: 0 (Not at all) to 5 (Consistently and strongly)")
    
    # Check if we should move to results immediately
    while st.session_state.current_question <= 200 and st.session_state.answers[st.session_state.current_question] is not None:
        st.session_state.current_question += 1

    if st.session_state.current_question <= 200:
        
        # Input Form
        with st.form("question_form"):
            st.write(f"### Question {st.session_state.current_question} / 200")
            
            # Pre-populate with previous answer if available
            default_value = st.session_state.answers[st.session_state.current_question] if st.session_state.answers[st.session_state.current_question] is not None else 0
            
            ans = st.number_input(
                "Select your score (0 to 5):",
                min_value=0, max_value=5, step=1,
                value=default_value,
                key=f"q_{st.session_state.current_question}",
                help="Type the number (0-5) and press Enter to submit."
            )
            
            # Use a unique key for the submit button to aid in JavaScript targeting, 
            # although standard st.form behavior should handle Enter.
            submitted = st.form_submit_button("Submit Score and Go to Next Question", key="submit_btn")

        if submitted:
            # --- VALIDATION FIX: Ensure the value is strictly within bounds before processing ---
            if 0 <= ans <= 5:
                # Check if this question was already answered (for counting correctly)
                if st.session_state.answers[st.session_state.current_question] is None:
                    st.session_state.answered_count += 1
                
                st.session_state.answers[st.session_state.current_question] = ans
                st.session_state.current_question += 1
                st.rerun() # Refresh to next question
            else:
                # If validation fails, show a clear error message.
                st.error(f"Score '{ans}' is invalid. Please enter a value between 0 and 5. This score was not recorded.")
                # We do not rerun here, forcing the user to correct the input.

        # --- AUTO-FOCUS FIX: FINAL ATTEMPT FOR MAXIMUM RELIABILITY ---
        st.markdown(
            f"""
            <script>
                (function() {{
                    // We must wait longer for Streamlit's rendering pipeline to stabilize.
                    setTimeout(() => {{
                        // Target the input element by its type and ensure it's within the main form area.
                        // We target the *last* number input created, which is the current question.
                        const inputElements = document.querySelectorAll('input[type="number"]');
                        if (inputElements.length > 0) {{
                            const inputElement = inputElements[inputElements.length - 1]; // Select the most recently created input
                            
                            if (inputElement && document.activeElement !== inputElement) {{
                                inputElement.focus();
                                // This is crucial: selects the entire current value (usually '0') so the user can type the new score immediately.
                                inputElement.select(); 
                            }}
                        }}
                    }}, 250); // Increased delay to 250ms for maximum stability across devices
                }})(); 
            </script>
            """,
            unsafe_allow_html=True
        )
            
        # Progress Bar
        st.markdown("---")
        progress_value = st.session_state.answered_count / 200
        st.progress(progress_value, text=f"Progress: {st.session_state.answered_count}/200 ({progress_value:.0%})")
        
    else:
        # Completed all questions, show button to see results
        if st.session_state.answered_count == 200:
            st.success("Assessment Complete!")
            if st.button("View Results"):
                st.session_state.show_results = True
                st.rerun()
        else:
            # Should only happen if session state is inconsistent, fallback to refresh
            st.warning("Please submit all questions or reload a full assessment.")
            if st.button("Attempt to Recalculate"):
                st.session_state.show_results = True
                st.rerun()


else:
    # --- RESULTS VIEW ---
    row_sums = compute_row_sums()
    sorted_gifts = get_sorted_gifts(row_sums)
    top_score, top_gift = sorted_gifts[0]
    percent = percent_estimates.get(top_gift, 0)
    message = encouragement_messages.get(top_gift, "No message found.")

    st.subheader("🎉 Your Spiritual Gifts Assessment Results 🎉")
    st.markdown("---")

    # Top Gift Highlight
    st.markdown(
        f"""
        <div style='background-color: #E6F2FF; padding: 20px; border-radius: 10px; border: 2px solid #007BFF; text-align: center;'>
            <h4 style='color: #0056b3; margin-bottom: 5px;'>TOP GIFT IDENTIFIED</h4>
            <h1 style='color: #007BFF; font-size: 36px; margin-top: 0px;'>{top_gift}</h1>
            <p style='color: #343A40; margin-top: 10px;'>Score: <b>{top_score}</b> (Estimated Rarity: <b>{percent}%</b> of Christians with this primary gift)</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Encouragement
    st.subheader("Your Encouragement Message")
    st.info(f"{message}")

    # Top 4 List
    st.subheader("Your Top 4 Gifts")
    
    # Create a nice markdown table for the top 4
    table_content = "| Rank | Gift | Score |\n| :---: | :--- | :---: |\n"
    for rank in range(4):
        score, gift = sorted_gifts[rank]
        table_content += f"| {rank+1} | **{gift}** | {score} |\n"
    st.markdown(table_content)
    
    st.markdown("---")

    # Action Buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Show All Gifts Breakdown", use_container_width=True):
            st.session_state.show_all = not st.session_state.show_all
            st.rerun()

    with col2:
        if st.button("Back to Assessment", use_container_width=True):
            st.session_state.show_results = False
            st.session_state.current_question = 1 # Re-find next question
            st.rerun()

    # Show All Gifts Expansion
    if st.session_state.show_all:
        st.subheader("Full Score Breakdown")
        
        # Display all gifts in a structured list
        for i, (score, gift) in enumerate(sorted_gifts):
            st.markdown(f"**{i+1}.** {gift} (Score: {score})")

    st.markdown("---")
    
    # Edit Answer
    st.subheader("Edit/Correct an Answer")
    q = st.number_input("Question number to edit (1-200)", min_value=1, max_value=200, value=1)
    # Default value shows current score for the selected question
    current_score = st.session_state.answers[q] if st.session_state.answers[q] is not None else 0
    
    # NOTE: Using a number_input here too, which automatically validates min/max on its widget buttons.
    new_ans = st.number_input(f"Current Score for Q{q} is {current_score}. New Score (0-5):", 0, 5, value=current_score)
    
    if st.button("Update Score and Recalculate"):
        # Explicit check for the edit field too
        if 0 <= new_ans <= 5: 
            if st.session_state.answers[q] is None:
                # If the original was None, we count it now
                st.session_state.answered_count += 1
                
            st.session_state.answers[q] = new_ans
            st.session_state.show_results = True # Recalculate immediately
            st.toast(f"Question {q} updated!")
            st.rerun()
        else:
            st.error(f"Score '{new_ans}' is invalid. Please enter a value between 0 and 5. This score was not recorded.")

        
    # Export Results Text File
    st.markdown("---")
    export_content = "--- Spiritual Gifts Assessment Results ---\n\n"
    export_content += f"TOP GIFT: {top_gift} (Score: {top_score}, Rarity: {percent}% of Christians with this primary gift)\n\n"
    export_content += "Your Top 4 Gifts:\n"
    for rank in range(4):
        score, gift = sorted_gifts[rank]
        export_content += f"{rank+1}. {gift} (Score: {score})\n"
    export_content += f"\nEncouragement Message: {message}\n\n"
    export_content += "Full Score Breakdown:\n"
    for score, gift in sorted_gifts:
        export_content += f"- {gift}: {score}\n"
        
    st.download_button("Download Results as TXT", data=export_content, file_name="spiritual_gifts_results.txt")
