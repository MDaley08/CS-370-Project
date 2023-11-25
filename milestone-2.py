import whisper
import os
import ffmpeg
from flask import Flask
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter

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

def sep_audio(video:str, save_path): #seperates audio from video file
    try:
        input = ffmpeg.input(video)
        audio = input.audio.filter("anull")
    except FileNotFoundError:
        print("%s file couldn't be accessed"%video)
    
    temp = video.split('/')[-1] #gets last element if a file path
    file_name = temp.split('.')[0] + '.mp3'
    file_path = os.path.join(save_path, file_name)
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
        print("%s file was not found ", input_file)

    try:
        file_name = input_file.split('/')[-1]
        file_name = file_name.split('.')[0]
        file_path = os.path.join(output_path, file_name)
        with open(file_path, 'w', encoding='utf-8') as out_file:
            out_file.write(result["text"])

    except FileNotFoundError:
        print("%s this dir can't be accessed ", output_path)
        

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


    transcribe_audio(sep_audio(in_file,audio_dir_path),whisper_dir_path) 

    return 200, "audio has been transcribed successfully"

if __name__ == "__main__":
    app.run(debug=True)