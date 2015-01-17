from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from forms import UserForm
from django.contrib.auth.models import User
from datetime import datetime
from myblog.models import *
from django.shortcuts import redirect
from datetime import datetime
from django.contrib.auth import login,logout,authenticate
from django.http import Http404
import json
import csv

def graph(request) :

	if(request.method == "POST") :
		atr1 = request.POST['attribute1']
		atr2 = request.POST['attribute2']
		atr3 = request.POST['attribute3']
		atr4 = request.POST['attribute4']
		atr5 = request.POST['attribute5']
		atr6 = request.POST['option']
		atr7 = request.POST['value']
		file1 = open("/home/lifecodemohit/DjangoProjects/Blog/myblog/static/graph/abcd.json", "r+")
		settings = ""
		settings = json.load(file1)
		#settings[atr1][atr2][atr3][atr4][atr5].append(int(atr7))
		#settings['Skills']['Web Development']['Server Side']['Active 2']['Proper'].append(int(atr6))
		#settings['Skills']['Web Development']['Server Side']['Active 2']['Proper'].append(70)
		#settings['Skills']['Web Development']['Server Side']['Active 2']['Proper']=[50,60,70]
		#settings['Skills']['Web Development']['Server Side']['Active 2'] ={}
		#settings['Skills']['Web Development']['Server Side']['Active Page']['ABYYKT']=[0,90,90] #update the make of the first car
		file1.close()
		
		jsonFile = open("/home/lifecodemohit/DjangoProjects/Blog/myblog/static/graph/abcd.json", "w+")
	 	jsonFile.write(json.dumps(settings))
	 	jsonFile.close()

	 	file1 = open("/home/lifecodemohit/DjangoProjects/Blog/myblog/static/graph/abcd.json", "r+")
	 	file2 = open("/home/lifecodemohit/DjangoProjects/Blog/myblog/static/graph/skillsdata.js", "w+")
	 	file2.write("var skillsdata;" + "\n" + "skillsdata =\n")
	 	for line in file1 :
	 		file2.write(line)
	 	file1.close()
	 	file2.close()
		print 'Sample File Successfully Updated!'
	return render(request, 'graph.html', "")

def index(request) :
	print request.user.username + " currently logged in"
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				print "Username : " + request.user.username
				print "Login Success"
				return HttpResponseRedirect('/')
			else:
				print "User not active"
		else:
			print "User doesn't exist"
	return render(request, 'index.html', "")

def signout(request) :
	current_user = request.user.username 
	logout(request)
	print current_user + " logged out"
	return HttpResponseRedirect('/')


def signup(request) :
	if request.method == "POST":
		#form = UserForm(request.POST)
		#if form.is_valid() :
		print "Sign Up Success"
		new_user = User.objects.create_user(username=request.POST['username'],email=request.POST['email'],password=request.POST['password'])
		return HttpResponseRedirect('/')
		#else :
		#	print "Sign Up Failed"
	else:
		print "Signup Form Load"
		form = UserForm() 
	context={'form': form}
	return render(request, 'signup.html', context)

def change_password(request):
	if request.method == "POST":
		oldpassword = request.POST['oldpassword']
		newpassword = request.POST['newpassword']
		confirmpassword = request.POST['confirmpassword']
		user = authenticate(username=request.user.username, password=oldpassword)
		if user is not None:
			if user.is_active and newpassword==confirmpassword:
				u = User.objects.get(username__exact=request.user.username)
				u.set_password(newpassword)
				u.save()
				print request.user.username + " password changed"
			else:
				print "Wrong Details entered"
		else:
			print "Invalid password"
	context =""
	return render(request, 'change_password.html', context)

def add_question(request) :
	if not request.user.is_authenticated():
		print "login to post a question"
	if request.method == 'POST' :
		split_hash = request.POST.get('hash_tag')
		list_of_hash = split_hash.split('#')
		hash_dup =""
		for hashtag in list_of_hash :
			hash_dup = hash_dup + hashtag + " "
		new_ques=Question(user_name=request.user.username,heading=request.POST.get('heading'),main_text= request.POST.get('main_text'),hash_tag= hash_dup,votes=0,views=0,num_answers=0,votes_user="",views_user="")
		new_ques.save()
		#return HttpResponse('Hello World!')
		return render(request, 'index.html', "")
	return render(request, 'add_question.html', "")

def question(request,question_id) :
	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404
	if request.user.is_authenticated():
		list_of_viewers = question.views_user.split(' ')
		flag =1
		for user_string in list_of_viewers :
			if user_string == request.user.username :
				flag =0
				break
		if flag==1 :
			question.views = question.views + 1
			question.views_user = question.views_user + request.user.username + " "
			question.save()
	if request.method == 'POST' :
		if request.user.is_authenticated():
			new_comment =question.comment_set.create(comment_user_name=request.user.username,comment_main_text= request.POST.get('comment_main_text'),comment_votes=0,comment_votes_user="")
			new_comment.save()
			question.num_answers = question.num_answers +1
			question.save()
			print "Comment posted"
			return HttpResponseRedirect('/question/'+question_id)
	context ={'question':question}
	return render(request, 'question_display.html', context)

def question_upvote(request,question_id) :
	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404
	if request.user.is_authenticated():
		list_of_viewers = question.votes_user.split(' ')
		flag =1
		for user_string in list_of_viewers :
			if user_string == request.user.username :
				flag =0
				break
		if flag==1 :
			print "UpVote"
			question.votes = question.votes + 1
			question.votes_user = question.votes_user + request.user.username + " "
			question.save()
		else :
			print "Already Done"
		return HttpResponseRedirect('/question/'+question_id)
	return render(request, 'question_display.html', context)
