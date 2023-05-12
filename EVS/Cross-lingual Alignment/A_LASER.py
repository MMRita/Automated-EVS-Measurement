import pandas as pd
import numpy as np
from fastdtw import fastdtw
from datetime import datetime
from laserembeddings import Laser
import sys

def time_difference(time1, time2):
    time_format = "%H:%M:%S,%f"
    t1 = datetime.strptime(time1, time_format)
    t2 = datetime.strptime(time2, time_format)
    return abs((t2 - t1).total_seconds())

def seconds_to_time(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}".replace('.', ',')

def cosine_similarity(x, y):
    return np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))

def align_sentences(source_file, target_file, output_file, similarity_threshold, source_lang, target_lang):
    source_df = pd.read_csv(source_file)
    target_df = pd.read_csv(target_file)

    laser = Laser()

    def encode(sentences, language):
        return np.array(laser.embed_sentences(sentences, lang=language))

    source_embeddings = encode(source_df['sentence'].tolist(), source_lang)
    target_embeddings = encode(target_df['sentence'].tolist(), target_lang)

    distance, path = fastdtw(source_embeddings, target_embeddings, dist=lambda x, y: np.linalg.norm(x - y))

    aligned = []
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

            evs = seconds_to_time(time_difference(source_start_time, target_start_time))

            aligned.append({
                'sequence': len(aligned) + 1,
                'source_sentence': source_df.iloc[source_idx]['sentence'],
                'target_sentence': target_df.iloc[target_idx]['sentence'],
                'source_start': source_start_time,
                'target_start': target_start_time,
                'EVS': evs,
            })

            aligned_source_idx.add(source_idx)
            aligned_target_idx.add(target_idx)

    aligned_df = pd.DataFrame(aligned)
    aligned_df.to_csv(output_file, index=False)

source_file = sys.argv[1]
target_file = sys.argv[2]
source_lang = sys.argv[3]
target_lang = sys.argv[4]
similarity_threshold = float(sys.argv[5])
output_file = 'Alignment_EVS.csv'  # You can change this as needed

align_sentences(source_file, target_file, output_file, similarity_threshold, source_lang, target_lang)
