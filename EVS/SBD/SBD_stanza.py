import csv
import stanza
from datetime import datetime, timedelta
import pysrt
import string
import re
import sys

def load_stanza_model(language):
    try:
        stanza.download(language)
        nlp = stanza.Pipeline(language)
        return nlp
    except Exception as e:
        print(f"Error loading model '{language}': {e}")
        print("Please make sure the language model is installed.")
        sys.exit(1)

def parse_srt(file_path):
    subs = pysrt.open(file_path)
    subtitles = []
    for sub in subs:
        start = sub.start.to_time()
        end = sub.end.to_time()
        text = sub.text
        subtitles.append({"index": sub.index, "start": start, "end": end, "text": text})
    return subtitles

def clean_sentence(sentence):
    sentence = sentence.strip()
    sentence = re.sub(r'\s([?.!,"](?:\s|$))', r'\1', sentence)
    sentence = re.sub(r'\s+([,;])', r'\1', sentence)
    sentence = re.sub(r'\s*-\s*', '-', sentence)
    sentence = re.sub(r'\s*%\s*', '%', sentence)
    sentence = re.sub(r'(\$)\s*', r'\1', sentence)
    return sentence

def find_timestamp(subtitles, text, word_index):
    for sub in subtitles[word_index:]:
        if text in sub["text"]:
            return sub["start"], sub["end"], sub["index"]
    return None, None, None

def reconstruct_sentences_stanza(subtitles, nlp):
    combined_text = " ".join([s["text"] for s in subtitles])
    doc = nlp(combined_text)

    new_sentences = []
    word_index = 0

    for sent in doc.sentences:
        sentence = clean_sentence(sent.text)
        sentence_word_count = len(sentence.split())

        first_word = sentence.split()[0]
        start_time, _, start_index = find_timestamp(subtitles, first_word, word_index)

        last_word = sentence.split()[-1]
        _, end_time, end_index = find_timestamp(subtitles, last_word, word_index)

        if start_time and end_time:
            duration = timedelta(
                milliseconds=(timestamp_to_ms(end_time) - timestamp_to_ms(start_time))
            )

            new_sentences.append(
                [
                    len(new_sentences) + 1,
                    sentence,
                    time_to_str(start_time),
                    time_to_str(end_time),
                    timedelta_to_str(duration),
                    sentence_word_count,
                ]
            )

            word_index = end_index

    return new_sentences

def timestamp_to_ms(timestamp):
    return (
        (timestamp.hour * 60 * 60 * 1000)
        + (timestamp.minute * 60 * 1000)
        + (timestamp.second * 1000)
        + (timestamp.microsecond // 1000)
    )

def time_to_str(time_obj):
    return f"{time_obj.hour:02}:{time_obj.minute:02}:{time_obj.second:02},{time_obj.microsecond // 1000:03}"

def timedelta_to_str(timedelta_obj):
    total_seconds = timedelta_obj.total_seconds()
    hours, remainder = divmod(total_seconds, 3600)
    minutes, remainder = divmod(remainder, 60)
    seconds, milliseconds = divmod(remainder, 1)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{int(milliseconds * 1000):03}"

def write_csv(output_file, sentences):
    with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["sequence", "sentence", "start", "end", "duration", "word_count"])
        for sentence in sentences:
            writer.writerow(sentence)

if len(sys.argv) > 2:
    language = sys.argv[1]
    srt_file_path = sys.argv[2]
else:
    print("Please provide both the language model name and the path to the .word.srt file.")
    sys.exit(1)
    
nlp = load_stanza_model(language)

if srt_file_path.endswith(".word.srt"):
    output_file = srt_file_path.replace(".word.srt", ".csv")
    subtitles = parse_srt(srt_file_path)
    reconstructed_sentences = reconstruct_sentences_stanza(subtitles, nlp)
    write_csv(output_file, reconstructed_sentences)
else:
    print(f"Invalid file type: {srt_file_path}. Please provide a .word.srt file.")

