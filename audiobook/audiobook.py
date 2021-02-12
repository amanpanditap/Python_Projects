# Python code to read out a pdf / audiobook module
# run the install code in Terminal first
import pyttsx3   # install pip pyttsx3
import PyPDF2    # install pip pyPDF2
book = open('book.pdf', 'rb')    # put the pdf name instead of 'A_Christmas_Carol_NT.pdf'
pdfReader = PyPDF2.PdfFileReader(book)
pages = pdfReader.numPages
print(pages)
speaker = pyttsx3.init()
for page_num in range(pages):
    page = pdfReader.getPage(page_num)   # put page no instead of 3
    voices = speaker.getProperty('voices')
    speaker.setProperty('voice', voices[0].id)  # put 0 or 1 to change voice 0:male 1:female
    speaker.setProperty('rate', 180)  # put the letters per minute rate in place og 150
    speaker.say(page.extractText())
    speaker.runAndWait()
speaker.stop()
