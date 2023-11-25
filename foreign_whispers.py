import whisper
import os
import ffmpeg
import textwrap 
from flask import Flask
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter
from deep_translator import GoogleTranslator


'''
    to run api paste " uvicorn milestone-2:app " in terminal
'''

def download_audio(url:str, download_path:str):

    try:
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()
        vid_title = yt.title
        file_name = vid_title + '.mp3'
        audio.download(output_path=download_path, filename=file_name)
    
    except KeyError:
        return 400, "Error: audio souce not avaliable or cannot be download"
    except ValueError:
        return 400, "Error: invalide URL"
    except Exception as e:
        return 400, "Error downloading video: " + str(e)
    
    return os.path.join(download_path, file_name)
    

def download_captions(url:str, download_path:str):

    formatter = SRTFormatter()

    try:
        yt = YouTube(url)
        vid_id = url.split("v=")[1]
        caption = YouTubeTranscriptApi.get_transcript(vid_id)
        srt_formatted = formatter.format_transcript(caption)
        file_name = yt.title + '.srt'
        file_path = os.path.join(download_path, file_name)
        with open(file_path, 'w', encoding='utf-8') as srt_file:
            srt_file.write(srt_formatted)
    except KeyError:
        return 400, "Error: video not avaliable or cannot be download"
    except ValueError:
        return 400, "Error: invalide URL"
    except Exception as e:
        400, "Error extracting transcript from: " + str(e)

    srt_file.close()

def sep_audio(video:str, output_path): #seperates audio from video file

    try:
        input = ffmpeg.input(video)
        audio = input.audio.filter("anull")
    except FileNotFoundError:
        print("%s file couldn't be accessed"%video)
    
    temp = video.split('/')[-1] #gets last element if a file path
    file_name = temp.split('.')[0] + '.mp3'
    file_path = os.path.join(output_path, file_name)

    try:
        output = ffmpeg.output(audio, file_path)
        output.run()
        return file_path
    except:
        print("error creating audio file")


def transcribe_audio(input_file:str, output_path:str): #eventually add a check for if file is mp3
    try:
        model = whisper.load_model("base")
        result = model.transcribe(input_file)
    except FileNotFoundError:
        print("%s file was not found " % input_file)

    try:
        file_name = input_file.split('/')[-1]
        file_name = file_name.split('.')[0]
        file_path = os.path.join(output_path, file_name) + ".txt"
        with open(file_path, 'w', encoding='utf-8') as out_file:
            wrapped_text = textwrap.fill(result["text"], width=100)
            out_file.write(wrapped_text)

    except FileNotFoundError:
        print("%s this dir can't be accessed " % output_path)
    
    out_file.close()
    return(file_path)

def translate_text(input_file:str, output_path:str, lang: str):

    translator = GoogleTranslator(source= 'english', target=lang)

    try: #try to open our caption file
        in_file = open(input_file, 'r', encoding="utf8") #opening file to read
    except FileNotFoundError:
        print("%s file was not found " % input_file)

    try: #try to create a new file to store translation
        out_file_name = (input_file.split('/')[-1]).split('.')[0] + ' translation.txt' # we do a split incase file is abs path then take old name
        out_file_path = os.path.join(output_path, out_file_name)
        out_file = open(out_file_path, 'w', encoding='utf8')
    except FileNotFoundError:
        print("%s this dir can't be accessed " % output_path)
        
    for i in in_file.readlines(): #reading all files in the 'captions' directory
        translated_line = translator.translate(i)
        out_file.write(translated_line+'\n')

    print('%s has be sucessfully translate' % input_file)
    in_file.close()
    out_file.close()

        

app = Flask(__name__)


@app.route("/")

def main():
    audio_dir_name = 'audio'
    video_dir_name = 'videos'
    whisper_dir_name = 'whisper_transcripts'
    current_dir = os.getcwd()
    audio_dir_path = os.path.join(current_dir, audio_dir_name)
    video_dir_path = os.path.join(current_dir, video_dir_name)
    whisper_dir_path = os.path.join(current_dir, whisper_dir_name)

    if(not(os.path.exists(audio_dir_path))):
        os.makedirs(audio_dir_path)
    if(not(os.path.exists(whisper_dir_path))):
        os.makedirs(whisper_dir_path)
    

    files = os.listdir(video_dir_path) # accessing all files in audio dir
    in_file = os.path.join(video_dir_path, files[0]) #grabs first file in the directory 


    translate_text(transcribe_audio(sep_audio(in_file,audio_dir_path),whisper_dir_path),current_dir,'german')

    return 200, "audio has been transcribed successfully"

if __name__ == "__main__":
    app.run(debug=True)