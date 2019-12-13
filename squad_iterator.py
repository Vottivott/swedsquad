from googletrans import Translator

from html_parser import get_answers_and_answer_starts, strip_html_tags

translator = Translator()

def get_questions(qas):
    positions = []
    questions = []
    for qa in qas:
        if len(qa['answers']) == 0:
            continue
        for a in qa['answers']:
            span = (a['answer_start'], a['answer_start'] + len(a['text']))
            if span not in positions:
                positions.append(span)
                questions.append((qa['question'],qa['translated_question']))
    s = ""
    for i,(en,sv) in enumerate(questions):
        s+=str(i)+") " + sv + "//" + en + "//\\\\"
        s+="\n"
    return s

def get_html(paragraph, qas):
    positions = []
    for qa in qas:
        if len(qa['answers']) == 0:
            continue
        for a in qa['answers']:
            span = (a['answer_start'], a['answer_start'] + len(a['text']))
            if span not in positions:
                positions.append(span)
    txt = paragraph#" " * len(paragraph)

    #for start,end in positions:
    #    for s,e in positions:
    #        if (s,e) != (start,end):
    #            if s < start < e and end > e:
    #                print("!")

    # Todo: Split the text into pieces by cutting at all start and end positions. keep track of which pieces should not have any span.
    #       For each answer, make a list of the ids of the pieces that need to be concatenated to get that answer.
    #       Then I can also keep all answers in the list without having to ignore duplicates
    pieces_for_answer = [[] for answer in range(len(positions))]

    problem = set()
    for i, (start, end) in enumerate(positions):
        for s, e in positions:
            if (s, e) != (start, end):
                if s < start < e and end > e:
                    problem.add(i)
                    #print(txt[start:e] + "|" + txt[e:end])



    original_positions = list(positions)

    for id, (start, end) in enumerate(positions):

        if id in problem:
            continue
            start_tag = "<!--start %d-->" % id
            end_tag = "<!--end %d-->" % id
            #start_tag = "<prob id=\"%d\">" % id
            #end_tag = "</prob id=\"%d\">" % id
        else:
            start_tag = "<span id=\"%d\">" % id
            end_tag = "</span>"#"</span id=\"%d\">" % id

        txt = txt[:start] + start_tag + txt[start:end] + end_tag + txt[end:]
        for i in range(id+1,len(positions)):
            s, e = positions[i]

            # Make sure tags are nested correctly
            if s == start and e < end:
                s = s + len(start_tag)
            else:
                s = s + len(start_tag) + len(end_tag) if s >= end else (s + len(start_tag) if s >= start + 1 else s)
            if e == end and s > start:
                e = e + len(start_tag)
            else:
                e = e + len(start_tag)+len(end_tag) if e >= end else (e + len(start_tag) if e >= start+1 else e)


            #s, e = [pos + len(start_tag)+len(end_tag) if pos >= end else (pos + len(start_tag) if pos >= start+1 else pos) for pos in (s, e)]
            #s, e = [pos + 2 if pos >= end else (pos + 1 if pos >= start+1 else pos) for pos in (s, e)]
            positions[i] = (s, e)
    #r = txt.replace(" ", "")
    #problematic = r.find("<<") != -1 or r.find(">>") != -1
    if 'Three addition' in paragraph:
        print("Problems:")
        print(len(problem))
        print(txt)
        print()
        print(paragraph)
        print()
        print("\n".join(map(str,original_positions)))
    #print()
    return txt

def interpret_html(html, paragraph, qas):
    positions = []
    span_id = {}
    for q_i, qa in enumerate(qas):
        if len(qa['answers']) == 0:
            continue
        for a_i,a in enumerate(qa['answers']):
            span = (a['answer_start'], a['answer_start'] + len(a['text']))
            if span not in positions:
                positions.append(span)
            span_id[(q_i, a_i)] = positions.index(span)

    txt = paragraph#" " * len(paragraph)

    # Done: If a span has been split into multiple, take the start of the earliest one and the end of the last one
    # TODO: Remove untranslated answers where impossible=False, or questions with no translated answers
    answer_text, answer_start = get_answers_and_answer_starts(html)

    for q_i, qa in enumerate(qas):
        if len(qa['answers']) == 0:
            continue
        for a_i,a in enumerate(qa['answers']):
            span = (a['answer_start'], a['answer_start'] + len(a['text']))
            id = span_id[(q_i, a_i)]
            if id not in answer_start:
                continue # Skipped because problematic
            a['translated_answer_start'] = answer_start[id]
            a['translated_text'] = answer_text[id]
            #print(a['text'])
            #print(a['translated_text'])


import json
import datetime
import time

#fname = "train-v2.0"
#name = "dev-v2.0"
#name = "train-v2.0"
#name = "translated_dev-v2.0 no answers"
name = "translated_train-v2.0 no answers"
#name = "translated dev exclude problematic"
#name = "translated dev exclude problematic interpreted"
#name = ""
date = datetime.datetime.now().strftime("%I.%M.%S.%f %p on %B %d, %Y")
outname = "translated_" + name + " " + date
with open(name+".json","r", encoding="utf-8") as f:
    data = json.loads(f.read())

n_articles = len(data['data'])
skipped = 0

translate_answers = True

n_questions = 0
t0 = time.time()
to_translate = []
t_i = 0
for mode in ['read', 'write']:#['read', 'write']:
#for mode in ['read', 'write']:
    if mode == 'write':
        with open("translated train answers.txt", encoding="utf-8") as f:
            translated = f.read().splitlines()
        assert (len(translated) == len(to_translate))
    paragraph_index = 0
    for i,article in enumerate(sorted(data['data'], key=lambda article: article['title'])):
        for p in article['paragraphs']:
            context = p['context']
            qas = [qa for qa in p['qas']]
            n_questions += len(qas)
            if False:
                if mode == 'write':
                    html = ("<div id=\"%d\">" % paragraph_index) + get_html(context, qas) + "</div>"
                    assert html == to_translate[t_i]
                    p['translated_context_html_exclude_problematic'] = translated[t_i]#.text
                    p['context_html_exclude_problematic'] = html#.text
                    t_i += 1

                    #to_translate.append(html)
                    paragraph_index += 1
                else:
                    #html = ("<div id=\"%d\">" % paragraph_index) + get_html(context, qas) + "</div>"
                    html = p['translated_context_html_exclude_problematic']
                    p['translated_context_cloud'] = strip_html_tags(html)
                    interpret_html(html, context, qas)
                    #to_translate.append(get_questions(qas))
                    to_translate.append(html)
                    paragraph_index += 1
            include_questions = True
            if include_questions:
                for q_i, qa in enumerate(qas):
                    if False:
                        if mode == 'write':
                            assert qas[q_i]['question'] == to_translate[t_i]
                            qas[q_i]['translated_question'] = translated[t_i]#.text
                            t_i += 1
                        else:
                            to_translate.append(qas[q_i]['question'])
                    if translate_answers:
                        for a_i, ans in enumerate(qa['answers']):
                            if mode == 'write':
                                assert qa['answers'][a_i]['text'] == to_translate[t_i]
                                qa['answers'][a_i]['translated_text'] = translated[t_i]#.text
                                t_i += 1
                            else:
                                to_translate.append(qa['answers'][a_i]['text'])
        #article['translated'] = True
    if mode == "write":
        t0 = time.time()
        with open(outname + ".json", "w") as out:
           json.dump(data, out)
        print("Updated file " + outname + ".json in %.2f seconds" % (time.time()-t0))
    with open("to_translate.txt","w", encoding="utf-8") as out:
        out.write("\n".join([txt.replace("\n"," ") for txt in to_translate]))
    print(len(to_translate))



    #print("Translated %d paragraphs and %d questions from 1 article in %.2f seconds" % (n_paragraphs, n_questions, time.time()-t0))
    #t0 = time.time()
    #with open(outname + ".json", "w") as out:
    #    json.dump(data, out)
    #print("Updated file " + outname + ".json in %.2f seconds" % (time.time()-t0))