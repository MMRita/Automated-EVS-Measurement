import sys
import pandas as pd
import numpy as np
from fastdtw import fastdtw
from datetime import datetime, timedelta
import tensorflow_hub as hub
import tensorflow_text

def time_difference(time1, time2):
    time_format = "%H:%M:%S,%f"
    t1 = datetime.strptime(time1, time_format)
    t2 = datetime.strptime(time2, time_format)
    return (t2 - t1).total_seconds()

def seconds_to_time_format(seconds):
    return (datetime.min + timedelta(seconds=abs(seconds))).time().strftime('%H:%M:%S,%f')[:-3]

def cosine_similarity(x, y):
    return np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))

def align_sentences(source_file, target_file, output_file, similarity_threshold):
    source_df = pd.read_csv(source_file)
    target_df = pd.read_csv(target_file)

    model = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual/3")

    def encode(sentences):
        return np.array(model(sentences))

    source_embeddings = encode(source_df['sentence'].tolist())
    target_embeddings = encode(target_df['sentence'].tolist())

    distance, path = fastdtw(source_embeddings, target_embeddings, dist=lambda x, y: np.linalg.norm(x - y))

    aligned = []
    count = 0

    aligned_source_idx = set()
    aligned_target_idx = set()

    for pair in path:
        source_idx, target_idx = pair

        if source_idx in aligned_source_idx or target_idx in aligned_target_idx:
            continue

        similarity = cosine_similarity(source_embeddings[source_idx], target_embeddings[target_idx])

        if similarity >= similarity_threshold:
            source_start_time = source_df.iloc[source_idx]['start']
            target_start_time = target_df.iloc[target_idx]['start']

            evs = time_difference(source_start_time, target_start_time)

            count += 1

            aligned.append({
                'sequence': count,
                'source_sentence': source_df.iloc[source_idx]['sentence'],
                'target_sentence': target_df.iloc[target_idx]['sentence'],
                'source_start': source_start_time,
                'target_start': target_start_time,
                'EVS': seconds_to_time_format(evs)
            })

            aligned_source_idx.add(source_idx)
            aligned_target_idx.add(target_idx)

    aligned_df = pd.DataFrame(aligned)
    aligned_df.to_csv(output_file, index=False)

source_file = sys.argv[1]
target_file = sys.argv[2]
output_file = 'Alignment_EVS.csv'
similarity_threshold = float(sys.argv[5])

align_sentences(source_file, target_file, output_file, similarity_threshold)
