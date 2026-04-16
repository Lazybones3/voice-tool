import os
import sys
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

def main():
    if len(sys.argv) != 2:
        print('Usage: python audio.py <input_file>')
        return
    print('[Convert] ' + sys.argv[1])
    video_to_audio(sys.argv[1])


if __name__ == '__main__':
    main()