# Software Engineering Project ~ Projet Génie Logiciel (M1 ENS Cachan) - CANABAELDE
- Canabalt like

### Introduction

This is a rythmic auto-scrolling game, where you can either play set levels (Campaign mode) or create your own levels out of the music of your choice (Free Play mode).


Be sure to read the documentation in the [./doc](./doc) folder. UML files give you an overview of the global stucture, whereas you can learn about performance in the [eponymous pdf](./doc/performances.pdf) (in French), and see detailed information about all modules, files, classes and functions in the [./doc/wiki](./doc/wiki) folder

## Running the tests
To run the game: ```python init.py``` or ```python3 init.py```
To run the auto tests : ```xvfb-run -a --server-args="-screen 0 1600x900x24" pytest```

Some libraries have some problems :
- Pygame cannot read some musical files on some computers
- Librosa also crashes sometimes.

## Running the tests (In French)
Pour lancer le jeu : ```python init.py``` ou ```python3 init.py``` ou ```python3.7 init.py``` 
Pour lancer les tests : ```xvfb-run -a --server-args="-screen 0 1600x900x24" pytest```

Il reste certains problèmes à régler avec les bibliothèques :
- Pygame semble ne pas pouvoir lire certaines musiques sur certaines machines
- Librosa plante en tentant d'exécuter certains algorithmes sur certaines musiques (dépend également de la machine). Si vous voulez lire des fichiers mp3 il faut installer ffmpeg.

## Informations à propos du jeu
Deux modes de jeu sont à votre disposition. Un mode campagne avec une histoire, des dialogues, des objets (permettant pour le moment de débloquer des niveaux uniquement) et bien entendu des niveaux de jeu. A cause des problèmes avec librosa, nous avons conçu des niveaux à la main (donc qui ne concordent pas parfaitement bien avec le rythme). En effet nous voulons que vous puissiez profiter au maximum des deux modes de jeu et librosa risque de crash sur certaines musiques ne vous permettant donc pas de valider le niveau et de profiter de la suite. C'est pourquoi les niveaux de la campagne ont été faits à la main.

Le mode free play vous permet de lancer un niveau de jeu sur n'importe laquelle de vos musiques (selon la volonté de librosa bien entendu). Pour cela il vous suffit de créer un dossier data/'your music' (vous pouvez suivre la bulle d'aide dans le mode free play) et d'y ajouter vos musiques. Pour le moment vous ne pouvez que selectionner un fichier mp3 ou wav (donc pensez à utiliser audacity ou un logiciel similaire pour convertir vos formats). Voici la liste de bugs recensés avec librosa jusqu'à l'heure actuelle : Librosa peut planter et renvoyer une erreur, librosa peut renvoyer un seul beat au lieu d'une séquence de beats (ce qui fait planter le sound_parseur), il peut renvoyer un niveau vide ou bien renvoyer un niveau incomplet (la musique continue mais il n'y a plus de plateformes. Pour la partie II nous allons voir comment limiter ce problème (on aimerait donc bien avoir vos retours sur si librosa a bien marché ou non) que ce soit en utilisant autre chose ou en codant à la main notre propre module d'analyse.

Nous esperons que malgré ce problème vous prendrez plaisir à jouer au jeu (nous y avons passé beaucoup de temps), au moins sur les niveaux de campagne.
