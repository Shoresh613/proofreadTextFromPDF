# proofreadTextFromPDF
Proof reads text that is extracted from PDF files, the path is specified in the PDFpath variable. 
By default the proof reading is done in Swedish. This can be changed in the prompt sent to OpenAI.
You can also change what "Page" is called in your language through the variable page_name.

Initially the idea was to increase the likelyhood of finding what you search for if you have a 
large library of PDF files, where the OCR process has been less than perfect.

Put all PDF files in a folder named PDF, or specify the path in the variable PDFpath.

The temperature is set to 0.1, as that is what is used in the OpenAI example for correcting grammar.

You need an OpenAI API key environment variable. Remember OpenAI charges for the processing.
The cost can be reduced by an order of magnitude by instead using the gpt-3.5-turbo model
and adapting the code accordingly.

Unfortunately the results are dissappointing using the best text completion model (text-davinci-003).