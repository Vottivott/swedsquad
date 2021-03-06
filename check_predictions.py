import json

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

fname = "train-v2.0.json"
#fname = "dev-v2.0.json"
#fname = 'translated_dev-v2.0 06.35.01.949109 PM on December 06, 2019.json'
#fname = 'translated_train-v2.0 01.28.26.007134 AM on December 07, 2019.json'
#fname = "translated dev exclude problematic.json"
fname ="translated dev answers translated.json"
fname ="confident translated dev.json"
fname ="confident_translated_train.json"
fname ="translated train answers translated.json"
fname ="confident_translated_train_no_impossible.json"
fname ="confident_translated_dev_no_impossible.json"
with open(fname,"r") as f:
    data = json.loads(f.read())['data']

with open("predictions_ml_bert_sv_large.json","r") as f:
    pred = json.loads(f.read())


num_answers_individually = []

questions = []
num_questions = []
num_problematic = 0
num_quote_containing = 0
num_weird_quote_containing = 0
num_translated_articles = 0
num_mult_answers = 0
num_more_problematic = 0
num_answers = 0
num_answerable_questions = 0
for article in data:
    if 'translated' in article and article['translated']:
        num_translated_articles+=1
    for p in article['paragraphs']:
        context = p['context']
        #print(p['context_html_exclude_problematic'])
        #print()
        #print(p['translated_context_html_exclude_problematic'])
        #print()
        #print()
        qas = p['qas']
        for qa in qas:
            questions.append(qa['question'])
            prediction = pred[qa['id']]

            print(bcolors.BOLD + qa['question'] + bcolors.ENDC)
            s = qa['answers'][0]['answer_start']
            e = s + len(qa['answers'][0]['text'])
            sp = context.find(prediction)
            c = context
            col = bcolors.BOLD
            colp = bcolors.OKBLUE
            colb = bcolors.OKGREEN + bcolors.BOLD
            end = bcolors.ENDC
            if sp == -1:
                print("Not found!!")
                continue
            else:
                ep = sp + len(prediction)
                if ep==e and sp==s:
                    tx = c[:s] + colb + c[s:e] + end+end + c[e:]
                elif ep < s:
                    colp = bcolors.FAIL
                    tx = c[:sp] + colp + c[sp:ep] + end + c[ep:s] + col + c[s:e] + end + c[e:]
                elif e < sp:
                    colp = bcolors.FAIL
                    tx = c[:s] + col + c[s:e] + end + c[e:sp] + colp + c[sp:ep] + end + c[ep:]
                elif s <= sp and ep <= e:
                    tx = c[:s] + col + c[s:sp] + end + colb + c[sp:ep] + end+end + col + c[ep:e] + end + c[e:]
                elif sp <= s and e <= ep:
                    tx = c[:sp] + colp + c[sp:s] + end + colb + c[s:e] + end+end + colp + c[e:ep] + end + c[ep:]
                elif sp < s:
                    tx = c[:sp] + colp + c[sp:s] + end + colb + c[s:ep] + end+end + col + c[ep:e] + end + c[e:]
                else:
                    tx = c[:s] + col + c[s:sp] + end + colb + c[sp:e] + end+end + colp + c[e:ep] + end + c[ep:]



            print(tx)
            if prediction in [a['text'] for a in qa['answers']]:
                anscol = bcolors.OKGREEN
            else:
                anscol = bcolors.FAIL
            print(anscol + prediction + bcolors.ENDC)

            print(bcolors.BOLD + qa['answers'][0]['text'] + bcolors.ENDC)
            print()

            #print(qa['question'])
            #print(qa['translated_question'])
            #print()
        num_questions.append(len(qas))

        #if context.find("\n") != -1:
        #    print("!")

        txt = " "*len(context)
        positions = []
        for qa in qas:
            if not qa['is_impossible']:
                num_answerable_questions += 1
            if len(qa['answers']) == 0:
                # print(":(")
                continue
            if len(qa['answers']) > 1:
                num_mult_answers += 1
                #print(len(qa['answers']))
            #a = qa['answers'][0]
            s = qa['answers'][0]['answer_start']
            e = s+len(qa['answers'][0]['text'])
            #print(context[s:e])
            #print(qa['answers'][0]['text'])
            num_answers += len(qa['answers'])
            num_answers_individually.append(len(qa['answers']))

            for a in qa['answers']:
                #print(a['text'])
                #print(a['translated_text'])
                positions.append((a['answer_start'], a['answer_start'] + len(a['text'])))

        for start,end in positions:
           for s,e in positions:
               if (s,e) != (start,end):
                   if s < start < e and end > e:
                        num_more_problematic += 1
                        #print(context)

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
print("Number of answers: %d" % num_answers)
print("Number of quote-containing paragraphs: %d (%.2f %%)" % (num_quote_containing, 100*(num_quote_containing/len(num_questions))))
print("Number of weird-quote-containing paragraphs: %d (%.2f %%)" % (num_weird_quote_containing, 100*(num_weird_quote_containing/len(num_questions))))
print("Number of translated articles: %d (%.2f %%)" % (num_translated_articles, 100*(num_translated_articles/len(data))))
print("Number of multi-answer questions: %d (%.2f %%)" % (num_mult_answers, 100*(num_mult_answers/sum(num_questions))))
print("Number of possible questions: %d (%.2f %%)" % (num_answerable_questions, 100*((num_answerable_questions)/sum(num_questions))))

import matplotlib.pyplot as plt
plt.hist(num_answers_individually)
plt.show()