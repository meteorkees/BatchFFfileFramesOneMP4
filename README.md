# BatchFFfileFramesOneMP4
## RMS Utils tool to concatenated two or more FFfile into one MP4.
This tool can be used in the RMS enviroment in the case a meteor of fireball event is captured in two or more FFfiles. This script is largely based on a other RMS/Utils tool: `GenerateMP4s.py` BatchFFfileFramesOneMP4.py does not need the FTPdetect file, the .config file or platepar file. It only needs to get pointed to the directory where the two or more 'event FFfiles' are stored. 

Each FFfile in a directory will be coverted into a set of 256 frames-->

Each set of frames will be converted into a mp4-->

All mp4's will be concatenated into one mp4.
