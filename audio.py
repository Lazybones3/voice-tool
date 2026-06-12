import os
import sys
import re
import ffmpeg


def video_to_audio(input_file: str):
    stream = ffmpeg.input(input_file)
    filename = os.path.basename(input_file)
    try:
        pos = filename.rindex('.')
        output_file = './out/' + filename[0:pos] + '.mp3'
        stream = ffmpeg.output(stream, output_file)
        ffmpeg.run(stream)
    except ValueError:
        print("filename error: " + filename)
        sys.exit(1)

def is_video(filename: str):
    pattern = r'.*\.(mp4|avi|flv|mov|mkv)$'
    return re.match(pattern, filename, flags=re.IGNORECASE)

def load_dir(input_dir: str):
    for dirpath, _, filenames in os.walk(input_dir):
        print(f"Current directory: {dirpath}")
        for filename in filenames:
            if is_video(filename):
                full_filename = os.path.join(dirpath, filename)
                video_to_audio(full_filename)

def main():
    if len(sys.argv) != 2:
        print('Usage: python audio.py <input_dir>')
        return
    print('[Convert] ' + sys.argv[1])
    load_dir(sys.argv[1])


if __name__ == '__main__':
    main()
