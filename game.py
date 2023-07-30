import tkinter as tk
from tkinter import messagebox
from random import sample


class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        self.root.geometry("400x500")
        self.root.configure(bg='#F0F0F0')

        self.create_widgets()

        self.board = [[0 for _ in range(9)] for _ in range(9)]

        self.generate_random_puzzle()

        self.update_input_from_board()

    def create_widgets(self):
        self.entry_grid = [[None for _ in range(9)] for _ in range(9)]

        for i in range(9):
            for j in range(9):
                self.entry_grid[i][j] = tk.Entry(self.root, width=4, font=('Arial', 18), justify='center')
                self.entry_grid[i][j].grid(row=i, column=j, padx=2, pady=2)

        self.check_button = tk.Button(self.root, text="Check", command=self.check_board, bg='#4CAF50', fg='white',
                                      font=('Arial', 14))
        self.check_button.grid(row=9, column=0, columnspan=3, pady=10, padx=5)

        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear_board, bg='#FF5722', fg='white',
                                      font=('Arial', 14))
        self.clear_button.grid(row=9, column=3, columnspan=3, pady=10, padx=5)

        self.new_game_button = tk.Button(self.root, text="New Game", command=self.new_game, bg='#FF9800', fg='white',
                                         font=('Arial', 14))
        self.new_game_button.grid(row=9, column=6, columnspan=3, pady=10, padx=5)

        self.status_label = tk.Label(self.root, text="", font=('Arial', 16, 'bold'), bg='#F0F0F0', fg='green')

        self.status_label.grid(row=10, columnspan=9)

    def generate_random_puzzle(self):
        base = 3
        side = base * base

        def pattern(r, c):
            return (base * (r % base) + r // base + c) % side

        def shuffle(s):
            return sample(s, len(s))

        rBase = range(base)
        rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
        cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
        nums = shuffle(range(1, base * base + 1))

        self.board = [[nums[pattern(r, c)] for c in cols] for r in rows]

        squares = side * side
        empties = squares * 3 // 4
        for p in sample(range(squares), empties):
            self.board[p // side][p % side] = 0

    def update_input_from_board(self):
        for i in range(9):
            for j in range(9):
                num = self.board[i][j]
                if num == 0:
                    self.entry_grid[i][j].delete(0, tk.END)
                else:
                    self.entry_grid[i][j].delete(0, tk.END)
                    self.entry_grid[i][j].insert(0, str(num))

    def get_board_from_input(self):
        for i in range(9):
            for j in range(9):
                value = self.entry_grid[i][j].get()
                if value.isdigit():
                    num = int(value)
                    if num < 0 or num > 9:
                        messagebox.showerror("Invalid Input", "Please enter valid numbers (1-9) in the Sudoku board.")
                        return False

                    self.board[i][j] = num
                else:
                    self.board[i][j] = 0

        return True

    def clear_board(self):
        for i in range(9):
            for j in range(9):
                self.entry_grid[i][j].delete(0, tk.END)
                self.board[i][j] = 0
        self.status_label.config(text="")

    def check_board(self):
        if not self.get_board_from_input():
            return

        if self.is_valid_solution():
            self.status_label.config(text="Congratulations! You solved the Sudoku puzzle.", fg="green")
        else:
            self.status_label.config(text="Oops! There are errors in the Sudoku puzzle.", fg="red")

    def is_valid_solution(self):
        return self.is_valid_rows() and self.is_valid_columns() and self.is_valid_subgrids()

    def is_valid_rows(self):
        for i in range(9):
            row_values = [self.board[i][j] for j in range(9)]
            if not self.is_valid_set(row_values):
                return False
        return True

    def is_valid_columns(self):
        for j in range(9):
            col_values = [self.board[i][j] for i in range(9)]
            if not self.is_valid_set(col_values):
                return False
        return True

    def is_valid_subgrids(self):
        for r in range(0, 9, 3):
            for c in range(0, 9, 3):
                subgrid_values = [self.board[r + i][c + j] for i in range(3) for j in range(3)]
                if not self.is_valid_set(subgrid_values):
                    return False
        return True

    @staticmethod
    def is_valid_set(numbers):

        return set(numbers) == set(range(1, 10))

    def new_game(self):
        self.clear_board()
        self.generate_random_puzzle()
        self.update_input_from_board()
        self.status_label.config(text="New game started!", fg="black")



def main():
    root = tk.Tk()
    root.geometry("400x500")
    root.configure(bg='#F0F0F0')

    game = SudokuGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
