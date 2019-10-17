from os import walk
import networkx as nx
import pylab as plt
from tqdm import tqdm
import csv

f = []
for (dirpath, dirnames, filenames) in walk('playlists_name'):
    f.extend(filenames)
    break

print(f)

G = nx.Graph()

max = 0

i = 0
for file in tqdm(f):
    playlist = file[:-4]
    with open('playlists_name/' + file, 'r') as current:
        content = current.readlines()

    for q in range(0, len(content)):
        for p in range(q, len(content)):
            track1 = content[q][:-1].split(";")
            track2 = content[p][:-1].split(";")

            if track1[0] != track2[0] and track1[0] != 'None' and track2[0] != 'None':
                if G.has_edge(track1[0], track2[0]):
                    if G[track1[0]][track2[0]]['weight'] > max:
                        max = G[track1[0]][track2[0]]['weight']
                    # print('Found high weight for edge (' + track1[0] + ", " + track2[0] + "): " + str(
                    #    G[track1[0]][track2[0]]['weight']))
                    G[track1[0]][track2[0]]['weight'] += 1

                else:
                    G.add_edge(track1[0], track2[0], weight=1)
                    G.node[track1[0]]['name'] = track1[1]
                    G.node[track1[0]]['artist'] = track1[2]
                    G.node[track2[0]]['name'] = track2[1]
                    G.node[track2[0]]['artist'] = track2[2]

    # print('Added ' + str(i) + '/' + str(len(f)))
    i = i + 1
    if i > 300:
        break

print('Nodes: ' + str(len(G.nodes)))
print('Edges: ' + str(len(G.edges)))