from html_parser import get_answers_and_answer_starts, strip_html_tags

import json
import datetime
import time

#fname = "train-v2.0"
#name = "dev-v2.0"
#name = "train-v2.0"
#name = "translated_dev-v2.0 no answers"
#name = "translated_train-v2.0 no answers"
#name = "translated dev exclude problematic interpreted"
name ="confident_translated_train_no_impossible"
#name ="confident_translated_train"#_no_impossible"
name_orig ="train-v2.0"
#name ="translated train answers translated"
date = datetime.datetime.now().strftime("%I.%M.%S.%f %p on %B %d, %Y")
outname = "translated_" + name + " " + date
with open(name+".json","r", encoding="utf-8") as f:
    data = json.loads(f.read())
with open(name_orig+".json","r", encoding="utf-8") as f:
    data_orig = json.loads(f.read())

n_articles = len(data['data'])
skipped = 0

translate_answers = True

cloud = False

deleted_answers = 0
deleted_questions = 0

n_questions = 0
t0 = time.time()
to_translate = []
t_i = 0
paragraph_index = 0

for i,article in enumerate(data['data']):
    article['title'] = 'sv_' + article['title']
    for j,p in enumerate(article['paragraphs']):
        for q_i, qa in enumerate(p['qas']):
            p['qas'][q_i]['id'] = "sv_" + p['qas'][q_i]['id']

for i,article in enumerate(data_orig['data']):
    for j, p in enumerate(article['paragraphs']):
        if True:
            to_remove = []
            for q_i, qa in enumerate(p['qas']):
                if qa['is_impossible']:
                    to_remove.append(q_i)
            for q_i in reversed(to_remove): # Remove impossible questions
                del p['qas'][q_i]
    data['data'].append(article)
t0 = time.time()
with open(outname + ".json", "w") as out:
   json.dump(data, out)
print("Updated file " + outname + ".json in %.2f seconds" % (time.time()-t0))
#with open("to_translate.txt","w", encoding="utf-8") as out:
#    out.write("\n".join([txt.replace("\n"," ") for txt in to_translate]))
#print(len(to_translate))



    #print("Translated %d paragraphs and %d questions from 1 article in %.2f seconds" % (n_paragraphs, n_questions, time.time()-t0))
    #t0 = time.time()
    #with open(outname + ".json", "w") as out:
    #    json.dump(data, out)
    #print("Updated file " + outname + ".json in %.2f seconds" % (time.time()-t0))