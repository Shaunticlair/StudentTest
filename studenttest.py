

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
        """Returns the internal representation of the correct answer. Also saves it as self.right_answer"""
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

    def display_test(self, reset=True):
        # Create the main window
        root = tk.Tk()
        root.title("Student Test")

        if reset:
            self.streak=0
        
        # Function to check the selected answer and update the result label
        def check_answer(selected_answer):
            if np.array_equal(selected_answer, self.right_answer):
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
            self.problem = self.generate_problem()
            self.right_answer = self.generate_right_answer()
            self.wrong_answers = self.generate_wrong_answers()
            
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
        self.problem = self.generate_problem()
        self.right_answer = self.generate_right_answer()
        self.wrong_answers = self.generate_wrong_answers()
        
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
            if np.array_equal(answer, self.right_answer):
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


class ConvolutionTest(StudentTest):
    def __init__(self, max_streak=10, mode='dot'):
        super().__init__(max_streak)
        self.mode = mode
        self.image_num = 0

    def generate_dot_image(self, image_size, pixel_count, filter, old_image=None):
        """
        Generate an image with randomly placed pixels, excluding pixels too close to each other and the edges.
        Returns the generated image.
        """
        filter_shape = filter.shape
        seed = int(time()) + self.image_num
        random.seed(seed)
        self.image_num += 1
        image = np.zeros((image_size, image_size))
        
        # Define a buffer to avoid placing pixels at the edges
        buffer = max(filter_shape)
        possible_pixels = {(i, j) for i in range(buffer, image_size - buffer) for j in range(buffer, image_size - buffer)}
        
        selected_pixels = set()
        while len(selected_pixels) < pixel_count and possible_pixels:
            # Randomly select a pixel from the possible pixels
            pixel = random.choice(list(possible_pixels))
            selected_pixels.add(pixel)

            # Store pixels that are too close to the selected pixel in a separate set
            pixels_to_remove = set()
            for i in range(max(buffer, pixel[0] - filter_shape[0] + 1), min(image_size - buffer, pixel[0] + filter_shape[0])):
                for j in range(max(buffer, pixel[1] - filter_shape[1] + 1), min(image_size - buffer, pixel[1] + filter_shape[1])):
                    if (i, j) in possible_pixels:
                        pixels_to_remove.add((i, j))

            # Remove pixels that are too close to the selected pixel from possible_pixels
            possible_pixels -= pixels_to_remove

        # Set the selected pixels to 1 in the image
        for pixel in selected_pixels:
            image[pixel] = 1

        if old_image is not None:
            # Used if we want to avoid a duplicate image
            if np.array_equal(old_image, image):
                return self.generate_dot_image(image_size, pixel_count, filter, old_image=old_image)

        return image
    
    def generate_pattern_image(self, dot_image, filter):
        """
        Generate a pattern image by placing the filter over the pixels surrounding
        the modified pixels in the dot image.
        Returns the generated pattern image.
        """
        filter_shape = filter.shape
        pattern_image = np.zeros(dot_image.shape)
        image_size = dot_image.shape[0]

        for i in range(image_size):
            for j in range(image_size):
                if dot_image[i, j] == 1:
                    start_row = max(0, i - filter_shape[0] // 2)
                    end_row = min(image_size, start_row + filter_shape[0])
                    start_col = max(0, j - filter_shape[1] // 2)
                    end_col = min(image_size, start_col + filter_shape[1])

                    pattern_image[start_row:end_row, start_col:end_col] = filter

        return pattern_image
    
    def generate_filter(self, filter_size, old_filter = None):
        seed = int(time()) + self.image_num
        np.random.seed(seed)
        self.image_num+=1

        while True: #Make sure our filter is at least a little interesting
            filter = np.random.randint(0, 2, size=(filter_size, filter_size))
            black_pixels = np.sum(filter == 0)
            white_pixels = np.sum(filter == 1)
            if black_pixels >= 2 and white_pixels >= 2:
                break

        if old_filter is not None: #Avoid duplicate filter
            if np.array_equal(old_filter, filter):
                return self.generate_filter(filter_size, old_filter=old_filter)
        return filter

    def generate_problem(self, filter_size=3):
        """
        Generate a random convolution problem.
        Returns a list containing the problem description and a tuple of the filter and image.

        Also writes it to self.problem.
        """
        # Generate a random filter
        filter = self.generate_filter(filter_size)

        # Generate a random image size and pixel count
        image_size = random.randint(20, 25)
        pixel_count = random.randint(4, 8)

        # Generate the image with randomly placed pixels
        dot_image = self.generate_dot_image(image_size, pixel_count, filter)

        # Generate the problem description
        problem_description = f"Given the following {filter.shape[0]}x{filter.shape[1]} filter, convolve it with the following {image_size}x{image_size} image:"

        self.problem = [problem_description, (filter, dot_image)]

        return self.problem
    
    def generate_right_answer(self):
        """
        Generate the right answer for the convolution problem.
        Returns the convolved image as the right answer.
        """
        filter, image = self.problem[1]

        if self.mode == 'pattern':
            image = self.generate_pattern_image(image, filter)
        
        convolved_image = convolve2d(image, filter, mode='same')
        return convolved_image

    def generate_wrong_answers(self):
        """
        Generate wrong answers for the convolution problem.
        Returns a list of 3 wrong answers:
        - Correct filter, incorrect image
        - Incorrect filter, correct image
        - Incorrect filter, incorrect image
        """
        wrong_answers = []
        filter, image = self.problem[1]

        # Generate a wrong answer with the correct filter and an incorrect image
        filter_1= filter
        image_1 = self.generate_dot_image(image.shape[0], np.sum(image), filter_1, old_image=image)

        # Generate a wrong answer with an incorrect filter and the correct image
        filter_2 = self.generate_filter(filter.shape[0], old_filter=filter)
        image_2 = image

        # Generate a wrong answer with an incorrect filter and an incorrect image
        filter_3 = self.generate_filter(filter.shape[0], old_filter=filter)
        image_3 = self.generate_dot_image(image.shape[0], np.sum(image), filter_2, old_image=image)

        wrong_problems = [(image_1, filter_1), (image_2, filter_2), (image_3, filter_3)]

        if self.mode == 'pattern':

            wrong_problems = [ (self.generate_pattern_image(im, fil), fil) for im, fil in wrong_problems]

        wrong_answers = [convolve2d(im, fil, mode='same') for im, fil in wrong_problems]

        return wrong_answers

    def render_problem(self):
        """
        Render the convolution problem as an image.
        Returns a PIL Image object representing the problem.
        """
        filter, image = self.problem[1]

        if self.mode == 'pattern':
            image = self.generate_pattern_image(image, filter)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 3))
        cmap = plt.cm.gray

        # Display the filter
        ax1.imshow(filter, cmap=cmap, interpolation='nearest', vmin=0, vmax=1, extent= [0,1,0,1])
        ax1.set_title('Filter')
        ax1.axis('off')

        # Add a border around the plot
        border_width = 2  # Adjust the border width as needed
        border_color = 'black'  # Adjust the border color as needed
        rect = patches.Rectangle((0, 0), 1, 1, linewidth=border_width, edgecolor=border_color, facecolor='none')
        ax1.add_patch(rect)

        # Display the image
        ax2.imshow(image, cmap=cmap, interpolation='nearest', vmin=0, vmax=1, extent= [0,1,0,1])
        ax2.set_title('Image')
        ax2.axis('off')

        # Add a border around the plot
        border_width = 2  # Adjust the border width as needed
        border_color = 'black'  # Adjust the border color as needed
        rect = patches.Rectangle((0,0), 1, 1, linewidth=border_width, edgecolor=border_color, facecolor='none')
        ax2.add_patch(rect)

        plt.tight_layout()
        plt.savefig('convolution_problem.png')
        plt.close()

        return Image.open('convolution_problem.png')

    
        
    def render_answer(self, answer):
        """
        Render the answer (convolved image) as an image.
        Returns a PIL Image object representing the answer.
        """
        fig, ax = plt.subplots(figsize=(2, 2))  # Adjust the figsize to make the image smaller
        cmap = plt.cm.gray

        # Display the convolved image
        ax.imshow(answer, cmap=cmap, interpolation='nearest', vmin=0, vmax=np.max(answer), extent= [0,1,0,1])
        ax.set_title('Convolved Image', fontsize=8)  # Adjust the fontsize of the title
        ax.axis('off')

        # Add a border around the plot
        border_width = 2  # Adjust the border width as needed
        border_color = 'black'  # Adjust the border color as needed
        rect = patches.Rectangle((0, 0), 1, 1, linewidth=border_width, edgecolor=border_color, facecolor='none')
        ax.add_patch(rect)

        plt.tight_layout()
        plt.savefig('convolved_image.png')
        plt.close()

        return Image.open('convolved_image.png')


# Create an instance of the ConvolutionTest class
test = ConvolutionTest(max_streak=3, mode='dot')

# Call the display_test() method to run the test
test.display_test()