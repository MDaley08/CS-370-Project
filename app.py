import os
import ffmpeg
import textwrap 
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter
import whisper
from whisper.utils import get_writer
from deep_translator import MyMemoryTranslator
from gtts import gTTS
import gtts.lang

def download_video(url:str, download_path:str):

    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        vid_title = yt.title
        vid_title = vid_title.replace(" ", '_')
        file_name = vid_title + '.mp4'
        video.download(output_path=download_path, filename=file_name)
    
    except KeyError:
       print("Error: video not avaliable or cannot be download")
    except ValueError:
        print("Error: invalid URL")
    except Exception as e:
        print("Error downloading video: %s" % e)
    
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
        print("Error: video not avaliable or cannot be download")
    except ValueError:
        print("Error: invalid URL")
    except Exception as e:
        print("Error extracting transcript from: %s" % e)

    srt_file.close()

def sep_audio(video:str, output_path): #seperates audio from video file

    try:
        input = ffmpeg.input(video).audio
    except FileNotFoundError:
        print("%s file couldn't be accessed"%video)
    
    temp = video.split('/')[-1] #gets last element if a file path
    file_name = temp.split('.')[0] + '.mp3'
    file_path = os.path.join(output_path, file_name)

    try:
        output = ffmpeg.output(input, file_path)
        output.run()
        return file_path
    except:
        print("error creating audio file")

def sep_video(video:str, output_path): #seperates audio from video file

    try:
        input = ffmpeg.input(video).video
    except FileNotFoundError:
        print("%s file couldn't be accessed"%video)
    
    temp = video.split('/')[-1] #gets last element if a file path
    file_name = temp.split('.')[0] + ' vid' + '.mp4'
    file_path = os.path.join(output_path, file_name)

    try:
        output = ffmpeg.output(input, file_path)
        output.run()
        return file_path
    except:
        print("error creating video file")

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
        srt_path = os.path.join(output_path, file_name) + ".srt"

        srt_writer = get_writer("srt", output_path)
        srt_writer(result, input_file)
        with open(file_path, 'w', encoding='utf-8') as out_file:
            wrapped_text = textwrap.fill(result["text"], width=100)
            out_file.write(wrapped_text)

    except FileNotFoundError:
        print("%s this dir can't be accessed " % output_path)
    
    out_file.close()
    return file_path, srt_path

def translate_text(input_file:str, output_path:str, lang: str):

    translator = MyMemoryTranslator(source= 'english', target=lang)

    try: #try to open our caption file
        in_file = open(input_file, 'r', encoding="utf8") #opening file to read
    except FileNotFoundError:
        print("%s file was not found " % input_file)

    try: #try to create a new file to store translation
        out_file_name = (input_file.split('/')[-1]).split('.')[0] + ' translation.' + input_file.split('.')[-1] # we do a split incase file is abs path then take old name
        out_file_path = os.path.join(output_path, out_file_name)
        out_file = open(out_file_path, 'w', encoding='utf8')
    except FileNotFoundError:
        print("%s this dir can't be accessed " % output_path)
        
    for i in in_file.readlines(): #reading all files in the 'captions' directory
        translated_line = translator.translate(i)
        out_file.write(translated_line+'\n')

    print('%s has be sucessfully translated' % input_file)
    in_file.close()
    out_file.close()
    return out_file_path

def text_to_speech(input_file:str, output_path:str):
    try:
        in_file = open(input_file,'r',encoding="utf8")

    except FileNotFoundError:
        print("%s file was not found \n" % input_file)
    
    out_file_name = (input_file.split('/')[-1]).split('.')[0] + '.mp3'
    out_file_path = os.path.join(output_path, out_file_name)

    in_text = ""
    language = 'de'

    for i in in_file.readlines():
        in_text += i

    output = gTTS(text= in_text, lang= language)
    output.save(out_file_path)
    return out_file_path

def main():
    import streamlit as st
    import streamlit_scrollable_textbox as stx
    from transformers import pipeline
    working_dir = os.getcwd()
    final_video_name = 'final_vid.mp4'
    final_video_path = os.path.join(working_dir,final_video_name)

    ### FRONT END ###
    text = st.text_area('Enter a YouTube video url! (shorts not allowed)')
    submit = st.button('Generate')

    if submit:
        #downloading video, splitting stream, operating on, recombining
        in_video = download_video(text,working_dir)
        audio = sep_audio(in_video,working_dir)
        video = sep_video(in_video,working_dir)
        audio_to_text = transcribe_audio(audio, working_dir)
        trans_text = translate_text(audio_to_text[0],working_dir, 'german')
        trans_caps = translate_text(audio_to_text[1],working_dir, 'german')
        video_stream = ffmpeg.input(video) .filter("subtitles", str(trans_caps))
        audio_stream = ffmpeg.input(text_to_speech(trans_text, working_dir))
        final_video = ffmpeg.output(audio_stream,video_stream,final_video_path)
        final_video.run()
        #opening our video file and displaying on site
        video_file = open(final_video_path, 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)

main()