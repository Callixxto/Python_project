import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import random

# Main application controller
class ZodiacApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zodiac Horoscope")
        self.root.geometry("400x700")  # Fixed window size
        self.root.resizable(False, False)

        self._day = 1
        self._month = 1
        self.current_screen = None

        # Start with the title screen
        self.show_screen(TitleScreen)

    # Replaces current screen with a new one
    def show_screen(self, screen_class, **kwargs):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = screen_class(self, self.root, **kwargs)
        self.current_screen.pack(fill="both", expand=True)

    # Store user's selected birthday
    def set_birthday(self, day, month):
        self._day = day
        self._month = month

    # Retrieve birthday as a tuple
    def get_birthday(self):
        return self._day, self._month

    # Determine zodiac sign from stored birthday
    def get_zodiac_sign(self):
        return ZodiacLogic.determine_sign(self._day, self._month)


# Base class for all screens (inherits from tk.Frame)
class ZodiacFrame(tk.Frame):
    def __init__(self, app, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.app = app

    # Load and display a background image
    def load_background(self, path):
        img = Image.open(path)
        img = img.resize((400, 700), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(img)
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Adds a hover color change effect to buttons
    def make_hoverable(self, button, color="#343a65", original="#1b1b3a"):
        button.bind("<Enter>", lambda e: button.config(bg=color))
        button.bind("<Leave>", lambda e: button.config(bg=original))


# First screen the user sees
class TitleScreen(ZodiacFrame):
    def __init__(self, app, root):
        super().__init__(app, root)
        self.load_background("Title_screen.png")

        # Tarot button (top)
        tarot_btn = tk.Button(self,
                              text="Tarot",
                              font=("Georgia", 14, "bold"),
                              bg="#1b1b3a", fg="white",
                              activebackground="#2c2c54",
                              relief="raised", bd=3,
                              padx=10, pady=5,
                              command=lambda: self.app.show_screen(TarotScreen))
        self.make_hoverable(tarot_btn)
        tarot_btn.place(x=200, y=540, anchor="center")

        # Zodiac check button (below)
        zodiac_btn = tk.Button(self,
                               text="Check Your Sign",
                               font=("Georgia", 14, "bold"),
                               bg="#1b1b3a", fg="white",
                               activebackground="#2c2c54",
                               relief="raised", bd=3,
                               padx=10, pady=5,
                               command=lambda: self.app.show_screen(BirthdayScreen))
        self.make_hoverable(zodiac_btn)
        zodiac_btn.place(x=200, y=595, anchor="center")


# Screen where user selects their birthday
class BirthdayScreen(ZodiacFrame):
    def __init__(self, app, root):
        super().__init__(app, root)
        self.load_background("day.png")

        self.day_var = tk.StringVar(value="1")
        self.month_var = tk.StringVar(value="January")

        # Style configuration for dropdowns
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.TCombobox",
                        fieldbackground="#f7e6c4",
                        background="#f7e6c4",
                        foreground="#1b1b3a",
                        font=("Georgia", 12),
                        padding=5)

        # Day dropdown menu
        day_dd = ttk.Combobox(self, textvariable=self.day_var,
                              state="readonly", width=5, style="Custom.TCombobox")
        day_dd['values'] = list(range(1, 32))
        day_dd.place(x=70, y=280)

        # Month dropdown menu
        month_dd = ttk.Combobox(self, textvariable=self.month_var,
                                state="readonly", width=10, style="Custom.TCombobox")
        month_dd['values'] = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        month_dd.place(x=260, y=280)

        # Submit button to find zodiac sign
        submit_btn = tk.Button(self,
                               text="Find Your Sign",
                               font=("Georgia", 14, "bold"),
                               bg="#1b1b3a", fg="white",
                               activebackground="#2c2c54",
                               relief="raised", bd=3,
                               padx=10, pady=5,
                               command=self.submit)
        self.make_hoverable(submit_btn)
        submit_btn.place(x=200, y=595, anchor="center")

    # Extract birthday and show zodiac result
    def submit(self):
        try:
            day = int(self.day_var.get())
            month_index = [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ].index(self.month_var.get()) + 1

            self.app.set_birthday(day, month_index)
            zodiac_sign = self.app.get_zodiac_sign()

            if zodiac_sign:
                self.app.show_screen(ResultScreen, sign=zodiac_sign)
            else:
                messagebox.showerror("Error", "Invalid date.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not determine zodiac: {str(e)}")


# Screen that shows the zodiac result
class ResultScreen(ZodiacFrame):
    def __init__(self, app, root, sign):
        super().__init__(app, root)

        try:
            self.load_background(f"{sign}.png")
        except FileNotFoundError:
            messagebox.showerror("Missing Image", f"{sign}.png not found.")
            self.app.show_screen(TitleScreen)
            return

        # Back button to return to birthday input
        back_btn = tk.Button(self,
                             text="Back",
                             font=("Georgia", 10),
                             bg="#1b1b3a", fg="white",
                             activebackground="#2c2c54",
                             relief="raised", bd=1,
                             padx=4, pady=2,
                             command=lambda: self.app.show_screen(TitleScreen))
        self.make_hoverable(back_btn)
        back_btn.place(x=200, y=670, anchor="center")


# Tarot card screen that displays a random card
class TarotScreen(ZodiacFrame):
    def __init__(self, app, root):
        super().__init__(app, root)

        tarot_files = [f"Tarot{i}.png" for i in range(1, 7)]
        tarot_image = random.choice(tarot_files)

        try:
            self.load_background(tarot_image)
        except FileNotFoundError:
            messagebox.showerror("Missing Image", f"{tarot_image} not found.")
            self.app.show_screen(TitleScreen)
            return

        # Back button to return to title screen
        back_btn = tk.Button(self,
                             text="Back",
                             font=("Georgia", 10),
                             bg="#1b1b3a", fg="white",
                             activebackground="#2c2c54",
                             relief="raised", bd=1,
                             padx=4, pady=2,
                             command=lambda: self.app.show_screen(TitleScreen))
        self.make_hoverable(back_btn)
        back_btn.place(x=200, y=670, anchor="center")


# Logic for determining zodiac sign based on birthday
class ZodiacLogic:
    @staticmethod
    def determine_sign(day, month):
        # Each zodiac sign has a start and end date (day, month)
        signs = [
            ("Capricorn", (22, 12), (19, 1)),
            ("Aquarius", (20, 1), (18, 2)),
            ("Pisces", (19, 2), (20, 3)),
            ("Aries", (21, 3), (19, 4)),
            ("Taurus", (20, 4), (20, 5)),
            ("Gemini", (21, 5), (20, 6)),
            ("Cancer", (21, 6), (22, 7)),
            ("Leo", (23, 7), (22, 8)),
            ("Virgo", (23, 8), (22, 9)),
            ("Libra", (23, 9), (22, 10)),
            ("Scorpio", (23, 10), (21, 11)),
            ("Sagittarius", (22, 11), (21, 12)),
            ("Capricorn", (22, 12), (31, 12)),  # End of year wraparound
        ]

        # Check if date falls within a zodiac range
        for sign, start, end in signs:
            if ((month == start[1] and day >= start[0]) or
                (month == end[1] and day <= end[0])):
                return sign.lower()
        return None


# Starts the app if the script is run directly
if __name__ == "__main__":
    root = tk.Tk()
    app = ZodiacApp(root)
    root.mainloop()
