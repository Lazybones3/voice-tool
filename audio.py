import argparse
import os
import re
import ffmpeg
import logging


def video_to_audio(input_file: str, prefix: str):
    stream = ffmpeg.input(input_file)
    filename = os.path.basename(input_file)
    try:
        pos = filename.rindex('.')
        output_file = f'./out/{prefix + filename[0:pos]}.mp3'
        stream = ffmpeg.output(stream, output_file)
        ffmpeg.run(stream)
    except ValueError:
        logging.error("filename error: " + filename)

def is_video(filename: str):
    pattern = r'.*\.(mp4|avi|flv|mov|mkv)$'
    return re.match(pattern, filename, flags=re.IGNORECASE)

def load_dir(input_dir: str, prefix: str):
    for dirpath, _, filenames in os.walk(input_dir):
        logging.info(f"Current directory: {dirpath}")
        for filename in filenames:
            if is_video(filename):
                full_filename = os.path.join(dirpath, filename)
                video_to_audio(full_filename, prefix)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir', help='Input directory')
    parser.add_argument('--prefix', help='filename prefix')
    args = parser.parse_args()
    load_dir(args.input_dir, args.prefix)


if __name__ == '__main__':
    main()
