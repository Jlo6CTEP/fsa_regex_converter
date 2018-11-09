import re
from Graph import *

error_messages = ["E1: A state '{}' is not in set of states", "E2: Some states are disjoint",
                  "E3: A transition '{}' is not represented in the alphabet", "E4: Initial state is not defined",
                  "E5: Input file is malformed", "E6: FSA is nondeterministic"]
warning_messages = ["W1: Accepting state is not defined", "W2: Some states are not reachable from initial state"]

from_file = open("fsa.txt", "r").read().replace(" ", "")

states = re.sub("states={((\w*.,\w*.,)*|(\w*.,\w*)*|(\w*))*}\n", "", from_file)
alpha = re.sub("alpha={(((._|\w)*.,(._|\w)*)*|((._|\w)*.,(._|\w)*.,)*|(._|\w)*)*}\n", "", states)
init = re.sub("init\.st={(\w*)}\n", "", alpha)
fin = re.sub("fin[.]st={((\w*.,\w*)*|\w*)}\n", "", init)
trans = re.sub("trans={((\w*.>\w*.>\w*.,\w*.>\w*.>\w*.,)*|(\w*.>\w*.>\w*.,\w*.>\w*.>\w*)*|(\w*.>\w*.>\w*))*}$", "", fin)

data = list(zip(from_file.split("\n"), ["states=", "alpha=", "init.st=", "fin.st=", "trans="]))
file = open("result.txt", "w")
fsa = [re.sub("[,{\}]", " ", x[0].replace(x[1], "")).strip().split() for x in data]
fsa[4] = [tuple(k.split(" ") for k in x.replace(">", " ").strip().split(","))[0] for x in fsa[4]]

head = Graph()

for x in fsa[0]:
    head.node.append(Node(st=x))
for x in fsa[4]:
    try:
        head.find_node(x[0]).trans.append(Transition(head.find_node(x[2]), x[1]))
        head.find_node(x[2]).back.append(head.find_node(x[0]))
    except ValueError:
        pass
head.bfs(fsa[2][0])

#error_codes = [(set(fsa[2]) | set(fsa[3]) | set(x[0] for x in fsa[4]) | set(x[2] for x in fsa[4])) - set(fsa[0]),
#               len(head.bfs(directed=False)) != len(fsa[0]),
#               set([x[1] for x in fsa[4]]) - set(fsa[1]),
#               len(fsa[2]) < 1,
#               len(trans) > 0,
#               any([len(set([k.alpha for k in x.trans])) != len(x.trans) for x in head.node])]
#
#error_messages[0] = error_messages[0].format(", ".join(error_codes[0]))
#error_messages[2] = error_messages[2].format(", ".join(error_codes[2]))
#error_log = [x[1] for x in zip(error_codes, error_messages) if x[0]]
#
#print()
#
#if len(error_log) == 0:
#    warning_codes = [len(fsa[3]) == 0 or not set([x.state for x in head.bfs(fsa[2][0])]) >= set(fsa[3]),
#                     set(head.bfs(fsa[2][0], directed=True)) != set(head.node)]
#
#    warning_log = [x[1] for x in zip(warning_codes, warning_messages) if x[0]]
#
#    final_solution = ""
#    file.write(final_solution)
#    if len(warning_log) != 0:
#        file.write("\n" + "Warning:\n" + "\n".join(warning_log))
#else:
#    file.write("Error:\n" + "\n".join(error_log))
#file.close()
