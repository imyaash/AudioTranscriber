import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

r = sr.Recognizer()

path = input("Enter the path of the mp3 file to be transcribed:")

# Spliting audio file into chunks & applying speech recognition
def get_large_audio_transcription(path):
    # Opening the audio file using pydub
    sound = AudioSegment.from_mp3(path)
    # Spliting audio where silence is more than 500ms or more and making chunks
    chunks = split_on_silence(sound,
                              min_silence_len = 500,
                              silence_thresh = sound.dBFS-14,
                              keep_silence = 500,
                              )
    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # Processing each chunks
    for i, audio_chunk in enumerate(chunks, start=1):
        # Exporting audio chunks and saving them in folder_name directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format = "wav")
        # Recognising the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # Converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}."
                print(chunk_filename, ":", text)
                whole_text += text
    # Returning the text for all chunks
    return whole_text
print('\nFull text:', get_large_audio_transcription(path))
