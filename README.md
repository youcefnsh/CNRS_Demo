Voici quelques petits bouts de code du projet Patent.

Le projet a consistait à faire une appli web qui permet aux utilisateurs de visualiser des transactions de brevets entre différentes companies. 

On devait créer une base de données Neo4j à partis de fichiers CSV et json, puis consevoir l'appli-web sur Django. 

Vous avez un exemple de comment on transformait les informations de l'utilisateur (qu'il entrait via des forms) en une requete Cypher (langage qu'utilise Neo4j).

Vous avez aussi un exemple de comment on utilisait les données récupérées par Neo4j pour créer des objets qui seront envoyés coté front à display (pour le display on utilise la libraire js Cytoscape).
