import re

import networkx

error_messages = ["E1: A state '{}' is not in set of states", "E2: Some states are disjoint",
                  "E3: A transition '{}' is not represented in the alphabet", "E4: Initial state is not defined",
                  "E5: Input file is malformed"]
warning_messages = ["W1: Accepting state is not defined", "W2: Some states are not reachable from initial state",
                    "W3: FSA is nondeterministic"]

from_file = open("fsa.txt", "r").read().replace(" ", "")

states = re.sub("states={((\w*.,\w*.,)*|(\w*.,\w*)*|(\w*))*}\n", "", from_file)
alpha = re.sub("alpha={(((._|\w)*.,(._|\w)*)*|((._|\w)*.,(._|\w)*.,)*|(._|\w)*)*}\n", "", states)
init = re.sub("init\.st={(\w*)}\n", "", alpha)
fin = re.sub("fin[.]st={((\w*.,\w*)*|\w*)}\n", "", init)
trans = re.sub("trans={((\w*.>\w*.>\w*.,\w*.>\w*.>\w*.,)*|(\w*.>\w*.>\w*.,\w*.>\w*.>\w*)*|(\w*.>\w*.>\w*))*}$", "", fin)


data = list(zip(from_file.split("\n"), ["states=", "alpha=", "init.st=", "fin.st=", "trans="]))
file = open("result.txt", "w")
regex = re.compile("[,{\}]")
fsa = [regex.sub(" ", x[0].replace(x[1], "")).strip().split() for x in data]
fsa[4] = [tuple(k.split(" ") for k in x.replace(">", " ").strip().split(","))[0] for x in fsa[4]]

fsa_graph = networkx.DiGraph()
fsa_graph.add_nodes_from(fsa[0])
fsa_graph.add_weighted_edges_from([(x[0], x[2], x[1]) for x in fsa[4]])
print(fsa_graph['on']['off'])

print()
