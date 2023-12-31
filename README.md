### BatchFFfileFramesOneMP4.py
## RMS Utils tool to concatenated (merge) two or more FFfiles into one .mp4 video.
This tool can be used in the RMS enviroment in the case a meteor of fireball event is captured in two or more FFfiles. This script is largely based on a other RMS/Utils tool: `GenerateMP4s.py` BatchFFfileFramesOneMP4.py does not need the FTPdetect file, the .config file or platepar file. It only needs to get pointed to the directory where the two or more 'event_FFfiles' are stored. 

Each FFfile in a directory will be coverted into a set of 256 frames-->

Each set of frames will be converted into a .mp4 video-->

All mp4's will be concatenated (merged) into one .mp4 video.

#### Notes:
This script is running best when `only` FFfiles which should be merged into one .mp4 are stored in a seperate folder!

When RMS is running via Anaconda on Windows make sure ffmpeg is installed. If not, install with:
````
conda install -c conda-forge ffmpeg
````

## Usage:
RMS should be installed on your system to run this script. See: https://github.com/CroatianMeteorNetwork/RMS

When RMS is installed on your system, check the directory `~/source/RMS/Utils`. 

If the script BatchFFfileFramesOneMP4.py is not there, copy-paste it into this Utils directory.

Next; Copy-paste the desired FFfiles into a folder somewhere on your system and remember the location. 
Now you are ready to run the script by:

1. make sure vRMS is activated:
````
source vRMS/bin/activate
````
2. change into the RMS directory:

````
cd ~/source/RMS
````
3. Run the script BatchFFfileFRamesOneMP4 and show the available options with: (note: do not add .py at the end of the script-name!)

````
python -m Utils.BatchFFfileFramesOneMP4 -h
````
4. You will see some explanation about how to use the script. In this case you only need to add the folder path of the folder containing the 'event_FFfiles' like:

````
python -m Utils.BatchFFfileFramesOneMP4 /path/to/your/folder/with/event_FFfiles
````
When the script is done you will find in your 'event_FFfiles' folder a .mp4 of each FFfile and the `Merged_event_FFfileFrames.mp4` file. You could rename this file to suit your needs.
