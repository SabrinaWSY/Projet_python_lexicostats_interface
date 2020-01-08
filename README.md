# Projet_lexicostats_python_interface
Project for the course Langage de Script at Master 2 NLP Multilingual Engineering, INALCO

Project in python creating an program with user interface to detect language, proceed tokennization and POS tagging, and show statistic information of the input corpus 

- Des pips installés sont dans 'requirements.txt', il faut les installer avant l'utiliser cette interface.
- Des modèles de langues de spacy sont téléchargé pour le POS tagging de ces langues, il faut aussi les installer avant l'utilisation de l'interface.
    python -m spacy download de_core_news_sm
    python -m spacy download fr_core_news_sm
    python -m spacy download es_core_news_sm
    python -m spacy download it_core_news_sm