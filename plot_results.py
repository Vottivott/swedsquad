import re
import matplotlib.pyplot as plt
import os

def get_r(start, latest=False):
    #if start.startswith("3rd_mlbert_only"):
    #    print("!")
    f = get_r_with_prefix("", start, latest)
    if f is None:
        f = get_r_with_prefix("results ", start, latest)
        return f
    else:
        return "results/" + f

def get_r_with_prefix(prefix, start, latest=False):
    if True:#not start.startswith('150k_ev3'):
        #if start.startswith("150k") or \
        if 'proj_' in start or start.startswith('3rd') or start.startswith('12th') or start.startswith('150k_ev3') or start.startswith("160k") or start.startswith("ev_mlbert_cross"):
            return None
    start = prefix + start + " "
    files = os.listdir("./") + os.listdir("./results/")
    print(os.listdir("./results/"))
    found = []
    for f in files:
        if f.startswith(start):
            found.append(f)
    if len(found) == 0:
        print("File starting with " + start + " not found!")
        #raise FileNotFoundError("File starting with " + start + " not found!")
    elif len(found) > 1:
        if latest:
            print("Chose " + str(sorted(found)[-1]) + " out of " + str(sorted(found)))
            return sorted(found)[-1]
        else:
            print("Multiple files starting with " + start + "!")
            #raise FileNotFoundError("Multiple files starting with " + start + "!")
    else:
        return found[0]
    return None



fnames = [{'model':'Multilingual BERT Base cased', 'experiment': 'tränad på eng + naiv sv + ot sv',
           'results': {
               'sv':{
                'file': None},#"results ev_mlbert_en_plus_sv_plus_ot 05.40.09.270718 PM on January 10, 2020.json"},
               'en':{
                'file': get_r('ev_en_eval_mlbert_en_plus_sv_plus_ot')}
           }
          },
           {'model':'Multilingual BERT Base cased', 'experiment': 'tränad på naiv sv',
           'results': {
               'sv':{
                'file': None},#get_r('ev_mlbert_only_sv')},
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
          {'model': 'Multilingual BERT Base cased',
           'experiment': 'tränad på eng fast frågorna är översatta till svenska',
           'results': {
               'sv': {
                   'file': get_r('ev_mlbert_cross_qa_only_en')},
               'en': {
                   'file': get_r('even_mlbert_cross_qa_only_en')}
           }
           },
           {'model': 'Multilingual BERT Base cased',
           'experiment': 'eng + naiv sv + ot + cross sv q/en a + cross en q/sv a',
           'results': {
               'sv': {
                   'file': get_r('ev_mlbert_cross_qa')},
               'en': {
                   'file': get_r('even_mlbert_cross_qa')}
           }
           },

          {'model': 'Multilingual BERT Base cased', 'experiment': 'tränad på naiv sv + ot sv',
           'results': {
               'sv': {
                   'file': None},#get_r('150k_ev_mlbert_sv_plus_ot', latest=True)},
               'en': {
                   'file': get_r('150k_even_mlbert_sv_plus_ot', latest=True)}
           }
           },
          {'model': 'Multilingual BERT Base cased', 'experiment': 'tränad på naiv sv',
           'results': {
               'sv': {
                   'file': None},#get_r('150k_ev_mlbert_only_sv', latest=True)},
               'en': {
                   'file': get_r('150k_even_mlbert_only_sv', latest=True)}
           }
           },

           {'model': 'Multilingual BERT Base cased', 'experiment': 'tränad på naiv sv 3',
           'results': {
               'sv': {
                   'file': get_r('150k_ev3_mlbert_only_sv', latest=True)},
               'en': {
                   'file': get_r('150k_even_mlbert_only_sv', latest=True)}
           }
           },

{'model': 'Multilingual BERT Base cased', 'experiment': 'tränad på naiv sv + ot sv 2',
           'results': {
               'sv': {
                   'file': None},#get_r('160k_ev_mlbert_sv_plus_ot', latest=True)},
               'en': {
                   'file': get_r('160k_even_mlbert_sv_plus_ot', latest=True)}
           }
           },
          {'model': 'Multilingual BERT Base cased', 'experiment': 'tränad på naiv sv 2',
           'results': {
               'sv': {
                   'file': get_r('160k_ev_mlbert_only_sv', latest=True)},
               'en': {
                   'file': get_r('160k_even_mlbert_only_sv', latest=True)}
           }
           },

          {'model': 'Multilingual BERT Base cased', 'experiment': 'tränad på naiv sv + ot sv (1/3 lr)',
           'results': {
               'sv': {
                   'file': get_r('3rd_mlbert_sv_plus_ot', latest=True)},
               'en': {
                   'file': get_r('3rd_even_mlbert_sv_plus_ot', latest=True)}
           }
           },
          {'model': 'Multilingual BERT Base cased', 'experiment': 'tränad på naiv sv (1/3 lr)',
           'results': {
               'sv': {
                   'file': get_r('3rd_mlbert_only_sv', latest=True)},
               'en': {
                   'file': get_r('3rd_even_mlbert_only_sv', latest=True)}
           }
           },

{'model': 'Multilingual BERT Base cased', 'experiment': 'tränad på naiv sv + ot sv (1/6 lr)',
           'results': {
               'sv': {
                   'file': get_r('6th_mlbert_sv_plus_ot', latest=True)},
               'sv_n': {
                   'file': get_r('n6th_mlbert_sv_plus_ot', latest=True)}, # o 3666
               'en': {
                   'file': get_r('6th_even_mlbert_sv_plus_ot', latest=True)}
           }
           },
          {'model': 'Multilingual BERT Base cased', 'experiment': 'tränad på naiv sv (1/6 lr)',
           'results': {
               'sv': {
                   'file': get_r('6th_mlbert_only_sv', latest=True)},
               'en': {
                   'file': get_r('6th_even_mlbert_only_sv', latest=True)}
           }
           },
          {'model': 'Multilingual BERT Base cased', 'experiment': 'tränad på en + naiv sv + ot sv (1/6 lr)',
           'results': {
               'sv': {
                   'file': get_r('6th_mlbert_en_plus_sv_plus_ot', latest=True)},
'sv_n': {
                   'file': get_r('n6th_mlbert_en_plus_sv_plus_ot', latest=True)},
               'en': {
                   'file': get_r('6th_even_mlbert_en_plus_sv_plus_ot', latest=True)}
           }
           },
          {'model': 'Multilingual BERT Base cased', 'experiment': 'tränad på en + proj sv (1/6 lr)',
           'results': {
               'sv': {
                   'file': get_r('6th_mlbert_en_plus_proj_sv', latest=True)},
               'en': {
                   'file': get_r('6th_even_mlbert_en_plus_proj_sv', latest=True)}
           }
           },
          {'model': 'Multilingual BERT Base cased', 'experiment': 'tränad på proj sv (1/6 lr)',
           'results': {
               'sv': {
                   'file': get_r('6th_mlbert_only_proj_sv', latest=True)},
               'en': {
                   'file': get_r('6th_even_mlbert_only_proj_sv', latest=True)}
           }
           },

           {'model': 'Multilingual BERT Base cased', 'experiment': 'tränad på en + projfixed sv (1/6 lr)',
           'results': {
               'sv': {
                   'file': get_r('6th_mlbert_en_plus_projfixed_sv', latest=True)},
               'en': {
                   'file': get_r('6th_even_mlbert_en_plus_projfixed_sv', latest=True)}
           }
           },
          {'model': 'Multilingual BERT Base cased', 'experiment': 'tränad på projfixed sv (1/6 lr)',
           'results': {
               'sv': {
                   'file': get_r('6th_mlbert_only_projfixed_sv', latest=True)},
               'en': {
                   'file': get_r('6th_even_mlbert_only_projfixed_sv', latest=True)}
           }
           },
{'model': 'Multilingual BERT Base cased', 'experiment': 'tränad på en + newprojfixed sv (1/6 lr)',
           'results': {
               'sv': {
                   'file': get_r('6th_mlbert_en_plus_newprojfixed_sv', latest=True)},
               'sv_n': {
                   'file': get_r('n6th_mlbert_en_plus_newprojfixed_sv', latest=True)},
               'en': {
                   'file': get_r('6th_even_mlbert_en_plus_newprojfixed_sv', latest=True)}
           }
           },
          {'model': 'Multilingual BERT Base cased', 'experiment': 'tränad på newprojfixed sv (1/6 lr)',
           'results': {
               'sv': {
                   'file': get_r('6th_mlbert_only_newprojfixed_sv', latest=True)},
               'en': {
                   'file': get_r('6th_even_mlbert_only_newprojfixed_sv', latest=True)}
           }
           },

          {'model': 'Multilingual BERT Base cased',
           'experiment': 'eng + projfixed sv + cross sv q/en a + cross en q/sv a (1/6 lr)',
           'results': {
               'sv': {
                   'file': get_r('6th_mlbert_cross_en_projfixed_sv', latest=True)},
               'en': {
                   'file': get_r('e6th_mlbert_cross_en_projfixed_sv', latest=True)}
           }
           },
{'model': 'Multilingual BERT Base cased', 'experiment': 'en (1/6 lr)',
           'results': {
               'sv': {
                   'file': get_r('6th_mlbert_en', latest=True)},
               'en': {
                   'file': get_r('e6th_mlbert_en', latest=True)}
           }
           },
{'model': 'XLM', 'experiment': 'XLM tränad på eng + newprojfixed sv (1/6 lr)',
           'results': {
               'sv': {
                   'file': get_r('6th_xlm_en_plus_newprojfixed_sv')},
               'en': {
                   'file': get_r('e6th_xlm_en_plus_newprojfixed_sv')}
           }
           },

          {'model': 'Multilingual BERT Base cased', 'experiment': 'tränad på naiv sv + ot sv (1/12 lr)',
           'results': {
               'sv': {
                   'file': get_r('12th_mlbert_sv_plus_ot', latest=True)},
               'en': {
                   'file': get_r('12th_even_mlbert_sv_plus_ot', latest=True)}
           }
           },
          {'model': 'Multilingual BERT Base cased', 'experiment': 'tränad på naiv sv (1/12 lr)',
           'results': {
               'sv': {
                   'file': get_r('12th_mlbert_only_sv', latest=True)},
               'en': {
                   'file': get_r('12th_even_mlbert_only_sv', latest=True)}
           }
           },

{'model': 'Multilingual BERT Base cased', 'experiment': 'v2 tränad på en plus newprojfixed (1/6 lr)',
           'results': {
               'sv': {
                   'file': get_r('6th_v2_mlbert_en_plus_newprojfixed_sv', latest=True)},
               'sv_n': {
                   'file': get_r('n6th_v2_mlbert_en_plus_newprojfixed_sv', latest=True)},
               'en': {
                   'file': get_r('e6th_v2_mlbert_en_plus_newprojfixed_sv', latest=True)}
           }
           },




           {'model': 'XLM', 'experiment': 'XLM tränad på eng',
           'results': {
               'sv': {
                   'file': get_r('ev_xlm_sv')},
               'en': {
                   'file': get_r('even_xlm_sv')}
           }
           },

          {'model': 'Svenska BERT Base, uncased', 'experiment': 'tränad på naiv sv',
           'results': {
               'sv': {
                   'file': get_r('ev_bert_sv_base')},
               'en': {
                   'file': get_r('even_bert_sv_base')}
           }
           },{'model': 'Svenska BERT Base, uncased', 'experiment': 'tränad på naiv sv + ot sv',
           'results': {
               'sv': {
                   'file': get_r('ev_bert_sv_base_plus_ot')},
               'en': {
                   'file': get_r('even_bert_sv_base_plus_ot')}
           }
           },
{'model': 'Svenska BERT Base, uncased', 'experiment': 'svBERT base tränad på newprojfixed sv',
           'results': {
               'sv': {
                   'file': get_r('6th_svbertbase_newprojfixed_sv')},
               'en': {
                   'file': get_r('e6th_svbertbase_newprojfixed_sv')}
           }
 },
{'model': 'Svenska BERT Base, uncased', 'experiment': 'svBERT base tränad på naiv sv + ot sv',
           'results': {
               'sv': {
                   'file': get_r('6th_svbertbase_naive_plus_ot_sv')},
               'en': {
                   'file': get_r('e6th_svbertbase_naive_plus_ot_sv')}
           }
 },
{'model': 'Svenska BERT Base, uncased', 'experiment': 'svBERT base tränad på naiv sv',
           'results': {
               'sv': {
                   'file': get_r('6th_svbertbase_naive_sv')},
               'en': {
                   'file': get_r('e6th_svbertbase_naive_sv')}
           }
 },



           {'model': 'Svenska BERT Large, uncased', 'experiment': 'tränad på naiv sv',
           'results': {
               'sv': {
                   'file': get_r('ev_mlbert_sv_large')},
               'en': {
                   'file': get_r('even_mlbert_sv_large')}
           }
           },
           {'model': 'Svenska BERT Large, uncased', 'experiment': 'ALT1 tränad på naiv sv + ot sv',
           'results': {
               'sv': {
                   'file': get_r('ev_bert_sv_large_plus_ot')},
               'en': {
                   'file': get_r('even_bert_sv_large_plus_ot')}
           }
           },
          {'model': 'Svenska BERT Large, uncased', 'experiment': 'ALT2 tränad på naiv sv + ot sv',
           'results': {
               'sv': {
                   'file': get_r('ev_bert_sv_large_conf_plus_ot')},
               'en': {
                   'file': get_r('even_bert_sv_large_conf_plus_ot')}
           }
           }
          ]






def group_keys(d):
    result = {}
    for key in d.keys():
        s = re.search("_([0-9]+)$", key)
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

labels = []

for m in fnames:
    model = m['model']
    exp = m['experiment']
    for lang,result in m['results'].items():
        if lang is "sv_n":
            print(lang)
        if result['file'] is not None and lang != 'en':
            with open(result['file']) as f:
                d = eval(f.read())
                g = group_keys(d)
                print(g.keys())
                #print(g['f1'].keys())
                if exp == "tränad på naiv sv 2":
                    print("!")


                if "best_f1" in g:
                    plotvar_f1 = "best_f1"
                    plotvar_em = "best_exact"
                else:
                    plotvar_f1 = "f1"
                    plotvar_em = "exact"
                plot(g[plotvar_f1])
                if ('x' in g[plotvar_f1]):
                    plt.text(g[plotvar_f1]['x'][-1],g[plotvar_f1]['y'][-1],"%.2f" % g[plotvar_f1]['y'][-1])
                best_f1 = max(g[plotvar_f1]['y'])
                best_f1_i = max(range(len(g[plotvar_f1]['y'])), key=lambda i:g[plotvar_f1]['y'][i])
                best_em = g[plotvar_em]['y'][best_f1_i]
                labels.append(('%.2f/%.2f %s/%s (%s) ' % (best_f1, best_em, plotvar_f1, plotvar_em, lang)) + exp)
                #plot(g['exact'])

plt.legend(labels)
#plt.legend(['f1','exact'])
plt.title('Multilingual BERT tränad på eng + naiv sv + ot sv')

plt.show()