
# Python Multiplayer Game

This is the first ever Multiplayer Game that I am making.



## Acknowledgements

- I followed [DaFluffyPotato](https://www.youtube.com/@DaFluffyPotato)'s excellent video tutorial, [Pygame Platformer Tutorial - Full Course](https://www.youtube.com/watch?v=2gABYM5M0ww), to build the core gameplay mechanics. However, I wanted to take it a step further and add multiplayer functionality, which is the focus of this project.



## Documentation


### The Game
perform these steps on all the machines you want to play the game on.
\
\
create a copy of this Repository locally using
```bash
git clone https://github.com/PahulGogna/Pygame_Multiplayer_Game.git
```

Now, install pygame
```cmd
pip install pygame==2.5.2
```


Now, change the `self.server` in `network.py`  file to the IP of one of your machines, lets say `A`, which can be found by running the following command in your Cammand Prompt - 
```cmd
ipconfig
```
the `IPv4 Address` is the IP Address of `A`,

Now, run the `server.py` file on `A` whose ip you took.

After this you can run the `main.py` file to start the game (you can also run it on `A`). as long as you are on the same Network you can play the game together. 


### Tile Editor
- This Repository contains a Tile Editor, for creating/editing your own custom maps. A map is already provided for playing, which you can also edit.
- To use the editor, Just run the editor file and select if you want to create a new map or edit an existing one. to play that map though you have to change path of the map in `main.py`.as of now there is no implementation for swithing maps from the game itself.
## Screenshots

![Game Screenshot](https://github.com/PahulGogna/Pygame_Multiplayer_Game/assets/135852041/a2f065c6-8483-41d9-aaa9-5a2fdbb59f96)

https://github.com/PahulGogna/Pygame_Multiplayer_Game/assets/135852041/223985da-15b0-4e05-83ae-f00ffca063de
