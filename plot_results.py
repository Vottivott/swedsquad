import re
import matplotlib.pyplot as plt

fnames = ["results ev_mlbert_en_plus_sv_plus_ot 05.40.09.270718 PM on January 10, 2020.json"]

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