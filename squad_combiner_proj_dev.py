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
name_orig ="dev_ext_2_ext_5_multialt"
#name ="confident_translated_train"#_no_impossible"
name ="translated dev answers translated"
#name ="translated train answers translated"
date = datetime.datetime.now().strftime("%I.%M.%S.%f %p on %B %d, %Y")
outname = "translated_" + name + " " + date
with open(name+".json","r", encoding="utf-8") as f:
    data = json.loads(f.read())
with open(name_orig+".json","r", encoding="utf-8") as f:
    data_orig = json.loads(f.read())

with open(name+".json","r", encoding="utf-8") as f:
    data_new = json.loads(f.read())
with open(name_orig+".json","r", encoding="utf-8") as f:
    data_old = json.loads(f.read())

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

remove_impossible = True

orig_questions = {}
for i,article in enumerate(data_orig['data']):
    for j, p in enumerate(article['paragraphs']):
        for q_i, qa in enumerate(p['qas']):
            orig_questions[qa['id']] = qa

new_questions = {}
for i,article in enumerate(data['data']):
    article['title'] = 'sv_' + article['title']
    for j,p in enumerate(article['paragraphs']):
        for q_i, qa in enumerate(p['qas']):
            new_questions[qa['id']] = qa
            p['qas'][q_i]['id'] = "sv_" + p['qas'][q_i]['id']


for i,article in enumerate(data_old['data']):
    #article['title'] = 'new' + article['title']
    for j,p in enumerate(article['paragraphs']):
        for q_i, qa in enumerate(p['qas']):
            if 'is_impossible' not in qa:
                qa['is_impossible'] = False
            if not (remove_impossible and qa['is_impossible']):
                ans_index = int(qa['id'][-1])
                transl_ans = new_questions[qa['id'][:-2]]['answers'][ans_index]['translated_text']
                q_parts = p['qas'][q_i]['question'].split(' [SEP] ')
                q = ' [SEP] '.join([transl_ans] + q_parts[1:])
                p['qas'][q_i]['question'] = q
                print(q_parts[0])
                print(q)
            #p['qas'][q_i]['id'] = "sv_q_en_a_" + p['qas'][q_i]['id']
        if remove_impossible:
            to_remove = []
            for q_i, qa in enumerate(p['qas']):
                if qa['is_impossible']:
                    to_remove.append(q_i)
            for q_i in reversed(to_remove): # Remove impossible questions
                del p['qas'][q_i]


t0 = time.time()



with open(outname + ".json", "w") as out:
   json.dump(data_old, out)
print("Updated file " + outname + ".json in %.2f seconds" % (time.time()-t0))


#with open("to_translate.txt","w", encoding="utf-8") as out:
#    out.write("\n".join([txt.replace("\n"," ") for txt in to_translate]))
#print(len(to_translate))



    #print("Translated %d paragraphs and %d questions from 1 article in %.2f seconds" % (n_paragraphs, n_questions, time.time()-t0))
    #t0 = time.time()
    #with open(outname + ".json", "w") as out:
    #    json.dump(data, out)
