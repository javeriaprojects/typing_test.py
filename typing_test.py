import tkinter as tk
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

def get_motivational_feedback(wpm, accuracy):
    if wpm >= 80:
        return "🚀 Typing Titan! Incredible speed!"
    elif wpm >= 60:
        return "🔥 You’re on fire! Keep it up!"
    elif wpm >= 40:
        return "⚡ Solid performance—aim higher!"
    else:
        return "💡 Don’t worry—practice makes perfect!"

def get_accuracy_feedback(accuracy):
    if accuracy >= 95:
        return "🎯 Sharp accuracy!"
    elif accuracy >= 80:
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

class TypingSpeedTestApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Jaweria's Typing Speed Game 👩‍💻")
        self.master.geometry("700x600")
        self.sentence = random.choice(sentences)
        self.start_time = None
        self.best_wpm = 0
        self.streak = 0

        # 🌟 Welcome Banner
        self.greeting = tk.Label(master, text="✨ Welcome to Jaweria’s Typing Speed Game!", font=("Helvetica", 15, "bold"), fg="purple")
        self.greeting.pack(pady=10)

        self.instructions = tk.Label(master, text="Type the sentence below as fast and accurately as you can:",
                                     font=("Helvetica", 12))
        self.instructions.pack(pady=5)

        self.challenge_label = tk.Label(master, text="🔔 Challenge: Beat your best speed!", font=("Helvetica", 11), fg="darkgreen")
        self.challenge_label.pack()

        self.display = tk.Label(master, text=self.sentence, wraplength=640, font=("Courier", 14), fg="navy")
        self.display.pack(pady=10)

        self.input_box = tk.Text(master, height=4, font=("Courier", 12), wrap="word")
        self.input_box.pack(pady=10)
        self.input_box.bind("<FocusIn>", self.start_timer)

        self.result_btn = tk.Button(master, text="Finish Test", command=self.calculate_results)
        self.result_btn.pack(pady=6)

        self.results = tk.Label(master, text="", font=("Helvetica", 12, "bold"))
        self.results.pack(pady=10)

        self.feedback = tk.Label(master, text="", font=("Helvetica", 11))
        self.feedback.pack()

        self.streak_label = tk.Label(master, text="", font=("Helvetica", 10, "italic"))
        self.streak_label.pack(pady=5)

        self.mistake_label = tk.Text(master, height=5, font=("Courier", 11), wrap="word", bg="#fff0f0")
        self.mistake_label.pack(pady=10)
        self.mistake_label.config(state="disabled")

        self.reset_btn = tk.Button(master, text="🎯 Try Another Sentence", command=self.reset_game)
        self.reset_btn.pack(pady=10)

        self.footer = tk.Label(master, text="Made with ❤️ by Jaweria", font=("Helvetica", 9))
        self.footer.pack(side="bottom", pady=5)

    def start_timer(self, event):
        if not self.start_time:
            self.start_time = time.time()

    def calculate_results(self):
        typed = self.input_box.get("1.0", tk.END).strip()
        time_taken = time.time() - self.start_time if self.start_time else 1
        words_typed = len(typed.split())
        wpm = round((words_typed / time_taken) * 60)

        correct_chars = sum(1 for i, c in enumerate(typed) if i < len(self.sentence) and c == self.sentence[i])
        accuracy = round((correct_chars / len(self.sentence)) * 100)

        feedback = get_motivational_feedback(wpm, accuracy)
        medal = get_medal(wpm)
        accuracy_msg = get_accuracy_feedback(accuracy)

        if wpm > self.best_wpm:
            self.best_wpm = wpm
            self.streak += 1
            streak_msg = f"🔁 New streak: {self.streak} 🌟 Personal best!"
        else:
            self.streak = 0
            streak_msg = "🔄 Reset streak. Let’s beat that score!"

        self.results.config(text=f"Speed: {wpm} WPM   |   Accuracy: {accuracy}%   |   {medal}")
        self.feedback.config(text=f"{feedback}\n{accuracy_msg}")
        self.streak_label.config(text=streak_msg)

        self.show_mistakes(typed)

    def show_mistakes(self, typed_text):
        self.mistake_label.config(state="normal")
        self.mistake_label.delete("1.0", tk.END)

        # Visual comparison: show mistakes in red
        mistake_display = ""
        for i in range(len(self.sentence)):
            if i < len(typed_text):
                if typed_text[i] == self.sentence[i]:
                    mistake_display += typed_text[i]
                else:
                    mistake_display += f"❌{typed_text[i]}"
            else:
                mistake_display += "⬜"

        if len(typed_text) > len(self.sentence):
            mistake_display += f" ➕Extra: {typed_text[len(self.sentence):]}"

        self.mistake_label.insert(tk.END, f"Typed vs. Actual:\n{mistake_display}\n")
        self.mistake_label.config(state="disabled")

    def reset_game(self):
        self.sentence = random.choice(sentences)
        self.display.config(text=self.sentence)
        self.input_box.delete("1.0", tk.END)
        self.results.config(text="")
        self.feedback.config(text="")
        self.streak_label.config(text="")
        self.challenge_label.config(text="🔔 Challenge: Beat your best speed!")
        self.mistake_label.config(state="normal")
        self.mistake_label.delete("1.0", tk.END)
        self.mistake_label.config(state="disabled")
        self.start_time = None

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTestApp(root)
    root.mainloop()