# Split 8-Channel WAV Files

This tool splits an 8-channel WAV file into either:

* **Four stereo pairs** (1–2, 3–4, 5–6, 7–8)
* **Eight mono stems** (one per channel)

It works well for multitrack exports from hardware recorders, DAWs, or field recorders that store multiple channels in a single WAV.

---

## Features

* Handles **8-channel** interleaved WAV files
* Outputs:

  * **4 stereo WAVs**
  * **8 mono WAVs**
* Preserves input sample format (bit depth / subtype)
* Simple Python script using `soundfile`

---

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

Your `requirements.txt` should include:

```
soundfile
numpy
```

---

## Usage

### Command-line

```bash
python wavsplitter.py input.wav output_directory
```

This will produce:

* `*_stereo_pair1_ch1-2.wav`
* `*_stereo_pair2_ch3-4.wav`
* `*_stereo_pair3_ch5-6.wav`
* `*_stereo_pair4_ch7-8.wav`
* `*_ch1_mono.wav` through `*_ch8_mono.wav`

All files will be written to the directory you provide.

---

## Customization

The script exposes optional arguments inside `split_8ch_wav()`:

```python
split_8ch_wav(
    input_path,
    output_dir,
    make_stereo_pairs=True,
    make_mono_tracks=True,
    prefix=None,
    subtype=None,
)
```

* Set `make_stereo_pairs=False` to skip stereo output.
* Set `make_mono_tracks=False` to skip mono stems.
* `prefix` lets you override the base filename.
* `subtype` lets you force an output format (e.g., `"PCM_16"`).

---

## Example

```bash
python split_8ch_wav.py recordings/session01.wav out/session01/
```

Output:

```
out/session01/session01_stereo_pair1_ch1-2.wav
out/session01/session01_stereo_pair2_ch3-4.wav
out/session01/session01_stereo_pair3_ch5-6.wav
out/session01/session01_stereo_pair4_ch7-8.wav
out/session01/session01_ch1_mono.wav
...
out/session01/session01_ch8_mono.wav
```

---

## Notes

* The input file **must** be 8 channels. The script will raise an error otherwise.
* Works with WAV files readable by `soundfile` (PCM, float, etc.).
* Large multichannel files may use significant memory; the script loads the file into RAM.
