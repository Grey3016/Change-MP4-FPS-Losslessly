This is a python based convertor - 

Requirements (to be in same folder)
FFMpeg (from FFMpeg package)
FFProbe (from FFMpeg package)
MKVMerge (from MKVToolNix package)

For some reason, the code will not listen to Windows Paths settings for FFMpeg.

The way to losslessly convert the FPS of an existing MP4 file (which is how this code works) is to firstly (losslessly) convert it to MKV format. The FPS is then amended (to your input FPS) and the MKV file is finally converted back to MP4 (losslessly again) . After the conversion, the intermediate MKV files are deleted, with the new MP4 filename being appended with its new framerate.

MKV files are just containers. 


Code made by ChatGPT via several prompts 

1.Basic code made and tested with FFMpeg

2.Added current FPS output to window (FFProbe)

3.Added MP4 selection via file selector

4.Amended code in load as MP4 (FFMpeg), convert to MKV (with MKVMerge) and convert back to MP4 (FFMpeg)

python code to make a file loader to load an mp4 and request a new fps setting and change the fps with ffmpeg command line parameters

python code to convert an mp4 to mkv losslessly

python code to convert an mp4 to mkv losslessly, then use mkvmerge to adjust its framerate losslessly to a new framerate that is requested of the user, then finally reconvert the mkv back to an mp4

adjust the previous code to include it showing the initial fps of the mp4 file and loading the mp4 with a file selector

5.Amended code to delete intermediate MKV files



 
