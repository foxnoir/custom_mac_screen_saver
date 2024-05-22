import subprocess
import os
import sys

def loop_video(input_file, output_file, duration_seconds):
    # Create a temporary file for the looped video
    temp_file = "temp_loop.mp4"
    
    # Calculate the number of loops
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", input_file], capture_output=True, text=True)
    video_duration = float(result.stdout.strip())
    num_loops = int(duration_seconds // video_duration) + 1

    # Loop the video
    with open("concat_list.txt", "w") as f:
        for _ in range(num_loops):
            f.write(f"file '{input_file}'\n")

    subprocess.run([
        "ffmpeg", "-f", "concat", "-safe", "0", "-i", "concat_list.txt",
        "-c", "copy", temp_file
    ])

    # Trim the video to the exact duration
    subprocess.run([
        "ffmpeg", "-i", temp_file, "-t", str(duration_seconds), "-c", "copy", output_file
    ])

    # Remove temporary files
    os.remove(temp_file)
    os.remove("concat_list.txt")

def convert_to_mov(input_file, output_file):
    subprocess.run([
        "ffmpeg", "-i", input_file, "-c:v", "copy", "-c:a", "copy", output_file
    ])

def parse_duration(duration):
    parts = list(map(int, duration.split(":")))
    if len(parts) == 2:
        minutes, seconds = parts
        hours = 0
    elif len(parts) == 3:
        hours, minutes, seconds = parts
    else:
        raise ValueError("Invalid duration format. Use 'hours:minutes:seconds' or 'minutes:seconds'.")
    
    return hours * 3600 + minutes * 60 + seconds

def main(input_file, duration):
    looped_file = "looped_output.mp4"
    final_output_file = "final_output.mov"

    # Convert the time format to seconds
    duration_seconds = parse_duration(duration)

    # Loop the video
    loop_video(input_file, looped_file, duration_seconds)

    # Convert the video to MOV
    convert_to_mov(looped_file, final_output_file)

    # Remove the temporary file
    os.remove(looped_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_video> <duration in hours:minutes:seconds or minutes:seconds>")
        sys.exit(1)

    input_file = sys.argv[1]
    duration = sys.argv[2]
    main(input_file, duration)
