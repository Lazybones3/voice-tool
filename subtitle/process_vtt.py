#!/usr/bin/env python3
"""
Processes a VTT subtitle file following the merge-broken-subtitle skill rules.
"""

import re
import argparse
from pathlib import Path

def read_vtt(file_path):
    """Read a VTT file and parse it into blocks."""
    path = Path(file_path)
    lines = path.read_text().splitlines()
    
    blocks = []
    current_block = {}
    in_cue = False
    cue_text = []
    
    # Skip the first line ("WEBVTT")
    for line in lines[1:]:
        line = line.strip()
        if not line:
            if in_cue and cue_text:
                current_block['text'] = cue_text
                blocks.append(current_block)
                current_block = {}
                cue_text = []
                in_cue = False
        elif re.match(r'^\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}$', line) or re.match(r'^\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}\.\d{3}$', line):
            in_cue = True
            current_block['timestamp'] = line
        else:
            if in_cue:
                cue_text.append(line.strip())
    
    # Add the last block
    if in_cue and cue_text:
        current_block['text'] = cue_text
        blocks.append(current_block)
    
    return blocks

def write_vtt(merged, output_path):
    """Write merged blocks to VTT file."""
    lines = ["WEBVTT", ""]
    for block in merged:
        lines.append(f"{block['start']} --> {block['end']}")
        lines.append(block['text'])
        lines.append("")
    Path(output_path).write_text('\n'.join(lines))

def merge_blocks(blocks, is_one_line):
    """Merge subtitle blocks into sentences."""
    merged = []
    current_sentence = []
    current_start = None
    closing_symbols = ['.', '!', '?', ',', ']']
    separator = ' ' if is_one_line else '\n'
    
    for block in blocks:
        # Extract start and end times
        timestamp = block['timestamp']
        start_time, end_time = timestamp.split(' --> ')
        
        # Join the text from this block
        text = ' '.join(block['text'])
        
        if not current_sentence:
            current_start = start_time
        
        current_sentence.append(text)
        
        # Check if this text ends with a closing symbol
        has_closing = any(text.strip().endswith(s) for s in closing_symbols)
        
        if has_closing:
            # Merge the current sentence
            full_text = separator.join(current_sentence)
            
            # Remove trailing spaces and ensure only one closing symbol
            # Clean up the text
            cleaned = full_text.strip()
            
            merged.append({
                'start': current_start,
                'end': end_time,
                'text': cleaned
            })
            current_sentence = []
            current_start = None
    
    # Handle remaining sentences that don't end with a closing symbol
    if current_sentence:
        full_text = separator.join(current_sentence)
        cleaned = full_text.strip()
        # Add a period if no closing symbol
        if not any(cleaned.endswith(s) for s in closing_symbols):
            cleaned += '.'

        # Get last end time
        last_block = blocks[-1]
        _, end_time = last_block['timestamp'].split(' --> ')
        merged.append({
            'start': current_start,
            'end': end_time,
            'text': cleaned
        })
    
    return merged

def main():
    parser = argparse.ArgumentParser(prog='MergeBrokenSubtitles')
    parser.add_argument('directory', type=str, help='Directory containing VTT files')
    parser.add_argument(
        '--one-line',
        action='store_true',
        help='Merge multiple lines of subtitles into one line'
    )
    args = parser.parse_args()
    data_dir = Path(args.directory)
    for input_file in data_dir.glob("*.vtt"):
        output_file = Path("./output") / f"{input_file.stem}.vtt"
        blocks = read_vtt(input_file)
        merged = merge_blocks(blocks, args.one_line)
        write_vtt(merged, output_file)
        print(f"Merged subtitles saved to {output_file}")

if __name__ == "__main__":
    main()
