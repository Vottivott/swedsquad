from html_parser import get_answers_and_answer_starts, strip_html_tags

import json
import datetime
import time

#fname = "train-v2.0"
#name = "dev-v2.0"
#name = "train-v2.0"
#name = "translated_dev-v2.0 no answers"
#name = "translated_train-v2.0 no answers"
name = "translated dev exclude problematic interpreted"
date = datetime.datetime.now().strftime("%I.%M.%S.%f %p on %B %d, %Y")
outname = "translated_" + name + " " + date
with open(name+".json","r", encoding="utf-8") as f:
    data = json.loads(f.read())

n_articles = len(data['data'])
skipped = 0

translate_answers = True

deleted_answers = 0
deleted_questions = 0

n_questions = 0
t0 = time.time()
to_translate = []
t_i = 0
paragraph_index = 0
for i,article in enumerate(sorted(data['data'], key=lambda article: article['title'])):
    for j,p in enumerate(article['paragraphs']):

        if 'translated_context_cloud' not in p:
            print(p['context'])

        context = p['context']
        qas = [qa for qa in p['qas']]
        n_questions += len(qas)
        del p['translated_context']
        del p['translated_context_html_exclude_problematic']
        del p['context_html_exclude_problematic']
        p['context'] = p['translated_context_cloud']
        del p['translated_context_cloud']


        t_i += 1

        #to_translate.append(html)
        paragraph_index += 1

        include_questions = True
        if include_questions:

            questions_to_delete = []
            for q_i, qa in enumerate(qas):
                qas[q_i]['question'] = qas[q_i]['translated_question']
                del qas[q_i]['translated_question']
                t_i += 1
                if translate_answers:
                    to_delete = []
                    any_answer = False
                    for a_i, ans in enumerate(qa['answers']):
                        if 'translated_answer_start' not in qa['answers'][a_i]:
                            to_delete.append(a_i)
                            continue
                        else:
                            any_answer = True
                        qa['answers'][a_i]['text'] = qa['answers'][a_i]['translated_text']
                        qa['answers'][a_i]['answer_start'] = qa['answers'][a_i]['translated_answer_start']
                        del qa['answers'][a_i]['translated_text']
                        del qa['answers'][a_i]['translated_answer_start']
                        t_i += 1
                    if not any_answer and not qas[q_i]['is_impossible']:
                        questions_to_delete.append(q_i)
                    for a_i in reversed(to_delete):
                        print("Deleted answer %d/%d" % (q_i,len(qa['answers'])))
                        del qa['answers'][a_i]
                        deleted_answers+=1
            for q_i in reversed(questions_to_delete):
                print("Deleted question %d/%d" % (q_i,len(qas)))
                del qas[q_i]
                deleted_questions += 1

print("Total deleted answers: %d" % deleted_answers)
print("Total deleted questions: %d" % deleted_questions)

    #article['translated'] = True
if True:#mode == "write":
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