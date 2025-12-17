"""
Quiz Application (Tkinter GUI)
- Uses JSON for questions & scores
- GUI for taking quiz and viewing score
"""

import json
import os
import datetime
from tkinter import *
from tkinter import messagebox

QUEST_FILE = "questions.json"
SCORES_FILE = "quiz_scores.json"

#  SAMPLE QUESTIONS 
SAMPLE_QUESTIONS = [
    {
        "q": "What is the output of print(2**3)?",
        "options": ["5", "6", "8", "9"],
        "answer_index": 2
    },
    {
        "q": "Which data structure uses key-value pairs?",
        "options": ["List", "Tuple", "Dictionary", "Set"],
        "answer_index": 2
    }
]

# FILE HANDLING 

def ensure_questions():
    if not os.path.exists(QUEST_FILE):
        with open(QUEST_FILE, "w") as f:
            json.dump(SAMPLE_QUESTIONS, f, indent=4)


def load_questions():
    ensure_questions()
    with open(QUEST_FILE, "r") as f:
        return json.load(f)


def save_score(name, total, correct):
    record = {
        "name": name,
        "total": total,
        "correct": correct,
        "percentage": round(correct / total * 100, 2),
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    scores = []
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "r") as f:
            scores = json.load(f)

    scores.append(record)
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f, indent=4)

#  GUI LOGIC 

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("600x400")

        self.questions = load_questions()
        self.index = 0
        self.correct = 0

        self.username = StringVar()
        self.answer = IntVar(value=-1)

        self.start_screen()

    def start_screen(self):
        self.clear()
        Label(self.root, text="Quiz Application", font=("Arial", 20)).pack(pady=20)
        Label(self.root, text="Enter your name").pack()
        Entry(self.root, textvariable=self.username).pack()
        Button(self.root, text="Start Quiz", command=self.start_quiz).pack(pady=10)

    def start_quiz(self):
        if self.username.get().strip() == "":
            messagebox.showerror("Error", "Enter your name")
            return
        self.index = 0
        self.correct = 0
        self.show_question()

    def show_question(self):
        self.clear()
        q = self.questions[self.index]

        Label(self.root, text=f"Q{self.index+1}: {q['q']}", wraplength=500,
              font=("Arial", 14)).pack(pady=10)

        self.answer.set(-1)
        for i, opt in enumerate(q['options']):
            Radiobutton(self.root, text=opt, variable=self.answer, value=i).pack(anchor=W)

        Button(self.root, text="Next", command=self.next_question).pack(pady=10)

    def next_question(self):
        if self.answer.get() == -1:
            messagebox.showwarning("Warning", "Select an option")
            return

        if self.answer.get() == self.questions[self.index]['answer_index']:
            self.correct += 1

        self.index += 1
        if self.index < len(self.questions):
            self.show_question()
        else:
            self.show_result()

    def show_result(self):
        self.clear()
        total = len(self.questions)
        percent = round(self.correct / total * 100, 2)
        Label(self.root, text="Quiz Finished!", font=("Arial", 18)).pack(pady=20)
        Label(self.root, text=f"Score: {self.correct}/{total} ({percent}%)").pack()

        save_score(self.username.get(), total, self.correct)

        Button(self.root, text="Restart", command=self.start_screen).pack(pady=10)
        Button(self.root, text="Exit", command=self.root.destroy).pack()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# MAIN 

if __name__ == "__main__":
    root = Tk()
    QuizApp(root)
    root.mainloop()