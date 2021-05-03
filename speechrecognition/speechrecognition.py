'''
APIs
recognize_bing(): Microsoft Bing Speech - https://azure.microsoft.com/en-us/services/cognitive-services/speech-services/
recognize_google(): Google Web Speech API (50 requests per day) - https://wicg.github.io/speech-api/
recognize_google_cloud(): Google Cloud Speech - https://cloud.google.com/speech-to-text
recognize_houndify(): Houndify by SoundHound - https://www.houndify.com/
recognize_ibm(): IBM Speech to Text - https://www.ibm.com/cloud/watson-speech-to-text
recognize_sphinx(): CMU Sphinx - requires installing PocketSphinx - https://cmusphinx.github.io/
recognize_wit(): Wit.ai - https://wit.ai/
Of the seven, only recognize_sphinx() works offline with the CMU Sphinx engine. The other six all require an internet connection.
'''
#Install PyAudio package to access the microphone

import speech_recognition as sr

'''
   // Voice Recognition (Speech-to-Text) - Google Speech Recognition API
   -> This API converts spoken text (microphone) into written text (Python strings)
   -> Personal or testing purposes only
   -> Generic key is given by default (it may be revoked by Google at any time)
   -> If using API key, quota for your own key is 50 requests per day
'''

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.
    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)         #  analyze the audio source for 1 second
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    # update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio, language = 'en-IN')        #Detect Indian English (For Hindi code : hi-IN)
        #For other language codes check these : https://stackoverflow.com/questions/14257598/what-are-language-codes-in-chromes-implementation-of-the-html5-speech-recogniti
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable/unresponsive"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

def recognize_speech_from_audio(recognizer, filename):
    ''' SpeechRecognition supports the following file formats:
    WAV: must be in PCM/LPCM format
    AIFF
    AIFF-C
    FLAC: must be native FLAC format; OGG-FLAC is not supported'''

    audio_file = filename + '.wav'
    file = sr.AudioFile(audio_file)
    with file as source:
        recognizer.adjust_for_ambient_noise(source, duration = 0.5)         #  analyze the audio source for 0.5 second
        audio = recognizer.record(source, duration = 5)     #convert text of first 5 seconds of audio

    recognizer.recognize_google(audio)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio, language = 'en-US')
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable/unresponsive"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

if __name__ == "__main__":
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=1)
    response = recognize_speech_from_mic(recognizer, mic)
    print('\nSuccess : {}\nError   : {}\n\nText from Mic\n{}\n\n{}' \
    .format(response['success'], response['error'], '-'*17, response['transcription']))

    filename = input('Enter the filename without the extension : ')
    response = recognize_speech_from_audio(recognizer, filename)
    print('\nSuccess : {}\nError   : {}\n\nText from Audio File\n{}\n\n{}' \
    .format(response['success'], response['error'], '-'*17, response['transcription']))
