import streamlit as st
import time
import random

# Sentences to choose from
sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Typing is a fundamental skill in the digital age.",
    "Python makes programming accessible and fun.",
    "Practice daily to improve speed and accuracy.",
    "Streamlining your workflow boosts productivity."
]

# Feedback functions
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

def get_medal(wpm):
    if wpm >= 80:
        return "🥇 Gold Medal"
    elif wpm >= 60:
        return "🥈 Silver Medal"
    elif wpm >= 40:
        return "🥉 Bronze Medal"
    else:
        return "🎓 Keep Practicing"

# Session state init
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "sentence" not in st.session_state:
    st.session_state.sentence = random.choice(sentences)
if "best_wpm" not in st.session_state:
    st.session_state.best_wpm = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0

st.title("✨ Welcome to Jaweria's Typing Speed Game 👩‍💻")

st.markdown("#### 🔔 Challenge: Beat your best speed!")
st.markdown("**Type the sentence below as fast and accurately as you can:**")

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

        correct_chars = sum(1 for i, c in enumerate(typed) if i < len(st.session_state.sentence) and c == st.session_state.sentence[i])
        accuracy = round((correct_chars / len(st.session_state.sentence)) * 100)

        st.markdown(f"### 📊 Results")
        st.success(f"Speed: **{wpm} WPM**  |  Accuracy: **{accuracy}%**  |  {get_medal(wpm)}")
        st.info(get_motivational_feedback(wpm) + "  \n" + get_accuracy_feedback(accuracy))

        if wpm > st.session_state.best_wpm:
            st.session_state.best_wpm = wpm
            st.session_state.streak += 1
            st.success(f"🌟 New Personal Best! 🔁 Streak: {st.session_state.streak}")
        else:
            st.session_state.streak = 0
            st.write("🔄 Streak reset. Try again!")

        # Mistake display
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

# Start timer only when typing begins
if user_input and st.session_state.start_time is None:
    st.session_state.start_time = time.time()

st.markdown("---")
st.caption("Made with ❤️ by Jaweria")