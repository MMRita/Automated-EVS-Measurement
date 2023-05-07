import os
import pandas as pd
import numpy as np
from fastdtw import fastdtw
from datetime import datetime
from laserembeddings import Laser

def time_difference(time1, time2):
    time_format = "%H:%M:%S,%f"
    t1 = datetime.strptime(time1, time_format)
    t2 = datetime.strptime(time2, time_format)
    return abs((t2 - t1).total_seconds())

def cosine_similarity(x, y):
    return np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))

def align_sentences(source_file, target_file, output_file, similarity_threshold):
    source_df = pd.read_csv(source_file)
    target_df = pd.read_csv(target_file)

    laser = Laser()

    def encode(sentences, language):
        return np.array(laser.embed_sentences(sentences, lang=language))
    

    source_embeddings = encode(source_df['sentence'].tolist(), 'en')
    target_embeddings = encode(target_df['sentence'].tolist(), 'pt')

    distance, path = fastdtw(source_embeddings, target_embeddings, dist=lambda x, y: np.linalg.norm(x - y))

    aligned = []
    total_evs = 0
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
            total_evs += evs
            count += 1

            aligned.append({
                'sequence': count,
                'sentences_in_English': source_df.iloc[source_idx]['sentence'],
                'sentences_in_portugues': target_df.iloc[target_idx]['sentence'],
                'start_of_english_sentence': source_start_time,
                'start_of_portuguese_sentence': target_start_time,
                'wordcount_of_English_sentence': source_df.iloc[source_idx]['word_count'],
                'wordcount_of_portuguese_sentence': target_df.iloc[target_idx]['word_count']
            })

            aligned_source_idx.add(source_idx)
            aligned_target_idx.add(target_idx)

    aligned_df = pd.DataFrame(aligned)
    aligned_df.to_csv(output_file, index=False)

source_directory = sys.argv[1] if len(sys.argv) > 1 else 'data/sentences_en'
target_directory = sys.argv[2] if len(sys.argv) > 2 else 'data/sentences_pt'
output_directory = sys.argv[3] if len(sys.argv) > 3 else 'data/EVS_SBERT'

if len(sys.argv) > 4:
    similarity_threshold = float(sys.argv[4])
else:
    similarity_threshold = float(input("Please enter the similarity threshold value (e.g., 0.7): "))

for filename in os.listdir(source_directory):
    if filename.endswith('_en.csv'):
        base_name = filename[:-7]
        source_file = os.path.join(source_directory, f"{base_name}_en.csv")
        target_file = os.path.join(target_directory, f"{base_name}_pt.csv")
        output_file = os.path.join(output_directory, f"{base_name}.csv")
        align_sentences(source_file, target_file, output_file, similarity_threshold)
