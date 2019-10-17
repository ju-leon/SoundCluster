import requests
import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network

headers = {
    'Authorization': 'Bearer BQCl-EIMg-EYkxnCuAOrITxXGAZ66NRpbE_Sn0SP4tH8Y9rMksLVUi4W8XM9sqZAjjqEs5uABmPBege9CFvV6OuH9Zb-1fbmrguc_oDaJQ-BuevQwERoJ2BBnTa0WfD92CETlwTc1hcBs0A_cKgAC8Cm0FydPDknnk9JwfIzoZeZ5Z_DByiRS2_qaR7UxjgCqSVIZAaHVyzLlTUB78wGB_skLySo'}

playlists = set()

for m in range(0, 10000):
    r = requests.get('https://api.spotify.com/v1/search?q=cl*&type=playlist&limit=50&offset=' + str(m * 50),
                     headers=headers)
    print(r.text)
    print(str(m) + "/100")

    try:
        data = r.json()["playlists"]["items"]

        for playlist in data:
            playlists.add(playlist["id"])

            with open('playlists_broad/' + playlist["id"] + '.txt', 'w') as play:
                k = requests.get('https://api.spotify.com/v1/playlists/' + playlist["id"], headers=headers)

                try:
                    data = k.json()["tracks"]["items"]

                    for track in data:
                        try:
                            play.write(
                                track["track"]["id"] + ';' + track["track"]["name"] + ';' +
                                track['track']["artists"][0]["name"] + "\n")
                        except TypeError:
                            print("Skipped song")

                except KeyError:
                    print("Skipped playlist")


    except KeyError:
        print("Skipped playlist")

print("Saved")

exit(0)

plt.figure(figsize=(18, 18))
G = nx.Graph()

for playlist in playlists:
    r = requests.get('https://api.spotify.com/v1/playlists/' + playlist, headers=headers)
    data = r.json()["tracks"]["items"]

    tracks_in_playlist = []

    for track in data:
        try:
            tracks_in_playlist.append(
                track["track"]["id"] + ';' + track["track"]["name"] + ';' + track["artists"][0]["name"])
        except TypeError:
            print("Skipped song")

    # Increase edge weight for each pair of tracks that are together in a playlist
    for i in range(0, len(tracks_in_playlist)):
        for k in range(i, len(tracks_in_playlist)):
            if tracks_in_playlist[i] != tracks_in_playlist[k]:
                if G.has_edge(tracks_in_playlist[i], tracks_in_playlist[k]):
                    G[tracks_in_playlist[i]][tracks_in_playlist[k]]['weight'] += 1
                else:
                    G.add_edge(tracks_in_playlist[i], tracks_in_playlist[k], weight=1);

print('Removed edges with weight 1')

G.remove_nodes_from(list(nx.isolates(G)))

net = Network(height=800, width=800, notebook=True)
net.toggle_hide_edges_on_drag(False)
net.barnes_hut()

net.from_nx(G)
net.show("graph.html")

print(G.nodes)
