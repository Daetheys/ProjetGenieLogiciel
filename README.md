# Software Engineering Project ~ Projet Génie Logiciel (M1 ENS Cachan) - CANABAELDE
- Canabalt like

### Introduction

This is a rythmic auto-scrolling game, where you can either play set levels (Campaign mode) or create your own levels out of the music of your choice (Free Play mode).


##Running the tests 
To run the game: ```python init.py``` or ```python3 init.py```
To run the auto tests : ```xvfb-run -a --server-args="-screen 0 1600x900x24" pytest```

Some libraries still have some problems :
- Pygame cannot read some musical files on some computers 
- Librosa also crashes sometimes.

##Running the tests (In French)
Pour lancer le jeu : ```python init.py``` ou ```python3 init.py```
Pour lancer les tests : ```xvfb-run -a --server-args="-screen 0 1600x900x24" pytest```

Il reste certains problèmes à régler avec les bibliothèques :
- Pygame semble ne pas pouvoir lire certaines musiques sur certaines machines
- Librosa plante en tentant d'exécuter certains algorithmes sur certaines musiques (dépend également de la machine) 

