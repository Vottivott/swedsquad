import json

fname = "train-v2.0.json"
with open(fname,"r") as f:
    data = json.loads(f.read())['data']


article = data[4]
title = article['title']
paragraphs = article['paragraphs']
print(title)
print('-'*len(title))
print()
for p in paragraphs:
    context = p['context']
    qas = p['qas']
    qa = qas[0]
    question = qa['question']
    impossible = qa['is_impossible']
    ans = qa['answers'][0]
    ans_text = ans['text']
    ans_start = ans['answer_start']
    positions = []
    quoted = context
    for qa in qas:
        if qa['is_impossible']:
            print(qa['question'])
        else:
            continue
        if len(qa['answers']) == 0:
            #print(":(")
            continue
        a = qa['answers'][0]
        positions.append((a['answer_start'],a['answer_start']+len(a['text'])))
