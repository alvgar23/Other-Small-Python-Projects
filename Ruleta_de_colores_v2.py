# -*- coding: utf-8 -*-
"""
Color Guess Game v1.1
Author: Avtomat Agentics
Created: Oct 2020
Updated: Nov 2025

Description:
A simple console-based color guessing game.
The program randomly selects five unique colors from a predefined list.
The player must guess the colors one by one. Each correct guess earns a point.
If the player repeats a color or guesses incorrectly, the game ends.
"""

from random import sample

# ============================================================
# GAME SETUP
# ============================================================

# Initial color pool (unique and lowercase)
AVAILABLE_COLORS = [
    "red", "white", "grey", "green", "brown",
    "yellow", "black", "orange", "blue", "purple", "pink"
]

# Select five unique colors randomly
SECRET_COLORS = sample(AVAILABLE_COLORS, 5)

# Initialize state variables
guessed_colors = []
score = 0
playing = True

# ============================================================
# GAME LOOP
# ============================================================

print("Welcome to the Color Guess Game!")
print("Try to guess the 5 secret colors. Type your answers in lowercase.")
print("If you repeat or miss a color, the game ends.\n")

while playing:
    guess = input("Enter a color: ").strip().lower()

    if guess in SECRET_COLORS and guess not in guessed_colors:
        score += 1
        guessed_colors.append(guess)
        print(f"Correct! Score: {score}")
        print(f"Guessed so far: {guessed_colors}\n")

        if len(guessed_colors) == 5:
            print("Congratulations! You guessed all the colors!")
            playing = False

    elif guess in guessed_colors:
        print(f"You already guessed '{guess}'. Game over.")
        playing = False

    elif guess not in SECRET_COLORS:
        print(f"'{guess}' is not one of the colors. Game over.")
        playing = False

print(f"\nFinal score: {score}")
print(f"The secret colors were: {SECRET_COLORS}")
print("Thanks for playing!")