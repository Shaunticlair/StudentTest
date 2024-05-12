import numpy as np
import random
import matplotlib.pyplot as plt
plt.rcParams.update({'text.usetex': True})
plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'
from scipy.signal import convolve2d

from time import time


import tkinter as tk
from PIL import ImageTk, Image
import random
import matplotlib.patches as patches
from collections import Counter

from studenttest import StudentTest

class MatrixMultiplyTest(StudentTest):
    def __init__(self, max_streak=10, mode = 'shape_matching', visual = 'numerical'):
        """
        Two modes:
        - shape_matching: The user has to find which multiplication has matching shapes
        - shape_calcuation: The user has to find the correct shape for the output of a valid multiplication
        
        Two settings:
        - numerical: Matrices displayed with numerical values
        - dot: Matrices displayed with dots"""
        super().__init__(max_streak)
        
        #Check for valid mode and visual settings
        if mode not in ['shape_matching', 'shape_calculation']:
            raise ValueError("Invalid mode. Choose 'shape_matching' or 'shape_calculation'")
        if visual not in ['numerical', 'dot']:
            raise ValueError("Invalid setting. Choose 'numerical' or 'dot'")
        

        self.mode = mode
        self.visual = visual

    def generate_matrix_pair(self, m, n, p):
        """
        Generate a pair of random matrices with dimensions m x p and p x n.
        """
        A = np.random.randint(0, 9, size=(m, p))
        B = np.random.randint(0, 9, size=(p, n))
        return A, B

    def generate_problem(self):
        """
        Generate a random matrix multiplication problem.
        Returns a list containing the problem description and a tuple of matrices A and B.
        Also writes it to self.problem.
        """
        # Generate distinct dimensions m, n, p
        # Make sure they are DISTINCT.
        
        dimensions = random.sample(range(1, 6), 3)
        m, n, p= dimensions

        # Generate random matrices A and B
        A,B  = self.generate_matrix_pair(m, n, p)

        # Randomly determine whether to display transposed matrices
        display_A_transposed = random.choice([True, False])
        display_B_transposed = random.choice([True, False])

        # Generate the problem description
        if self.mode == 'shape_matching':
            problem_description = f"Given the following matrices A ({m}x{n}) and B ({n}x{p}), find a valid matrix multiplication:"
        elif self.mode == 'shape_calculation':
            problem_description = f"Given the following matrices A ({m}x{n}) and B ({n}x{p}), choose the correct result, based on shape:"
            display_A_transposed, display_B_transposed = False, False # We want a valid multiplication

        self.problem = [problem_description, (A, B, display_A_transposed, display_B_transposed)]

        return self.problem

    def generate_right_answer(self):
        """
        Generate the right answer for the matrix multiplication problem.
        Returns the correct matrix multiplication result.
        """
        A, B, _, _ = self.problem[1]

        if self.mode == 'shape_calculation':
            # Calculate the shape of the result
            right_answer = np.dot(A, B)

        if self.mode == 'shape_matching':
    
            # Generate four variations of matrix multiplication
            variations = [
                [A, B],
                [A, B.T],
                [B, A],
                [A.T, B]
            ]

            transposed_variations = [
                [B.T, A.T],
                [B,   A.T],
                [A.T, B.T],
                [B.T, A]
            ]

            # Find the valid matrix multiplication
            right_answer = None
            for i in range(len(variations)):
                display_transposed = random.choice([True, False])
                variation = transposed_variations[i] if display_transposed else variations[i]
                if variation[0].shape[1] == variation[1].shape[0]:
                    right_answer = variation

            if right_answer == None:
                raise ValueError("No valid matrix multiplication found:", A.shape, B.shape)


        self.right_answer = right_answer
        return self.right_answer

    def generate_wrong_answers(self):
        """
        Generate wrong answers for the matrix multiplication problem.
        Returns a list of 3 wrong answers.
        """
        A, B, _, _ = self.problem[1]
        wrong_answers = []

        if self.mode == 'shape_calculation':
            # Calculate the shape of the result
            m,p = A.shape 
            p,n = B.shape

            #Sample three elements
            options = [(m,p,n),(n,p,m), (p,n,m), (p,m,n),(n,m,p), (p,p,m)]
            selected_optionas = random.sample(options, 3)

            for M,N,P in selected_optionas: #Generate two wrong answers
                A,B = self.generate_matrix_pair(M,N,P)
                wrong_answers.append(np.dot(A,B))
            

           

        if self.mode == 'shape_matching':

            # Generate four variations of matrix multiplication
            variations = [
                [A, B],
                [A, B.T],
                [B, A],
                [A.T, B]
            ]
            transposed_variations = [
                [B.T, A.T],
                [B,   A.T],
                [A.T, B.T],
                [B.T, A]
            ]

            # Find the invalid matrix multiplications
            
            for i in range(len(variations)):
                display_transposed = random.choice([True, False])
                variation = transposed_variations[i] if display_transposed else variations[i]
                #print(i)
                #print(variation[0].shape, variation[1].shape)
                if variation[0].shape[1] != variation[1].shape[0]:
                    wrong_answers.append(variation)

        self.wrong_answers = wrong_answers

        return self.wrong_answers
    
    def latex_matrix(self, matrix):
        """
        Generate LaTeX code for a matrix.
        """
        if self.visual == 'numerical':
            matrix_latex = r'$\begin{bmatrix}'
            for i in range(matrix.shape[0]):
                row = ' & '.join(str(x) for x in matrix[i])
                matrix_latex += row + r' \\ '
            matrix_latex += r'\end{bmatrix}$'
            return matrix_latex
        if self.visual == 'dot':
            matrix_latex = r'$\begin{bmatrix}'
            for i in range(matrix.shape[0]):
                row = ' & '.join('\cdot' for x in matrix[i])
                matrix_latex += row + r' \\ '
            matrix_latex += r'\end{bmatrix}$'
        return matrix_latex

    def render_problem(self):
        """
        Render the matrix multiplication problem as an image.
        Returns a PIL Image object representing the problem.
        """
        A, B, display_A_transposed, display_B_transposed = self.problem[1]
        if display_A_transposed:
            A = A.T
        if display_B_transposed:
            B = B.T

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(3, 3))

        # Generate LaTeX code for matrix A
        matrix_a_latex = self.latex_matrix(A)

        # Generate LaTeX code for matrix B
        matrix_b_latex = self.latex_matrix(B)

        # Render LaTeX equations
        ax1.text(0.5, 0.5, matrix_a_latex, fontsize=20, ha='center', va='center')
        ax1.set_title(f'Matrix A ({A.shape[0]}x{A.shape[1]})')
        ax1.axis('off')

        ax2.text(0.5, 0.5, matrix_b_latex, fontsize=20, ha='center', va='center')
        ax2.set_title(f'Matrix B ({B.shape[0]}x{B.shape[1]})')
        ax2.axis('off')

        plt.tight_layout()
        plt.savefig('matrix_multiplication_problem.png')
        plt.close()
        return Image.open('matrix_multiplication_problem.png')



    def render_answer(self, answer): #Currently not working
        """
        Render the answer (two matrices side-by-side in multiplication) as an image.
        Returns a PIL Image object representing the answer.
        """
        
        fig, ax = plt.subplots(figsize=(3,3))
        ax.axis('off')
        
        if self.mode == 'shape_matching':
            A, B = answer
            # Generate LaTeX code for matrix A
            matrix_a_latex = self.latex_matrix(A)[:-1]
            
            # Generate LaTeX code for matrix B
            matrix_b_latex = self.latex_matrix(B)[1:]
        
        if self.mode == 'shape_calculation': # Use \cdot to indicate each number
            C = answer
            # Generate LaTeX code for matrix C
            matrix_a_latex = self.latex_matrix(C)
            matrix_b_latex = ''


        # Render LaTeX equations
        ax.text(0, 0.5, matrix_a_latex+matrix_b_latex, fontsize=20, va='center')
        #ax.text(offset, 0.5, matrix_b_latex, fontsize=20, va='center')
        
        plt.tight_layout()
        plt.savefig('matrix_multiplication_answer.png')
        plt.close()
        
        return Image.open('matrix_multiplication_answer.png')
    
    
    def is_correct(self, answer):
        """
        Check if the given answer is correct.
        Returns True if the answer is correct, False otherwise.
        """
        if self.mode == 'shape_matching':
            Aright, Bright = self.right_answer
            A, B = answer
            return np.array_equal(Aright, A) and np.array_equal(Bright, B)
        if self.mode == 'shape_calculation':
            return np.array_equal(self.right_answer, answer)
    
if __name__ == '__main__':
    # Create an instance of the ConvolutionTest class
    test = MatrixMultiplyTest(max_streak=3, mode='shape_calculation', visual = 'numerical')

    # Call the display_test() method to run the test
    test.display_test()