# WikiSophie
Simple Data web lab: for the Big Data cursus at Télécom ParisTech
  
   
   
## Tous les chemins mènent à la philosophie  
  
Le but de ce TP est de créer une application Web qui permet d’utiliser l’API de **Wikipédia** afin de trouver le nombre de 
liens qui séparent un mot (quelconque, choisi par l’utilisateur) à la page Wikipédia "Philosophie".  
Des applications en ligne de ce genre existent déjà:  
* http://mu.netsoc.ie/wiki/  
* https://flowingdata.com/2011/06/08/all-roads-lead-to-philosophy-on-wikipedia/  
  
Par exemple, avec notre application, on peut relier le mot *ketchup* à *philosophie* avec 8 liens intermédiaires.  
  
Pour la suite du TP,  notamment par rapport à la section 4, j’ai choisi de diviser la fonction `getPage` en deux fonctions, 
ce qui était, de mon point de vue, plus simple: une fonction `parsing_link` qui va utiliser **Beautifulsoup** pour parser 
la page wiki et une fonction `getPage` qui va utiliser le cache et les résultats de `parsing_link`.  
  
La fonction `parsing_link` récupère les résultats de la fonction `getRawPage`, permet de supprimer les liens qui ne sont pas 
dans l’espace de noms principal selon le schéma ci-dessous. Elle permet également de créer une liste des URLs qui pointent 
vers des pages inexistantes en remarquant que la classe associée dans le code HTML est `{"class" : "new"}` ainsi que les URLs 
externes avec `{"class" : "external autonumber"}`. Une regex permet ensuite de sélectionner les URLs qui contiennent `/wiki/`. 
On ne garde de cette liste que les liens uniques grâce à la librairie collections.  
Au final seulement les 10 premiers liens sont renvoyés.  
  
![Espace_nom](http://fr.wikipedia.org/wiki/Aide:Espace_de_noms#/media/File:StructurationPagesWikipediaV0.5.jpg)
