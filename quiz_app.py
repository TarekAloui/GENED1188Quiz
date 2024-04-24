import tkinter as tk
from tkinter import messagebox
import csv
from PIL import Image, ImageTk


class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz")
        self.current_question = 0
        self.correct_count = 0
        self.incorrect_count = 0
        self.load_questions()
        self.create_widgets()
        self.display_question()

    def load_questions(self):
        self.questions = []
        with open("questions.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.questions.append(row)

    def display_question(self):
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            self.question_label.config(text=question_data["Question"])
            self.radio_var.set(None)
            for i, option in enumerate(
                ["Option A", "Option B", "Option C", "Option D"]
            ):
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
        self.submit_button.pack(pady=10)
        self.end_button = tk.Button(
            self.master, text="End Quiz", command=self.show_results
        )
        self.end_button.pack(pady=10)

    def check_answer(self):
        selected_option = self.radio_var.get()
        correct_option = self.questions[self.current_question]["Correct Answer"]
        correct_answer = self.questions[self.current_question][correct_option]

        if selected_option == correct_option:
            self.correct_count += 1
            self.show_popup("Correct!", "You got it right!", "correct.png")
        else:
            self.incorrect_count += 1
            self.show_popup(
                "Incorrect!",
                f"Incorrect. The correct answer was {correct_answer}.",
                "incorrect.png",
            )
        self.next_question()

    def next_question(self):
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.display_question()
        else:
            self.show_results()

    def show_popup(self, title, message, image_path):
        popup = tk.Toplevel(self.master)
        popup.title(title)
        pil_image = Image.open(image_path)
        pil_image = pil_image.resize((100, 100), Image.Resampling.LANCZOS)
        icon = ImageTk.PhotoImage(pil_image)

        icon_label = tk.Label(popup, image=icon)
        icon_label.image = icon
        icon_label.pack(side="top", fill="both", pady=(10, 20))

        message_label = tk.Label(popup, text=message)
        message_label.pack(side="top", fill="both", pady=(0, 10))

        button = tk.Button(popup, text="OK", command=popup.destroy)
        button.pack(pady=20)

    def show_results(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        result_text = f"Quiz Complete!\nCorrect answers: {self.correct_count}\nIncorrect answers: {self.incorrect_count}"
        result_label = tk.Label(
            self.master, text=result_text, font=("Helvetica", 16), justify="center"
        )
        result_label.pack(pady=(20, 20))
        quit_button = tk.Button(self.master, text="Quit", command=self.master.quit)
        quit_button.pack(pady=(0, 20))


root = tk.Tk()
app = QuizApp(root)
root.mainloop()
