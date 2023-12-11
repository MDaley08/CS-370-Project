import whisper
import os
import ffmpeg
import textwrap 
from flask import Flask
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter
from deep_translator import MyMemoryTranslator
from deep_translator import GoogleTranslator
from gtts import gTTS
import gtts.lang

def download_video(url:str, download_path:str):

    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        vid_title = yt.title
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

    translator = MyMemoryTranslator(source= 'english', target=lang)

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

    print('%s has be sucessfully translated' % input_file)
    in_file.close()
    out_file.close()

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

def get_captions(url:str):

    formatter = SRTFormatter()

    try:
        yt = YouTube(url)
        vid_id = url.split("v=")[1]
        caption = YouTubeTranscriptApi.get_transcript(vid_id)
        return caption
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

def translate_line(input_str: str, lang: str):

    translator = GoogleTranslator(source= 'english', target=lang)
    translated_line = translator.translate(input_str)

    return translated_line

### FRONT END ###
import streamlit as st
import streamlit_scrollable_textbox as stx
from transformers import pipeline

text = st.text_area('Enter a YouTube video url! (shorts not allowed)')
submit = st.button('Generate')  
if submit:
    video_file = open(download_video(text,os.getcwd()), 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)
    captions = get_captions(text)
    
    col1, col2, col3 = st.columns(3)
    col1.header("Original")
    col2.header("Translated")
    col3.header("Timestamp")


    caption_string = ""
    translated_string = ""

    bar = st.progress(0, text='Translating text...')
    # for i in range(len(captions)): #prints captions
    #     caption_line = captions[i]["text"]
    #     translated_line = translate_line(captions[i]["text"], 'de')

    #     caption_string += caption_line
    #     translated_string += translated_line

    #     percent = i / len(captions)
    #     bar.progress(percent, text='Translating text... '+str(i)+' out of '+str(len(captions))+ " lines")

    #     col1.write(captions[i]["text"], use_column_width=True) #original
    #     col2.write(translated_line, use_column_width=True) #translated
    #     col3.write(captions[i]["start"], use_column_width=True) #timestamps

    bar.progress(100, text='Done! '+str(len(captions))+' out of '+str(len(captions))+ " lines")
