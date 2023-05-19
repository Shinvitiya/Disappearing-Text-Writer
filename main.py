from google.cloud import texttospeech
from google.oauth2 import service_account
import os
import PyPDF2


client_file = "key.json"  # Your Google Cloud credentails json file
credentials = service_account.Credentials.from_service_account_file(client_file)

client = texttospeech.TextToSpeechClient(credentials=credentials)

# Setting up Google Text-To-Speech API
voice = texttospeech.VoiceSelectionParams(language_code="en-US",
                                           name="en-US-Standard-C",
                                           ssml_gender=texttospeech.SsmlVoiceGender.FEMALE, )  # Set voice settings

audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)


for file in os.listdir("PDFs"):
    # Open and read pdf files
    with open(f"PDFs/{file}", 'rb') as book:
        reader = PyPDF2.PdfReader(book)
        num_pages = len(reader.pages)
    # --------------------------------------------------------------------------------------------#

    # Loop through the pages and extract the text in them into a single variable
        text = ''
        for page_number in range(num_pages):
            page = reader.pages[page_number]
            text += page.extract_text()

    # Get the file name of the Pdf file without the extension
    path = os.path.basename(file)
    file_name = os.path.splitext(path)[0]
    # --------------------------------------------------------------------------------------------#

    # Set text to turn into speech
    input_text = texttospeech.SynthesisInput(text=text)
    response = client.synthesize_speech(input=input_text,
                                        voice=voice,
                                        audio_config=audio_config)

    # --------------------------------------------------------------------------------------------#

    # Create Audiobook
    with open(f"AudioBooks/{file_name}.mp3", "wb") as audiobook:
        audiobook.write(response.audio_content)
        print(f"{file_name} audiobook hass been successfully created")
    # --------------------------------------------------------------------------------------------#


