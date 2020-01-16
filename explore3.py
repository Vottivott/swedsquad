import json

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
fname = "original_plus_confident_translated_train_no_impossible.json"
fname = "train-v2.0.json"
fname = "DRCD_training.json"
fname = "translated_en_plus_all_sv_plus_chinese_train_only.json"
fname = "DRCD_dev.json"
fname = "DRCD_test.json"
fname = "translated_en_plus_all_sv_plus_chinese.json"
fname = "confident_plus_ot_train_no_impossible.json"
fname = "confident_translated_train_no_impossible.json"
fname = "cross_qa_no_impossible.json"
fname = "train-v2.0.json"
fname = "projection_squad_train.json"
fname = "projection_squad_ext_2_ext_5_train.json"
fname = "projection_squad_ext_2_ext_5_train_Swedish.json"
fname = "swe_squad_bert_project.json"
fname = "train_en_plus_proj_sv_no_impossible.json"

with open(fname,"r", encoding='utf-8') as f:
    data = json.loads(f.read())['data']
num_answers_individually = []


article = data[4]
title = article['title']
paragraphs = article['paragraphs']
print(title)
#print('-'*len(title))
#print()

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
            questions.append([qa['question'],"SVAR: " + qa['answers'][0]['text']])
            #if not qa['is_impossible']:
            #    questions.append([context,qa['translated_question'],"SVAR: " + qa['answers'][0]['text']])
            #questions.append([context,qa['question'],"SVAR: " + qa['answers']['text']])

            #print(qa['question'])
            #print(qa['translated_question'])
            #print()
        num_questions.append(len(qas))

        #if context.find("\n") != -1:
        #    print("!")

        txt = " "*len(context)
        positions = []
        for qa in qas:
            if 'is_impossible' not in qa or not qa['is_impossible']:
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
questions = sum(questions[:1000],[])
print("\n".join(questions[:10]))
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
exit(0)
import matplotlib.pyplot as plt
plt.hist(num_answers_individually)
plt.show()