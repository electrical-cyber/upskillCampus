import tkinter as tk
from tkinter import ttk
import json
import random
import os

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Quiz Application")
        self.root.geometry("700x600")

        self.score = 0
        self.current_question = 0
        self.timer_running = False
        self.time_left = 10
        self.popup_open = False  # Flag to track if a popup is open

        self.create_widgets()
        self.load_quiz_data(self.topic_var.get())  # Load default topic

    def create_widgets(self):
        # Styling
        self.root.configure(bg='#f4f4f4')
        font_main = ('Helvetica', 14)
        font_header = ('Helvetica', 16, 'bold')
        font_source = ('Helvetica', 12, 'italic')
        font_scoreboard = ('Helvetica', 14, 'bold')

        # Frame for topic selection
        self.topic_selection_frame = tk.Frame(self.root, bg='#007bff', padx=20, pady=10)
        self.topic_selection_frame.pack(fill=tk.X)

        self.topic_var = tk.StringVar()
        self.topic_var.set(self.load_available_topics()[0])  # Set default topic

        self.topic_menu = ttk.Combobox(self.topic_selection_frame, textvariable=self.topic_var, values=self.load_available_topics(), state='readonly')
        self.topic_menu.pack()

        self.topic_menu.bind('<<ComboboxSelected>>', self.on_topic_selected)

        # Frame for the topic
        self.topic_frame = tk.Frame(self.root, bg='#007bff', padx=20, pady=10)
        self.topic_frame.pack(fill=tk.X)

        self.topic_label = tk.Label(self.topic_frame, text="Topic: Unit/Measurement/Measuring Instrument", font=font_header, bg='#007bff', fg='white')
        self.topic_label.pack()

        # Frame for the scoreboard
        self.scoreboard_frame = tk.Frame(self.root, bg='#28a745', padx=20, pady=10)
        self.scoreboard_frame.pack(fill=tk.X)

        self.scoreboard_label = tk.Label(self.scoreboard_frame, text="Score: 0/0", font=font_scoreboard, bg='#28a745', fg='white')
        self.scoreboard_label.pack()

        # Frame for the question and source
        self.question_frame = tk.Frame(self.root, bg='#007bff', padx=20, pady=10)
        self.question_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Question text with scrollbar
        self.question_text = tk.Text(self.question_frame, wrap=tk.WORD, font=('Helvetica', 14), bg='#007bff', fg='white', height=5, width=80)
        self.question_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.question_scrollbar = tk.Scrollbar(self.question_frame, command=self.question_text.yview)
        self.question_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.question_text.config(yscrollcommand=self.question_scrollbar.set)

        # Source of the question
        self.source_label = tk.Label(self.root, text="", font=font_source, bg='#007bff', fg='white', wraplength=660)
        self.source_label.pack(pady=5, fill=tk.X, padx=20)

        # Frame for the options
        self.options_frame = tk.Frame(self.root, bg='#ffffff', padx=20, pady=10)
        self.options_frame.pack(padx=20, pady=10, fill=tk.X)

        self.radio_var = tk.IntVar()
        self.radio_buttons = []

        for i in range(4):  # Assuming there are always 4 options
            radio_button = tk.Radiobutton(self.options_frame, text="", variable=self.radio_var, value=i, font=font_main, bg='#ffffff', activebackground='#e3e3e3', indicatoron=0, selectcolor='#d0d0d0', command=self.submit_answer)
            radio_button.pack(anchor='w', padx=10, pady=5, fill=tk.X)
            self.radio_buttons.append(radio_button)

        # Frame for buttons and timer
        self.controls_frame = tk.Frame(self.root, bg='#28a745', padx=20, pady=10)
        self.controls_frame.pack(padx=20, pady=10, fill=tk.X)

        self.timer_label = tk.Label(self.controls_frame, text="Time Left: 10", font=font_main, bg='#28a745', fg='white')
        self.timer_label.pack(side=tk.LEFT, padx=10)

        self.previous_button = tk.Button(self.controls_frame, text="Previous", command=self.show_previous_question, font=font_main, bg='#ffc107', fg='black', relief=tk.RAISED, width=10)
        self.previous_button.pack(side=tk.LEFT, padx=5)

        self.stop_resume_button = tk.Button(self.controls_frame, text="Stop", command=self.stop_resume_timer, font=font_main, bg='#dc3545', fg='white', relief=tk.RAISED, width=10)
        self.stop_resume_button.pack(side=tk.LEFT, padx=5)

        self.submit_button = tk.Button(self.controls_frame, text="Submit", command=self.submit_answer, font=font_main, bg='#007bff', fg='white', relief=tk.RAISED, width=10)
        self.submit_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(self.controls_frame, text="Next", command=self.show_next_question, font=font_main, bg='#17a2b8', fg='white', relief=tk.RAISED, width=10)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.feedback_label = tk.Label(self.root, text="", font=font_main, bg='#f4f4f4', wraplength=660)
        self.feedback_label.pack(pady=10)

    def load_available_topics(self):
        # Assuming all quiz files are in the 'quizzes' directory
        quiz_dir = 'quizzes'
        files = [f for f in os.listdir(quiz_dir) if f.endswith('_quiz.json')]
        return [f.replace('_quiz.json', '') for f in files]

    def on_topic_selected(self, event):
        selected_topic = self.topic_var.get()
        self.load_quiz_data(selected_topic)
        self.topic_label.config(text=f"Topic: {selected_topic.replace('_', ' ')}")
        self.load_question()

    def load_quiz_data(self, topic):
        file_path = f'quizzes/{topic}_quiz.json'
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            self.questions = data[0]['quiz_items']
            self.shuffle_questions()
            self.current_question = 0  # Reset to first question
        except FileNotFoundError:
            self.feedback_label.config(text=f"Quiz data file for {topic} not found.", fg='red')

    def shuffle_questions(self):
        random.shuffle(self.questions)
        for question in self.questions:
            correct_answer = question['answers'][question['correct']]
            random.shuffle(question['answers'])
            question['correct'] = question['answers'].index(correct_answer)
    
    def adjust_question_text(self, text_widget, text):
        """Break long questions into multiple lines to fit within the text widget."""
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, text)
        text_widget.update_idletasks()

        # Adjust text size to fit within the widget
        bbox = text_widget.bbox("end")
        if bbox is not None:
            widget_height = text_widget.winfo_height()
            if bbox[3] > widget_height:
                text_widget.config(height=5)  # Set a fixed height for question section
                lines = text.split('\n')
                wrapped_lines = []
                for line in lines:
                    while text_widget.bbox("end") and text_widget.bbox("end")[2] > text_widget.winfo_width():
                        line = line[:-1]  # Remove last character
                        text_widget.delete(1.0, tk.END)
                        text_widget.insert(tk.END, line + '...')
                    wrapped_lines.append(line)
                text_widget.delete(1.0, tk.END)
                text_widget.insert(tk.END, '\n'.join(wrapped_lines))
                text_widget.update_idletasks()

    def load_question(self):
        if self.timer_running:
            self.root.after_cancel(self.timer_id)
        
        if self.current_question >= len(self.questions):
            self.show_next_topic()
            return
        
        question_data = self.questions[self.current_question]
        self.adjust_question_text(self.question_text, question_data['question'])
        self.source_label.config(text=f"Source: {question_data['source']}")
        
        correct_answer = question_data['answers'][question_data['correct']]
        random.shuffle(question_data['answers'])
        question_data['correct'] = question_data['answers'].index(correct_answer)

        for i, answer in enumerate(question_data['answers']):
            self.radio_buttons[i].config(text=answer)
        
        self.radio_var.set(-1)
        self.feedback_label.config(text="")
        
        # Update the scoreboard
        self.scoreboard_label.config(text=f"Score: {self.score}/{len(self.questions)}")
        
        # Start the timer
        self.time_left = 10
        self.timer_label.config(text=f"Time Left: {self.time_left}")
        self.timer_running = True
        self.update_timer()
    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time Left: {self.time_left}")
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.times_up()

    def times_up(self):
        if self.popup_open:
            return
        
        self.timer_running = False
        self.root.after_cancel(self.timer_id)
        
        question_data = self.questions[self.current_question]
        correct_answer_index = question_data['correct']
        correct_answer = question_data['answers'][correct_answer_index]
        explanation = question_data['explanation']
        self.show_popup(False, explanation, correct_answer=correct_answer)

    def stop_resume_timer(self):
        if self.timer_running:
            self.root.after_cancel(self.timer_id)
            self.stop_resume_button.config(text="Resume")
        else:
            self.update_timer()
            self.stop_resume_button.config(text="Stop")
        self.timer_running = not self.timer_running

    def show_popup(self, is_correct, explanation, correct_answer=None):
        self.popup_open = True

        popup = tk.Toplevel(self.root)
        popup.title("Answer")
        popup.geometry("400x200")
        popup.transient(self.root)
        popup.grab_set()

        color = 'green' if is_correct else 'red'
        message = "Correct!" if is_correct else "Wrong!"

        if explanation == "Time's up!":
            message = "Time's Up!"
        elif not is_correct:
            message = "Read Everyday"

        frame = tk.Frame(popup)
        frame.pack(expand=True, fill=tk.BOTH)

        label = tk.Label(frame, text=message, font=('Helvetica', 16, 'bold'), fg=color)
        label.pack(pady=10)

        explanation_text = f"Explanation: {explanation}"
        if correct_answer:
            explanation_text = f"Correct Answer: {correct_answer}\nExplanation: {explanation}"

        explanation_label = tk.Label(frame, text=explanation_text, font=('Helvetica', 12), wraplength=380)
        explanation_label.pack(pady=10, padx=10, fill=tk.BOTH)

        popup.update_idletasks()

        x = (self.root.winfo_screenwidth() - popup.winfo_width()) // 2
        y = (self.root.winfo_screenheight() - popup.winfo_height()) // 2
        popup.geometry(f'+{x}+{y}')

        self.root.after(4000, lambda: [popup.destroy(), self.show_next_question()])

    def submit_answer(self):
        if self.popup_open:
            return

        selected_answer_index = self.radio_var.get()
        
        if selected_answer_index == -1:
            self.show_popup(False, "No answer was selected. The correct answer is provided below.")
            return

        question_data = self.questions[self.current_question]
        correct_answer_index = question_data['correct']
        is_correct = correct_answer_index == selected_answer_index

        self.score += int(is_correct)
        self.show_popup(is_correct, question_data['explanation'], correct_answer=question_data['answers'][correct_answer_index])
        self.timer_running = False
        self.root.after_cancel(self.timer_id)

    def show_next_question(self):
        self.popup_open = False
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.load_question()
        else:
            self.show_next_topic()

    def show_previous_question(self):
        if self.current_question > 0:
            self.current_question -= 1
            self.load_question()

    def show_next_topic(self):
        # Get the list of topics
        topics = self.load_available_topics()
        current_topic = self.topic_var.get()
        try:
            next_topic_index = (topics.index(current_topic) + 1) % len(topics)
            next_topic = topics[next_topic_index]
        except ValueError:
            next_topic = topics[0]  # Default to first topic if the current one is not found
        
        self.topic_var.set(next_topic)
        self.on_topic_selected(None)

    def end_quiz(self):
        self.feedback_label.config(text=f"Quiz finished! Your final score is {self.score}/{len(self.questions)}", fg='blue')
        self.score = 0
        self.current_question = 0
        self.timer_running = False
        self.root.after_cancel(self.timer_id)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
