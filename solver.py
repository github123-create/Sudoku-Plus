import tkinter as tk
from tkinter import messagebox


class SudokuSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.configure(bg='#F0F0F0')

        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.night_mode = False
        self.create_widgets()
        self.stop_visualizing = False
        self.is_solved = False
        self.modified_cells = []

    def create_widgets(self):
        self.entry_grid = [[None for _ in range(9)] for _ in range(9)]

        for i in range(9):
            for j in range(9):
                self.entry_grid[i][j] = tk.Entry(self.root, width=4, font=('Arial', 18), justify='center')
                self.entry_grid[i][j].grid(row=i, column=j, padx=2, pady=2)

        self.solve_button = tk.Button(self.root, text="Fast Solve", command=self.solve_fast, bg='#2196F3', fg='white',
                                      font=('Arial', 14))
        self.solve_button.grid(row=9, column=0, columnspan=3, pady=10, padx=5)

        self.clear_button = tk.Button(self.root, text="Clear", command=self.clear, bg='#FF5722', fg='white',
                                      font=('Arial', 14))
        self.clear_button.grid(row=9, column=3, columnspan=3, pady=10, padx=5)

        self.visualize_solve_button = tk.Button(self.root, text="Visualize Solve", command=self.visualize_solve,
                                                bg='#FF9800', fg='white', font=('Arial', 14))
        self.visualize_solve_button.grid(row=9, column=6, columnspan=3, pady=10, padx=5)

        self.stop_visualize_button = tk.Button(self.root, text="Stop Visualize", command=self.stop_visualization,
                                               bg='#FF0000', fg='white', font=('Arial', 14))
        self.stop_visualize_button.grid(row=9, column=9, columnspan=3, pady=10, padx=5)

        self.night_mode_button = tk.Button(self.root, text="Night Mode", command=self.toggle_night_mode,
                                           bg='black', fg='white', font=('Arial', 14))
        self.night_mode_button.grid(row=9, column=12, columnspan=3, pady=10, padx=5)

        self.status_label = tk.Label(self.root, text="", font=('Arial', 16, 'bold'), bg='#F0F0F0', fg='green')
        self.status_label.grid(row=11, columnspan=9)

    def solve_fast(self):
        if self.is_solved:
            return

        if not self.get_board_from_input():
            return

        if self.solve_sudoku():
            self.update_input_from_board()
            self.status_label.config(text="Sudoku Solved Successfully", fg="green")
            self.is_solved = True  # Set the flag to True on successful solution
        else:
            self.status_label.config(text="No solution exists for the given Sudoku board", fg="red")

    def disable_buttons(self):
        self.solve_button.config(state=tk.DISABLED)
        self.clear_button.config(state=tk.DISABLED)

    def enable_buttons(self):
        self.solve_button.config(state=tk.NORMAL)
        self.clear_button.config(state=tk.NORMAL)

    def solve_sudoku(self):
        empty_cell = self.find_empty_cell()
        if not empty_cell:
            self.stop_visualizing = True
            return self.board

        row, col = empty_cell

        for num in range(1, 10):
            if self.is_valid(num, row, col):
                self.board[row][col] = num

                solution = self.solve_sudoku()
                if solution is not None:
                    return solution

                self.board[row][col] = 0

        return None

    def get_board_from_input(self):
        for i in range(9):
            for j in range(9):
                value = self.entry_grid[i][j].get()
                if value.isdigit():
                    num = int(value)
                    if num < 0 or num > 9:
                        messagebox.showerror("Invalid Input", "Please enter valid numbers (0-9) in the Sudoku board.")
                        return False

                    if num != 0 and not self.is_valid(num, i, j):
                        messagebox.showerror("Invalid Input",
                                             "There are conflicting numbers in the same row, column, or 3x3 grid.")
                        return False

                    self.board[i][j] = num
                else:
                    self.board[i][j] = 0

        return True

    def update_input_from_board(self):
        for i in range(9):
            for j in range(9):
                self.entry_grid[i][j].delete(0, tk.END)
                self.entry_grid[i][j].insert(0, str(self.board[i][j]))

    def find_empty_cell(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None

    def is_valid(self, num, row, col):
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False

        return True

    def clear(self):
        for i in range(9):
            for j in range(9):
                self.entry_grid[i][j].delete(0, tk.END)
                self.board[i][j] = 0
        self.status_label.config(text="")

        self.enable_buttons()
        self.is_solved = False

    def visualize_solve(self):
        if self.is_solved:
            return

        if not self.get_board_from_input():
            return

        self.modified_cells.clear()
        self.is_solved = False
        self.disable_buttons()
        self.stop_visualizing = False
        self.visualize_sudoku()

    def visualize_sudoku(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(num, row, col):
                            original_value = self.board[row][col]
                            self.board[row][col] = num
                            self.entry_grid[row][col].delete(0, tk.END)
                            self.entry_grid[row][col].insert(0, str(num))
                            self.root.update()
                            self.root.after(50)

                            if self.stop_visualizing:
                                self.revert_modified_cells()
                                self.enable_buttons()
                                self.clear()
                                return

                            if self.visualize_sudoku():
                                return

                            self.board[row][col] = 0
                            self.entry_grid[row][col].delete(0, tk.END)
                            self.entry_grid[row][col].insert(0, '')
                            self.board[row][col] = original_value
                    return

        self.enable_buttons()
        self.status_label.config(text="Sudoku Solved Successfully", fg="green")
        self.is_solved = True

    def stop_visualization(self):
        self.stop_visualizing = True

    def revert_modified_cells(self):
        for cell_info in self.modified_cells:
            row, col, value_before_modification = cell_info
            self.board[row][col] = value_before_modification
            self.entry_grid[row][col].delete(0, tk.END)
            self.entry_grid[row][col].insert(0, str(value_before_modification))

        self.modified_cells.clear()

    def toggle_night_mode(self):
        self.night_mode = not self.night_mode
        bg_color = 'black' if self.night_mode else '#F0F0F0'
        fg_color = 'white' if self.night_mode else 'black'
        entry_bg_color = 'dark gray' if self.night_mode else 'white'
        entry_fg_color = 'light gray' if self.night_mode else 'black'

        self.root.configure(bg=bg_color)
        self.status_label.configure(bg=bg_color, fg='green')
        self.night_mode_button.configure(bg=bg_color, fg=fg_color)

        for i in range(9):
            for j in range(9):
                self.entry_grid[i][j].configure(bg=entry_bg_color, fg=entry_fg_color)

        if not self.night_mode:
            self.root.after(1, self.enable_buttons)



if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x500")
    app = SudokuSolver(root)
    root.mainloop()
