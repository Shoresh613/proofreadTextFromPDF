# Corrects text extracted from PDF files in Swedish. The PDF is typically an OCR of scanned paper.
# Put all PDF files in a folder named PDF.
# You need an OpenAI API key environment variable.

# importing required modules
from PyPDF2 import PdfReader
import os
import openai
import re
import textwrap

PDFpath='./'
openai.api_key = os.getenv("OPENAI_API_KEY")
max_width = 7777

def process_text(text, max_width):
    # Wrap text into paragraphs of a given width without breaking lines within words
    wrapped_text = textwrap.fill(text, width=max_width)
    # Split wrapped text into chunks of a given size
    chunks = textwrap.wrap(wrapped_text, width=max_width)
    return chunks

def proofread_page(text):
    #Send to OpenAI for proof reading and return result
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=("Korrigera stavfel på svenska utan att lägga till någonting varken före eller efter. " 
                "Texten kommer från OCR, så ta hänsyn till grammatiken och sammanhanget "
                "för att lista ut vad det kan tänkas stå:\n\n")+extracted_text,
        temperature=0.1,
        max_tokens=2047,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )
    return response.choices[0].text

for filename in os.listdir(PDFpath):
    if filename.endswith('.pdf'):
        extracted_text =""
        reader = PdfReader(PDFpath+filename)
        # printing number of pages in pdf file
        pages=len(reader.pages)
        # getting a specific page from the pdf file and extracting text from page, loop through all pages
        i=0
        corrected_text = ""
        original_text = "" #For comparison and testing purposes
        
        while(i<pages):
            page = reader.pages[i]
            extracted_text = page.extract_text()
            if extracted_text is not None:
                print(extracted_text)
                original_text += extracted_text
                #Clean it up a bit
                pattern = r"([^a-zA-Z0-9.])(\\1)+" # matches any non letter or digit character except "." that is repeated
                replacement = "" # replaces the match with an empty string
                extracted_text = re.sub (pattern, replacement, extracted_text) # performs the substitution

                #Process the text in chunks of 7777 characters, roughly 2000 tokens, which is the OpenAI API limit              
                chunks = process_text(extracted_text, max_width)
                for chunk in chunks:
                    corrected_page_text = proofread_page(chunk)
                    if (chunk==chunks[0]):
                        corrected_text += f"Sida {i+1}\n\n{corrected_page_text}\n\n"
                    else:
                        corrected_text += f"{corrected_page_text}\n\n"
                    
            #    print("Corrected text: "+response.choices[0].text)
            #    corrected_text += 'Sida ' + str(i+1) + "\n\n" + response.choices[0].text + "\n\n"
                i+=1
      
        with open(PDFpath+filename+'_original.txt', 'w', encoding="utf-8") as f:            
            f.write(original_text)
        
        with open(PDFpath+filename+'_corrected.txt', 'w', encoding="utf-8") as f:            
            f.write(corrected_text)

        print("Done!")
