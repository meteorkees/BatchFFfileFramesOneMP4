#!/usr/bin/env python

""" Generate an High Quality MP4 movie from two FF files ore more.
    Based on code from contributor: Tioga Gulon
    Modified by: Kees Habraken
"""

from __future__ import print_function, division, absolute_import

import glob
import os
import platform
import argparse
import subprocess
import shutil
import datetime
import cv2
import time
import Utils.FFtoFrames as f2f

from RMS.Formats import FTPdetectinfo

from PIL import ImageFont

from RMS.Formats.FFfile import read as readFF
from RMS.Formats.FFfile import filenameToDatetime
from RMS.Misc import mkdirP

first_frame = 0
last_frame = 255

def generateMP4s(folder_path):
    t1 = datetime.datetime.utcnow()

    # Load the font for labeling
    try:
        font = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSans.ttf", 18)
    except:
        font = ImageFont.load_default()
    
    print("Preparing files for the timelapse...")
    
    # assign directory
    for filename in os.scandir(folder_path):
        folder_path = os.path.split(filename)
        print('folder_path = ', folder_path[0])
        print('file_name = ', folder_path[1])
        # Open the FF file
        dir_path, file_name = os.path.split(filename)
        ff = readFF(dir_path, file_name)
        ff_name = file_name
        print('ff = ', ff)

        # Skip the file if it could not be read
        if ff is None:
            continue

        # Create temporary directory
        dir_tmp_path = os.path.join(dir_path, "temp_img_dir")

        if os.path.exists(dir_tmp_path):
            shutil.rmtree(dir_tmp_path)
            print("Deleted directory : " + dir_tmp_path)
            
        mkdirP(dir_tmp_path)
        print("Created directory : " + dir_tmp_path)

        # extract the individual frames
        name_time_list = f2f.FFtoFrames(dir_path+'/'+ff_name, dir_tmp_path, 'jpg', -1, first_frame, last_frame)

        # Get id cam from the file name
        # e.g.  FF499_20170626_020520_353_0005120.bin
        # or FF_CA0001_20170626_020520_353_0005120.fits

        file_split = ff_name.split('_')

        # Check the number of list elements, and the new fits format has one more underscore
        i = 0
        if len(file_split[0]) == 2:
            i = 1
        camid = file_split[i]

        font = cv2.FONT_HERSHEY_SIMPLEX

        # add datestamp to each frame
        for img_file_name, timestamp in name_time_list:
            img=cv2.imread(os.path.join(dir_tmp_path, img_file_name))

            # Draw text to image
            text = camid + " " + timestamp.strftime("%Y-%m-%d %H:%M:%S.%f") + " UTC"
            cv2.putText(img, text, (10, ff.nrows - 6), font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

            # Save the labelled image to disk
            cv2.imwrite(os.path.join(dir_tmp_path, img_file_name), img, [cv2.IMWRITE_JPEG_QUALITY, 100])
    
        ffbasename = os.path.splitext(ff_name)[0]
        mp4_path = ffbasename + ".mp4"
        temp_img_path = os.path.join(dir_tmp_path, ffbasename+"_%03d.jpg")

        # If running on Windows, use ffmpeg.exe
        if platform.system() == 'Windows':

            # ffmpeg.exe path
            root = os.path.dirname(__file__)
            ffmpeg_path = os.path.join(root, "ffmpeg.exe")
            # Construct the ecommand for ffmpeg           
            com = ffmpeg_path + " -y -f image2 -pattern_type sequence -start_number " + str(first_frame) + " -i " + temp_img_path +" " + mp4_path
            print("Creating timelapse using ffmpeg...")
        else:
            # If avconv is not found, try using ffmpeg
            software_name = "avconv"
            print("Checking if avconv is available...")
            if os.system(software_name + " --help > /dev/null"):
                software_name = "ffmpeg"
                # Construct the ecommand for ffmpeg           
                com = software_name + " -y -f image2 -pattern_type sequence -start_number " + str(first_frame) + " -i " + temp_img_path +" " + mp4_path
                print("Creating timelapse using ffmpeg...")
            else:
                print("Creating timelapse using avconv...")
                com = "cd " + dir_path + ";" \
                    + software_name + " -v quiet -r 30 -y -start_number " + str(first_frame) + " -i " + temp_img_path \
                    + " -vcodec libx264 -pix_fmt yuv420p -crf 25 -movflags faststart -g 15 -vf \"hqdn3d=4:3:6:4.5,lutyuv=y=gammaval(0.97)\" " \
                    + mp4_path

        #print(com)
        subprocess.call(com, shell=True, cwd=dir_path)
        
        #Delete temporary directory and files inside
        if os.path.exists(dir_tmp_path):
            try:
                shutil.rmtree(dir_tmp_path)
            except:
                # may occasionally fail due to ffmpeg thread still terminating
                # so catch this and wait a bit
                time.sleep(2)
                shutil.rmtree(dir_tmp_path)

            print("Deleted temporary directory : " + dir_tmp_path)

    print("Total time:", datetime.datetime.utcnow() - t1)


        ##############################################################
        

if __name__ == "__main__":

    # COMMAND LINE ARGUMENTS

    # Init the command line arguments parser
    arg_parser = argparse.ArgumentParser(description="Convert all FF files in a folder to MP4s")

    arg_parser.add_argument('folder_path', metavar='FOLDER_PATH', type=str,
        help='Path to directory with FF files.')

    # Parse the command line arguments
    cml_args = arg_parser.parse_args()

    #########################

    folder_path = os.path.normpath(cml_args.folder_path)
   
    generateMP4s(folder_path)
