import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import PyPDF2
import subprocess
import threading
import os
import sys
import datetime

class PDFProcessor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF Merger and Compressor")
        self.root.geometry("500x400")
        
        # Store selected files and output directory
        self.selected_files = []
        self.output_dir = os.path.expanduser("~\\Documents")
        
        self.create_gui()

    def create_gui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Step 1: File Selection Section
        step1_frame = ttk.LabelFrame(main_frame, text="Step 1: Select PDF Files", padding="5")
        step1_frame.pack(fill=tk.X, pady=5)

        button_frame = ttk.Frame(step1_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Select PDFs", command=self.select_pdfs).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Selection", command=self.clear_selection).pack(side=tk.LEFT, padx=5)

        # Selected files listbox
        self.files_listbox = tk.Listbox(step1_frame, height=6)
        self.files_listbox.pack(fill=tk.BOTH, expand=True, pady=5)

        # Step 2: Output Settings Section
        step2_frame = ttk.LabelFrame(main_frame, text="Step 2: Configure Output", padding="5")
        step2_frame.pack(fill=tk.X, pady=5)

        ttk.Button(step2_frame, text="Set Output Folder", command=self.select_output_dir).pack(anchor=tk.W, padx=5, pady=2)
        self.output_label = ttk.Label(step2_frame, text=f"Output Directory: {self.output_dir}")
        self.output_label.pack(anchor=tk.W, padx=5, pady=2)

        # Quality selection
        quality_frame = ttk.Frame(step2_frame)
        quality_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(quality_frame, text="Compression Quality:").pack(side=tk.LEFT, padx=5)
        self.quality_var = tk.StringVar(value="ebook")
        quality_combo = ttk.Combobox(quality_frame, textvariable=self.quality_var, 
                                   values=["screen", "ebook", "printer", "prepress"],
                                   state="readonly", width=10)
        quality_combo.pack(side=tk.LEFT, padx=5)

        # Step 3: Start Processing Section
        step3_frame = ttk.LabelFrame(main_frame, text="Step 3: Start Processing", padding="5")
        step3_frame.pack(fill=tk.X, pady=5)

        # Big START button
        self.start_button = ttk.Button(step3_frame, text="START", 
                                     command=self.merge_and_compress_pdfs,
                                     style='Start.TButton')
        self.start_button.pack(pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(step3_frame, mode='indeterminate')
        
        # Create custom style for START button
        style = ttk.Style()
        style.configure('Start.TButton', font=('helvetica', 12, 'bold'))

    def select_pdfs(self):
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if files:
            self.selected_files = sorted(files)  # Sort files alphabetically
            self.update_files_listbox()

    def update_files_listbox(self):
        self.files_listbox.delete(0, tk.END)
        for file in self.selected_files:
            self.files_listbox.insert(tk.END, os.path.basename(file))

    def clear_selection(self):
        self.selected_files = []
        self.files_listbox.delete(0, tk.END)

    def select_output_dir(self):
        directory = filedialog.askdirectory(initialdir=self.output_dir)
        if directory:
            self.output_dir = directory
            self.output_label.config(text=f"Output Directory: {self.output_dir}")

    def merge_pdfs(self, pdf_list, output_path):
        pdf_merger = PyPDF2.PdfMerger()
        for pdf in pdf_list:
            with open(pdf, 'rb') as f:
                pdf_merger.append(f)
        with open(output_path, 'wb') as output_file:
            pdf_merger.write(output_file)

    def compress_pdf_with_ghostscript(self, input_pdf, output_pdf):
        if getattr(sys, 'frozen', False):
            gs_executable = os.path.join(sys._MEIPASS, 'gs', 'gswin64c.exe')
        else:
            gs_executable = 'gswin64c'

        gs_command = [
            gs_executable, '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
            f'-dPDFSETTINGS=/{self.quality_var.get()}', '-dNOPAUSE', '-dQUIET', '-dBATCH',
            f'-sOutputFile={output_pdf}', input_pdf
        ]
        
        result = subprocess.run(gs_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise Exception(f"Ghostscript Error: {result.stderr.decode()}")

    def process_pdfs(self):
        try:
            if not self.selected_files:
                raise Exception("No PDF files selected!")

            # Generate output filenames
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            merged_pdf = os.path.join(self.output_dir, f'merged_{timestamp}.pdf')
            compressed_pdf = os.path.join(self.output_dir, f'compressed_{timestamp}.pdf')

            # Merge PDFs
            self.merge_pdfs(self.selected_files, merged_pdf)
            
            # Compress the merged PDF
            self.compress_pdf_with_ghostscript(merged_pdf, compressed_pdf)

            # Clean up merged PDF if compression successful
            if os.path.exists(compressed_pdf):
                os.remove(merged_pdf)
                messagebox.showinfo("Success", 
                    f"PDFs successfully merged and compressed!\nOutput saved to:\n{compressed_pdf}")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.progress.stop()
            self.progress.pack_forget()
            self.start_button.config(state='normal')

    def merge_and_compress_pdfs(self):
        self.start_button.config(state='disabled')
        self.progress.pack(fill=tk.X, pady=5)
        self.progress.start()
        thread = threading.Thread(target=self.process_pdfs)
        thread.start()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PDFProcessor()
    app.run()