import re

import numpy as np
import os
import glob

def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()


def split_model_file(model, chunksize=50000000, remove=False):
    """
    Split model in smaller files that can be uploaded to Git wothout LFS.
    """
    if len(glob.glob(str(model)+'*.0')) > 0:
        raise ValueError("model already split")

    for m in glob.glob(str(model)+'*'):
        with open(m) as f:
            chunk = f.read(chunksize)
            file_number = 0
            while chunk:
                with open(m+'.' + str(file_number), 'a+') as chunk_file:
                    chunk_file.write(chunk)
                file_number += 1
                chunk = f.read(chunksize)

        if remove:
            os.remove(m)
           

def merge_model_file(model, remove=False):
    """
    Merge sub-models by joining multiple sub-files.
    """
    for m in glob.glob(str(model)+'*.0'):
        with open(m[:-2], 'wb') as f:
            for m2 in sorted(glob.glob(m[:-2]+'.*'), key=lambda f: os.path.splitext(f)):
                with open(m2) as f2:
                    f.write(f2.read())

                if remove:
                    os.remove(m2)
