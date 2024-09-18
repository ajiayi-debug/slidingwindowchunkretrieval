import fitz
import os
from gpt import *
from tqdm import tqdm
import shutil

#delete directory after processing
def delete_folder(folder_path):
    """
    Deletes the specified folder and all of its contents.
    
    Parameters:
        folder_path (str): The path to the folder to delete.
    """
    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)
            print(f"Successfully deleted folder: {folder_path}")
        except Exception as e:
            print(f"Error deleting folder {folder_path}: {e}")
    else:
        print(f"Folder does not exist: {folder_path}")

# Function to convert PDF to text
def pdf_to_text(pdf_path, txt_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    text = ""
    
    # Iterate through the pages
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        text += page.get_text()

    # Save the extracted text to a .txt file
    with open(txt_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(text)

    print(f"Text extracted and saved to {txt_path}")

def process_pdfs_in_directory(pdf_directory, output_directory):
    """
    Convert all PDF files in a specified directory to text files.

    Args:
    - pdf_directory (str): The directory containing PDF files.
    - output_directory (str): The directory where the extracted text files will be saved.

    """
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Iterate through all files in the pdf_directory
    for filename in tqdm(os.listdir(pdf_directory), desc='Converting pdf files to .txt files and renaming them to their actual names'):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, filename)
            txt_filename = os.path.splitext(filename)[0] + ".txt"  # Create a .txt filename
            txt_path = os.path.join(output_directory, txt_filename)

            # Extract text from the PDF
            pdf_to_text(pdf_path, txt_path)

            # Generate a new filename using the naming function
            new_txt_filename = generate_new_filename(txt_path)
            new_pdf_path=os.path.join(pdf_directory, new_txt_filename)

            # Rename the .pdf file to the new name
            os.rename(pdf_path, new_pdf_path)
            print(f"Renamed {pdf_path} to {new_pdf_path}")
    delete_folder(output_directory)




def generate_new_filename(txt_path):
    """
    Generate a new filename for the .txt file based on its content using GPT.

    Args:
    - txt_path (str): The path of the .txt file.

    Returns:
    - str: A new filename for the .txt file.
    """
    # Read the content of the text file
    with open(txt_path, "r", encoding="utf-8") as txt_file:
        text_content = txt_file.read()

    # Use the naming function to determine the new filename
    new_filename = naming(text_content).strip()

    # Make sure the new filename is valid and append the .txt extension and .pdf extension in original directory
    new_filename = "".join(c for c in new_filename if c.isalnum() or c in (' ', '_')).rstrip()
    return new_filename + ".pdf"  # Limit length to 50 characters

#to send df to excel
def send_excel(df,directory, filename):
    # os.makedirs(directory)
    output_path=os.path.join(directory,filename)
    df.to_excel(output_path, index=False)
    print(f'Data has been written to {output_path}')

