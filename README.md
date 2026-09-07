<a name="readme-top"></a>

<!-- Top Links Bar -->

[![LinkedIn](assets/badges/linkedin.svg)](https://www.linkedin.com/in/tanja-polz-5636401a5/)
[![X](assets/badges/x.svg)](https://twitter.com/_foxnoir_?lang=de)
[![Instagram](assets/badges/instagram.svg)](https://www.instagram.com/codeincouture/)

<!-- PROJECT LOGO -->
<br />

<div align="center">
  <img src="assets/logo.png" alt="Logo" width="179" height="179">
  <h1 align="center">Custom Mac Screen Saver</h1>
  <p>
     Here you will find instructions on how to save your own video as a screensaver on your Mac under Sonoma and a Python script that converts an mp4 into a mov file and loops the video at a time of your choice.
  </p>
</div>

---

<div align="left">

[![Python](assets/badges/python.svg)](https://www.python.org/)
[![ffmpeg](assets/badges/ffmpeg.svg)](https://ffmpeg.org/)
[![macOS](assets/badges/macos.svg)](https://www.apple.com/macos/)
[![HEVC](assets/badges/hevc.svg)](https://www.itu.int/rec/T-REC-H.265)

</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#preparation">Preparation</a></li>
    <li><a href="#video-loop-and-convert-script">Video Loop and Convert Script</a></li>
    <li><a href="#requirements">Requirements</a></li>
    <li><a href="#run-script-examples">Run script examples</a></li>
    <li><a href="#badges">Badges</a></li>
  </ol>
</details>

---

## Preparation

1. go to/Library/Application Support/com.apple.idleassetsd/Customer/4KSDR240FPS
2. parallel open screen saver in systemsettings and download whatever video
3. find an mp4 you want as your screensaver

Your own video must be EXACTLY the length of the downloaded video. The script here converts an mp4 into a mov video and lets it run in the loop for a very specific time.
Follow the instructions below.

<p align="right"><a href="#readme-top">back to top</a></p>

---

## Video Loop and Convert Script

This script takes an input MP4 video, loops it to a specified duration, and writes a single MOV file (`final_output.mov` by default). The duration can be specified as `hours:minutes:seconds` or `minutes:seconds`.

It loops with ffmpeg in one pass and does not create giant temp copies. If a lossless stream copy would not fit on disk, it encodes HEVC instead.

<p align="right"><a href="#readme-top">back to top</a></p>

---

## Requirements

- Python 3.x
- `ffmpeg` and `ffprobe`

<p align="right"><a href="#readme-top">back to top</a></p>

---

## Run script examples

```sh
python3 loop_and_convert.py input_video.mp4 33:02  # 33 minutes and 2 seconds
python3 loop_and_convert.py input_video.mp4 1:33:02  # 1 hour, 33 minutes, and 2 seconds
python3 loop_and_convert.py input_video.mp4 4:00:00  # 4 hours
python3 loop_and_convert.py input_video.mp4 4:00:00 my_screensaver.mov  # custom output name
```

<p align="right"><a href="#readme-top">back to top</a></p>

---

## Badges

Tech-stack and social badges live once in [`assets/badges/`](assets/badges/). After changing labels or colors:

```
python3 assets/badges/generate.py
```

Target URLs sit **on the badge line** (`[![Python](assets/badges/python.svg)](https://www.python.org/)`). GitHub cannot import another file into a README, so there is no footer of `[python-url]:` refs. The href list is [`assets/badges/links.json`](assets/badges/links.json) when you add a badge.

Every badge is a vertical dark → mid → light gradient (same contrast as Instagram). The mid stop is the brand or playground color. Official colors stay official, except black — it is hard to see. Everything else uses purple, blue, turquoise, pink, or green — not black, orange, red, or yellow.

| File | Color (dark → mid → light) | Why |
| --- | --- | --- |
| `python.svg` | `#1E415E` → `#3776AB` → `#97B8D3` | official Python |
| `ffmpeg.svg` | `#294D3D` → `#4A8C6F` → `#A1C3B4` | green (replaces red) |
| `macos.svg` | `#2A656C` → `#4DB8C4` → `#A2DAE0` | pastel turquoise (replaces black) |
| `hevc.svg` | `#194C4A` → `#2D8A86` → `#92C2C0` | teal |
| `linkedin.svg` | `#06386B` → `#0A66C2` → `#80AFDF` | official LinkedIn |
| `instagram.svg` | `#4C3469` → `#8B5FBF` → `#C3ACDE` | lilac |
| `x.svg` | `#456576` → `#7EB8D6` → `#BCDAEA` | pastel light blue |

<p align="right"><a href="#readme-top">back to top</a></p>
