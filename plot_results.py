import re
import matplotlib.pyplot as plt
import os


def get_r(start):
    start = "results " + start
    files = os.listdir("./")
    found = []
    for f in files:
        if f.startswith(start):
            found.append(f)
    if len(found) == 0:
        raise FileNotFoundError("File starting with " + start + " not found!")
    elif len(found) > 0:
        raise FileNotFoundError("Multiple files starting with " + start + "!")
    else:
        return found[0]



fnames = [{'model':'Multilingual BERT Base cased', 'experiment': 'tränad på eng + naiv sv + ot sv',
           'results': {
               'sv':{
                'file': "results ev_mlbert_en_plus_sv_plus_ot 05.40.09.270718 PM on January 10, 2020.json"},
               'en':{
                'file': get_r('ev_en_eval_mlbert_en_plus_sv_plus_ot')}
           }
          },
           {'model':'Multilingual BERT Base cased', 'experiment': 'tränad på naiv sv',
           'results': {
               'sv':{
                'file': get_r('ev_mlbert_only_sv')},
               'en':{
                'file': get_r('even_mlbert_only_sv')}
           }
          },
           {'model':'Multilingual BERT Base cased', 'experiment': 'tränad på eng + naiv sv + ot sv + kinesiska',
           'results': {
               'sv':{
                'file': get_r('ev_mlbert_en_plus_sv_plus_ot_plus_chinese')},
               'en':{
                'file': get_r('even_mlbert_en_plus_sv_plus_ot_plus_chinese')}
               # Maybe add chinese?
           }
          },
           {'model':'Multilingual BERT Base cased', 'experiment': 'tränad på eng + naiv sv',
           'results': {
               'sv':{
                'file': get_r('ev_mlbert_en_plus_sv')},
               'en':{
                'file': get_r('even_mlbert_en_plus_sv')}
           }
          },
          {'model': 'Multilingual BERT Base cased', 'experiment': 'tränad på eng',
           'results': {
               'sv': {
                   'file': get_r('ev_mlbert_en')},
               'en': {
                   'file': get_r('even_mlbert_en')}
           }
           },
          {'model': 'Multilingual BERT Base cased', 'experiment': 'tränad på eng fast frågorna är översatta till svenska',
           'results': {
               'sv': {
                   'file': get_r('ev_mlbert_cross_qa_only_en')},
               'en': {
                   'file': get_r('even_mlbert_cross_qa_only_en')}
           }
           },

          ]






def group_keys(d):
    result = {}
    for key in d.keys():
        s = re.search("_([0-9]+)", key)
        if s is not None:
            var = key[:s.start()]
            n = s.groups()[0]
            if var not in result:
                result[var] = {}
            result[var][int(n)] = d[key]
        else:
            result[key] = d[key]
    for key in result.keys():
        if type(result[key]) is dict:
            x = sorted(result[key].keys())
            result[key] = {'x': x, 'y': [result[key][x_key] for x_key in x]}
    return result

def plot(v):
    plt.plot(v['x'],v['y'])

for fname in fnames:
    with open(fname) as f:
        d = eval(f.read())
        g = group_keys(d)
        print(g.keys())
        #print(g['f1'].keys())
        plot(g['f1'])
        plot(g['exact'])

plt.legend(['f1','exact'])
plt.title('Multilingual BERT tränad på eng + naiv sv + ot sv')

plt.show()