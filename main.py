import tkinter as tk
from tkinter import messagebox
import locales.en as en
import locales.pl as pl
from pdf_manager import PDFManagerApp
import pkg_resources

class LanguageSelector(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Choose Language")
        self.geometry("300x200")

        self.language = None
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Choose your language:")
        label.pack(pady=10)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        try:
            polish_flag = tk.PhotoImage(file=pkg_resources.resource_filename(__name__, 'images/polish_flag.png')).subsample(20, 20)
            english_flag = tk.PhotoImage(file=pkg_resources.resource_filename(__name__, 'images/english_flag.png')).subsample(20, 20)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load images: {e}")
            self.destroy()
            return

        polish_button = tk.Button(button_frame, image=polish_flag, command=self.select_polish)
        polish_button.image = polish_flag
        polish_button.pack(side=tk.LEFT, padx=10)

        english_button = tk.Button(button_frame, image=english_flag, command=self.select_english)
        english_button.image = english_flag
        english_button.pack(side=tk.LEFT, padx=10)

    def select_polish(self):
        self.language = pl.translations
        self.destroy()
        self.open_main_app()

    def select_english(self):
        self.language = en.translations
        self.destroy()
        self.open_main_app()

    def open_main_app(self):
        app = PDFManagerApp(self.language)
        app.mainloop()

if __name__ == "__main__":
    selector = LanguageSelector()
    selector.mainloop()
