
# Corrects text extracted from PDF files in Swedish. The PDF is typically an OCR of scanned paper.
# Put all PDF files in a folder named PDF.
# You need an OpenAI API key environment variable. Remember OpenAI charges for the processing.

# importing required modules
from PyPDF2 import PdfReader
import os
import openai
import re
import textwrap
import sys

PDFpath='./PDF/' #Path to the PDF files to process
openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key == None:
    print("You need to set the 'OPENAI_API_KEY' environment variable")
    sys.exit()

max_width = 7777 #To fit nicely within the 2000 token limit of the OpenAI API
page_name = "Sida" #Translate to what "Page" is called in your language
total_pages=0
total_files=0

def chunk_text(text:str, max_width:int) -> list[str]:
    """
    Wrap text into paragraphs of a given width without breaking lines within words.
    
    Args:
        text (str): The text to be wrapped.
        max_width (int): The maximum width of each line.
        
    Returns:
        list[str]: A list of strings where each string is a paragraph.
    """
    wrapped_text = textwrap.fill(text, width=max_width)
    # Split wrapped text into chunks of a given size
    chunks = textwrap.wrap(wrapped_text, width=max_width)
    return chunks

def proofread_page(text:str, page:int, pages:int, file:str) -> str:
    """
    Send text to OpenAI for proofreading and return result.
    
    Args:
        text (str): The text to be proofread.
        page (int): The current page number.
        pages (int): The total number of pages.
        file (str): The name of the file being processed.
        
    Returns:
        str: The proofread text.
    """
    print(f"Page {page} of {pages} in {file} being processed by OpenAI")
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=("Korrigera stavfel på svenska utan att lägga till någonting varken före eller efter. " 
                "Texten kommer från OCR, så ta hänsyn till grammatiken och sammanhanget "
                "för att lista ut vad det kan tänkas stå:\n\n")+extracted_text,
        temperature=0.1,
        max_tokens=2000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )
    return response.choices[0].text

def clean_up_text(extracted_text:str) -> str:
    """
    Clean up text by removing clutter and if some PDF isn't interpreted correctly.
    
    Args:
        extracted_text (str): The text to be cleaned up.
        
    Returns:
        str: The cleaned up text.
    """
    #Clean it up a bit, removing clutter and if some PDF isn't interpreted correctly
    pattern = r"([^a-zA-Z0-9.])(\\1)+" # matches any non letter or digit character except "." that is repeated
    replacement = "" # replaces the match with an empty string
    return re.sub (pattern, replacement, extracted_text) # performs the substitution

for filename in os.listdir(PDFpath):
    if filename.endswith('.pdf'):
        total_files += 1
        extracted_text =""
        reader = PdfReader(PDFpath+filename)
        # number of pages in pdf file for debug purpose
        pages=len(reader.pages)

        corrected_text = ""
        original_text = "" #For comparison and testing purposes
        
        # getting a specific page from the pdf file and extracting text from page, loop through all pages
        for i, page in enumerate(reader.pages, 1):
            extracted_text = page.extract_text()
            total_pages+=1
            if extracted_text is not None:
                print(f"** Text prior to processing, page {i} of {pages} in {filename}: **\n\n{extracted_text}")
                original_text += extracted_text

                #Clean it up a bit
                extracted_text = clean_up_text(extracted_text)

                #Split the text in chunks of 7777 characters, roughly 2000 tokens, which is the OpenAI API limit              
                chunks = chunk_text(extracted_text, max_width)
                
                #Process the chunks one by one
                for chunk in chunks:
                    page_name_written=0
                    corrected_page_text = proofread_page(chunk, i, pages, filename)
                    if (chunk==chunks[0] and page_name_written==0):
                        corrected_text += f"- {page_name} {i} -\n\n"
                        page_name_written=1
                    corrected_text += f"{corrected_page_text}\n\n"
                print(f"\n** Corrected text: ** \n\n{corrected_page_text}\n\n")
      
        with open(PDFpath+filename+'_original.txt', 'w', encoding="utf-8") as f:            
            f.write(original_text)
        
        with open(PDFpath+filename+'_corrected.txt', 'w', encoding="utf-8") as f:            
            f.write(corrected_text)

if total_files > 0:
    print(f"Finished processing {total_pages} pages in {total_files} files!")
else:
    print("No PDF files in specified directory.")