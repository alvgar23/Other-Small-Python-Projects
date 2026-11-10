# -*- coding: utf-8 -*-
"""
Password Validator & Brute-Force Simulator (Tkinter)
Author: Avtomat Agentics (refactor based on original script)
Updated: Nov 2025

Description:
- Validates a user-entered password (length, digits, upper/lower, special chars).
- Estimates the brute-force search space and time at a configurable trial rate.
- Provides an educational simulation: a progress bar that "finds" the password
  at the correct lexicographic position within the search space — WITHOUT
  actually enumerating all combinations (safe and fast).
- Includes UI controls (Validate, Simulate, Cancel).
- Clear warning: educational only.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from time import perf_counter, sleep
from math import log10
import threading

# -------------------------
# Configuration / Charset
# -------------------------
UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER = "abcdefghijklmnopqrstuvwxyz"
DIGITS = "0123456789"
SPECIALS = "@#%&=$*-+"
# Order for lexicographic brute-force simulation:
CHARSET_ORDER = UPPER + LOWER + DIGITS + SPECIALS

# Safety caps (to avoid insane numbers in UI)
MAX_COMBINATIONS_DISPLAY = 10**18  # show scientific notation if larger
MAX_COMBINATIONS_SIMULATE = 10**12  # if larger, simulation will scale time (but still safe)


# -------------------------
# Helper functions
# -------------------------
def validate_password(pw: str, min_len: int = 8, max_len: int = 32):
    """
    Returns a dict with boolean checks:
    length_ok, has_upper, has_lower, has_digit, has_special
    """
    checks = {
        "length_ok": min_len <= len(pw) <= max_len,
        "has_upper": any(c in UPPER for c in pw),
        "has_lower": any(c in LOWER for c in pw),
        "has_digit": any(c in DIGITS for c in pw),
        "has_special": any(c in SPECIALS for c in pw)
    }
    return checks


def charset_for_password(pw: str):
    """
    Determine the charset to use for estimating combinations: only characters
    from CHARSET_ORDER that may appear in the password space.
    For simplicity we will always use the full CHARSET_ORDER in estimates,
    but if you want tighter estimates you could restrict to only used categories.
    """
    return CHARSET_ORDER


def estimate_combinations(charset_size: int, length: int):
    """Return charset_size ** length as integer (may be huge)."""
    return pow(charset_size, length)


def format_large_number(n):
    """Nice string for large numbers."""
    if n >= MAX_COMBINATIONS_DISPLAY:
        # scientific notation with 3 significant digits
        exp = int(log10(n))
        mant = n / (10**exp)
        return f"{mant:.3f}e{exp}"
    else:
        return f"{n:,}"


def index_of_password_in_lexicographic_order(pw: str, charset: str):
    """
    Compute the zero-based index (position) of the password in the lexicographic
    ordering where the leftmost char is the most-significant (like base-N number).
    This assumes brute-force enumerates strings of exactly len(pw) in the order
    given by 'charset' (from charset[0] to charset[-1]).
    Returns an integer index (0..charset_size**len - 1).
    """
    base = len(charset)
    # Map characters to indices
    char_to_idx = {ch: i for i, ch in enumerate(charset)}
    idx = 0
    L = len(pw)
    for pos, ch in enumerate(pw):
        if ch not in char_to_idx:
            # character not in charset -> can't find in this ordering
            raise ValueError(f"Character '{ch}' not in simulation charset.")
        power = L - pos - 1
        idx = idx * base + char_to_idx[ch]
    return idx


# -------------------------
# Tkinter Application
# -------------------------
class PasswordSimulatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Validator & Brute-Force Simulator")
        self.geometry("1000x700")
        self.configure(bg="#232323")
        self.resizable(False, False)

        # State
        self.sim_thread = None
        self.sim_running = False
        self.sim_cancel = False

        # UI
        self._build_ui()

    def _build_ui(self):
        pad = 10
        fg = "#e6e6e6"
        bg = "#232323"
        bold_font = ("Segoe UI", 10, "bold")

        header = tk.Label(self, text="Password Validator & Brute-Force Simulator (Educational)",
                          bg=bg, fg=fg, font=("Segoe UI", 14, "bold"))
        header.pack(pady=(12, 6))

        note = tk.Label(self, text="This tool is for educational purposes only. It simulates "
                                   "how a brute-force search scales; it does not perform attacks.",
                        bg=bg, fg="#cfcfcf", wraplength=620, justify="left")
        note.pack(pady=(0, 8))

        frame = tk.Frame(self, bg=bg)
        frame.pack(padx=pad, pady=pad, fill="x")

        # Password entry
        tk.Label(frame, text="Enter password to validate:", bg=bg, fg=fg).grid(row=0, column=0, sticky="w")
        self.pw_entry = tk.Entry(frame, width=40, show="*")
        self.pw_entry.grid(row=0, column=1, sticky="w", padx=(8, 0))

        # Validate button
        self.validate_btn = tk.Button(frame, text="Validate", command=self.on_validate, width=12)
        self.validate_btn.grid(row=0, column=2, padx=(12, 0))

        # Checks area
        checks_frame = tk.Frame(self, bg=bg)
        checks_frame.pack(fill="x", padx=pad)
        self.check_vars = {
            "length_ok": tk.StringVar(value="—"),
            "has_upper": tk.StringVar(value="—"),
            "has_lower": tk.StringVar(value="—"),
            "has_digit": tk.StringVar(value="—"),
            "has_special": tk.StringVar(value="—"),
        }
        row = 0
        tk.Label(checks_frame, text="Validation results:", bg=bg, fg=fg, font=bold_font).grid(row=row, column=0, sticky="w")
        row += 1
        tk.Label(checks_frame, text="Length (>=8 and <=32):", bg=bg, fg=fg).grid(row=row, column=0, sticky="w", padx=(8, 0))
        tk.Label(checks_frame, textvariable=self.check_vars["length_ok"], bg=bg, fg="#ffcc66").grid(row=row, column=1, sticky="w")
        row += 1
        tk.Label(checks_frame, text="Uppercase letter:", bg=bg, fg=fg).grid(row=row, column=0, sticky="w", padx=(8, 0))
        tk.Label(checks_frame, textvariable=self.check_vars["has_upper"], bg=bg, fg="#ffcc66").grid(row=row, column=1, sticky="w")
        row += 1
        tk.Label(checks_frame, text="Lowercase letter:", bg=bg, fg=fg).grid(row=row, column=0, sticky="w", padx=(8, 0))
        tk.Label(checks_frame, textvariable=self.check_vars["has_lower"], bg=bg, fg="#ffcc66").grid(row=row, column=1, sticky="w")
        row += 1
        tk.Label(checks_frame, text="Digit:", bg=bg, fg=fg).grid(row=row, column=0, sticky="w", padx=(8, 0))
        tk.Label(checks_frame, textvariable=self.check_vars["has_digit"], bg=bg, fg="#ffcc66").grid(row=row, column=1, sticky="w")
        row += 1
        tk.Label(checks_frame, text="Special char (allowed):", bg=bg, fg=fg).grid(row=row, column=0, sticky="w", padx=(8, 0))
        tk.Label(checks_frame, textvariable=self.check_vars["has_special"], bg=bg, fg="#ffcc66").grid(row=row, column=1, sticky="w")

        # Separator
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=(12, 12))

        # Simulation controls
        sim_frame = tk.Frame(self, bg=bg)
        sim_frame.pack(fill="x", padx=pad)

        tk.Label(sim_frame, text="Simulation controls:", bg=bg, fg=fg, font=bold_font).grid(row=0, column=0, sticky="w")

        tk.Label(sim_frame, text="Trials/sec (simulation speed):", bg=bg, fg=fg).grid(row=1, column=0, sticky="w", padx=(8, 0))
        self.rate_var = tk.IntVar(value=100000)  # default 100k trials/sec (simulated)
        tk.Entry(sim_frame, textvariable=self.rate_var, width=12).grid(row=1, column=1, sticky="w", padx=(8, 0))

        tk.Label(sim_frame, text="Use charset (fixed order):", bg=bg, fg=fg).grid(row=2, column=0, sticky="w", padx=(8, 0))
        charset_label = tk.Label(sim_frame, text=f"{len(CHARSET_ORDER)} chars (A-Z a-z 0-9 specials)", bg=bg, fg="#bdbdbd")
        charset_label.grid(row=2, column=1, sticky="w")

        # Info / estimates area
        info_frame = tk.Frame(self, bg=bg)
        info_frame.pack(fill="x", padx=pad, pady=(8, 0))

        tk.Label(info_frame, text="Estimates:", bg=bg, fg=fg, font=bold_font).grid(row=0, column=0, sticky="w")
        self.estimate_text = tk.Text(info_frame, height=4, width=74, bg="#1e1e1e", fg="#dcdcdc", bd=0)
        self.estimate_text.grid(row=1, column=0, padx=(0, 0))
        self.estimate_text.configure(state="disabled", wrap="word")

        # Progress bar / status
        progress_frame = tk.Frame(self, bg=bg)
        progress_frame.pack(fill="x", padx=pad, pady=(8, 0))
        self.progress = ttk.Progressbar(progress_frame, orient="horizontal", mode="determinate", length=520)
        self.progress.grid(row=0, column=0, padx=(0, 8), pady=(4, 4))
        self.progress_label = tk.Label(progress_frame, text="Progress: 0%", bg=bg, fg=fg)
        self.progress_label.grid(row=0, column=1)

        # Buttons (Simulate / Cancel)
        buttons_frame = tk.Frame(self, bg=bg)
        buttons_frame.pack(pady=(10, 6))
        self.simulate_btn = tk.Button(buttons_frame, text="Simulate Brute-Force", command=self.on_simulate, width=20)
        self.simulate_btn.grid(row=0, column=0, padx=8)
        self.cancel_btn = tk.Button(buttons_frame, text="Cancel Simulation", command=self.cancel_simulation, width=18, state="disabled")
        self.cancel_btn.grid(row=0, column=1, padx=8)

    # -------------------------
    # UI Callbacks
    # -------------------------
    def on_validate(self):
        pw = self.pw_entry.get()
        checks = validate_password(pw)
        # Update textual indicators
        self.check_vars["length_ok"].set("OK" if checks["length_ok"] else "FAIL")
        self.check_vars["has_upper"].set("OK" if checks["has_upper"] else "FAIL")
        self.check_vars["has_lower"].set("OK" if checks["has_lower"] else "FAIL")
        self.check_vars["has_digit"].set("OK" if checks["has_digit"] else "FAIL")
        self.check_vars["has_special"].set("OK" if checks["has_special"] else "FAIL")

        # Update estimate block
        self.update_estimates()

    def update_estimates(self):
        """
        Compute and display combination counts and ETA for the current password
        and chosen trials/sec rate.
        """
        pw = self.pw_entry.get()
        if not pw:
            self._set_estimate_text("Please enter a password and press Validate.")
            return

        # Basic validation of length
        l = len(pw)
        charset = charset_for_password(pw)
        base = len(charset)
        combos = estimate_combinations(base, l)

        rate = max(1, self.rate_var.get())
        # position index (0-based) for where password would be found
        try:
            index = index_of_password_in_lexicographic_order(pw, charset)
        except ValueError as e:
            self._set_estimate_text(f"Error: {e}\nCharset must contain all characters present in the password.")
            return

        # ops required to reach the password = index + 1 (1-based)
        ops_to_find = index + 1

        # Estimated times
        est_total_seconds = combos / rate
        est_find_seconds = ops_to_find / rate

        s = []
        s.append(f"Password length: {l}")
        s.append(f"Charset size: {base}")
        s.append(f"Total combinations: {format_large_number(combos)}")
        s.append(f"Trials/sec (simulated): {rate:,}")
        s.append(f"Estimated time to exhaust space: {est_total_seconds:.2f} s ({est_total_seconds/60:.2f} min)")
        s.append(f"Estimated time to FIND this password (lexicographic position): {est_find_seconds:.2f} s ({est_find_seconds/60:.2f} min)")
        s.append(f"(Position in order: {ops_to_find:,} / {format_large_number(combos)})")

        # If too big, add a warning
        if combos > MAX_COMBINATIONS_SIMULATE:
            s.append("\nWarning: search space is huge. Simulation will scale times proportionally but remain fast for demo purposes.")

        self._set_estimate_text("\n".join(s))

    def _set_estimate_text(self, txt):
        self.estimate_text.configure(state="normal")
        self.estimate_text.delete("1.0", "end")
        self.estimate_text.insert("1.0", txt)
        self.estimate_text.configure(state="disabled")

    def on_simulate(self):
        """
        Start the simulation in a background thread (so UI remains responsive).
        The simulation will advance "simulated ops/sec" and update progress bar
        until the lexicographic index is reached (password 'found').
        """
        if self.sim_running:
            return

        pw = self.pw_entry.get()
        if not pw:
            messagebox.showwarning("Input required", "Please enter a password first and press Validate.")
            return

        # Validate charset containment
        try:
            charset = charset_for_password(pw)
            index = index_of_password_in_lexicographic_order(pw, charset)
        except ValueError as e:
            messagebox.showerror("Charset error", str(e))
            return

        base = len(charset)
        combos = estimate_combinations(base, len(pw))
        rate = max(1, self.rate_var.get())

        # Prepare simulation parameters
        ops_to_find = index + 1
        total_ops = combos

        # If total_ops is extremely big, we will keep simulated time scaled:
        scale_factor = 1.0
        if total_ops > MAX_COMBINATIONS_SIMULATE:
            # scale time down so simulation finishes in a reasonable demo window
            # maintain ratio ops_to_find / total_ops so "found" moment is correct relative position
            scale_factor = total_ops / MAX_COMBINATIONS_SIMULATE
            # effectively we will simulate as if rate_scaled = rate * scale_factor
        self.sim_running = True
        self.sim_cancel = False
        self.simulate_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")
        self.progress["value"] = 0
        self.progress_label.config(text="Progress: 0%")
        self._set_estimate_text("Simulation running... See progress bar. You can cancel.")

        # Start background thread to perform timed updates (safe UI updates via after)
        def sim_thread_fn():
            start = perf_counter()
            ops_done = 0.0
            # rate_scaled is how many ops/sec we advance in the simulated world
            rate_scaled = rate * (scale_factor if scale_factor > 1.0 else 1.0)
            # target fraction = ops_to_find / total_ops
            target_fraction = ops_to_find / total_ops
            # target_ops_scaled = target_fraction * MAX_COMBINATIONS_SIMULATE if scaled, else ops_to_find
            # but simpler: we'll advance simulated ops and compute fraction = ops_done/total_ops (the denominator is real total_ops)
            last_update = perf_counter()
            while not self.sim_cancel:
                now = perf_counter()
                dt = now - last_update
                last_update = now
                ops_done += rate_scaled * dt
                fraction = min(ops_done / total_ops, 1.0)
                percent = fraction * 100.0
                # schedule UI update
                self.after(0, self._update_progress_ui, percent, ops_done, total_ops, start)
                # check if we've reached ops_to_find in the simulated ops_done sense
                if ops_done >= ops_to_find:
                    break
                # small sleep to avoid busy loop
                sleep(0.02)
            # finish sequence
            elapsed = perf_counter() - start
            if not self.sim_cancel:
                self.after(0, self._simulation_finished, elapsed, True, pw)
            else:
                self.after(0, self._simulation_finished, perf_counter() - start, False, pw)

        self.sim_thread = threading.Thread(target=sim_thread_fn, daemon=True)
        self.sim_thread.start()

    def _update_progress_ui(self, percent, ops_done, total_ops, start_time):
        pct = max(0.0, min(percent, 100.0))
        self.progress["value"] = pct
        self.progress_label.config(text=f"Progress: {pct:.2f}%")
        # also update estimate text with live info
        elapsed = perf_counter() - start_time
        est = f"Simulated ops done: {int(ops_done):,} / {format_large_number(total_ops)}\nElapsed (sim): {elapsed:.2f} s"
        self._set_estimate_text(est)

    def _simulation_finished(self, elapsed_seconds, found, pw):
        self.sim_running = False
        self.simulate_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")
        if self.sim_cancel:
            messagebox.showinfo("Simulation", "Simulation canceled by user.")
            self._set_estimate_text("Simulation canceled. You can run again or adjust parameters.")
            return
        self.progress["value"] = 100.0
        self.progress_label.config(text="Progress: 100%")
        if found:
            messagebox.showinfo("Password Found (SIMULATED)", f"The password '{pw}' would be found in ~{elapsed_seconds:.2f} seconds (simulated).")
            # Display final summary
            self.update_estimates()
        else:
            messagebox.showinfo("Simulation", "Simulation ended without finding the password.")
            self.update_estimates()

    def cancel_simulation(self):
        if not self.sim_running:
            return
        self.sim_cancel = True


# -------------------------
# Run application
# -------------------------
if __name__ == "__main__":
    app = PasswordSimulatorApp()
    app.mainloop()