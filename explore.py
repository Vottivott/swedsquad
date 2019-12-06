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
        if len(qa['answers']) == 0:
            #print(":(")
            continue
        a = qa['answers'][0]
        positions.append((a['answer_start'],a['answer_start']+len(a['text'])))
    for start,end in positions:
        context = context[:start] + "<" + context[start:end] + ">" + context[end:]
        quoted = quoted[:start] + '"' + quoted[start:end] + '"' + quoted[end:]
        for i in range(len(positions)):
            s,e = positions[i]
            s,e = [pos + 2 if pos >= end-1 else (pos + 1 if pos >= start else pos) for pos in (s,e)]
            positions[i] = (s,e)
    print(context)
    print()
    print(quoted)
    print()
    print(p['context'])
    print()
    print()
    #print(context)
    #print()
    #print(question)
    #print()
    #print(ans_text)
    #print()
    #print()