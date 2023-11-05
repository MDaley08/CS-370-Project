import uvicorn
import whisper
import os
from fastapi import FastAPI, HTTPException
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter

def download_audio(url:str, download_path:str):

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
        raise HTTPException(status_code=400, detail="Error: video not avaliable or cannot be download")
    except ValueError:
        raise HTTPException(status_code=400, detail="Error: invalide URL")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error extracting transcript from: " + str(e))
    

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
        

app = FastAPI()

@app.get("/download")

async def main():
    audio_dir_name = 'audio'
    cap_dir_name = 'captions'
    whisper_dir_name = 'whisper_transcripts'
    current_dir = os.getcwd()
    audio_dir_path = os.path.join(current_dir, audio_dir_name)
    cap_dir_path = os.path.join(current_dir, cap_dir_name)
    whisper_dir_path = os.path.join(current_dir, whisper_dir_name)

    if(not(os.path.exists(audio_dir_path))):
        os.makedirs(audio_dir_path)
    if(not(os.path.exists(cap_dir_path))):
        os.makedirs(cap_dir_path)
    if(not(os.path.exists(whisper_dir_path))):
        os.makedirs(whisper_dir_path)

    youtube_links = ['https://www.youtube.com/watch?v=bNKdlnoAqIs&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=27',
                    'https://www.youtube.com/watch?v=RldpC8a9Zv4&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=31',
                    'https://www.youtube.com/watch?v=aDzm9_vthFo&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=32',
                    'https://www.youtube.com/watch?v=6in8fx1Tc38&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=37',
                    'https://www.youtube.com/watch?v=n9adLsXTpZQ&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=63',
                    'https://www.youtube.com/watch?v=_Lx5VmAdZSI&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=54',
                    'https://www.youtube.com/watch?v=EIVTf-C6oQo&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=58',
                    'https://www.youtube.com/watch?v=FwEKCP7DVFc&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=56',
                    'https://www.youtube.com/watch?v=cU3rmlDgfbg&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=60',
                    'https://www.youtube.com/watch?v=Du-RQu4soIs&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=61'
                    ]
    
    for i in range(len(youtube_links)):
        current_link = youtube_links[i]
        download_captions(current_link, cap_dir_path)
        download_audio(current_link, audio_dir_path)

    files = os.listdir(audio_dir_path) # accessing all files in audio dir
    in_file = os.path.join(audio_dir_path, files[0]) #grabs first file in the directory 

    transcribe_audio(in_file,whisper_dir_path) 

