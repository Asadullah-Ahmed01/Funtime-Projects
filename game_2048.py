import random
import tkinter as tk
from tkinter import messagebox


GRID_SIZE = 4
CELL_SIZE = 100
CELL_PADDING = 10
BACKGROUND_COLOR = "#bbada0"
EMPTY_CELL_COLOR = "#cdc1b4"
FONT = ("Helvetica", 24, "bold")

TILE_COLORS = {
    0: ("#cdc1b4", "#776e65"),
    2: ("#eee4da", "#776e65"),
    4: ("#ede0c8", "#776e65"),
    8: ("#f2b179", "#f9f6f2"),
    16: ("#f59563", "#f9f6f2"),
    32: ("#f67c5f", "#f9f6f2"),
    64: ("#f65e3b", "#f9f6f2"),
    128: ("#edcf72", "#f9f6f2"),
    256: ("#edcc61", "#f9f6f2"),
    512: ("#edc850", "#f9f6f2"),
    1024: ("#edc53f", "#f9f6f2"),
    2048: ("#edc22e", "#f9f6f2"),
}


class Game2048:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("2048")
        self.score = 0
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

        self.main_frame = tk.Frame(root, bg=BACKGROUND_COLOR, bd=8)
        self.main_frame.pack(padx=20, pady=20)

        self.score_label = tk.Label(
            root,
            text="Score: 0",
            font=("Helvetica", 14, "bold"),
            fg="#776e65",
        )
        self.score_label.pack(pady=(0, 10))

        self.cells = []
        for i in range(GRID_SIZE):
            row = []
            for j in range(GRID_SIZE):
                cell = tk.Frame(
                    self.main_frame,
                    bg=EMPTY_CELL_COLOR,
                    width=CELL_SIZE,
                    height=CELL_SIZE,
                )
                cell.grid(row=i, column=j, padx=CELL_PADDING, pady=CELL_PADDING)
                label = tk.Label(
                    cell,
                    text="",
                    bg=EMPTY_CELL_COLOR,
                    justify="center",
                    font=FONT,
                    width=4,
                    height=2,
                )
                label.pack(expand=True, fill="both")
                row.append(label)
            self.cells.append(row)

        restart_button = tk.Button(
            root,
            text="Restart",
            command=self.restart,
            font=("Helvetica", 12, "bold"),
            bg="#8f7a66",
            fg="#f9f6f2",
            padx=10,
            pady=5,
        )
        restart_button.pack(pady=(0, 15))

        self.root.bind("<Up>", lambda _: self.make_move("up"))
        self.root.bind("<Down>", lambda _: self.make_move("down"))
        self.root.bind("<Left>", lambda _: self.make_move("left"))
        self.root.bind("<Right>", lambda _: self.make_move("right"))

        self.start_game()

    def start_game(self) -> None:
        self.add_random_tile()
        self.add_random_tile()
        self.update_ui()

    def restart(self) -> None:
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.start_game()

    def add_random_tile(self) -> None:
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.grid[i][j] == 0]
        if not empty_cells:
            return
        i, j = random.choice(empty_cells)
        self.grid[i][j] = 4 if random.random() < 0.1 else 2

    def compress(self, row: list[int]) -> list[int]:
        filtered = [num for num in row if num != 0]
        filtered += [0] * (GRID_SIZE - len(filtered))
        return filtered

    def merge(self, row: list[int]) -> list[int]:
        for i in range(GRID_SIZE - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0
        return row

    def move_left(self) -> bool:
        moved = False
        new_grid = []
        for row in self.grid:
            compressed = self.compress(row)
            merged = self.merge(compressed)
            final = self.compress(merged)
            if final != row:
                moved = True
            new_grid.append(final)
        self.grid = new_grid
        return moved

    def reverse(self) -> None:
        self.grid = [row[::-1] for row in self.grid]

    def transpose(self) -> None:
        self.grid = [list(row) for row in zip(*self.grid)]

    def move_right(self) -> bool:
        self.reverse()
        moved = self.move_left()
        self.reverse()
        return moved

    def move_up(self) -> bool:
        self.transpose()
        moved = self.move_left()
        self.transpose()
        return moved

    def move_down(self) -> bool:
        self.transpose()
        moved = self.move_right()
        self.transpose()
        return moved

    def can_move(self) -> bool:
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] == 0:
                    return True
                if j < GRID_SIZE - 1 and self.grid[i][j] == self.grid[i][j + 1]:
                    return True
                if i < GRID_SIZE - 1 and self.grid[i][j] == self.grid[i + 1][j]:
                    return True
        return False

    def has_won(self) -> bool:
        return any(2048 in row for row in self.grid)

    def make_move(self, direction: str) -> None:
        moves = {
            "left": self.move_left,
            "right": self.move_right,
            "up": self.move_up,
            "down": self.move_down,
        }

        moved = moves[direction]()
        if moved:
            self.add_random_tile()
            self.update_ui()

            if self.has_won():
                if messagebox.askyesno("You won!", "You reached 2048! Continue playing?"):
                    return
                self.restart()
                return

            if not self.can_move():
                messagebox.showinfo("Game Over", "No more moves available. Starting a new game.")
                self.restart()

    def update_ui(self) -> None:
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.grid[i][j]
                bg, fg = TILE_COLORS.get(value, ("#3c3a32", "#f9f6f2"))
                label = self.cells[i][j]
                label.configure(text=str(value) if value else "", bg=bg, fg=fg)

        self.score_label.configure(text=f"Score: {self.score}")
        self.root.update_idletasks()


if __name__ == "__main__":
    app = tk.Tk()
    game = Game2048(app)
    app.mainloop()
