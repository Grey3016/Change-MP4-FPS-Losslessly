This is a python based convertor - 

Requirements (to be in same folder)
FFMpeg (from FFMpeg package)
FFProbe (from FFMpeg package)
MKVMerge (from MKVToolNix package)

For some reason, the code will not listen to Windows Paths settings for FFMpeg.

The way to losslessly convert the FPS of an existing MP4 file (which is how this code works) is to firstly (losslessly) convert it to MKV format. The FPS is then amended (to your input FPS) and the MKV file is finally converted back to MP4 (losslessly again) . After the conversion, the intermediate MKV files are deleted, with the new MP4 filename being appended with its new framerate.

MKV files are just containers. 
