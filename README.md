# POSTaggingCRF
étiqueteur morphosyntaxique basé sur le modèle  CRF

Pour exécuter cet étiquetteur, il faut:
  - installer python
  - installer numpy
  - installer 'nltk'
  - télécharger le .zip du corpus de Brown à l'adresse "https://archive.org/details/BrownCorpus"
  - décompresser ce .zip et le stocker à un endroit bien precis de votre ordinateur
  - remplacer le fichier 'crf.py' par défaut qui se trouve dans '/usr/local/lib/python2.7/dist-packages/nltk/tag' par le fichier "crf.py" de ce dépôt
  - exécuter le fichier 'POSTagger.py' en ligne de commande en lui passant en premier paramètre le chemin absolu de votre machine vers le corpus et en second paramètre le mot train(sans tenir compte du castin) si on souhaite entrainer le modèle sinon autre chose. Exemple: python -u POSTagger.py .../chemin/BrownCorpus/brown train
  
