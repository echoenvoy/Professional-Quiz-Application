import json
import tkinter as tk
from tkinter import messagebox, ttk
from styles import COLORS, FONTS, SIZES

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Quiz Application")
        self.root.geometry(SIZES['window'])
        self.root.configure(bg=COLORS['background'])
        # Center the window
        self.center_window()
        
        # Initialize variables
        self.questions = []
        self.current_question = 0
        self.score = 0
        self.user_answers = []
        self.timer_running = False
        self.time_left = 30
        self.total_questions = 0
        self.timer_id = None  # Store timer ID to cancel it
        
        # Load questions from JSON file
        self.load_questions()
        
        # Setup styles
        self.setup_styles()
        
        # Create main menu
        self.show_main_menu()
    
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button styles
        style.configure('Primary.TButton',
                        font=FONTS['button'],
                        background=COLORS['button'],
                        foreground='white',
                        borderwidth=1,
                        focusthickness=3,
                        focuscolor='none')
        
        style.map('Primary.TButton',
                  background=[('active', COLORS['button_hover'])])
        
        style.configure('Choice.TButton',
                       font=FONTS['choice'],
                       background=COLORS['secondary'],
                       foreground='white',
                       width=SIZES['choice_button_width'])
        
        style.map('Choice.TButton',
                  background=[('active', COLORS['accent'])])
    
    def load_questions(self):
        """Load questions from JSON file"""
        try:
            with open('questions.json', 'r', encoding='utf-8') as file:
                self.questions = json.load(file)
                self.total_questions = len(self.questions)
                print(f"Loaded {self.total_questions} questions successfully.")
        except FileNotFoundError:
            messagebox.showerror("Error", "questions.json file not found!")
            self.root.quit()
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format in questions.json!")
            self.root.quit()
    
    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_main_menu(self):
        """Display the main menu"""
        self.clear_window()
        
        # Title frame
        title_frame = tk.Frame(self.root, bg=COLORS['primary'])
        title_frame.pack(fill='x', pady=(0, 50))
        
        title_label = tk.Label(title_frame, text="Quiz Master", 
                              font=FONTS['title'], 
                              bg=COLORS['primary'], 
                              fg='white',
                              pady=20)
        title_label.pack()
        
        # Info label
        info_label = tk.Label(self.root, 
                             text=f"Total Questions: {self.total_questions}\nTime per question: 30 seconds",
                             font=('Helvetica', 12),
                             bg=COLORS['background'],
                             fg=COLORS['text'])
        info_label.pack(pady=(0, 40))
        
        # Buttons frame
        button_frame = tk.Frame(self.root, bg=COLORS['background'])
        button_frame.pack(expand=True)
        
        # Start Quiz button
        start_btn = ttk.Button(button_frame, 
                              text="START QUIZ", 
                              style='Primary.TButton',
                              command=self.start_quiz)
        start_btn.pack(pady=10, ipadx=20, ipady=10)
        
        # Quit button
        quit_btn = ttk.Button(button_frame, 
                             text="QUIT", 
                             style='Primary.TButton',
                             command=self.root.quit)
        quit_btn.pack(pady=10, ipadx=20, ipady=10)
    
    def start_quiz(self):
        """Start the quiz"""
        # Cancel any existing timer
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
            
        self.current_question = 0
        self.score = 0
        self.user_answers = []
        self.show_question()
    
    def show_question(self):
        """Display the current question"""
        self.clear_window()
        
        # Stop any existing timer
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        
        # Timer display
        self.time_left = 30
        self.timer_label = tk.Label(self.root, 
                                   text=f"Time: {self.time_left}s",
                                   font=FONTS['timer'],
                                   bg=COLORS['background'],
                                   fg=COLORS['primary'])
        self.timer_label.pack(anchor='ne', padx=20, pady=10)
        
        # Progress bar
        progress = (self.current_question / self.total_questions) * 100
        self.progress_bar = ttk.Progressbar(self.root, 
                                           length=400, 
                                           mode='determinate')
        self.progress_bar['value'] = progress
        self.progress_bar.pack(pady=(0, 30))
        
        # Question number
        q_num_label = tk.Label(self.root, 
                              text=f"Question {self.current_question + 1} of {self.total_questions}",
                              font=('Helvetica', 12, 'bold'),
                              bg=COLORS['background'],
                              fg=COLORS['secondary'])
        q_num_label.pack(pady=(0, 20))
        
        # Question text
        question_data = self.questions[self.current_question]
        question_label = tk.Label(self.root, 
                                 text=question_data['question'],
                                 font=FONTS['question'],
                                 bg=COLORS['background'],
                                 fg=COLORS['text'],
                                 wraplength=600,
                                 justify='center')
        question_label.pack(pady=(0, 30))
        
        # Choices frame
        choices_frame = tk.Frame(self.root, bg=COLORS['background'])
        choices_frame.pack(expand=True, fill='both', padx=50)
        
        # Create choice buttons
        self.choice_var = tk.StringVar()
        self.choice_buttons = []
        
        for i, choice in enumerate(question_data['choices']):
            btn = tk.Radiobutton(choices_frame,
                                text=choice,
                                variable=self.choice_var,
                                value=choice,
                                font=FONTS['choice'],
                                bg=COLORS['background'],
                                fg=COLORS['text'],
                                selectcolor=COLORS['accent'],
                                indicatoron=0,
                                width=40,
                                height=2,
                                relief='raised',
                                bd=2,
                                cursor='hand2')
            btn.pack(pady=5, fill='x')
            self.choice_buttons.append(btn)
        
        # Next button
        next_btn = ttk.Button(self.root,
                             text="Next Question" if self.current_question < self.total_questions - 1 else "Finish Quiz",
                             style='Primary.TButton',
                             command=self.next_question)
        next_btn.pack(pady=30, ipadx=20, ipady=10)
        
        # Start the timer
        self.timer_running = True
        self.update_timer()
    
    def update_timer(self):
        """Update the countdown timer - FIXED TIMER"""
        if not self.timer_running:
            return
        
        # Update timer display
        self.timer_label.config(text=f"Time: {self.time_left}s")
        
        # Change color based on time left
        if self.time_left <= 10:
            self.timer_label.config(fg=COLORS['timer_critical'])
        elif self.time_left <= 20:
            self.timer_label.config(fg=COLORS['timer_warning'])
        else:
            self.timer_label.config(fg=COLORS['primary'])
        
        # Countdown logic
        if self.time_left > 0:
            self.time_left -= 1
            # Schedule next update after 1000ms (1 second) - CORRECTED
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            # Time's up - auto next question
            self.user_answers.append(None)  # No answer given
            self.next_question()
    
    def next_question(self):
        """Move to the next question or show results"""
        # Stop the timer
        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        
        # Record the answer if one was selected
        if hasattr(self, 'choice_var') and self.choice_var.get():
            self.user_answers.append(self.choice_var.get())
            
            # Check if answer is correct
            correct_answer = self.questions[self.current_question]['correct']
            if self.choice_var.get() == correct_answer:
                self.score += 1
        else:
            self.user_answers.append(None)
        
        # Clear the choice variable
        if hasattr(self, 'choice_var'):
            self.choice_var.set('')
        
        # Move to next question or show results
        self.current_question += 1
        if self.current_question < self.total_questions:
            self.show_question()
        else:
            self.show_results()
    
    def show_results(self):
        self.clear_window()
        
        # Calculate percentage before displaying
        percentage = (self.score / self.total_questions) * 100 if self.total_questions > 0 else 0
        
        # Create main container
        main_container = tk.Frame(self.root, bg=COLORS['background'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Top section - Score display
        top_frame = tk.Frame(main_container, bg=COLORS['background'])
        top_frame.pack(fill='x', pady=(0, 20))
        
        # Title
        title_label = tk.Label(top_frame, 
                            text="Quiz Results",
                            font=FONTS['title'],
                            bg=COLORS['background'],
                            fg=COLORS['primary'])
        title_label.pack(pady=(0, 10))
        
        # Score display
        score_frame = tk.Frame(top_frame, bg=COLORS['background'])
        score_frame.pack()
        
        score_label = tk.Label(score_frame,
                            text="Your Score:",
                            font=('Helvetica', 14),
                            bg=COLORS['background'],
                            fg=COLORS['text'])
        score_label.pack()
        
        # Score value - FIXED: Ensure score display is clear
        score_display = f"{self.score} / {self.total_questions}"
        score_value = tk.Label(score_frame,
                            text=score_display,
                            font=FONTS['score'],
                            bg=COLORS['background'],
                            fg=COLORS['correct'] if percentage >= 60 else COLORS['incorrect'])
        score_value.pack()
        
        # Percentage
        percentage_label = tk.Label(score_frame,
                                text=f"{percentage:.1f}%",
                                font=('Helvetica', 14),
                                bg=COLORS['background'],
                                fg=COLORS['text'])
        percentage_label.pack()
        
        # Add a separator
        ttk.Separator(main_container, orient='horizontal').pack(fill='x', pady=10)
        
        # Middle section - Detailed results with scrollbar
        middle_frame = tk.Frame(main_container, bg=COLORS['background'])
        middle_frame.pack(fill='both', expand=True)
        
        # Create a canvas with scrollbar for detailed results
        canvas = tk.Canvas(middle_frame, bg=COLORS['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(middle_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['background'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add question-by-question results
        for i, question_data in enumerate(self.questions):
            q_frame = tk.Frame(scrollable_frame, bg=COLORS['background'])
            q_frame.pack(fill='x', pady=5, padx=5)
            
            # Question number and text
            q_text = f"Q{i+1}: {question_data['question']}"
            q_label = tk.Label(q_frame,
                            text=q_text,
                            font=('Helvetica', 10, 'bold'),
                            bg=COLORS['background'],
                            fg=COLORS['text'],
                            wraplength=500,
                            justify='left',
                            anchor='w')
            q_label.pack(fill='x', pady=(0, 2))
            
            # User's answer
            user_answer = self.user_answers[i] if i < len(self.user_answers) else "No answer"
            correct_answer = question_data['correct']
            
            if user_answer == correct_answer:
                answer_color = COLORS['correct']
                answer_text = f"✓ Your answer: {user_answer}"
            else:
                answer_color = COLORS['incorrect']
                answer_text = f"✗ Your answer: {user_answer if user_answer else 'No answer'}"
            
            answer_label = tk.Label(q_frame,
                                text=answer_text,
                                font=('Helvetica', 9),
                                bg=COLORS['background'],
                                fg=answer_color,
                                anchor='w')
            answer_label.pack(fill='x')
            
            # Correct answer (if wrong)
            if user_answer != correct_answer:
                correct_label = tk.Label(q_frame,
                                        text=f"→ Correct answer: {correct_answer}",
                                        font=('Helvetica', 9, 'italic'),
                                        bg=COLORS['background'],
                                        fg=COLORS['text'],
                                        anchor='w')
                correct_label.pack(fill='x')
            
            # Add separator between questions
            if i < len(self.questions) - 1:
                ttk.Separator(q_frame, orient='horizontal').pack(fill='x', pady=5)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bottom section - Buttons
        bottom_frame = tk.Frame(main_container, bg=COLORS['background'])
        bottom_frame.pack(fill='x', pady=(20, 0))
        
        # Buttons frame
        button_frame = tk.Frame(bottom_frame, bg=COLORS['background'])
        button_frame.pack()
        
        # Restart button
        restart_btn = ttk.Button(button_frame,
                                text="Restart Quiz",
                                style='Primary.TButton',
                                command=self.start_quiz)
        restart_btn.pack(side='left', padx=5, ipadx=15, ipady=8)
        
        # Main Menu button
        menu_btn = ttk.Button(button_frame,
                            text="Main Menu",
                            style='Primary.TButton',
                            command=self.show_main_menu)
        menu_btn.pack(side='left', padx=5, ipadx=15, ipady=8)
        
        # Quit button
        quit_btn = ttk.Button(button_frame,
                            text="Quit",
                            style='Primary.TButton',
                            command=self.root.quit)
        quit_btn.pack(side='left', padx=5, ipadx=15, ipady=8)


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = QuizApp(root)
    
    # Make window resizable with minimum size
    root.minsize(800, 600)
    root.resizable(True, True)
    
    root.mainloop()

if __name__ == "__main__":
    main()