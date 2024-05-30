import random
import tkinter as tk
from tkinter import messagebox

COLORS = ['R', 'G', 'B', 'Y', 'W', 'O']
TRIES = 10
CODE_LENGTH = 4


class MastermindGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Mastermind")

        self.code = []
        self.attempts_left = TRIES

        self.create_widgets()
        self.start_game()

    def create_widgets(self):
        self.info_label = tk.Label(self.root, text=f'Welcome to Mastermind, you have {TRIES} tries to guess the code.')
        self.info_label.pack(pady=10)

        self.colors_label = tk.Label(self.root, text=f'The valid colors are: {" ".join(COLORS)}')
        self.colors_label.pack(pady=10)

        self.guess_entry = tk.Entry(self.root)
        self.guess_entry.pack(pady=10)

        self.guess_button = tk.Button(self.root, text="Guess", command=self.make_guess)
        self.guess_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=10)

        self.play_again_button = tk.Button(self.root, text="Play Again", command=self.start_game)
        self.play_again_button.pack(pady=10)
        self.play_again_button.config(state=tk.DISABLED)

    def start_game(self):
        self.code = self.generate_code()
        self.attempts_left = TRIES
        self.info_label.config(text=f'Welcome to Mastermind, you have {TRIES} tries to guess the code.')
        self.result_label.config(text="")
        self.guess_entry.delete(0, tk.END)
        self.guess_button.config(state=tk.NORMAL)
        self.play_again_button.config(state=tk.DISABLED)
        print(f"DEBUG: Code is {self.code}")  # For debugging purposes, print the code to the console

    def generate_code(self):
        return [random.choice(COLORS) for _ in range(CODE_LENGTH)]

    def make_guess(self):
        guess_input = self.guess_entry.get().upper().strip()
        guess = guess_input.replace(" ", "")
        if len(guess) != CODE_LENGTH or any(color not in COLORS for color in guess):
            messagebox.showerror("Invalid Guess", f'You must guess {CODE_LENGTH} valid colors: {" ".join(COLORS)}.')
            return

        guess_list = list(guess)  # Convert string to list of characters
        correct_pos, incorrect_pos = self.check_code(guess_list, self.code)

        if correct_pos == CODE_LENGTH:
            self.result_label.config(text=f'You guessed the code in {TRIES - self.attempts_left + 1} tries!')
            self.end_game(won=True)
        else:
            self.attempts_left -= 1
            self.result_label.config(text=f'Correct Positions: {correct_pos} | Incorrect Positions: {incorrect_pos}')
            if self.attempts_left == 0:
                self.result_label.config(text=f'You ran out of tries. The code was: {" ".join(self.code)}')
                self.end_game(won=False)

    def check_code(self, guess, real_code):
        color_counts = {}
        correct_pos = 0
        incorrect_pos = 0

        for color in real_code:
            if color not in color_counts:
                color_counts[color] = 0
            color_counts[color] += 1

        for guess_color, real_color in zip(guess, real_code):
            if guess_color == real_color:
                correct_pos += 1
                color_counts[guess_color] -= 1

        for guess_color, real_color in zip(guess, real_code):
            if guess_color in color_counts and color_counts[guess_color] > 0:
                incorrect_pos += 1
                color_counts[guess_color] -= 1

        return correct_pos, incorrect_pos

    def end_game(self, won):
        self.guess_button.config(state=tk.DISABLED)
        self.play_again_button.config(state=tk.NORMAL)
        if won:
            messagebox.showinfo("Congratulations", "You guessed the code!")
        else:
            messagebox.showinfo("Game Over", f"You ran out of tries. The code was: {' '.join(self.code)}")


if __name__ == "__main__":
    root = tk.Tk()
    game = MastermindGame(root)
    root.mainloop()
