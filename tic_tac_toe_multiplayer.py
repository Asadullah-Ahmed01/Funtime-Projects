import random
import tkinter as tk
from tkinter import messagebox


class TicTacToeSeries:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Tic-Tac-Toe: Blue vs Red")
        self.root.resizable(False, False)
        self.root.configure(bg="#10141f")

        # Series settings
        self.best_of_var = tk.IntVar(value=3)
        self.total_games = 3
        self.games_played = 0
        self.score_blue = 0
        self.score_red = 0

        # Round state
        self.current_player = "Blue"
        self.board = ["" for _ in range(9)]
        self.game_over = False

        self._build_ui()
        self._start_new_series(reset_only=False)

    def _build_ui(self):
        top = tk.Frame(self.root, bg="#10141f", padx=14, pady=10)
        top.pack(fill="x")

        tk.Label(
            top,
            text="Series:",
            fg="white",
            bg="#10141f",
            font=("Segoe UI", 11, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=(0, 6))

        option = tk.OptionMenu(top, self.best_of_var, 3, 5, 7)
        option.config(font=("Segoe UI", 10), width=8)
        option.grid(row=0, column=1, sticky="w")

        tk.Button(
            top,
            text="Start Series",
            command=self._on_start_series,
            font=("Segoe UI", 10, "bold"),
            bg="#2a3450",
            fg="white",
            activebackground="#3a4a70",
            activeforeground="white",
            relief="flat",
            padx=10,
            pady=4,
        ).grid(row=0, column=2, padx=10)

        self.series_label = tk.Label(
            top,
            text="",
            fg="#bcd0ff",
            bg="#10141f",
            font=("Segoe UI", 10),
        )
        self.series_label.grid(row=1, column=0, columnspan=3, sticky="w", pady=(8, 0))

        score = tk.Frame(self.root, bg="#10141f", padx=14, pady=4)
        score.pack(fill="x")

        self.blue_label = tk.Label(
            score,
            text="🔵 Blue: 0",
            fg="#6ec1ff",
            bg="#10141f",
            font=("Segoe UI", 12, "bold"),
        )
        self.blue_label.pack(side="left", padx=(0, 20))

        self.red_label = tk.Label(
            score,
            text="🔴 Red: 0",
            fg="#ff7a7a",
            bg="#10141f",
            font=("Segoe UI", 12, "bold"),
        )
        self.red_label.pack(side="left")

        self.turn_label = tk.Label(
            self.root,
            text="",
            fg="white",
            bg="#10141f",
            font=("Segoe UI", 12),
            pady=8,
        )
        self.turn_label.pack()

        grid_frame = tk.Frame(self.root, bg="#10141f", padx=14, pady=10)
        grid_frame.pack()

        self.buttons = []
        for i in range(9):
            b = tk.Button(
                grid_frame,
                text="",
                width=5,
                height=2,
                font=("Segoe UI Emoji", 30, "bold"),
                bg="#1d2540",
                fg="white",
                activebackground="#2b3560",
                relief="flat",
                command=lambda idx=i: self._play_move(idx),
            )
            b.grid(row=i // 3, column=i % 3, padx=6, pady=6)
            self.buttons.append(b)

        self.animation_canvas = tk.Canvas(
            self.root,
            width=360,
            height=170,
            bg="#10141f",
            highlightthickness=0,
        )
        self.animation_canvas.pack(pady=(6, 12))

    def _on_start_series(self):
        self._start_new_series(reset_only=True)

    def _start_new_series(self, reset_only=True):
        self.total_games = int(self.best_of_var.get())
        self.games_played = 0
        self.score_blue = 0
        self.score_red = 0
        self._update_score_labels()

        self.series_label.config(text=f"Best of {self.total_games} · First to {self.total_games // 2 + 1} wins")
        self._clear_animation()
        self._new_round(starting_player="Blue")

        if reset_only:
            messagebox.showinfo("Series started", f"New best-of-{self.total_games} series started!")

    def _new_round(self, starting_player=None):
        self.board = ["" for _ in range(9)]
        self.game_over = False
        self.current_player = starting_player if starting_player else random.choice(["Blue", "Red"])

        for b in self.buttons:
            b.config(text="", state="normal")

        self._update_turn_label()

    def _play_move(self, index):
        if self.game_over or self.board[index] != "":
            return

        icon = "🔵" if self.current_player == "Blue" else "🔴"
        color = "#6ec1ff" if self.current_player == "Blue" else "#ff7a7a"

        self.board[index] = self.current_player
        self.buttons[index].config(text=icon, fg=color)

        winner = self._check_winner()
        if winner:
            self.game_over = True
            self.games_played += 1
            if winner == "Blue":
                self.score_blue += 1
            else:
                self.score_red += 1
            self._update_score_labels()
            self._finish_round(f"{icon} {winner} wins this game!")
            return

        if "" not in self.board:
            self.game_over = True
            self.games_played += 1
            self._finish_round("Draw! Nobody gets a point this game.")
            return

        self.current_player = "Red" if self.current_player == "Blue" else "Blue"
        self._update_turn_label()

    def _finish_round(self, round_message):
        for b in self.buttons:
            b.config(state="disabled")

        self._update_turn_label(extra=round_message)

        series_winner = self._check_series_winner()
        if series_winner:
            self._celebrate(series_winner)
            messagebox.showinfo(
                "Series Over",
                f"{series_winner} wins the best-of-{self.total_games} series!\nFinal score: Blue {self.score_blue} - Red {self.score_red}",
            )
            return

        if self.games_played >= self.total_games:
            self._clear_animation()
            messagebox.showinfo(
                "Series Over",
                f"Series draw!\nFinal score: Blue {self.score_blue} - Red {self.score_red}",
            )
            self._update_turn_label(extra="Series ended in a draw.")
            return

        self.root.after(1000, self._new_round)

    def _check_winner(self):
        lines = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        ]
        for a, b, c in lines:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return None

    def _check_series_winner(self):
        needed = self.total_games // 2 + 1
        if self.score_blue >= needed:
            return "Blue"
        if self.score_red >= needed:
            return "Red"
        return None

    def _update_score_labels(self):
        self.blue_label.config(text=f"🔵 Blue: {self.score_blue}")
        self.red_label.config(text=f"🔴 Red: {self.score_red}")

    def _update_turn_label(self, extra=""):
        icon = "🔵" if self.current_player == "Blue" else "🔴"
        color = "#6ec1ff" if self.current_player == "Blue" else "#ff7a7a"
        base = f"Turn: {icon} {self.current_player}"
        msg = f"{base}    {extra}" if extra else base
        self.turn_label.config(text=msg, fg=color if not extra else "#f5f7ff")

    def _clear_animation(self):
        self.animation_canvas.delete("all")

    def _celebrate(self, winner):
        self._clear_animation()
        winner_color = "#6ec1ff" if winner == "Blue" else "#ff7a7a"
        winner_icon = "🔵" if winner == "Blue" else "🔴"

        self.animation_canvas.create_text(
            180,
            28,
            text=f"{winner_icon} {winner} Wins!",
            fill=winner_color,
            font=("Segoe UI", 20, "bold"),
        )

        confetti = []
        colors = ["#f8e16c", "#8df58d", "#ff9ecd", "#8fd3ff", "#ffd37a", winner_color]
        for _ in range(60):
            x = random.randint(10, 350)
            y = random.randint(-150, -10)
            size = random.randint(4, 10)
            speed = random.uniform(2.0, 5.0)
            oid = self.animation_canvas.create_oval(
                x,
                y,
                x + size,
                y + size,
                fill=random.choice(colors),
                outline="",
            )
            confetti.append([oid, speed])

        steps = 70

        def animate(step=0):
            if step >= steps:
                return
            for oid, speed in confetti:
                self.animation_canvas.move(oid, random.uniform(-1, 1), speed)
                x1, y1, x2, y2 = self.animation_canvas.coords(oid)
                if y1 > 170:
                    new_x = random.randint(10, 350)
                    self.animation_canvas.coords(oid, new_x, -10, new_x + (x2 - x1), 0)
            self.root.after(40, animate, step + 1)

        animate()


def main():
    root = tk.Tk()
    TicTacToeSeries(root)
    root.mainloop()


if __name__ == "__main__":
    main()
