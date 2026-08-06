import os
import sys
import re



def replace_symbol(text: str):
  d = {
    "&nbsp;\n": " ",
    "&amp;" : "&"
  }
  for k, v in d.items():
    text = text.replace(k, v)
  return text

def srt_to_lrc(input_file: str):
    with open(input_file, 'r', encoding='utf8') as f:
        srt = f.read()
        text = re.sub(r"(?P<start>\d+:\d+:\d+.\d+) --> \d+:\d+:\d+.\d+\n", "[\g<start>]", srt)
        text = replace_symbol(text)
    filename = os.path.basename(input_file)
    try:
        pos = filename.rindex('.')
        output_file = './out/' + filename[0:pos] + '.lrc'
        with open(output_file, 'w', encoding='utf8') as f:
            f.write(text)
    except ValueError:
        print("filename error: " + filename)
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print('Usage: python lyric.py <input_file>')
        return
    print('[Convert] ' + sys.argv[1])
    srt_to_lrc(sys.argv[1])


if __name__ == '__main__':
    main()