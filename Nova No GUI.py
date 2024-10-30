def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter
import inflection
import re
import sys
import os


# reading the input text using the chosen path in _search()_
input_txt = open("text.txt", "r", encoding="utf8")
tag_cleaner = re.compile('<.*?>|/&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')  # removing tags from input text
input_string = re.sub(tag_cleaner, '', input_txt.read())  # defining tag-cleaned input string

def text2word(text):  # removing all special Characters
    result = re.findall('[\w]+', text.lower())
    return result

full_string_list = text2word(input_string)

no_numbers = [re.sub('[0-9]', '', i) for i in full_string_list]
# Defining and applying word length cut off
maximum = 25  # input("Choose upper cut for word lenght: ")
minimum = 3  # input("Choose lower cut for word lenght: ")
input_words = [word for word in no_numbers if int(maximum) > len(word) > int(minimum)]

# importing stop word txt
stop_txt = open(resource_path("stop-en.txt"), "r", True, "utf-8")
stop_words_list = stop_txt.read().split('\n')  # converting stop word string to list
low_list = []
for x in stop_words_list:
    low_list.append(x.lower())


for word in list(input_words):
    if word in low_list or word.isdigit():  # Wipe stop words and string digits
        input_words.remove(word)

output_words = [inflection.singularize(plural) for plural in input_words]   # Combines singulars and plurals into singulars

count_criteria = 20 # input("Choose count minimum: ")  # Define or take user input for count exclusion criteria
counted_words = Counter(output_words)
exclusion_list = []
for word in counted_words:
    if counted_words[word] < 1:
        exclusion_list.append(word)
inclusion_list = []
for word in output_words:
    if word not in exclusion_list:
        inclusion_list.append(word)  # Makes list of all words, not in exclusion list

inclusion_list = [x.title() for x in inclusion_list]  # capitalizes/lowers/titles displayed words
ordered_inclusion_list = [item for items, c in Counter(inclusion_list).most_common()
                          for item in [items] * c]
counted_words = Counter(ordered_inclusion_list)
final_dictionary = {i: ordered_inclusion_list.count(i) for i in counted_words}  # ordered and counted inclusion list
key_list = list(final_dictionary.keys())  # Lists the words in descending (count)order
counts_list = list(final_dictionary.values())  # Lists counts of the words in descending order

print(final_dictionary)

# Coocurences
bigrams = Counter()
for previous, current in zip(inclusion_list, inclusion_list[1:]):  # Checking for (vica-versa) bigrams
    opt1 = f"{previous}", f"{current}"
    opt2 = f"{current}", f"{previous}"
    if opt2 not in bigrams:
        bigrams[opt1] += 1
        continue
    bigrams[opt2] += 1 #
coocurences = dict(bigrams)

for key in list(coocurences.keys()):  # Checking for (same-same) bigrams
    if key[0] == key[1]:
        del coocurences[key]

total = sum(coocurences.values())
new_dict = {k: (v / total) * 100 for k, v in coocurences.items()}

graph = nx.Graph()
# plt.style.use('dark_background')

for x, y in new_dict.items():
    graph.add_weighted_edges_from([[str(x[0]), str(x[1]), 100 * y]])

messy_a_counts = list(map(final_dictionary.get, list(graph.nodes)))
node_size_list = []
for i in messy_a_counts:
    node_size_list.append((i / sum(counts_list)) * 4000)  # creates the node size list

pos = nx.spring_layout(graph, weight='weight')

node_color_map = []
for node in node_size_list:
    if 0 < (node / 4000) < 0.001:
        node_color_map.append('green')
    elif 0.001 < (node / 4000) < 0.003:
        node_color_map.append('lawngreen')
    elif 0.003 < (node / 4000) < 0.005:
        node_color_map.append('springgreen')
    elif 0.005 < (node / 4000) < 0.015:
        node_color_map.append('aquamarine')
    elif 0.015 < (node / 4000) < 0.02:
        node_color_map.append('cyan')
    elif 0.02 < (node / 4000) < 0.025:
        node_color_map.append('deepskyblue')
    elif 0.025 < (node / 4000) < 0.07:
        node_color_map.append('dodgerblue')
    elif 0.07 < (node / 4000) or node == max(node_size_list):
        node_color_map.append('red')

edge_width_list = []
for i in new_dict.values():
    edge_width_list.append(i/250)

# colors = ["black", "skyblue", "powderblue", "white"]
# edgesList = []
# for i in edge_width_list:
#     if i not in edgesList:
#         edgesList.append(i)

# edgesList = sorted(edgesList, reverse=True)
# print(edgesList)


# edge_color_map = []    

# for i in edge_width_list:
#     edge_color_map.append(colors[edgesList.index(i)])

print(sorted(edge_width_list))
# print(edge_color_map)


edge_color_map = []
for edge in edge_width_list:
    if edge > 0.01:
        edge_color_map.append('dodgerblue')    
    elif edge > 0.007:
        edge_color_map.append('springgreen')
    elif edge > 0.005:
         edge_color_map.append('aquamarine')
    else:
         edge_color_map.append('white')
        

colormap = plt.cool()

nx.draw_networkx_nodes(graph, pos, node_size=node_size_list, node_color=node_size_list, alpha=0.9, node_shape='o', cmap=colormap)
nx.draw_networkx_edges(graph, pos, edgelist=new_dict.keys(), width=[i for i in new_dict.values()],
                       edge_color=edge_color_map, alpha=0.5)
nx.draw_networkx_labels(graph, pos, font_size=9, font_family='Verdana', font_color='black')


plt.savefig("graph.jpg", dpi=200)
plt.figure(figsize=(9, 5))
#plt.subplot(132)
#names = list(reversed(key_list))
#values = list(reversed(counts_list))
#plt.scatter(values, names)
#plt.show()

