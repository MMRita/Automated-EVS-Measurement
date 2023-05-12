# Automated-EVS-Measurement for Interpreting Studies

This project aims to automate the measurement of Ear-Voice-Span (EVS) in Interpreting Studies through an end-to-end pipeline. The pipeline includes Automatic Speech Recognition (ASR), Sentence Boundary Detection (SBD), and Cross-Lingual Alignment.

## Pipeline Overview

1. **ASR**: The [WhisperX](https://github.com/m-bain/whisperX) ASR is used to convert audio files into text with word-level timestamps.
2. **SBD**: The ASR output is processed using various SBD models (Stanza by default).
3. **Cross-Lingual Alignment**: Sentences from two languages are aligned (using Universal Sentence Encoder (USE) with a similarity threshold of 0.5 by default), and EVS is extracted.

## Languages supported

This pipeline supports ten languages, each identified by their respective language codes:

`en` → English  
`fr` → French  
`de` → German  
`es` → Spanish  
`it` → Italian  
`ja` → Japanese  
`zh` → Chinese  
`nl` → Dutch  
`uk` → Ukrainian  
`pt` → Portuguese  


## Getting Started

To get started, clone the repository and install the necessary dependencies:
```
git clone https://github.com/MMRita/automated-evs-measurement.git
pip install -r requirements.txt
```

## Usage

### ASR for Audios
Perform Automatic Speech Recognition (ASR) on your audio file using WhisperX:
```bash
Whisperx <examples/sample01.wav> --language <X>
```
Replace `<examples/sample01.wav>` with the path to the audio file you wish to transcribe and replace `<X>` with the language code of your audio. After running this command, five files will be generated, the ".word.srt" file of which will be used in subsequent steps.

### Use Default Models to Generate EVS

Run the `main.py` script:
```bash
python main.py <source_language> <target_language> <source_path> <target_path>
```
Replace `<source_language>` and `<target_language>` with the respective language codes. Replace `<source_path>` and `<target_path>` with the respective ".word.srt" file paths. This command generates three files:
- source_language_sentences.csv (for SBD process)
- target_language_sentences.csv (for SBD process)
- cross_lingual_alignment.csv (for cross-lingual alignment process and EVS extraction)

## Customizing the Pipeline

Refer to the provided individual scripts to customize the SBD or Cross-Lingual Alignment models or to set different similarity thresholds for the Cross-Lingual Alignment process. Check the official websites of these models for their supported languages and processing capabilities.

### Sentence Boundary Detection Models

- `SBD_punkt.py`: [NLTK's Punkt tokenizer](https://www.nltk.org/api/nltk.tokenize.html) (Additional dependency: nltk)
- `SBD_spaCy.py`: [SpaCy](https://spacy.io/) (Additional dependencies: spacy)
- `SBD_stanza.py`: [Stanza](https://stanfordnlp.github.io/stanza/) (default) (Additional dependency: stanza)

To use one of these models, run:

```bash
python <script_name.py> <en> <path_to_your_file.word.srt>
```
Replace `<script_name.py>` with the name of the script you choose, `<en>` with the language code, and `<path_to_your_file.word.srt>` with the path to the ".word.srt" file you want to process.

Note: Before running the SBD_SpaCy.py script, ensure that the required language models are downloaded and installed. Refer to the official SpaCy website for more details.

### Cross-Lingual Alignment Models

- `A_SBERT.py`: [SBERT](https://www.sbert.net/) (Additional dependency: sentence-transformers)
- `A_LASER.py`: [LASER](https://github.com/facebookresearch/LASER) (Additional dependency: laserembeddings)
- `A_USE.py`: [Universal Sentence Encoder](https://tfhub.dev/google/collections/universal-sentence-encoder/) (default) (Additional dependencies: tensorflow, tensorflow-hub, tensorflow-text)
- `A_mT5`:[mT5](https://huggingface.co/google/mt5-small) (Additional dependency: transformers)
- `A_XLM-Roberta.py`: [XLM-Roberta](https://huggingface.co/docs/transformers/model_doc/xlm-roberta) (Additional dependency: transformers)

To use one of these models, run:

```bash
python <script_name.py> <source_file.csv> <target_file.csv> <source_language> <target_language> <similarity_threshold>
```
Replace `<script_name.py>` with the name of the script you wish to use, `<source_file.csv>` and `<target_file.csv>` with the paths to the source and target language files generated in the previous step. Replace `<source_language>` and `<target_language>` with the respective language codes, and `<similarity_threshold>` with your desired similarity threshold (between 0 and 1).

## Performance Evaluation

The robustness and performance of this automated EVS measurement pipeline have been evaluated using a comprehensive 20-hour English-to-Portuguese simultaneous interpretation corpus, encompassing 57 unique audio pairs. In the default combination of models, the mean EVS error value across the entire corpus is less than 0.1 seconds. We present key findings and figures illustrating the results below.

<p align="center">
  <img src="images/violin.png" alt="violin plot">
</p>

The width of the violin at any given vertical level signifies the density of EVS values, while the outline shape represents the kernel density plot. All automated methods demonstrated longer tails in their distributions compared to the manual approach, indicating a need for further exploration. The jittered black points overlaid on the violin plot represent individual EVS values, providing a sense of the raw data’s distribution. The bold line in the center of each violin illustrates a box plot, with the range between the upper and lower boundaries representing the interquartile range (IQR), and the center point indicating the median EVS value.

<p align="center">
  <img src="images/comparison.png" alt="comparison of models">
</p>

The overall accuracy of the mean EVS values generated by the three models is acceptable, with USE outperforming the others by confining both the mean absolute error (MAE) and root mean square error (RMSE) to less than 0.5. In terms of correlation with the manual approach, USE demonstrates a strong, positive relationship, whereas SBERT and LASER show a moderate correlation.

In conclusion, based on the performance metrics and visualizations presented in this section, we can see that the SBERT, LASER, and USE models can all generate results that closely resemble those derived from the human approach. This demonstrates the feasibility of automated measurement of EVS to a certain extent, promising for future research and applications in simultaneous interpretation studies.

Please note that our complete study and further details are available in our paper, which is currently under review.

## Contributing

We welcome contributions to this project. If you would like to contribute, please submit a pull request with your proposed changes.

## License

This project uses models from various sources, each with their respective licenses:

- WhisperX: BSD-4 License
- NLTK's Punkt tokenizer: Apache License 2.0
- SpaCy: MIT License
- Stanza: Apache License 2.0
- SBERT: Apache License 2.0
- LASER: BSD License
- Universal Sentence Encoder: Apache License 2.0
- mT5: Apache License 2.0
- XLM-Roberta: Apache License 2.0

The code and other content in this project, including the incorporation of the above models, are licensed under the MIT License.

## Contact
For questions or comments, please contact p2111921@mpu.edu.mo. Hope this helps! Let me know if you have any other questions.

## Citation
If you use this in your research, please cite the paper:
```
@misc{to-be-updated,
  title={To Be Updated},
  author={To Be Updated},
  year={To Be Updated},
  eprint={To Be Updated},
  archivePrefix={To Be Updated},
  primaryClass={To Be Updated}
}
```
Please note that the above citation will be updated when our paper is published.
