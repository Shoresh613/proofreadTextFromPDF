# proofreadTextFromPDF
Proof reads text that is extracted from PDF files, the path is specified in the path variable. 
By default the proof reading is done in Swedish. This can be changed in the prompt sent to OpenAI.
You can also change what "Page" is called in your language through the variable page_name.

Initially the idea was to increase the likelyhood of finding what you search for if you have a 
large library of PDF files, where the OCR process has been less than perfect.

Put all PDF files in a folder named PDF, or specify the path in the variable PDFpath.

You need an OpenAI API key environment variable. Remember OpenAI charges for the processing.

Unfortunately the results are dissappointing using GPT3 (text-davinci-003).

The temperature is set to 0.1, as that is what is used in the OpenAI example for correcting grammar.