#!/usr/bin/env python3
"""
Split an 8-channel WAV file into:
- 4 stereo pairs: (1-2), (3-4), (5-6), (7-8)
- 8 mono tracks (each channel)

Usage example:
    python split_8ch_wav.py input.wav output_dir
"""

import sys
from pathlib import Path

import soundfile as sf
import numpy as np


def split_8ch_wav(
    input_path,
    output_dir,
    *,
    make_stereo_pairs=True,
    make_mono_tracks=True,
    prefix=None,
    subtype=None,
):
    """
    Split an 8-channel WAV into stereo pairs and/or mono stems.

    Args:
        input_path (str or Path): Path to the 8-channel WAV.
        output_dir (str or Path): Directory to write the output files.
        make_stereo_pairs (bool): If True, write 4 stereo WAVs (1-2, 3-4, 5-6, 7-8).
        make_mono_tracks (bool): If True, write 8 mono WAVs.
        prefix (str): Optional prefix for output filenames. Defaults to input stem.
        subtype (str): Optional soundfile subtype (e.g., 'PCM_16'). If None, reuse input.
    """
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load audio as [num_samples, num_channels]
    data, samplerate = sf.read(input_path, always_2d=True)
    num_samples, num_channels = data.shape

    if num_channels != 8:
        raise ValueError(f"Expected 8 channels, got {num_channels}")

    # Keep same sample format unless explicitly overridden
    info = sf.info(input_path)
    if subtype is None:
        subtype = info.subtype

    base = prefix or input_path.stem

    written_files = []

    # ---- 4 stereo pairs: (1-2), (3-4), (5-6), (7-8) ----
    if make_stereo_pairs:
        # Channel indices are 0-based internally, 1-based in filenames
        pairs = [(0, 1), (2, 3), (4, 5), (6, 7)]
        for idx, (ch_l, ch_r) in enumerate(pairs, start=1):
            pair_data = data[:, [ch_l, ch_r]]  # shape: [N, 2]
            out_name = f"{base}_stereo_pair{idx}_ch{ch_l+1}-{ch_r+1}.wav"
            out_path = output_dir / out_name
            sf.write(out_path, pair_data, samplerate, subtype=subtype)
            written_files.append(out_path)

    # ---- 8 mono stems, one per channel ----
    if make_mono_tracks:
        for ch in range(8):
            mono_data = data[:, ch]  # shape: [N]
            out_name = f"{base}_ch{ch+1}_mono.wav"
            out_path = output_dir / out_name
            sf.write(out_path, mono_data, samplerate, subtype=subtype)
            written_files.append(out_path)

    return written_files


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python split_8ch_wav.py <input.wav> <output_dir>")
        sys.exit(1)

    input_wav = sys.argv[1]
    out_dir = sys.argv[2]

    files = split_8ch_wav(
        input_wav,
        out_dir,
        make_stereo_pairs=True,
        make_mono_tracks=True,
    )

    print("Wrote:")
    for f in files:
        print("  ", f)

