from collections import defaultdict
from math import log, e, log10
import sys, fileinput
from time import time

string_tree = ""
chart = defaultdict(list)
backpointer = defaultdict(dict)
dict_rules_prob = defaultdict(list)

def fill_chart(txt):
    global dict_rules_prob
    global string_tree
    global chart
    global backpointer
    for k in range(1, len(txt)+1):        
        for i in range(0, len(txt)):
            for j in range(i+1, len(txt)+1):
                if j-i == k:
                    if k == 1:
                        if not txt[i] in dict_rules_prob:
                            chart[(i,j)] = dict_rules_prob["<unk>"]
                        else:
                            chart[(i,j)] = dict_rules_prob[txt[i]]
                        for it in chart[(i,j)]:
                            backpointer[(i,j)][it[0]] = [-1, txt[i], txt[i]]
                    else:
                        for l in range(i+1,j):
                            temp = ""
                            probtemp = 0
                            for itemi in chart[(i,l)]:
                                for itemj in chart[(l,j)]:
                                    temp = itemi[0] + " " + itemj[0]
                                    probtemp = float(itemi[1]) + float(itemj[1])
                                    if temp in dict_rules_prob:
                                        for rule in dict_rules_prob[temp]:
                                            flag = False
                                            for dd in range(len(chart[(i,j)])):
                                                if rule[0] == chart[(i,j)][dd][0]:
                                                    flag = True
                                                    if (float(rule[1])+probtemp > chart[(i,j)][dd][1]):
                                                        chart[(i,j)][dd][1] = float(rule[1])+probtemp
                                                        backpointer[(i,j)][chart[(i,j)][dd][0]] = [l, itemi[0], itemj[0]]
                                                        
                                            if not flag:
                                                chart[(i,j)].append([rule[0], float(rule[1])+probtemp])
                                                backpointer[(i,j)][rule[0]] = [l, itemi[0], itemj[0]]

def createTree(root, necessary_string, left, right):
    global dict_rules_prob
    global string_tree
    global chart
    global backpointer
    global string_tree
    string_tree += "(" + necessary_string + " "
    if root[necessary_string][0] == -1:
        string_tree += root[necessary_string][1] + ") "
        return
    if not root[necessary_string][0] == -1:
        createTree(backpointer[(left, root[necessary_string][0])], root[necessary_string][1], left, root[necessary_string][0])
        createTree(backpointer[(root[necessary_string][0], right)], root[necessary_string][2], root[necessary_string][0], right)
    string_tree = string_tree[:-1]
    string_tree += ") "
    
def main():
    global dict_rules_prob
    global string_tree
    global chart
    global backpointer
    global reg
    
    d = defaultdict(int)
    d2 = defaultdict(int)
    fname="all.rules"
    with open(fname) as f:
	    content=f.readlines()
    content=[x.strip() for x in content]
    for ii in content:
        split_ii = ii.split(" ", 1)
        d[split_ii[1]] += int(split_ii[0])

    fname="left.count"
    with open(fname) as f:
	    content=f.readlines()
    content=[x.strip() for x in content]

    for ii in content:
        split_ii = ii.split()
        d2[split_ii[1]] += int(split_ii[0])

    stri = ""
    for ii in d.keys():
        dict_rules_prob[ii.split(" -> ")[1]].append([ii.split(" -> ")[0], log(float(d[ii])/d2[ii.split(" -> ")[0]])])
        
    content = []
    for line in fileinput.input():
        content.append(line.strip())
    parse_time = []
    sent_length = []
    string_to_write = ""
    sent_length_fit = []
    predicted_values = []
    plot_val = []
    for ii in content:
        chart = defaultdict(list)
        backpointer = defaultdict(dict)
        string_tree = ""
        sent_length.append(len(ii.split()))
        sent_length_fit.append(log10(len(ii.split())))
        start_time = 0
        duration = 0
        start_time = time()
        fill_chart(ii.split())
        try:
            createTree(backpointer[(0, len(ii.split()))], 'TOP', 0, len(ii.split()))
        except:
            duration = time() - start_time
            parse_time.append(duration)
            string_to_write += " \n"
            continue
        duration = time() - start_time
        parse_time.append(duration)
        string_to_write += string_tree.strip() + "\n"
    '''
    parse_time_fit = []
    for ii in parse_time:
        parse_time_fit.append(log10(ii))
    '''
    with open("dev.parses", "w+") as f:
        f.write(string_to_write)
    '''    
    polyfit_ret = np.polyfit(sent_length_fit, parse_time_fit, 1)
    y_values = []
    for ii in sent_length:
        y_values.append((10 ** polyfit_ret[1]) * (ii ** polyfit_ret[0]))
    plt.loglog(sent_length, y_values, linewidth = 1, color="red", basex=10)
    plt.loglog(sent_length, parse_time, '.', linewidth = 1, color="blue", basex=10)
    plt.suptitle('Parse Time vs Sentence Length\nslope = m = '+str(polyfit_ret[0]), fontsize=11, fontweight='bold')
    plt.ylabel('Parse_time')
    plt.xlabel('Sentence_length')
    plt.show()
    '''
    
main()
