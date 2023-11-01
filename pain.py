import ffmpeg
import os
import whisper




#converts a mp4 file to a mp3 and returns the audio portion of mp4, returns filename
def mp4_to_mp3(input_file, *args):

    if(not(input_file.endswith('.mp4'))):
        print('not a mp4 file')
        return 
    
    #checks if we have an output file name and it's format
    match len(args):
        case 0:
            temp = input_file.split('.')[0]
            out_name = temp + '.mp3'
        case 1:
            if(not(args[0].endswith('.mp3'))):
                out_name = args[0] + '.mp3'
            else:
                out_name = args[0]
        case _:
            print("can't have more than one output fill name")

    input = ffmpeg.input(input_file)
    audio = input.audio.filter("aecho", 0.8, 0.9, 1000, 0.3)
    out = ffmpeg.output(input, out_name)
    ffmpeg.run(out)
    return out_name
in_file = ''
model = whisper.load_model("base")
result = model.transcribe(mp4_to_mp3(in_file))

print(result['text'])