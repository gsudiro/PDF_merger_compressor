import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import subprocess
import threading
import os
import sys

def merge_pdfs(pdf_list, output_path):
    pdf_merger = PyPDF2.PdfMerger()
    for pdf in pdf_list:
        with open(pdf, 'rb') as f:
            pdf_merger.append(f)
    with open(output_path, 'wb') as output_file:
        pdf_merger.write(output_file)
    print(f"Merged {len(pdf_list)} PDFs into {output_path}")

def compress_pdf_with_ghostscript(input_pdf, output_pdf, quality='screen'):
    # Construct the path to the bundled Ghostscript binary (for PyInstaller)
    if getattr(sys, 'frozen', False):  # Check if running as a PyInstaller bundle
        gs_executable = os.path.join(sys._MEIPASS, 'gs', 'gswin64c.exe')
    else:
        gs_executable = 'gswin64c'  # Use system Ghostscript if not bundled

    gs_command = [
        gs_executable, '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
        f'-dPDFSETTINGS=/{quality}', '-dNOPAUSE', '-dQUIET', '-dBATCH',
        f'-sOutputFile={output_pdf}', input_pdf
    ]
    
    # Execute Ghostscript and handle errors
    result = subprocess.run(gs_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Ghostscript Error: {result.stderr.decode()}")
        messagebox.showerror("Error", "Ghostscript failed to compress the PDF.")
    else:
        print(f"Compressed PDF saved to {output_pdf}")

def merge_and_compress_pdfs():
    # Get the selected PDF files from the user
    pdf_files = filedialog.askopenfilenames(title="Select PDF files", filetypes=[("PDF Files", "*.pdf")])
    
    if not pdf_files:
        return

    # Define paths for merged and compressed PDFs
    merged_pdf = os.path.join(os.getenv('TEMP'), 'merged_output.pdf')
    compressed_pdf = os.path.join(os.getenv('TEMP'), 'compressed_output.pdf')

    # Create a thread to handle PDF processing
    thread = threading.Thread(target=process_pdfs, args=(pdf_files, merged_pdf, compressed_pdf))
    thread.start()

def process_pdfs(pdf_files, merged_pdf, compressed_pdf):
    # Merge PDFs
    merge_pdfs(pdf_files, merged_pdf)
    
    # Compress the merged PDF
    compress_pdf_with_ghostscript(merged_pdf, compressed_pdf, quality='ebook')

    # Notify the user that the process is complete
    messagebox.showinfo("Success", f"Merged and compressed PDFs into:\n\n{merged_pdf}\n{compressed_pdf}")

# Set up the main application window
root = tk.Tk()
root.title("PDF Merger and Compressor")
root.geometry("300x150")

# Create and place a button to trigger PDF merging and compression
merge_button = tk.Button(root, text="Select PDFs and Merge", command=merge_and_compress_pdfs)
merge_button.pack(expand=True)

# Start the Tkinter main loop
root.mainloop()