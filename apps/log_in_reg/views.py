from django.shortcuts import render,redirect
from django.contrib import messages
import re
import bcrypt
from .models import User

def index(request):
	return render(request, 'log_in_reg/index.html')

def register(request):
	first_name = request.POST['first_name']
	last_name = request.POST['last_name']
	email = request.POST['email']
	password = request.POST['password']
	confirm = request.POST['confirm']
	print first_name,last_name,email,password,confirm
	
	error = False
	# verify first_name > 2 characters and are letters only
	if not (len(first_name)>=2):
		messages.error(request,'First Name needs to have at least 2 charaters (letters only).')
		error = True
	if not(first_name.isalpha()):
		messages.error(request,'First Name can only have letters as characters.')
		error = True
	# verify last_name > 2 characters and are letters only
	if not (len(last_name)>=2):
		messages.error(request,'Last Name needs to have at least 2 charaters (letters only).')
		error = True
	if not(last_name.isalpha()):
		messages.error(request,'Last Name can only have letters as characters.')
		error = True
	# verify email format word@word.word
	if not re.match(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$',request.POST['email']):
		messages.error(request,email+' is an invalid email address.')
		error = True
	# verify pw is >= 8 chars long
	if not len(password)>=8:
		messages.error(request,'Your password needs to have at least 8 characters in it.')
		error = True
	# verify password and confirm match
	if not password == confirm:
		messages.error(request,'The confirmed password does not match the password you entered.')
		error = True
	if error == True:
		return redirect('/')
	else:
		# hash the pw + add the salt (bcrypt)
		hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
		print hashed
		print len(hashed)
		# add user to database
		new_user = User.objects.create(
			first_name = first_name,
			last_name = last_name,
			email = email,
			password = hashed,
		)
		request.session['first_name'] = first_name
		print new_user.first_name,new_user.last_name,new_user.email,new_user.password
		return redirect('/success')

def success(request):
	return render(request,'log_in_reg/success.html')
