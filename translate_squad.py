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

n_articles = len(data['data'])
skipped = 0

n_questions = 0
t0 = time.time()
to_translate = []
t_i = 0
for mode in ['read', 'write']:
    if mode == 'write':
        translated = translator.translate(to_translate, src='en', dest='sv')
        assert (len(translated) == len(to_translate))
    for i,article in enumerate(sorted(data['data'], key=lambda article: article['title'])):
        if False:
            if 'translated' in article and article['translated'] == True:
                skipped += 1
                continue
            else:
                if skipped > 0:
                    print("Skipped %d already translated articles" % skipped)
                    skipped = 0
            n_questions = 0
            t0 = time.time()
            print("Translating article %d/%d (%s)" % (i+1, n_articles+1, article['title']))
            to_translate = []
            n_paragraphs = len(article['paragraphs'])
            t_i = 0
        for p in article['paragraphs']:
            context = p['context']
            qas = [qa for qa in p['qas']]
            n_questions += len(qas)
            if mode == 'write':
                assert p['context'] == to_translate[t_i]
                p['translated_context'] = translated[t_i].text
                t_i += 1
            else:
                to_translate.append(context)
            for q_i, qa in enumerate(qas):
                if mode == 'write':
                    assert qas[q_i]['question'] == to_translate[t_i]
                    qas[q_i]['translated_question'] = translated[t_i].text
                    t_i += 1
                else:
                    to_translate.append(qas[q_i]['question'])
                for a_i, ans in enumerate(qa['answers']):
                    if mode == 'write':
                        assert qa['answers'][a_i]['text'] == to_translate[t_i]
                        qa['answers'][a_i]['translated_text'] = translated[t_i].text
                        t_i += 1
                    else:
                        to_translate.append(qa['answers'][a_i]['text'])
        article['translated'] = True
    #print("Translated %d paragraphs and %d questions from 1 article in %.2f seconds" % (n_paragraphs, n_questions, time.time()-t0))
    t0 = time.time()
    with open(outname + ".json", "w") as out:
        json.dump(data, out)
    print("Updated file " + outname + ".json in %.2f seconds" % (time.time()-t0))