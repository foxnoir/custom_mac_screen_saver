<a name="readme-top"></a>

<!-- Top Links Bar -->

[![LinkedIn][linkedin-shield]][linkedin-url]
[![Twitter][twitter-shield]][twitter-url]
[![Instagram][instagram-shield]][instagram-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <img src="images/logo.png" alt="Logo" width="80" height="80">
  <h1 align="center">Custom Mac Screen Saver</h1>
  </div>

<!-- PROJECT desc -->
  <p align="left">
Here you will find instructions on how to save your own video as a screensaver on your Mac under Sonoma and a Python script that converts an mp4 into a mov file and loops the video at a time of your choice.



# preperation

  1. go to/Library/Application Support/com.apple.idleassetsd/Customer/4KSDR240FPS
  2. parallel open screen saver in systemsettings and download whatever video
  3. find an mp4 you want as your screensaver

Your own video must be EXACTLY the length of the downloaded video. The script here converts an mp4 into a mov video and lets it run in the loop for a very specific time.
Follow the instructions below.


  
## Video Loop and Convert Script

This script takes an input MP4 video, loops it to a specified duration, and converts the final output to MOV format. The duration can be specified in the format of "hours:minutes:seconds" or "minutes:seconds".

### Requirements

- Python 3.x
- `ffmpeg` and `ffprobe`



#### run scrip examples

```sh
python3 loop_and_convert.py input_video.mp4 33:02  # for 33 minutes and 2 seconds
python3 loop_and_convert.py input_video.mp4 1:33:02  # for 1 hour, 33 minutes, and 2 seconds
```



