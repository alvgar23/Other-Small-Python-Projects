# -*- coding: utf-8 -*-
"""
Color Guess Game v2.0 — Tkinter GUI Edition
Author: Avtomat Agentics
Updated: Nov 2025

Description:
A graphical color guessing game.
- The program randomly selects five secret colors.
- The player must click the color buttons to guess them.
- Each correct color increases the score.
- Repeating a color or missing one ends the game.
- At the end, the secret colors are revealed.

A minimalist dark-mode interface for visual clarity and portfolio presentation.
"""

import tkinter as tk
from tkinter import messagebox
from random import sample, shuffle

# ============================================================
# GAME CONFIGURATION
# ============================================================

AVAILABLE_COLORS = [
    "red", "white", "grey", "green", "brown",
    "yellow", "black", "orange", "blue", "purple", "pink"
]

# ============================================================
# MAIN GAME CLASS
# ============================================================

class ColorGuessGame(tk.Tk):
    """Main application window for the Color Guess Game."""

    def __init__(self, lives=3):
        super().__init__()
        self.title("Color Guess Game")
        self.geometry("600x500")
        self.resizable(False, False)
        self.configure(bg="#1e1e1e")

        # --- GAME STATE ---
        self.secret_colors = sample(AVAILABLE_COLORS, 5)
        self.guessed_colors = []
        self.score = 0
        self.game_over = False
        self.lives = lives  # variable depending on difficulty

        # --- TITLE ---
        tk.Label(
            self, text="Color Guess Game",
            bg="#1e1e1e", fg="#ffffff", font=("Segoe UI", 18, "bold")
        ).pack(pady=15)

        # --- SCORE LABEL ---
        self.score_label = tk.Label(
            self, text="Score: 0", bg="#1e1e1e", fg="#00bcd4",
            font=("Segoe UI", 14, "bold")
        )
        self.score_label.pack(pady=5)

        # --- LIVES LABEL ---
        self.lives_label = tk.Label(
            self, text=f"Lives: {self.lives}", bg="#1e1e1e", fg="#ff6666",
            font=("Segoe UI", 12, "bold")
        )
        self.lives_label.pack(pady=5)

        # --- COLOR BUTTONS ---
        self.button_frame = tk.Frame(self, bg="#1e1e1e")
        self.button_frame.pack(pady=15)

        self.buttons = {}
        colors_shuffled = AVAILABLE_COLORS.copy()
        shuffle(colors_shuffled)

        for i, color in enumerate(colors_shuffled):
            btn = tk.Button(
                self.button_frame,
                bg=color, width=10, height=3,
                relief="flat", command=lambda c=color: self.guess_color(c)
            )
            btn.grid(row=i // 4, column=i % 4, padx=8, pady=8)
            self.buttons[color] = btn

        # --- STATUS LABEL ---
        self.status_label = tk.Label(
            self, text="Guess the 5 secret colors!",
            bg="#1e1e1e", fg="#cccccc", font=("Segoe UI", 12)
        )
        self.status_label.pack(pady=10)

        # --- RESET BUTTON ---
        self.reset_btn = tk.Button(
            self, text="New Game", bg="#00bcd4", fg="white",
            font=("Segoe UI", 11, "bold"), relief="flat",
            command=self.reset_game, activebackground="#03dac6"
        )
        self.reset_btn.pack(pady=10)

        # --- FOOTER ---
        tk.Label(
            self, text="By Avtomat Agentics — 2025",
            bg="#1e1e1e", fg="#777", font=("Segoe UI", 9)
        ).pack(side="bottom", pady=10)

    # ========================================================
    # GAME LOGIC
    # ========================================================

    def guess_color(self, color):
        """Handles a color button click."""
        if self.game_over:
            return

        # Disable clicked button
        self.buttons[color].config(state="disabled", relief="sunken")

        # Check the guess
        if color in self.secret_colors and color not in self.guessed_colors:
            self.guessed_colors.append(color)
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.status_label.config(text=f"Correct! '{color.title()}' is one of them.")

            if len(self.guessed_colors) == 5:
                self.end_game(win=True)

        elif color in self.guessed_colors:
            self.lose_life(reason=f"You already picked '{color}'.")

        else:
            self.lose_life(reason=f"'{color.title()}' is not in the list.")

    def lose_life(self, reason):
        """Subtracts one life and checks if the game should end."""
        self.lives -= 1
        self.lives_label.config(text=f"Lives: {self.lives}")

        if self.lives > 0:
            self.status_label.config(text=f"{reason} You lost a life! ({self.lives} left)")
        else:
            self.status_label.config(text=f"{reason} Game over.")
            self.end_game(win=False)

    def end_game(self, win):
        """Displays end game messages and reveals secret colors."""
        self.game_over = True

        # Disable all remaining buttons
        for btn in self.buttons.values():
            btn.config(state="disabled")

        # Reveal correct colors visually
        for color in self.secret_colors:
            self.buttons[color].config(highlightbackground="#00ff99", highlightthickness=3)

        if win:
            messagebox.showinfo("You Win!", f" Congratulations! You guessed all 5 colors!\n\nSecret colors:\n{', '.join(self.secret_colors)}")
        else:
            messagebox.showinfo("Game Over", f" You lost! Final score: {self.score}\n\nSecret colors:\n{', '.join(self.secret_colors)}")

    def reset_game(self):
        """Resets the entire game to start a new round."""
        # Instead of resetting directly, destroy the window and re-open difficulty menu
        self.destroy()
        choose_difficulty()


# ============================================================
# DIFFICULTY SELECTION WINDOW
# ============================================================

def choose_difficulty():
    """Opens a simple window to select difficulty level."""
    diff_win = tk.Tk()
    diff_win.title("Select Difficulty")
    diff_win.geometry("300x250")
    diff_win.configure(bg="#1e1e1e")
    diff_win.resizable(False, False)

    tk.Label(
        diff_win, text="Select difficulty level:",
        bg="#1e1e1e", fg="white", font=("Segoe UI", 13, "bold")
    ).pack(pady=20)

    def start_game(lives):
        diff_win.destroy()
        app = ColorGuessGame(lives=lives)
        app.mainloop()

    tk.Button(diff_win, text="Normal", width=20, bg="#00bcd4", fg="white",
              font=("Segoe UI", 8, "bold"), relief="flat",
              command=lambda: start_game(5)).pack(pady=8)

    tk.Button(diff_win, text="Hard", width=20, bg="#ff9800", fg="white",
              font=("Segoe UI", 8, "bold"), relief="flat",
              command=lambda: start_game(3)).pack(pady=8)

    tk.Button(diff_win, text="Very Hard", width=20, bg="#ff5722", fg="white",
              font=("Segoe UI", 8, "bold"), relief="flat",
              command=lambda: start_game(2)).pack(pady=8)

    tk.Button(diff_win, text="Impossible", width=20, bg="#f44336", fg="white",
              font=("Segoe UI", 8, "bold"), relief="flat",
              command=lambda: start_game(0)).pack(pady=8)

    diff_win.mainloop()


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    choose_difficulty()