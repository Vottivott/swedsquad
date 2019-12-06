from transformers.tokenization_bert import BertTokenizer
from transformers import BertForQuestionAnswering
import torch
import json
import urllib

squad_train = 'https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v1.1.json' #@param ["https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v2.0.json", "https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v2.0.json", "https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v1.1.json", "https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v1.1.json"]
squad_dev = 'https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v1.1.json' #@param ["https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v2.0.json", "https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v2.0.json", "https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v1.1.json", "https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v1.1.json"]
utils_squad = 'https://github.com/huggingface/transformers/raw/master/examples/utils_squad.py'
run_squad = 'https://github.com/huggingface/transformers/raw/master/examples/run_squad.py'
utils_squad_evaluate = 'https://github.com/huggingface/transformers/raw/master/examples/utils_squad_evaluate.py'

def download_file(url, path):
  f= open(path,"wb+")
  f.write(urllib.request.urlopen(url).read())
  f.close()

download_file(squad_train, "squad_train.json")
download_file(squad_dev, "squad_dev.json")

download_file(run_squad, "run_squad.py")
download_file(utils_squad, "utils_squad.py")
download_file(utils_squad_evaluate, "utils_squad_evaluate.py")

