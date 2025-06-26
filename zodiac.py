import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# Main application controller
class ZodiacApp:
    def __init__(self, root):
        self.root = root  # Main window
        self.root.title("Zodiac Horoscope")
        self.root.geometry("400x700")  # Fixed window size
        self.root.resizable(False, False)  # Prevent resizing

        self._day = 1  # Default day
        self._month = 1  # Start with January
        self.current_screen = None  # Initially no screen is shown

        # Start with the title screen
        self.show_screen(TitleScreen)

    # Replaces current screen with a new one
    def show_screen(self, screen_class, **kwargs):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = screen_class(self, self.root, **kwargs)  # Create new screen instance
        self.current_screen.pack(fill="both", expand=True)  # Expand to fill available space

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


# Base class for all screens (inherits from CTkFrame for custom methods and styles)
class ZodiacFrame(ctk.CTkFrame):
    def __init__(self, app, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.app = app  # Main app instance

    # Load and display a background image
    def load_background(self, path):
        img = Image.open(path).resize((400, 700))  # Resize for fixed window
        self.bg_image = ImageTk.PhotoImage(img)  # Convert to Tk-compatible image
        self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Fill frame


# Title screen
class TitleScreen(ZodiacFrame):
    def __init__(self, app, root):
        super().__init__(app, root)
        self.load_background("Title_screen.png")

        font_style = ("Lucida Calligraphy", 16, "bold")

        # Tarot button (top)
        tarot_btn = ctk.CTkButton(self,
                                  text="Tarot",
                                  font=font_style,
                                  width=200,
                                  height=45,
                                  fg_color="#2d1e45",
                                  hover_color="#4a326f",
                                  command=lambda: self.app.show_screen(TarotScreen))
        tarot_btn.place(x=100, y=540)

        # Zodiac check button (below)
        zodiac_btn = ctk.CTkButton(self,
                                   text="Check Your Sign",
                                   font=font_style,
                                   width=200,
                                   height=45,
                                   fg_color="#2d1e45",
                                   hover_color="#4a326f",
                                   command=lambda: self.app.show_screen(BirthdayScreen))
        zodiac_btn.place(x=100, y=595)


# Birthday input screen
class BirthdayScreen(ZodiacFrame):
    def __init__(self, app, root):
        super().__init__(app, root)
        self.load_background("day.png")

        self.day_var = ctk.StringVar(value="1")
        self.month_var = ctk.StringVar(value="January")

        font_style = ("Lucida Calligraphy", 14)

        # Day dropdown menu
        day_dd = ctk.CTkComboBox(self,
                                 variable=self.day_var,
                                 values=[str(i) for i in range(1, 32)],
                                 width=60,
                                 font=font_style,
                                 dropdown_font=font_style,
                                 fg_color="#2d1e45",
                                 border_color="#4a326f",
                                 button_color="#392759",
                                 text_color="white")
        day_dd.place(x=76, y=270)

        # Month dropdown menu
        months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        month_dd = ctk.CTkComboBox(self,
                                   variable=self.month_var,
                                   values=months,
                                   width=120,
                                   font=font_style,
                                   dropdown_font=font_style,
                                   fg_color="#2d1e45",
                                   border_color="#4a326f",
                                   button_color="#392759",
                                   text_color="white")
        month_dd.place(x=259, y=270)

        # Submit button to find zodiac sign
        submit_btn = ctk.CTkButton(self,
                                   text="Find Your Sign",
                                   font=("Lucida Calligraphy", 16, "bold"),
                                   width=220,
                                   height=45,
                                   fg_color="#2d1e45",
                                   hover_color="#4a326f",
                                   command=self.submit)
        submit_btn.place(x=90, y=595)

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


# Zodiac result screen
class ResultScreen(ZodiacFrame):
    def __init__(self, app, root, sign):
        super().__init__(app, root)

        try:
            self.load_background(f"{sign}.png")
        except FileNotFoundError:
            messagebox.showerror("Missing Image", f"{sign}.png not found.")
            self.app.show_screen(TitleScreen)
            return

        # Back button to return to title screen
        back_btn = ctk.CTkButton(self,
                                 text="Back",
                                 font=("Lucida Calligraphy", 12),
                                 width=65,
                                 height=24,
                                 fg_color="#2d1e45",
                                 hover_color="#4a326f",
                                 command=lambda: self.app.show_screen(TitleScreen))
        back_btn.place(x=160, y=660)


# Tarot screen showing a random image
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
        back_btn = ctk.CTkButton(self,
                                 text="Back",
                                 font=("Lucida Calligraphy", 12),
                                 width=65,
                                 height=24,
                                 fg_color="#2d1e45",
                                 hover_color="#4a326f",
                                 command=lambda: self.app.show_screen(TitleScreen))
        back_btn.place(x=160, y=660)


# Logic to determine zodiac sign based on birthday
class ZodiacLogic:
    @staticmethod
    def determine_sign(day, month):
        # Each zodiac sign has a start and end date (day, month)
        signs = [
            ("Capricorn", (1, 1), (19, 1)),
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
            ("Capricorn", (22, 12), (31, 12))  # End of year wraparound
        ]

        # Check if date falls within a zodiac range
        for sign, start, end in signs:
            if ((day >= start[0] and month == start[1]) or
                (day <= end[0] and month == end[1])):
                return sign.lower()
        return None


# Run the app
if __name__ == "__main__":
    root = ctk.CTk()  # Create main window
    app = ZodiacApp(root)
    root.mainloop()
