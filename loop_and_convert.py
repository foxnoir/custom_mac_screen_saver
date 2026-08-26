#!/usr/bin/env python3
"""Loop an input video to a target duration and write a single MOV file."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

HEADROOM_BYTES = 3 * 1024 * 1024 * 1024
MIN_HEVC_VIDEO_BITRATE = 3_000_000
DEFAULT_OUTPUT = "final_output.mov"


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(f"Error: {name} is not installed or not on PATH.")


def parse_duration(duration: str) -> int:
    parts = duration.split(":")
    if not parts or any(not part.isdigit() for part in parts):
        raise ValueError(
            "Invalid duration format. Use 'hours:minutes:seconds' or 'minutes:seconds'."
        )

    values = [int(part) for part in parts]
    if len(values) == 2:
        hours, minutes, seconds = 0, values[0], values[1]
    elif len(values) == 3:
        hours, minutes, seconds = values
    else:
        raise ValueError(
            "Invalid duration format. Use 'hours:minutes:seconds' or 'minutes:seconds'."
        )

    if minutes >= 60 or seconds >= 60:
        raise ValueError("Minutes and seconds must be between 0 and 59.")

    return hours * 3600 + minutes * 60 + seconds


def format_bytes(num_bytes: float) -> str:
    value = float(num_bytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{value:.1f} TB"


def format_clock(seconds: int) -> str:
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def probe_media(input_file: str) -> tuple[float, int, int]:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration,bit_rate",
            "-show_entries",
            "stream=codec_type,bit_rate",
            "-of",
            "json",
            input_file,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(f"Error: could not read '{input_file}'.\n{result.stderr}")

    data = json.loads(result.stdout)
    duration = float(data["format"]["duration"])
    format_bitrate = int(data["format"].get("bit_rate") or 0)
    audio_bitrate = 0
    video_bitrate = 0
    for stream in data.get("streams", []):
        bitrate = int(stream.get("bit_rate") or 0)
        if stream.get("codec_type") == "audio":
            audio_bitrate = bitrate
        elif stream.get("codec_type") == "video":
            video_bitrate = bitrate

    if duration <= 0:
        raise SystemExit(f"Error: '{input_file}' has no readable duration.")

    total_bitrate = format_bitrate or (video_bitrate + audio_bitrate)
    if total_bitrate <= 0:
        raise SystemExit(f"Error: '{input_file}' has no readable bitrate.")

    return duration, total_bitrate, audio_bitrate


def run_ffmpeg(args: list[str]) -> None:
    print("Running:", " ".join(args), flush=True)
    completed = subprocess.run(args)
    if completed.returncode != 0:
        raise SystemExit(f"ffmpeg failed with exit code {completed.returncode}")


def choose_encode(
    duration_seconds: int,
    copy_bitrate: int,
    audio_bitrate: int,
    free_bytes: int,
) -> tuple[str, list[str]]:
    copy_bytes = int(copy_bitrate * duration_seconds / 8)
    usable_bytes = free_bytes - HEADROOM_BYTES

    if copy_bytes <= usable_bytes:
        print(
            f"Estimated output size: {format_bytes(copy_bytes)} "
            f"(free: {format_bytes(free_bytes)}). Using stream copy."
        )
        return "copy", ["-c", "copy"]

    print(
        f"Stream copy would need about {format_bytes(copy_bytes)}, "
        f"but only {format_bytes(free_bytes)} is free."
    )

    if usable_bytes <= 0:
        raise SystemExit(
            f"Error: not enough disk space. Free at least "
            f"{format_bytes(copy_bytes + HEADROOM_BYTES)} and try again."
        )

    max_total_bitrate = int(usable_bytes * 8 / duration_seconds)
    video_bitrate = max_total_bitrate - audio_bitrate
    if video_bitrate < MIN_HEVC_VIDEO_BITRATE:
        needed = int((MIN_HEVC_VIDEO_BITRATE + audio_bitrate) * duration_seconds / 8)
        raise SystemExit(
            "Error: not enough disk space for a 4K encode. "
            f"Need about {format_bytes(needed + HEADROOM_BYTES)} free, "
            f"have {format_bytes(free_bytes)}."
        )

    print(
        f"Encoding HEVC at {video_bitrate / 1_000_000:.1f} Mbps so the "
        f"file fits in the remaining space."
    )
    return "hevc", [
        "-c:v",
        "hevc_videotoolbox",
        "-allow_sw",
        "1",
        "-b:v",
        str(video_bitrate),
        "-tag:v",
        "hvc1",
        "-c:a",
        "copy",
    ]


def loop_and_convert(input_file: str, duration: str, output_file: str) -> None:
    require_tool("ffmpeg")
    require_tool("ffprobe")

    source = Path(input_file)
    if not source.is_file():
        raise SystemExit(f"Error: input file '{input_file}' was not found.")

    duration_seconds = parse_duration(duration)
    if duration_seconds <= 0:
        raise SystemExit("Error: duration must be greater than 0.")

    _source_duration, copy_bitrate, audio_bitrate = probe_media(input_file)
    output_path = Path(output_file)
    free_bytes = shutil.disk_usage(output_path.parent or Path(".")).free
    _mode, encode_args = choose_encode(
        duration_seconds, copy_bitrate, audio_bitrate, free_bytes
    )

    if output_path.exists():
        output_path.unlink()

    try:
        run_ffmpeg(
            [
                "ffmpeg",
                "-y",
                "-nostdin",
                "-hide_banner",
                "-loglevel",
                "error",
                "-stats",
                "-fflags",
                "+genpts",
                "-stream_loop",
                "-1",
                "-i",
                input_file,
                "-t",
                str(duration_seconds),
                *encode_args,
                str(output_path),
            ]
        )
    except BaseException:
        if output_path.exists():
            output_path.unlink()
            print(f"Removed incomplete file '{output_path}'.", flush=True)
        raise

    size = output_path.stat().st_size
    print(
        f"Done. Wrote {output_path} ({format_bytes(size)}, "
        f"{format_clock(duration_seconds)})."
    )


def main() -> None:
    if len(sys.argv) not in (3, 4):
        print(
            "Usage: python3 loop_and_convert.py <input_video> "
            "<duration> [output.mov]"
        )
        print("Duration: hours:minutes:seconds or minutes:seconds")
        print("Example: python3 loop_and_convert.py input_video.mp4 4:00:00")
        sys.exit(1)

    input_file = sys.argv[1]
    duration = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) == 4 else DEFAULT_OUTPUT

    try:
        loop_and_convert(input_file, duration, output_file)
    except ValueError as error:
        raise SystemExit(f"Error: {error}") from error


if __name__ == "__main__":
    main()
