import uvicorn
import whisper
import os
import time
from fastapi import FastAPI, HTTPException
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter

async def download_audio(url:str, download_path:str):

    try:
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()
        vid_title = yt.title
        file_name = vid_title + '.mp3'
        audio.download(output_path=download_path, filename=file_name)
    
    except KeyError:
        raise HTTPException(status_code=400, detail="Error: audio souce not avaliable or cannot be download")
    except ValueError:
        raise HTTPException(status_code=400, detail="Error: invalide URL")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error downloading video: " + str(e))
    

async def download_captions(url:str, download_path:str):
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
        raise HTTPException(status_code=400, detail="Error: video not avaliable or cannot be download")
    except ValueError:
        raise HTTPException(status_code=400, detail="Error: invalide URL")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error extracting transcript from: " + str(e))
    

async def transcribe_audio(file_name:str, file_path:str):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(file_name)
    except FileNotFoundError:
        print("%s file was not found ", file_name)

app = FastAPI()

@app.get("/download")

async def download_data():
    audio_dir_name = 'audio'
    cap_dir_name = 'captions'
    current_dir = os.getcwd()
    audio_dir_path = os.path.join(current_dir, audio_dir_name)
    cap_dir_path = os.path.join(current_dir, cap_dir_name)

    if(not(os.path.exists(audio_dir_path))):
        os.makedirs(audio_dir_path)
    if(not(os.path.exists(cap_dir_path))):
        os.makedirs(cap_dir_path)

    link = 'https://www.youtube.com/watch?v=bNKdlnoAqIs&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=27'

    start_time = time.time()
    await download_audio(link, audio_dir_path)
    await download_captions(link, cap_dir_path)

    print("--- %s seconds ---" % (time.time() - start_time))

# def main():
#     start_time = time.time()
#     link = 'https://www.youtube.com/watch?v=Du-RQu4soIs&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=61'
#     src = YouTube(link)
#     audio = src.streams.filter(only_audio=True).first()
#     file_name = 'test1.mp3'
#     output = audio.download(output_path=dir_path, filename=file_name)

#     file_path = os.path.join(dir_path, file_name )

#     model = whisper.load_model("base")
#     result = model.transcribe(file_path)

#     print(result["text"])

#     print("--- %s seconds ---" % (time.time() - start_time))
