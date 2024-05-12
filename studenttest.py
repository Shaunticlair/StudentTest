

import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.signal import convolve2d

from time import time


import tkinter as tk
from PIL import ImageTk, Image
import random
import matplotlib.patches as patches
from collections import Counter



class StudentTest:
    def __init__(self, max_streak=10):
        self.problem = None
        self.right_answer = None
        self.wrong_answers = None
        self.streak = 0
        self.max_streak=max_streak

        self.image_num = 0 #Used for random seed purposes

    def generate_problem(self):
        """Returns a list containing [description of problem/prompt as a string, internal representation of problem].
        Also saves it as self.problem"""
        raise NotImplementedError  # Template class

    def generate_right_answer(self):
        """Returns the internal representation of the correct answer. 
        Also saves it as self.right_answer"""
        raise NotImplementedError  # Template class

    def generate_wrong_answers(self):
        """Return the incorrect answers as a list of n internal representations of answers.
        Also saves it as self.wrong_answers"""
        raise NotImplementedError  # Template class

    def render_problem(self):
        """Uses self.problem[1] to create an image of the problem"""
        raise NotImplementedError  #Template class
    
    def render_answer(self):
        """Create an image of the problem"""
        raise NotImplementedError  #Template class
    
    def is_correct(self, answer):
        """Returns True if the answer is correct, False otherwise
        Depends on the internal representation of the answer"""
        raise NotImplementedError

    def display_test(self, reset=True):
        # Create the main window
        root = tk.Tk()
        root.title("Student Test")

        if reset:
            self.streak=0
        
        # Function to check the selected answer and update the result label
        def check_answer(selected_answer):
            if self.is_correct(selected_answer):
                result_label.config(text="Correct!", fg="green", font=("Arial", 36))
                self.streak += 1
            else:
                result_label.config(text="Incorrect!", fg="red", font=("Arial", 36))
                self.streak = 0
            
            # Disable answer buttons and highlight the correct answer
            for button in answer_buttons:
                button.config(state=tk.DISABLED)
                #Determine correct button

            self.correct_button.config(bg="green")
            
            # Show the "Next" button
            next_button.grid(row=2, column=3, padx=10, pady=10)

        def next_question():
            # Clear the previous problem and answers

            if self.streak >= self.max_streak:
                game_over()

            prompt_label.config(text="")
            problem_label.config(image=None)
            result_label.config(text="")
            for button in answer_buttons:
                button.grid_forget()  # Hide the answer buttons instead of destroying them
            next_button.grid_forget()
            
            # Generate a new problem
            self.generate_problem()
            self.generate_right_answer()
            self.generate_wrong_answers()
            
            # Update the prompt text
            prompt_label.config(text=self.problem[0])
            
            # Render and update the problem image
            problem_image = self.render_problem()
            problem_photo = ImageTk.PhotoImage(problem_image)
            problem_label.config(image=problem_photo)
            problem_label.image = problem_photo  # Keep a reference to the photo to prevent garbage collection
            
            # Combine the right answer and wrong answers, and shuffle them randomly
            answers = [self.right_answer] + self.wrong_answers
            random.shuffle(answers)
            
            # Update the answer buttons with new images
            for i, answer in enumerate(answers):
                answer_image = self.render_answer(answer)
                answer_photo = ImageTk.PhotoImage(answer_image)
                answer_button = answer_buttons[i]
                answer_button.config(image=answer_photo, state=tk.NORMAL, command=lambda a=answer: check_answer(a))
                answer_button.image = answer_photo  # Keep a reference to the photo to prevent garbage collection
                answer_button.grid(row=3, column=i, padx=10, pady=5)  # Show the answer buttons again

                #Reset to background color
                answer_button.config(bg=root.cget('bg'))

                if np.array_equal(answer, self.right_answer):
                    self.correct_button = answer_button
            
            # Update the streak label
            streak_label.config(text=f"Streak: {self.streak}")
            
        
        def game_over():
            # Create a popup window to congratulate the user
            popup = tk.Toplevel(root)
            popup.title("Congratulations!")
            popup.geometry("300x100")
            congrats_label = tk.Label(popup, text=f"Congratulations! You reached a streak of {self.streak}!")
            congrats_label.grid(row=0, column=0, padx=10, pady=20)
            ok_button = tk.Button(popup, text="OK", command=lambda: (root.destroy(),popup.destroy())) #OK button makes everything better
            ok_button.grid(row=1, column=0, padx=10, pady=10)
            
            self.streak=0
        
        # Generate the problem, right answer, and wrong answers
        self.generate_problem()
        self.generate_right_answer()
        self.generate_wrong_answers()
        
        # Display the prompt text at the top
        prompt_label = tk.Label(root, text=self.problem[0])
        prompt_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        # Render and display the problem image on the top
        problem_image = self.render_problem()
        problem_photo = ImageTk.PhotoImage(problem_image)
        problem_label = tk.Label(root, image=problem_photo)
        problem_label.grid(row=1, column=1, columnspan=2, rowspan=2, padx=20, pady=10)
        
        # Combine the right answer and wrong answers, and shuffle them randomly
        answers = [self.right_answer] + self.wrong_answers
        random.shuffle(answers)
        
        # Create clickable image buttons for each answer on the right
        answer_buttons = []
        for i, answer in enumerate(answers):
            answer_image = self.render_answer(answer)
            answer_photo = ImageTk.PhotoImage(answer_image)
            answer_button = tk.Button(root, image=answer_photo, command=lambda a=answer: check_answer(a))
            answer_button.grid(row=3, column=i, padx=10, pady=5)
            answer_button.image = answer_photo  # Keep a reference to the photo to prevent garbage collection
            answer_buttons.append(answer_button)
            if self.is_correct(answer):
                self.correct_button = answer_button
        
        # Create a label to display the result (correct/incorrect)
        result_label = tk.Label(root, text="")
        result_label.grid(row=1, column=3, padx=20, pady=10)
        
        # Create a "Next" button
        next_button = tk.Button(root, text="Next", command=next_question, font=("Arial", 36))
        
        # Create a label to display the streak in the corner
        streak_label = tk.Label(root, text=f"Streak: {self.streak}", bg="green")
        streak_label.grid(row=0, column=3, padx=10, pady=10, sticky="ne")
        # Check if the streak reaches 10
        

        
        # Start the Tkinter event loop
        root.mainloop()


