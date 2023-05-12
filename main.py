import argparse
import punkt_en
import punkt_pt
import spacy_en
import spacy_pt
import stanza_en
import stanza_pt
import LASER
import mT5
import SBERT
import USE
import XLM_Roberta

def main():
    parser = argparse.ArgumentParser(description="Automated EVS Measurement")
    parser.add_argument('--sbd_model', choices=['punkt', 'spacy', 'stanza'], required=True, help='Model for sentence boundary detection')
    parser.add_argument('--sbd_language', choices=['en', 'pt'], required=True, help='Language for sentence boundary detection')
    parser.add_argument('--asr_output_directory', required=True, help='Path to the input directory containing ASR output files')
    parser.add_argument('--sbd_output_directory', required=True, help='Path to the output directory for sentence boundary detection results')
    parser.add_argument('--alignment_model', choices=['LASER', 'mT5', 'SBERT', 'USE', 'XLM_Roberta'], required=True, help='Model for cross-lingual alignment')
    parser.add_argument('--source_directory', required=True, help='Path to the source directory containing English sentences')
    parser.add_argument('--target_directory', required=True, help='Path to the target directory containing Portuguese sentences')
    parser.add_argument('--alignment_output_directory', required=True, help='Path to the output directory for cross-lingual alignment results')
    parser.add_argument('--similarity_threshold', type=float, default=0.7, help='Similarity threshold for aligning sentences')
    
    args = parser.parse_args()

    # Run the chosen SBD model
    if args.sbd_model == 'punkt':
        if args.sbd_language == 'en':
            punkt_en.process_sbd(args.asr_output_directory, args.sbd_output_directory)
        elif args.sbd_language == 'pt':
            punkt_pt.process_sbd(args.asr_output_directory, args.sbd_output_directory)
    elif args.sbd_model == 'spacy':
        if args.sbd_language == 'en':
            spacy_en.process_sbd(args.asr_output_directory, args.sbd_output_directory)
        elif args.sbd_language == 'pt':
            spacy_pt.process_sbd(args.asr_output_directory, args.sbd_output_directory)
    elif args.sbd_model == 'stanza':
        if args.sbd_language == 'en':
            stanza_en.process_sbd(args.asr_output_directory, args.sbd_output_directory)
        elif args.sbd_language == 'pt':
            stanza_pt.process_sbd(args.asr_output_directory, args.sbd_output_directory)

    # Run the chosen cross-lingual alignment model
    if args.alignment_model == 'LASER':
        LASER.align_sentences(args.source_directory, args.target_directory, args.alignment_output_directory, args.similarity_threshold)
    elif args.alignment_model == 'mT5':
        mT5.align_sentences(args.source_directory, args.target_directory, args.alignment_output_directory, args.similarity_threshold)
    elif args.alignment_model == 'SBERT':
        SBERT.align_sentences(args.source_directory, args.target_directory, args.alignment_output_directory, args.similarity_threshold)
    elif args.alignment_model == 'USE':
        USE.align_sentences(args.source_directory, args.target_directory, args.alignment_output_directory, args.similarity_threshold)
    elif args.alignment_model == 'XLM_Roberta':
    XLM_Roberta.align_sentences(args.source_directory, args.target_directory, args.alignment_output_directory, args.similarity_threshold)

if name == "main":
main()

