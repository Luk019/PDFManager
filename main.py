import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pypdf import PdfMerger, PdfReader, PdfWriter


class PDFManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Manager")
        self.geometry("400x500")

        self.create_widgets()

    def create_widgets(self):
        # Tabs
        self.tabControl = ttk.Notebook(self)

        self.merge_tab = ttk.Frame(self.tabControl)
        self.split_tab = ttk.Frame(self.tabControl)

        self.tabControl.add(self.merge_tab, text='Połącz PDFy')
        self.tabControl.add(self.split_tab, text='Rozdziel PDF')

        self.tabControl.pack(expand=1, fill="both")

        # Merge tab
        self.merge_label = ttk.Label(self.merge_tab, text="Wybierz pliki PDF do połączenia:")
        self.merge_label.pack(pady=10)

        self.merge_listbox = tk.Listbox(self.merge_tab, selectmode=tk.SINGLE)
        self.merge_listbox.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        self.merge_button_frame = ttk.Frame(self.merge_tab)
        self.merge_button_frame.pack(pady=10)

        self.merge_add_button = ttk.Button(self.merge_button_frame, text="Dodaj pliki", command=self.add_files_to_merge)
        self.merge_add_button.grid(row=0, column=0, padx=5)

        self.merge_remove_button = ttk.Button(self.merge_button_frame, text="Usuń wybrane",
                                              command=self.remove_selected_files)
        self.merge_remove_button.grid(row=0, column=1, padx=5)

        self.merge_up_button = ttk.Button(self.merge_button_frame, text="Góra", command=self.move_up)
        self.merge_up_button.grid(row=0, column=2, padx=5)

        self.merge_down_button = ttk.Button(self.merge_button_frame, text="Dół", command=self.move_down)
        self.merge_down_button.grid(row=0, column=3, padx=5)

        self.merge_execute_button = ttk.Button(self.merge_tab, text="Połącz", command=self.merge_pdfs)
        self.merge_execute_button.pack(pady=10)

        # Split tab
        self.split_label = ttk.Label(self.split_tab, text="Wybierz plik PDF do rozdzielenia:")
        self.split_label.pack(pady=10)

        self.split_file_entry = ttk.Entry(self.split_tab, width=40)
        self.split_file_entry.pack(pady=10, padx=20)

        self.split_browse_button = ttk.Button(self.split_tab, text="Wybierz plik", command=self.browse_file_to_split)
        self.split_browse_button.pack(pady=10)

        self.page_range_label = ttk.Label(self.split_tab, text="Podaj zakres stron (np. 1-3 lub 8):")
        self.page_range_label.pack(pady=10)

        self.page_range_entry = ttk.Entry(self.split_tab, width=20)
        self.page_range_entry.pack(pady=10)

        self.save_remainder_var = tk.BooleanVar()
        self.save_remainder_check = ttk.Checkbutton(self.split_tab, text="Zapisz pozostałe strony jako osobny plik",
                                                    variable=self.save_remainder_var)
        self.save_remainder_check.pack(pady=10)

        self.split_execute_button = ttk.Button(self.split_tab, text="Rozdziel", command=self.split_pdf)
        self.split_execute_button.pack(pady=10)

    def add_files_to_merge(self):
        files = filedialog.askopenfilenames(title="Wybierz pliki PDF do połączenia", filetypes=[("PDF files", "*.pdf")])
        for file in files:
            self.merge_listbox.insert(tk.END, file)

    def remove_selected_files(self):
        selected_indices = self.merge_listbox.curselection()
        for index in reversed(selected_indices):
            self.merge_listbox.delete(index)

    def move_up(self):
        selected_indices = self.merge_listbox.curselection()
        for index in selected_indices:
            if index > 0:
                file = self.merge_listbox.get(index)
                self.merge_listbox.delete(index)
                self.merge_listbox.insert(index - 1, file)
                self.merge_listbox.select_set(index - 1)

    def move_down(self):
        selected_indices = self.merge_listbox.curselection()
        for index in selected_indices:
            if index < self.merge_listbox.size() - 1:
                file = self.merge_listbox.get(index)
                self.merge_listbox.delete(index)
                self.merge_listbox.insert(index + 1, file)
                self.merge_listbox.select_set(index + 1)

    def merge_pdfs(self):
        files = self.merge_listbox.get(0, tk.END)
        if not files:
            messagebox.showwarning("Brak plików", "Nie wybrano plików do połączenia.")
            return

        merger = PdfMerger()
        for file in files:
            merger.append(file)

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if output_path:
            merger.write(output_path)
            merger.close()
            messagebox.showinfo("Sukces", "Pliki PDF zostały połączone!")

    def browse_file_to_split(self):
        file = filedialog.askopenfilename(title="Wybierz plik PDF do rozdzielenia", filetypes=[("PDF files", "*.pdf")])
        if file:
            self.split_file_entry.delete(0, tk.END)
            self.split_file_entry.insert(0, file)

    def split_pdf(self):
        file = self.split_file_entry.get()
        page_range = self.page_range_entry.get()

        if not file:
            messagebox.showwarning("Brak pliku", "Nie wybrano pliku do rozdzielenia.")
            return

        if not page_range:
            messagebox.showwarning("Brak zakresu stron", "Nie podano zakresu stron.")
            return

        try:
            if '-' in page_range:
                start_page, end_page = map(int, page_range.split('-'))
                pages = range(start_page - 1, end_page)
            else:
                page = int(page_range)
                pages = [page - 1]
        except ValueError:
            messagebox.showwarning("Błędny zakres", "Podany zakres stron jest niepoprawny.")
            return

        reader = PdfReader(file)
        num_pages = len(reader.pages)

        if any(p < 0 or p >= num_pages for p in pages):
            messagebox.showwarning("Błędny zakres", "Podany zakres stron jest poza zakresem dokumentu.")
            return

        # Write the selected pages to a new PDF
        writer = PdfWriter()
        for i in pages:
            writer.add_page(reader.pages[i])
        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")],
                                                   initialfile="split_document.pdf")
        if output_path:
            with open(output_path, "wb") as output_pdf:
                writer.write(output_pdf)

        # Write the remaining pages to a new PDF if the checkbox is selected
        if self.save_remainder_var.get():
            remainder_writer = PdfWriter()
            for i in range(num_pages):
                if i not in pages:
                    remainder_writer.add_page(reader.pages[i])
            remainder_output_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                                 filetypes=[("PDF files", "*.pdf")],
                                                                 initialfile="remainder_document.pdf")
            if remainder_output_path:
                with open(remainder_output_path, "wb") as remainder_output_pdf:
                    remainder_writer.write(remainder_output_pdf)

        messagebox.showinfo("Sukces", "Plik PDF został rozdzielony!")


if __name__ == "__main__":
    app = PDFManagerApp()
    app.mainloop()
