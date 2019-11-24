Pour lancer le jeu : `python init.py`
Pour lancer les tests : `xvfb-run -a --server-args="-screen 0 1600x900x24" pytest`

Il reste certains problèmes à régler avec les bibliothèques :
- Pygame semble ne pas pouvoir lire certaines musiques sur certaines machines
- Librosa plante en tentant d'exécuter certains algorithmes sur certaines musiques (dépend également de la machine)
