import random

with open("translated dev html.txt", encoding="utf-8") as f:
    lines = f.read().splitlines()


with open("translated questions dev exclude problematic.txt", encoding="utf-8") as f:
    questions = f.read().splitlines()


random.seed(0)

order = list(range(len(lines)))
random.shuffle(order)
lines = [lines[order[i]] for i in range(len(lines))]
questions = [questions[order[i]] for i in range(len(questions))]
spans = 0
total_num_spans = 9752#20302 - 425 # total number of answers - problematic answers
txt = ""
for i,(line,ques) in enumerate(zip(lines,questions)):
    print("[  ] [  ] [  ] :%s" % (line[:min(100,len(line))]))
    txt+="[  ] [  ] [  ] :%s" % (line[:min(100,len(line))])
    spans += line.count("<span")
    #print("%d spans = %.2f %%" % (spans,100*spans/total_num_spans))
    print("\n\\\\ "+"\n".join(ques.split("//")))
    txt+="\n\\\\ "+"\n".join(ques.split("//"))
    txt+="\n"
    print()
with open("questions test.txt", "w", encoding="utf-8") as f:
    f.write(txt)
print("Done")