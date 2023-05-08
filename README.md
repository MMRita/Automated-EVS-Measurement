# Automated-EVS-Measurement for Interpreting Studies

This project aims to automate the measurement of Ear-Voice-Span (EVS) in Interpreting Studies using an end-to-end pipeline consisting of ASR, Sentence Boundary Detection (SBD), and Cross-Lingual Alignment.

## Pipeline Overview
1. ASR: Use WhisperX ASR to convert audio files into text with timestamps.
2. SBD: Process ASR output with various SBD models (default: Stanza).
3. Cross-Lingual Alignment: Align the sentences from two languages (default: SBERT with a similarity threshold of 0.7).

## Dependencies

Install the dependencies using pip:

```bash
pip install -r requirements.txt

## Usage

### Using Default Models

1. Clone the repository and install the dependencies.
2. Run the `main.py` script with the language abbreviation:

```bash
python main.py <language>

### Customizing the Pipeline

To use different models for SBD or Cross-Lingual Alignment, please refer to the individual scripts provided for each model:

#### Sentence Boundary Detection Models

- `punkt.py`: NLTK's Punkt tokenizer (Additional dependency: nltk)
- `spacy_sbd.py`: Spacy (Additional dependencies: spacy, spacy-langdetect)
- `stanza_sbd.py`: Stanza (default) (Additional dependency: stanza)

#### Cross-Lingual Alignment Models

- `LASER.py`: LASER (Additional dependency: laserembeddings)
- `mT5.py`: mT5 (Additional dependencies: transformers)
- `SBERT.py`: SBERT (default) (Additional dependency: sentence-transformers)
- `USE.py`: Universal Sentence Encoder (Additional dependencies: tensorflow, tensorflow-hub, tensorflow-text)
- `XLM-Roberta.py`: XLM-Roberta (Additional dependency: transformers)

You can modify the respective scripts according to your needs and run them independently.

## Contributing

If you would like to contribute to this project, please submit a pull request with your proposed changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
