import re
from typing import List, Tuple
import soundfile as sf
import numpy as np
import numpy.typing as npt
from faster_qwen3_tts import FasterQwen3TTS


ref_audio = "IELTS_sample.wav"
ref_text  = "IELTS 20 published by Cambridge University Press and Assessment 2025. This recording is copyright. Test 1. This is the IELTS listening test. You will hear a number of different recordings and you will have to answer questions on what you hear. There will be time for you to read the instructions and questions, and you will have a chance to check your work. All the recordings will be played once only. The test is in four parts. At the end of the test, you will be given ten minutes to transfer your answers to an answer sheet."


def process_text(text: str) -> str:
    if text.startswith('#'):
        text = text.lstrip('#')
    elif text.startswith('>'):
        text = text.lstrip('>')
    elif text.startswith('-'):
        text = text.lstrip('-')
    return text.strip()


def split_text(text: str) -> List[str]:
    # \n\s*\n matches a newline, any optional whitespace, and another newline
    raw_sentences = re.split(r'\n\s*\n', text.strip())
    return [process_text(s) for s in raw_sentences]


def load_file(filename: str) -> List[str]:
    with open(filename, 'r', encoding='utf-8') as f:
        input_text = f.read()
    sentences = split_text(input_text)
    print(f"Total sentences to process: {len(sentences)}")
    return sentences


def generate_voice(sentences: List[str]) -> Tuple[List[npt.NDArray], int | None]:
    model = FasterQwen3TTS.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-Base")

    audio_chunks = []
    sampling_rate = None

    for i, sentence in enumerate(sentences, start=1):
        print(f"Processing ({i}/{len(sentences)}): {sentence}")

        wavs, sr = model.generate_voice_clone(
            text=sentence,
            language="English",
            ref_audio=ref_audio,
            ref_text=ref_text,
        )

        if sampling_rate is None:
            sampling_rate = sr

        # Ensure the audio chunk is a flat 1D array
        audio_chunk = wavs[0] if isinstance(wavs, list) else wavs.flatten()

        # Create a 1-second silence array using the model's sampling rate
        # np.zeros(sr) creates exactly 1 second of absolute silence
        silence = np.zeros(int(sampling_rate), dtype=audio_chunk.dtype)

        audio_chunks.append(silence)
        audio_chunks.append(audio_chunk)
    return audio_chunks, sampling_rate


def save_audio(audio_chunks: List[npt.NDArray], sampling_rate: int, output_filename: str = "output_voice_clone.wav"):
    final_audio = np.concatenate(audio_chunks, axis=0)

    sf.write(output_filename, final_audio, sampling_rate)
    print(f"Successfully saved consolidated audio to: {output_filename}")


if __name__ == '__main__':
    sentence_list = load_file("demo.txt")
    audio_chunks, sampling_rate = generate_voice(sentence_list)
    if sampling_rate:
        save_audio(audio_chunks, sampling_rate)
