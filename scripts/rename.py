import argparse
import os

def rename_file(input_dir: str, prefix: str):
    filenames = os.listdir(input_dir)
    for filename in filenames:
        print(filename)
        old_name = os.path.join(input_dir, filename)
        new_name = os.path.join(input_dir, prefix + filename)
        os.rename(old_name, new_name)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir', help='Input directory')
    parser.add_argument('--prefix', help='filename prefix')
    args = parser.parse_args()
    rename_file(args.input_dir, args.prefix)


if __name__ == '__main__':
    main()