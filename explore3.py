import json

#fname = "train-v2.0.json"
#fname = "dev-v2.0.json"
#fname = 'translated_dev-v2.0 06.35.01.949109 PM on December 06, 2019.json'
fname = 'translated_train-v2.0 01.28.26.007134 AM on December 07, 2019.json'
with open(fname,"r") as f:
    data = json.loads(f.read())['data']


article = data[4]
title = article['title']
paragraphs = article['paragraphs']
print(title)
print('-'*len(title))
print()

questions = []
num_questions = []
num_problematic = 0
num_quote_containing = 0
num_weird_quote_containing = 0
num_translated_articles = 0
num_mult_answers = 0
num_more_problematic = 0
num_answers = 0
for article in data:
    if 'translated' in article and article['translated']:
        num_translated_articles+=1
    for p in article['paragraphs']:
        context = p['context']
        qas = p['qas']
        for qa in qas:
            questions.append(qa['question'])
            #print(qa['question'])
            #print(qa['translated_question'])
            #print()
        num_questions.append(len(qas))

        #if context.find("\n") != -1:
        #    print("!")

        txt = " "*len(context)
        positions = []
        for qa in qas:
            if len(qa['answers']) == 0:
                # print(":(")
                continue
            if len(qa['answers']) > 1:
                num_mult_answers += 1
                #print(len(qa['answers']))
            #a = qa['answers'][0]
            num_answers += len(qa['answers'])
            for a in qa['answers']:
                positions.append((a['answer_start'], a['answer_start'] + len(a['text'])))

        for start,end in positions:
           for s,e in positions:
               if (s,e) != (start,end):
                   if s < start < e and end > e:
                        num_more_problematic += 1
                        print(context)

        include_existing_quotes = False
        if include_existing_quotes:
            pos = 0
            started = False
            last = None
            s = context
            while 1:
                poses = [s.find('"'), s.find('“'), s.find('”')]
                poses = [ps for ps in poses if ps != -1]
                if len(poses) == 0:
                    break
                pos = min(poses)
                s = s[:pos] + '*' + s[pos+1:]
                started = not started
                if not started:
                    positions.append((last, pos))
                last = pos
        positions = list(set(positions)) # remove exact duplicates, because they are easy to handle
        for start, end in positions:
            txt = txt[:start] + "<" + txt[start:end] + ">" + txt[end:]
            for i in range(len(positions)):
                s, e = positions[i]
                s, e = [pos + 2 if pos >= end - 1 else (pos + 1 if pos >= start else pos) for pos in (s, e)]
                positions[i] = (s, e)
        r = txt.replace(" ","")
        problematic = r.find("<<") != -1 or r.find(">>") != -1
        num_problematic += problematic
        if context.find('"') != -1 or context.find('“') != -1 or context.find('”') != -1:
            num_quote_containing += 1
        if context.find('❝') != -1 or context.find('❞') != -1:
            num_weird_quote_containing += 1





import random
random.shuffle(questions)
#print("\n".join(questions[:1000]))
print("Number of questions: %d" % sum(num_questions))
print("Number of paragraphs: %d" % len(num_questions))
print("Avg. num questions per paragraph: %.2f" % (sum(num_questions)/len(num_questions)))
print("Number of problematic paragraphs: %d (%.2f %%)" % (num_problematic, 100*(num_problematic/len(num_questions))))
print("Number of more problematic answers: %d (%.2f %%)" % (num_more_problematic, 100*(num_more_problematic/num_answers)))
print("Number of quote-containing paragraphs: %d (%.2f %%)" % (num_quote_containing, 100*(num_quote_containing/len(num_questions))))
print("Number of weird-quote-containing paragraphs: %d (%.2f %%)" % (num_weird_quote_containing, 100*(num_weird_quote_containing/len(num_questions))))
print("Number of translated articles: %d (%.2f %%)" % (num_translated_articles, 100*(num_translated_articles/len(data))))
print("Number of multi-answer questions: %d (%.2f %%)" % (num_mult_answers, 100*(num_mult_answers/sum(num_questions))))
import matplotlib.pyplot as plt
plt.hist(num_questions)
plt.show()