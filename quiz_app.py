import tkinter as tk
from tkinter import messagebox
import csv


class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz")
        self.current_question = 0
        self.load_questions()
        self.create_widgets()  # Ensure widgets are created before displaying questions
        self.display_question()

    def load_questions(self):
        self.questions = []
        with open("questions.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.questions.append(row)

    def display_question(self):
        question_data = self.questions[self.current_question]
        self.question_label.config(text=question_data["Question"])
        self.radio_var.set(None)  # Reset previous selection
        for i, option in enumerate(["Option A", "Option B", "Option C", "Option D"]):
            self.options[i].config(text=question_data[option], value=option)

    def create_widgets(self):
        self.question_label = tk.Label(
            self.master, text="", wraplength=400, justify="left"
        )
        self.question_label.pack(pady=(20, 10))

        self.radio_var = tk.StringVar()
        self.options = []
        for i in range(4):
            radio_button = tk.Radiobutton(
                self.master,
                text="",
                variable=self.radio_var,
                value="",
                wraplength=400,
                justify="left",
            )
            radio_button.pack(anchor="w")
            self.options.append(radio_button)

        self.submit_button = tk.Button(
            self.master, text="Submit", command=self.check_answer
        )
        self.submit_button.pack(pady=20)

    def check_answer(self):
        selected_option = self.radio_var.get()
        correct_option = self.questions[self.current_question]["Correct Answer"]
        if selected_option == correct_option:
            messagebox.showinfo("Result", "Correct!")
        else:
            messagebox.showinfo(
                "Result",
                "Incorrect. The correct answer was "
                + self.questions[self.current_question][correct_option]
                + ".",
            )
        self.next_question()

    def next_question(self):
        if self.current_question < len(self.questions) - 1:
            self.current_question += 1
            self.display_question()
        else:
            messagebox.showinfo("End", "No more questions!")
            self.master.quit()


root = tk.Tk()
app = QuizApp(root)
root.mainloop()
