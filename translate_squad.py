from googletrans import Translator

translator = Translator()





import json
import datetime
import time

#fname = "train-v2.0"
name = "dev-v2.0"
date = datetime.datetime.now().strftime("%I.%M.%S.%f %p on %B %d, %Y")
outname = "translated_" + name + " " + date
with open(name+".json","r") as f:
    data = json.loads(f.read())

data['data'] = sorted(data['data'])

n_articles = len(data['data'])
skipped = 0
for i,article in enumerate(data['data']):
    if 'translated' in article and article['translated'] == True:
        skipped += 1
        continue
    else:
        if skipped > 0:
            print("Skipped %d already translated articles" % skipped)
            skipped = 0
    n_questions = 0
    t0 = time.time()
    print("Translating article %d/%d" % (i, n_articles))
    to_translate = []
    n_paragraphs = len(article['paragraphs'])
    t_i = 0
    for mode in ['read', 'write']:
        if mode == 'write':
            translated = translator.translate(to_translate, src='en', dest='sv')
            assert(len(translated) == len(to_translate))
        for p in article['paragraphs']:
            context = p['context']
            questions = [qa['question'] for qa in p['qas']]
            n_questions += len(questions)
            if mode == 'write':
                assert p['context'] == to_translate[t_i]
                p['context'] = translated[t_i].text
                t_i += 1
            else:
                to_translate.append(context)
            for q_i, question in enumerate(questions):
                if mode == 'write':
                    assert questions[q_i] == to_translate[t_i]
                    questions[q_i] = translated[t_i].text
                    t_i += 1
                else:
                    to_translate.append(question)
    article['translated'] = True
    print("Translated %d paragraphs and %d questions from 1 article in %.2f seconds" % (n_paragraphs, n_questions, time.time()-t0))
    t0 = time.time()
    with open(outname + ".json", "w") as out:
        out.write(json.dump(data, out))
    print("Updated file " + outname + ".json in %.2f seconds" % (time.time()-t0))