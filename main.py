import tkinter as tk
from tkinter import messagebox
from solver import SudokuSolver
from game import SudokuGame


class WelcomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Welcome Page")
        self.root.geometry("400x300")
        self.root.configure(bg='#F0F0F0')

        self.create_widgets()

    def create_widgets(self):
        welcome_label = tk.Label(self.root, text="Welcome to Sudoku Plus: Solver and Game", font=('Arial', 24, 'bold'), bg='#F0F0F0')
        welcome_label.pack(pady=30)

        info_button = tk.Button(self.root, text="Info", command=self.show_info, bg='#2196F3', fg='white',
                                font=('Arial', 14))
        info_button.pack(pady=10)

        enter_solver_button = tk.Button(self.root, text="Enter Solver Mode", command=self.enter_solver_mode,
                                        bg='#4CAF50', fg='white', font=('Arial', 14))
        enter_solver_button.pack(pady=10)

        enter_game_button = tk.Button(self.root, text="Enter Game Mode", command=self.enter_game_mode,
                                      bg='#FF9800', fg='white', font=('Arial', 14))
        enter_game_button.pack(pady=10)

    def show_info(self):
        info_text = """
        Welcome to Sudoku Game!

        Rules:
        1. Fill in the grid so that every row, column, and 3x3 subgrid contains all digits from 1 to 9 without repetition.
        2. The initial puzzle may contain some filled cells, which cannot be changed.

        Have fun and enjoy the game!
        """
        messagebox.showinfo("Info", info_text)

    def enter_solver_mode(self):
        solver_root = tk.Tk()
        solver_root.title("Sudoku Solver")
        solver_root.geometry("400x500")
        solver_root.configure(bg='#F0F0F0')

        solver = SudokuSolver(solver_root)
        solver_root.mainloop()

    def enter_game_mode(self):
        game_root = tk.Tk()
        game_root.title("Sudoku Game")
        game_root.geometry("400x500")
        game_root.configure(bg='#F0F0F0')

        game = SudokuGame(game_root)
        game_root.mainloop()


def main():
    root = tk.Tk()
    root.geometry("400x300")
    root.configure(bg='#F0F0F0')

    welcome_page = WelcomePage(root)
    root.mainloop()


if __name__ == "__main__":
    main()
