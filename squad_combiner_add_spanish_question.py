from html_parser import get_answers_and_answer_starts, strip_html_tags

import json
import datetime
import time
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


#fname = "train-v2.0"
#name = "dev-v2.0"
#name = "train-v2.0"
#name = "translated_dev-v2.0 no answers"
#name = "translated_train-v2.0 no answers"
#name = "translated dev exclude problematic interpreted"
name ="swe_squad_bert_project"
name ="swe_squad_bert_project_ext"
name ="swe_squad_bert_project_ext_dev"
name ="swe_squad_bert_project_ext_dev_new"
name ="swe_squad_bert_project_ext_train_new"
name ="train_only_newprojfixed_sv_no_impossible"
name ="dev_only_newprojfixed_sv_no_impossible"
name ="train_only_newprojfixed_sv_no_impossible"
name ="es_squad"

name_orig = "dev-v2.0"
name_orig ="train-v2.0"
name_orig ="translated dev answers translated"
name_orig ="confident_translated_dev_no_impossible"
name_orig ="confident_translated_train_no_impossible"
name_orig ="spanish_squad_train"
#name ="translated train answers translated"

#name = "translated_train_en_plus_newprojfixed_sv_no_impossible 08.03.45.349500 PM on January 19, 2020"
#name_orig = "train-v2.0"

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

outputfile_question_by_id = {}

for i,article in enumerate(data['data']):
    for j, p in enumerate(article['paragraphs']):
        for q_i, qa in enumerate(p['qas']):
            outputfile_question_by_id[qa['id']] = qa

replaced = 0
diff_pos = 0
diff_text = 0
diff_text_and_pos = 0

for i,article in enumerate(data_orig['data']):
    for j, p in enumerate(article['paragraphs']):
        for q_i, qa in enumerate(p['qas']):
            print(qa['translated_question'])
            print(outputfile_question_by_id[qa['id']]['question'])
            print()
            outputfile_question_by_id[qa['id']]['question'] = qa['translated_question']

#exit(0)
t0 = time.time()
#exit(0)
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