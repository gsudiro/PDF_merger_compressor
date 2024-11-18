# PDF Merger and Compressor

## Overview
This Python application provides a user-friendly graphical interface for merging multiple PDF files into a single document and compressing the resulting PDF to reduce file size. Built with `tkinter` for the GUI and `PyPDF2` for PDF operations, the program allows users to easily select their PDF files and perform the merging and compression in a responsive manner using multithreading.

## Features
- **Select Multiple PDFs**: Easily choose multiple PDF files from your local filesystem.
- **Merge PDFs**: Combine selected PDFs into one merged PDF document.
- **Compress Output**: Generate a compressed version of the merged PDF using Ghostscript.
- **Cross-Platform**: Works on Windows, Linux, and macOS (with Ghostscript installed).

## Requirements
- Python 3.x
- `PyPDF2`: For PDF merging functionalities.
- Ghostscript: Required for PDF compression (must be installed separately).
- `tkinter`: Included with standard Python installations for creating the GUI.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pdf-merger-compressor.git
2. Create the virtual environemnt folder
   ```bash
   python3 -m venv .venv
4. Activate the environment ('deactivate' to exit)
   ```bash
   source .venv/Scripts/activate 
5. Install the required libraries
   ```bash
   pip install -r requirements.txt
6. Run the application using:
   ```bash 
   python pdfMerger.py