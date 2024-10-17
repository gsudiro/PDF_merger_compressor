import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import subprocess
import threading

def merge_pdfs(pdf_list, output_path):
    pdf_merger = PyPDF2.PdfMerger()
    for pdf in pdf_list:
        with open(pdf, 'rb') as f:
            pdf_merger.append(f)
    with open(output_path, 'wb') as output_file:
        pdf_merger.write(output_file)
    print(f"Merged {len(pdf_list)} PDFs into {output_path}")

def compress_pdf_with_ghostscript(input_pdf, output_pdf, quality='screen'):
    gs_command = [
        'gswin64c', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
        f'-dPDFSETTINGS=/{quality}',
        '-dNOPAUSE', '-dQUIET', '-dBATCH',
        f'-sOutputFile={output_pdf}', input_pdf
    ]
    subprocess.run(gs_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def merge_and_compress_pdfs():
    # Get the selected PDF files from the entry
    pdf_files = filedialog.askopenfilenames(title="Select PDF files", filetypes=[("PDF Files", "*.pdf")])
    
    if not pdf_files:
        return

    merged_pdf = '../pdfs/merged_output.pdf'
    compressed_pdf = '../pdfs/compressed_output.pdf'

    # Create a thread for merging and compressing PDFs
    thread = threading.Thread(target=process_pdfs, args=(pdf_files, merged_pdf, compressed_pdf))
    thread.start()

def process_pdfs(pdf_files, merged_pdf, compressed_pdf):
    # Merge PDFs
    merge_pdfs(pdf_files, merged_pdf)
    
    # Compress the merged PDF
    compress_pdf_with_ghostscript(merged_pdf, compressed_pdf, quality='ebook')

    # Show completion message
    messagebox.showinfo("Success", f"Merged and compressed PDFs into:\n\n{merged_pdf}\n{compressed_pdf}")

# Set up the main application window
root = tk.Tk()
root.title("PDF Merger and Compressor")
root.geometry("300x150")

# Create and place a merge button
merge_button = tk.Button(root, text="Select PDFs and Merge", command=merge_and_compress_pdfs)
merge_button.pack(expand=True)

# Start the Tkinter main loop
root.mainloop()