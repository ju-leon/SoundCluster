# SoundCluster

SoundCluster aims to give you better song recommendations that the standart spotify song recoomentations.

Instead of actually listening to that songs, publicly available playlists are crawled.
Sounds are then grouped depending on how often they appear in a playlist together.

A graph is constructed, featuring a node for each song and an edge weight depending on how of the songs appear in playlists together.
This graph is then layoutet using a Spring Layout.

All songs that have a small eucledian distance in the layout space are closely realted.
So if you like a song somewhere in the space, it is pretty likely that you will also like songs close to that one.

The cool thing about using a spring layout instead of other machine learning techniques such as neural networks is, that adding new songs is really easy.
New songs only have to appear in a small amount of playlists and there approximate location in the song space can be estiamted depending on the other sons in that playlist.

The positions in the layout space can also be utilised as training data for neural bnetworks in the future, e.g. a neural network that has a song as an input and outputs it's location in the layout space. 
This could be used to automatically classify genre and potential listeners for new songs.
