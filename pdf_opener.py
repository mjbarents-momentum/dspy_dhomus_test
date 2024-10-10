import PyPDF2

def check_pdf(file_path):
    # Open the PDF file
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        # Check if the PDF is empty
        num_pages = len(reader.pages)
        
        if num_pages == 0:
            return "PDF is empty."
        
        return f"No issues found. Number of pages: {num_pages}"

if __name__ == "__main__":
    # Specify the path to the PDF file
    pdf_file_path = input("Enter the path to the PDF file: ")
    result = check_pdf(pdf_file_path)
    print(result)
