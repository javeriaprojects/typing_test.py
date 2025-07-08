import streamlit as st
import time
import random

# ✍️ Sentence categories
normal_sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Typing is a fundamental skill in the digital age.",
    "Python makes programming accessible and fun.",
    "Practice daily to improve speed and accuracy.",
    "Streamlining your workflow boosts productivity."
]

tongue_twisters = [
    "She sells seashells by the seashore.",
    "How much wood would a woodchuck chuck if a woodchuck could chuck wood?",
    "Peter Piper picked a peck of pickled peppers.",
    "Fuzzy Wuzzy was a bear. Fuzzy Wuzzy had no hair. Fuzzy Wuzzy wasn't very fuzzy, was he?",
    "I scream, you scream, we all scream for ice cream!"
]

# 🎛 Difficulty selection
difficulty = st.selectbox("Select difficulty level:", ["Normal", "Tongue Twister"])

sentences = normal_sentences if difficulty == "Normal" else tongue_twisters

# 🧠 Feedback logic
def get_motivational_feedback(wpm):
    if wpm >= 80:
        return "🚀 Typing Titan! Incredible speed!"
    elif wpm >= 60:
        return "🔥 You're on fire! Keep it up!"
    elif wpm >= 40:
        return "⚡ Solid performance—aim higher!"
    else:
        return "💡 Don’t worry—practice makes perfect!"

def get_accuracy_feedback(acc):
    if acc >= 95:
        return "🎯 Sharp accuracy!"
    elif acc >= 80:
        return "✅ Great effort—almost there!"
    else:
        return "🧠 Take your time and focus!"

def get_medal(score):
    if score >= 80:
        return "🥇 Gold Medal"
    elif score >= 60:
        return "🥈 Silver Medal"
    elif score >= 40:
        return "🥉 Bronze Medal"
    else:
        return "🎓 Keep Practicing"

# 🧾 Session state
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "sentence" not in st.session_state:
    st.session_state.sentence = random.choice(sentences)
if "best_score" not in st.session_state:
    st.session_state.best_score = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0

st.title("✨ Welcome to Jaweria's Typing Speed Game 👩‍💻")
st.markdown("#### 🔔 Challenge: Beat your best score!")
st.markdown(f"**Type this{' tongue twister' if difficulty == 'Tongue Twister' else ''} as fast and accurately as you can:**")

st.code(st.session_state.sentence, language="")

user_input = st.text_area("Start typing here:", height=100)

if st.button("✅ Finish Test"):
    if st.session_state.start_time is None:
        st.warning("Click inside the box and start typing first!")
    else:
        end_time = time.time()
        duration = end_time - st.session_state.start_time
        typed = user_input.strip()
        word_count = len(typed.split())
        wpm = round((word_count / duration) * 60)

        correct_chars = sum(
            1 for i, c in enumerate(typed)
            if i < len(st.session_state.sentence) and c == st.session_state.sentence[i]
        )
        accuracy = round((correct_chars / len(st.session_state.sentence)) * 100)
        effective_score = round((accuracy * min(1, wpm / 60)))

        # Results
        st.markdown("### 📊 Results")
        st.success(f"Speed: **{wpm} WPM** | Accuracy: **{accuracy}%** | Time: **{round(duration, 2)} sec**")
        st.info(f"{get_motivational_feedback(wpm)}\n\n{get_accuracy_feedback(accuracy)}")
        st.write(f"🏁 **Effective Score**: {effective_score} | {get_medal(effective_score)}")

        if effective_score > st.session_state.best_score:
            st.session_state.best_score = effective_score
            st.session_state.streak += 1
            st.balloons()
            st.success(f"🌟 New Personal Best! 🔁 Streak: {st.session_state.streak}")
        else:
            st.session_state.streak = 0
            st.write("🔄 Streak reset. Try again!")

        # 🔍 Mistake viewer
        mistake_display = []
        for i in range(len(st.session_state.sentence)):
            if i < len(typed):
                if typed[i] == st.session_state.sentence[i]:
                    mistake_display.append(typed[i])
                else:
                    mistake_display.append(f"❌{typed[i]}")
            else:
                mistake_display.append("⬜")
        if len(typed) > len(st.session_state.sentence):
            mistake_display.append(f" ➕Extra: {typed[len(st.session_state.sentence):]}")

        st.markdown("#### 🔎 Mistake Viewer")
        st.code("".join(mistake_display), language="")

if st.button("🔄 Try Another Sentence"):
    st.session_state.sentence = random.choice(sentences)
    st.session_state.start_time = None
    st.experimental_rerun()

# ⏱ Timer start trigger
if user_input and st.session_state.start_time is None:
    st.session_state.start_time = time.time()

st.markdown("---")
st.caption("Made with ❤️ by Jaweria")
