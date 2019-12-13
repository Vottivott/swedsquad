import json

#fname = "train-v2.0.json"
#fname = "dev-v2.0.json"
fname = "translated dev using google cloud html.json"
#fname = "sv_squad_dev.json"
fname = "swe-squad-1.json"
#fname ="confident translated dev.json"
with open(fname,"r", encoding="utf-8") as f:
    data = json.loads(f.read())['data']


article = data[0]
#article = data[2]
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
    #impossible = qa['is_impossible']
    ans = qa['answers'][0]
    ans_text = ans['text']
    ans_start = ans['answer_start']
    positions = []
    quoted = context
    quoted2 = context
    quoted3 = context
    for qa in qas:
        if len(qa['answers']) == 0:
            #print(":(")
            continue
        a = qa['answers'][0]
        print(a['text'])
        positions.append((a['answer_start'],a['answer_start']+len(a['text'])))
    positions = list(set(positions))
    for start,end in positions:
        context = context[:start] + "<" + context[start:end] + ">" + context[end:]
        quoted = quoted[:start] + '"' + quoted[start:end] + '"' + quoted[end:]
        quoted2 = quoted2[:start] + '❝' + quoted2[start:end] + '❞' + quoted2[end:]
        quoted3 = quoted3[:start] + '❝' + quoted3[start:end] + '❞' + quoted3[end:]
        for i in range(len(positions)):
            s,e = positions[i]
            s,e = [pos + 2 if pos >= end-1 else (pos + 1 if pos >= start else pos) for pos in (s,e)]
            positions[i] = (s,e)
    #print(context)
    #print()
    #print(quoted)
    #print()
    #print(quoted2)
    #print()
    i = 1
    while 1:
        old = quoted3
        quoted3 = quoted3.replace('❝',"<span id=\"%d\">" % i, 1).replace('❞',"</span>", 1)
        if old == quoted3:
            break
        i+=1
    print(quoted3)
    print()

    #print(quoted3.replace('❝',"<span>", 1).replace('❞',"</span>", 1))
    #print(p['context'])
    #print()
    #print()
    #print(context)
    #print()
    #print(question)
    #print()
    #print(ans_text)
    #print()
    #print()