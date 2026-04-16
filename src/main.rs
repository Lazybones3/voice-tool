use std::{path::{Path, PathBuf}, process::Command};
use clap::Parser;
use walkdir::WalkDir;

fn video_to_audio(input_file: &Path) {
    let mut output_file = input_file.to_path_buf();
    output_file.set_extension("mp3");

    let command = Command::new("ffmpeg")
        .arg("-i")
        .arg(input_file)
        .arg(output_file.clone())
        .output()
        .expect("failed to execute process");

    if command.status.success() {
        println!("Success output: {:?}", output_file);
    } else {
        let err = String::from_utf8_lossy(&command.stderr);
        eprintln!("Convert error: {}", err);
    }
}

#[derive(Parser)]
struct Cli {
    #[arg(short, long, value_name = "DIR")]
    directory: PathBuf,
}

fn main() {
    let args = Cli::parse();

    if args.directory.is_dir() {
        for entry in WalkDir::new(args.directory).into_iter().filter_map(|e| e.ok()) {
            let path = entry.path();
            if path.is_file() {
                if path.extension().map_or(false, |ext| ext == "mp4") {
                    println!("Convert Video: {}", path.display());
                    video_to_audio(path);
                }
            }
        }
    } else {
        eprintln!("Error: {:?} is not a directory", args.directory);
    }
}
