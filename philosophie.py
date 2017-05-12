#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Ne pas se soucier de ces imports
import setpath
import numpy as np
from flask import Flask, render_template, session, request, redirect, flash
from getpage import *
import re

app = Flask(__name__)
app.secret_key = "TODO: mettre une valeur secrète ici"

global all_path
all_path = []

@app.route('/', methods=['GET'])
def index():
	session['score'] = 0
	session['article'] = None
	all_path = []
	return render_template("index.html")

@app.route('/new-game', methods=['POST'])
def new_game():
	#if form.validate_on_submit():

	title = request.form['titre']
	title_lwr = title.lower()
	title_prs, _ = getRawPage(title)
	
	if title_prs is None:
		flash(u'Watch your orthograph, this page does not exist!', 'alert')
		return redirect('/')

	if title_lwr == 'philosophie' or title_lwr == 'philosophique':
		flash(u'You, cheater!', 'alert')
		return redirect('/')
	else:
		session['article'] = title
		all_path.append(session['article'])
		session['score'] = 0
		return redirect('/game')

@app.route('/game', methods = ['GET'])
def game():
	title, url = getPage(all_path[-1])
	if title is None:
		flash(u'This is empty', 'error')
		return redirect('/')
	#if getPage(all_path[-1]):
	#title, url = getPage(all_path[-1])
	if not url:
		flash(u'This page '+title+' has no link', 'error')
		return redirect('/')
	else:
		session['url'] = url		
		return render_template("game.html",truescore=session['score'])
	#else:
	#	flash('This is empty')
	#	return redirect('/')

@app.route('/move', methods = ['POST'])
def move():
	link = request.form['link']
	temp = [x for x in session['url'] if link in x]
	if not temp:
		flash(u'You, cheater', 'alert')
		return redirect('/')
	score = request.form['score']
	if int(score) != session['score']:
		flash(u'You, cheater', 'alert')
		return redirect('/')
	session['score'] += 1
	pattern = re.compile('Philosophie')
	if pattern.match(link):
		set_path = set(all_path)
		flash(u'Congrats, you won with '+str(session['score'])+' redirect(s)', 'success')
		#flash(u'Check: The path number is '+str(len(set_path)), 'Win')
		return redirect('/')

	all_path.append(temp[-1])
	return redirect('/game')

if __name__ == '__main__':
	app.run(debug=True)

	


