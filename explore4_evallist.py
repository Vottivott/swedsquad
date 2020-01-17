class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

import json

#fname = "dev-v2.0.json"
#fname = 'translated_dev-v2.0 06.35.01.949109 PM on December 06, 2019.json'
#fname = 'translated_train-v2.0 01.28.26.007134 AM on December 07, 2019.json'
#fname = "translated dev exclude problematic.json"
fname ="translated train answers translated.json"
fname ="translated dev answers translated.json"
#fname ="confident_translated_dev_no_impossible.json"
#fname = "original_plus_confident_translated_train_no_impossible.json"
fname ="swe_squad_bert_project.json"
fname ="swe_squad_bert_project_ext.json"
fname = "train-v2.0.json"
fname = "dev_only_projfixed_sv_no_impossible"
#fname = "dev_ext_2_ext_5_multialt.json"
fname ="swe_squad_bert_project_ext_dev.json"
fname ="swe_squad_bert_project_ext_dev_new.json"


with open(fname,"r", encoding='utf-8') as f:
    data = json.loads(f.read())['data']


en_fname = "dev-v2.0.json"
with open(en_fname,"r", encoding='utf-8') as f:
    en_data = json.loads(f.read())['data']
en_questions = {}
for i,article in enumerate(en_data):
    for j, p in enumerate(article['paragraphs']):
        for q_i, qa in enumerate(p['qas']):
            for a_i,a in enumerate(qa['answers']):
                en_questions[(qa['id'],a_i)] = (qa, a, p)


structured_list = []

questions = []
num_questions = []
num_problematic = 0
num_quote_containing = 0
num_weird_quote_containing = 0
num_translated_articles = 0
num_mult_answers = 0
num_more_problematic = 0
num_answers = 0
num_naive_matches = 0
num_naive_matchquestions = 0
translated_answer_matchcounts = []
num_answers_individually = []
num_answerable_questions = 0
ids = []
for article in data:
    if 'translated' in article and article['translated']:
        num_translated_articles+=1
    for p in article['paragraphs']:
        context = p['context']
        if 'translated_context' in p:
            translated_context = p['translated_context']
        else:
            translated_context = "None"
        #print(p['context_html_exclude_problematic'])
        #print()
        #print(p['translated_context_html_exclude_problematic'])
        #print()
        #print()
        qas = p['qas']
        for qa in qas:
            questions.append(qa['question'])
            ids.append(qa['id'])
            if not qa['is_impossible']:
                num_answerable_questions += 1
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
            s = qa['answers'][0]['answer_start']
            e = s+len(qa['answers'][0]['text'])
            #print(context[s:e])
            #print(qa['answers'][0]['text'])
            num_answers += len(qa['answers'])
            num_answers_individually.append(len(qa['answers']))
            any_naive_answer = False
            for a in qa['answers']:

                # if a['answer_start']+len(a['text']) > len(context) or a['answer_start'] < 0:
                #     print(a['answer_start'])
                #     print(a['text'])
                #     print(len(context))
                #     #print(context)
                #     a = qa['answers'][0]
                #     print(bcolors.BOLD + qa['translated_question'] + bcolors.ENDC)
                #     s = a['answer_start']
                #     e = s + len(a['text'])
                #     tx = translated_context[:s] + bcolors.FAIL + bcolors.BOLD + translated_context[
                #                                                                 s:e] + bcolors.ENDC + translated_context[
                #                                                                                       e:]
                #     print(tx)
                #     print("(naiv: %s%s%s   proj: %s%s%s)" % (
                #     bcolors.BOLD, a['translated_text'], bcolors.ENDC, bcolors.BOLD + bcolors.FAIL, a['text'],
                #     bcolors.ENDC + bcolors.ENDC))
                #     print()

                if translated_context == 'None':
                    translated_answer_num_ocurrences = 0
                    translated_answer_cap_num_ocurrences =0
                    translated_answer_lower_num_ocurrences=0
                else:
                    translated_answer_num_ocurrences = translated_context.count(a['translated_text'])
                    translated_answer_cap_num_ocurrences = translated_context.count(a['translated_text'].capitalize())
                    translated_answer_lower_num_ocurrences = translated_context.count(a['translated_text'].lower())
                if translated_answer_num_ocurrences == 1:
                    num_naive_matches += 1
                    any_naive_answer = True
                    if False:
                        print(bcolors.BOLD+qa['translated_question']+bcolors.ENDC)
                        s = translated_context.find(a['translated_text'])
                        e = s+len(a['translated_text'])
                        tx = translated_context[:s] +bcolors.FAIL+bcolors.BOLD+translated_context[s:e]+bcolors.ENDC+translated_context[e:]
                        print(tx)
                        print()
                #elif translated_answer_num_ocurrences == 0:
                #    if translated_answer_lower_num_ocurrences == 1:
                #        num_naive_matches += 1
                #    elif translated_answer_lower_num_ocurrences == 0:
                #        if translated_answer_cap_num_ocurrences == 1:
                #            num_naive_matches += 1
                elif translated_answer_num_ocurrences == 0:
                    if False:
                        print(bcolors.BOLD + qa['translated_question'] + bcolors.ENDC)
                        tx = a['text'] + bcolors.FAIL + bcolors.BOLD+ a['translated_text']  + bcolors.ENDC
                        print(tx)
                        print(translated_context)


                translated_answer_matchcounts.append(translated_answer_num_ocurrences)

                #print(a['text'])
                #print(a['translated_text'])
                positions.append((a['answer_start'], a['answer_start'] + len(a['text'])))
            if any_naive_answer:
                num_naive_matchquestions += 1
            elif False:#len(qa['answers']):
                for a in qa['answers']:
                    #a = qa['answers'][0]
                    print(bcolors.BOLD + qa['translated_question'] + bcolors.ENDC)
                    s = a['answer_start']
                    e = s + len(a['text'])
                    tx = translated_context[:s] + bcolors.FAIL + bcolors.BOLD + translated_context[
                                                                                s:e] + bcolors.ENDC + translated_context[e:]
                    print(tx)
                    print("(naiv: %s%s%s   proj: %s%s%s)" % (bcolors.BOLD,a['translated_text'],bcolors.ENDC,bcolors.BOLD+bcolors.FAIL,a['text'],bcolors.ENDC+bcolors.ENDC))
                    print()

            for a_i,a in enumerate(qa['answers']):
                structured_list.append((qa, a, p, a_i))



            if False:#qa['question']=="What formed behind blockages?":#qa['translated_question']=="Vad bildades bakom blockeringar?":#'sjöar' in context:
                a = qa['answers'][0]
                if 'translated_question' not in qa:
                    qa['translated_question'] = qa['question']
                    a['translated_text'] = a['text']
                    translated_context = p['context']
                print(qa['question'])
                print(bcolors.BOLD + qa['translated_question'] + bcolors.ENDC)
                s = a['answer_start']
                e = s + len(a['text'])
                tx = translated_context[:s] + bcolors.FAIL + bcolors.BOLD + translated_context[
                                                                            s:e] + bcolors.ENDC + translated_context[e:]
                print(tx)
                print("(naiv: %s%s%s   proj: %s%s%s)" % (
                bcolors.BOLD, a['translated_text'], bcolors.ENDC, bcolors.BOLD + bcolors.FAIL, a['text'],
                bcolors.ENDC + bcolors.ENDC))
                print()

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

# Earlier version, all those are now fixed:
# correct_answer_wrong_position = [15, 22, 47, 52, 72]
# correct_answer_wrong_position_but_still_good = [26]

next_index = 0#100#100 (22)
errors = []

serious_missing_word_errors = [32] # 'cut off the French frontier forts' / avbröt 'framgångsrikt de franska gränsfortarna'
benign_errors = [10] # Corrected '185'5 to '1855' probably impossible because 1855 is one token?
added_word_but_still_good = [95]
minor_missing_word_errors = [11] # 'political activity caused exploitation' / orsakade 'politisk verksamhet utnyttjande'
huge_missing_word_errors = [75] # de flesta ord saknas
correct_answer_wrong_position = []
correct_answer_wrong_position_but_still_good = []
minor_missing_letter_logical = [31]
minor_missing_dollar_sign = [3]

if next_index > 0:
    errors = len(serious_missing_word_errors) + len(huge_missing_word_errors) + len(correct_answer_wrong_position) + len(correct_answer_wrong_position_but_still_good)
    print("Current error rate: %.2f%%" % (100.0*(float(errors) / next_index)))


import random
random.seed(42)
order = list(range(20302))
random.shuffle(order)
print(order[:5]) # Should be [7768, 10891, 93, 10620, 8756]
for i,n in enumerate(order[next_index:500]):
    i+=next_index
    qa, a, p, a_i = structured_list[n]
    qa_en, a_en, p_en = en_questions[(qa['id'], a_i)]
    #if 'translated_question' not in qa:
    #    qa['translated_question'] = qa['question']
    #    a['translated_text'] = a['text']
    #    translated_context = p['context']
    #else:
    translated_context = p['translated_context']
    #context = p['context']
    print(qa['question'])
    print(bcolors.BOLD + str(i) + ": " + qa['translated_question'] + bcolors.ENDC)
    s = a['answer_start']
    e = s + len(a['text'])
    tx = translated_context[:s] + bcolors.FAIL + bcolors.BOLD + translated_context[
                                                                s:e] + bcolors.ENDC + translated_context[e:]
    print(tx)
    print("( %s%s%s / %s%s%s / %s%s%s )" % (
        bcolors.BOLD, a['translated_text'], bcolors.ENDC, bcolors.BOLD+bcolors.OKBLUE, a_en['text'], bcolors.ENDC+bcolors.ENDC,
        bcolors.BOLD + bcolors.FAIL, a['text'],
        bcolors.ENDC + bcolors.ENDC))

    #print(en_questions.keys())
    #qa, a, p = en_questions[(qa['id'],a_i)]
    context = p_en['context']

    s = a_en['answer_start']
    e = s + len(a_en['text'])
    tx = context[:s] + bcolors.OKBLUE + bcolors.BOLD + context[
                                                            s:e] + bcolors.ENDC + context[e:]
    print(tx)
    print()


#random.shuffle(questions)



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
print("Number of naive translated-answer matches: %d (%.2f %%)" % (num_naive_matches, 100*(num_naive_matches/num_answers)))
print("Number of questions with naive translated-answer match: %d (%.2f %% of questions that have answers)" % (num_naive_matchquestions, 100*(num_naive_matchquestions/num_answerable_questions)))
print("Number of possible questions without naive translated-answer match: %d (%.2f %% of all questions)" % (num_answerable_questions-num_naive_matchquestions, 100*((num_answerable_questions-num_naive_matchquestions)/sum(num_questions))))
print("Number of questions either impossible or with a naive translated-answer match: %d (%.2f %% of all questions)" % ((sum(num_questions)-num_answerable_questions)+num_naive_matchquestions, 100*(((sum(num_questions)-num_answerable_questions)+num_naive_matchquestions)/sum(num_questions))))
print("Max number of answers for question: %d" % max(num_answers_individually))
print("Avg number of answers for question: %.2f" % (sum(num_answers_individually)/num_answerable_questions))
print("Avg number of naive answers for question: %.2f" % (num_naive_matches/num_answerable_questions))
#print("Avg number of naive answers for question: %.2f" % (sum(num_naive_matches)/len(num_answers_individually)))
#print()
print(set([len(id) for id in ids]))
exit(0)
import matplotlib.pyplot as plt
plt.hist(translated_answer_matchcounts, bins=100, color='orange')
plt.title("DEV: Number of perfect matches of translated answer in translated paragraph")
plt.xlim([0,10])
plt.show()