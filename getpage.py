#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Authors: Audrey Quessada, Antoine Amarilli
# Ne pas se soucier de ces imports
import setpath
import re
from bs4 import BeautifulSoup
import json
import pprint
from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode, urljoin, unquote, urldefrag
from collections import OrderedDict
# Si vous écrivez des fonctions en plus, faites-le ici

global cache 
cache = {}

def clean_url(url): #pour nettoyer les urls comme demandé en question 4
    temp1 = unquote(url)
    temp2, _ = urldefrag(temp1)
    new_url = temp2.replace('_', ' ')
    return new_url

def use_regex(text): #regex pour matcher des séquences d'url qui nous intéressent
    l = len(text)
    pattern = re.compile(text)
    return l, pattern

def getJSON(page):
    params = urlencode({
      'format': 'json',  # format
      'action': 'parse',  # TODO: compléter ceci
      'prop': 'text',  # TODO: compléter ceci
      'redirects':'True',
      'page': page})
    API = "https://fr.wikipedia.org/w/api.php"  # TODO: changer ceci
    response = urlopen(API + "?" + params)
    result = response.read().decode('utf-8')
    return result

def parsing_link(page):
    #parsing_link est la fonction getPage initiale avant la question 4 du TP
    title, content = getRawPage(page)
    if title is None:
      return None, None, [], []

    try:
      soup = BeautifulSoup(content, 'html.parser')
      soup_p = soup.find_all('p', recursive=False)
      table_url_tot = [] #liste de toutes les URLs de la page
      url_red = [] #liste des URLs qui pointent vers des pages inexistentes
      url_ext = [] #liste des URLs extérieures à Wikipédia

      #définition des espaces de noms
      name_space = ['Discussion:', 'Utilisateur:', 'Discussion MediaWiki:', 
      'Discussion Portail:', 'Modèle:', 'Discussion utilisateur:', 'Discussion modèle:', 
      'Discussion Projet:', 'Aide:', 'Référence:', 'Discussion Wikipédia:', 
      'Discussion aide:', 'Discussion Référence:', 'Fichier:', 'Catégorie:', 'Module:', 
      'Discussion fichier:', 'Discussion catégorie:', 'Discussion catégorie:', 
      'MediaWiki:', 'Portail:']

      not_principal = [] #liste des URLs qui ne sont pas dans l'espace de noms principal
      for el in soup_p:
        a = el.find_all('a')
        b = el.find_all('a', {"class" : "new"})
        c = el.find_all('a', {"class" : "external autonumber"})

        for u in a:
        #pour toutes les url de la page
        #on ne garde que celles qui sont dans l'espace de nom principal
        #https://fr.wikipedia.org/wiki/Aide:Espace_de_noms
          url = clean_url(u['href'])
          for n in name_space:
            _, p = use_regex(n)
            if p.search(url):
              not_principal.append(url)
          if url not in not_principal:
            table_url_tot.append(url)

        for u in b: #pour les url qui pointent vers des pages inexistentes
          url_red.append(clean_url(u['href']))

        for u in c: #pour des url qui pointent cers des pages externes
          url_ext.append(clean_url(u['href']))

      #on récupère maintenant les urls wiki et on slice l'url pour enlever le préfixe wiki
      #on liste toutes ces URLs danss url_wiki
      url_wiki = []
      for u in table_url_tot:
        wiki_link1 = '/wiki/' #prefixe des liens wiki
        wiki_link2 = '//fr.wiktionary.org/wiki/' #autre prefixe des liens wiki
        l1, pattern1 = use_regex(wiki_link1)
        l2, pattern2 = use_regex(wiki_link2)
        if pattern2.search(u):
          no_pref = u[l2:]
          url_wiki.append(no_pref)
        elif pattern1.search(u):
          no_pref = u[l1:]
          url_wiki.append(no_pref) 
        else:
          pass
        
      list_url_wiki = list(OrderedDict.fromkeys(url_wiki))
      len_wiki = len(list_url_wiki)

      #on veut ne garder que les 10 premiers liens wiki
      if len_wiki >= 10: 
        return title, list_url_wiki[0:10], url_red, url_ext
      else:
        return title, list_url_wiki, url_red, url_ext
    except KeyError:
      return None, None, None, None

def getRawPage(page):
    parsed = loads(getJSON(page))
    try:
      title = parsed['parse']['title']  # TODO: remplacer ceci
      content = parsed['parse']['text']['*']  # TODO: remplacer ceci
      return title, content
    except KeyError:
        # La page demandée n'existe pas
      return None, []


def getPage(page): 
    if page in cache.keys():
      print("Page already visited...")
      return page, cache[page]

    title, url, _, _ = parsing_link(page) 
    if title is None or url is None:
      return [], []
  
    if title in cache.keys():
      print("Page already visited...")
      return title, cache[title]
    else:
      cache[title] = url
      print("New page")
      return title, cache[title]

if __name__ == '__main__':
    # Ce code est exécuté lorsque l'on exécute le fichier
    print("Ça fonctionne !")
    
    # Voici des idées pour tester vos fonctions :
    pp = pprint.PrettyPrinter(indent=4)
    stuff_A3nm = getJSON("Utilisateur:A3nm/INF344")
    pp.pprint(stuff_A3nm)
    #print('============================')
    #print(getRawPage("Utilisateur:A3nm/INF344"))
    #print('============================')
    #print(parsing_link("Utilisateur:A3nm/INF344"))
    #print('============================')
    #print(' ')
    #print('============================')
    #stuff_Hist = getJSON("Histoire")
    #pp.pprint(stuff_Hist)
    #print('============================')
    #print(getRawPage("Histoire"))
    #print('============================')
    #print(parsing_link("Histoire"))
    #print('============================')
    #print(parsing_link("Geoffrey Miller"))
    #print('============================')
    #print(getPage("Histoire"))
    #print('============================')
    #print(getPage("Synecdoque"))
    #print('============================')
    #print(getPage("Abstraction (philosophie)"))
    #print('============================')
    #print(getPage("Synecdoque"))
    #print('============================')
    #print(getPage("Logique"))
    #print('============================')
    #print(getPage("Histoire"))
    #print('============================')
    #print(getPage("Utilisateur:A3nm/INF344"))
    #print('============================')
    #print(getPage("Geoffrey Miller"))
    #print('============================')
    #print(cache) 
    #print('============================')
    #print(getRawPage('philsophi')) 
    #print(parsing_link('philsophi'))
    #print(getPage('philsophi')) 



