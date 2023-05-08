# Automated-EVS-Measurement for Interpreting Studies

This project aims to automate the measurement of Ear-Voice-Span (EVS) in Interpreting Studies using an end-to-end pipeline consisting of ASR, Sentence Boundary Detection (SBD), and Cross-Lingual Alignment.

## Pipeline Overview

1. **ASR**: Use WhisperX ASR to convert audio files into text with timestamps at the word level.
2. **SBD**: Process ASR output with various SBD models (default: Stanza).
3. **Cross-Lingual Alignment**: Align the sentences from two languages (default: SBERT with a similarity threshold of 0.7) and extract EVS.

## Getting Started

1. Clone this repository:
```
git clone https://github.com/MMRita/automated-evs-measurement.git
```

2. Install the dependencies using pip:
```bash
pip install -r requirements.txt
```
3. Set up the ASR model (WhisperX) following the instructions in the [WhisperX repository](https://github.com/m-bain/whisperX).

## Usage

### Audios ASR
```bash
Whisperx <examples/sample01.wav> --language <X>
```
Replace `<examples/sample01.wav>` with the name of the audio you want to transcribe and replace `<X>` with the language of your audio transcribe. Currently, default models are provided for {en, fr, de, es, it, ja, zh, nl, uk, pt}. After running WhisperX, five files will be generated, in which the file ending with ".word.srt" will be used for the next steps.

### Use Default Models to Generate EVS

Run the `main.py` script:
```bash
python main.py <source_language> <target_language> <source_path> <target_path>
```
Replace `<source_language>` and `<target_language>` with the respective languages, e.g., {en, fr, de, es, it, ja, zh, nl, uk, pt}. Replace `<source_path>` and `<target_path>` with the respective file paths.

After running the code, four files will be generated:

- source_language_sentences.txt (for SBD process)
- target_language_sentences.txt (for SBD process)
- cross_lingual_alignment.txt (for cross-lingual alignment process)
- EVS.txt (for EVS extraction)

## Customizing the Pipeline

To use different models for SBD or Cross-Lingual Alignment and set different similarity thresholds for the Cross-Lingual Alignment process, please refer to the individual scripts provided for each model. You can find their supporting languages and processing models on their official sites:

### Sentence Boundary Detection Models

- `punkt.py`: [NLTK's Punkt tokenizer](https://www.nltk.org/api/nltk.tokenize.html) (Additional dependency: nltk)
- `spacy_sbd.py`: [Spacy](https://spacy.io/) (Additional dependencies: spacy)
- `stanza_sbd.py`: [Stanza](https://stanfordnlp.github.io/stanza/) (default) (Additional dependency: stanza)

### Cross-Lingual Alignment Models

- `LASER.py`: [LASER](https://github.com/facebookresearch/LASER) (Additional dependency: laserembeddings)
- `mT5.py`: [mT5](https://github.com/google-research/multilingual-t5) (Additional dependencies: transformers)
- `SBERT.py`: [SBERT](https://www.sbert.net/) (default) (Additional dependency: sentence-transformers)
- `USE.py`: [Universal Sentence Encoder](https://tfhub.dev/google/collections/universal-sentence-encoder/) (Additional dependencies: tensorflow, tensorflow-hub, tensorflow-text)
- `XLM-Roberta.py`: [XLM-Roberta](https://huggingface.co/transformers/model_doc/xlmroberta/) (Additional dependency: transformers)

You can modify the respective scripts according to your needs and run them independently.


## Contributing

If you would like to contribute to this project, please submit a pull request with your proposed changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.


## Contact
For questions or comments, please contact p2111921@mpu.edu.mo. Hope this helps! Let me know if you have any other questions.
