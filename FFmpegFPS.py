import os
import subprocess
from tkinter import Tk, filedialog


def get_video_fps(file_path):
    """
    Get the current FPS of a video using FFmpeg (ffprobe).
    """
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=r_frame_rate",
                "-of", "default=noprint_wrappers=1:nokey=1",
                file_path,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        # Parse FPS (e.g., "30000/1001" to 29.97)
        fps_parts = result.stdout.strip().split('/')
        if len(fps_parts) == 2:
            return round(int(fps_parts[0]) / int(fps_parts[1]), 2)
        return float(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to retrieve FPS: {e.stderr}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")


def convert_mp4_to_mkv(input_path, output_path=None):
    """
    Convert an MP4 file to MKV format without re-encoding (lossless conversion).
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"The file '{input_path}' does not exist.")

    if output_path is None:
        base_filename = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(os.path.dirname(input_path), f"{base_filename}.mkv")

    ffmpeg_command = [
        "ffmpeg",
        "-i", input_path,
        "-c", "copy",
        "-y",
        output_path
    ]

    subprocess.run(ffmpeg_command, check=True)
    return output_path


def adjust_framerate_with_mkvmerge(input_path, output_path, new_fps):
    """
    Adjust the framerate of an MKV file using mkvmerge.
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"The file '{input_path}' does not exist.")

    mkvmerge_command = [
        "mkvmerge",
        "--default-duration", f"0:{new_fps}fps",  # Set the framerate
        "-o", output_path,
        input_path
    ]

    subprocess.run(mkvmerge_command, check=True)
    return output_path


def convert_mkv_to_mp4(input_path, output_path=None):
    """
    Convert an MKV file back to MP4 format without re-encoding (lossless conversion).
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"The file '{input_path}' does not exist.")

    if output_path is None:
        base_filename = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(os.path.dirname(input_path), f"{base_filename}_converted.mp4")

    ffmpeg_command = [
        "ffmpeg",
        "-i", input_path,
        "-c", "copy",
        "-y",
        output_path
    ]

    subprocess.run(ffmpeg_command, check=True)
    return output_path


def main():
    # Use a file selector to load the MP4 file
    Tk().withdraw()  # Hide the root window
    input_mp4 = filedialog.askopenfilename(
        title="Select MP4 File",
        filetypes=[("MP4 files", "*.mp4")]
    )

    if not input_mp4:
        print("No file selected. Exiting.")
        return

    print(f"Selected file: {input_mp4}")

    # Step 1: Get and display the current FPS
    try:
        current_fps = get_video_fps(input_mp4)
        print(f"Current FPS of the selected video: {current_fps}")
    except RuntimeError as e:
        print(f"Error retrieving FPS: {e}")
        return

    # Step 2: Request new FPS from the user
    try:
        new_fps = float(input(f"Enter the new framerate (e.g., 30.0). Current FPS is {current_fps}: ").strip())
    except ValueError:
        print("Invalid FPS value. Exiting.")
        return

    # Step 3: Convert MP4 to MKV
    print("Converting MP4 to MKV...")
    try:
        mkv_path = convert_mp4_to_mkv(input_mp4)
        print(f"Converted to MKV: {mkv_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during MP4 to MKV conversion: {e.stderr}")
        return

    # Step 4: Adjust framerate using mkvmerge
    adjusted_mkv_path = os.path.splitext(mkv_path)[0] + f"_{int(new_fps)}fps.mkv"
    print("Adjusting framerate with mkvmerge...")
    try:
        adjust_framerate_with_mkvmerge(mkv_path, adjusted_mkv_path, new_fps)
        print(f"Framerate adjusted: {adjusted_mkv_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during framerate adjustment: {e.stderr}")
        return

    # Step 5: Convert MKV back to MP4
    final_mp4_path = os.path.splitext(adjusted_mkv_path)[0] + ".mp4"
    print("Converting MKV back to MP4...")
    try:
        convert_mkv_to_mp4(adjusted_mkv_path, final_mp4_path)
        print(f"Final MP4 saved: {final_mp4_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during MKV to MP4 conversion: {e.stderr}")
        return

    # Step 6: Cleanup intermediate MKV files
    try:
        print("Deleting intermediate MKV files...")
        os.remove(mkv_path)
        os.remove(adjusted_mkv_path)
        print("Intermediate MKV files deleted.")
    except Exception as e:
        print(f"Error during cleanup: {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
