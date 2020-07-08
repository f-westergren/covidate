import os
from unittest import TestCase

from models import db, connect_db, User, Search
from flask_login import current_user, login_user

from datetime import datetime

os.environ['DATABASE_URL'] = 'postgresql:///covid-test'

from app import app

app.config['WTF_CSRF_ENABLED'] = False
app.config['TESTING'] = True


class AuthRouteTestCase(TestCase):
	""" Test views for auth """

	def setUp(self):
		db.drop_all()
		db.create_all()

		self.client = app.test_client()
		self.testuser = User.signup(username='testuser', email='user@test.com', password='password') 
		self.testuser.id = 1000

		db.session.commit()

	def tearDown(self):
		db.session.rollback()

	def test_valid_login(self):
		# With invalid password
		with self.client as c:
			res = c.post('/login', 
				data={'username': self.testuser.username, 'password': 'badpassword'},
				follow_redirects=True)

			# Current_user is not testuser
			self.assertNotEqual(current_user, self.testuser)
		
		# User should be remain on login page with flashed message.
		self.assertIn('Invalid credentials', str(res.data))		
		self.assertIn('Log in', str(res.data))

		# With invalid username
		with self.client as c:
			res = c.post('/login', 
				data={'username': 'badusername', 'password': 'password'},
				follow_redirects=True)

			# Current_user is not testuser
			self.assertNotEqual(current_user, self.testuser)
		
		# User should be remain on login page with flashed message.
		self.assertIn('Invalid credentials', str(res.data))		
		self.assertIn('Log in', str(res.data))		

		# With valid password
		with self.client as c:
			res = c.post('/login', 
				data={'username': self.testuser.username, 'password': 'password'},
				follow_redirects=True)

			# Current_user is set to logged in user
			self.assertEqual(current_user, self.testuser)
		
		# User should be redirected to index page.
		self.assertIn('Covid-19 Outbreak Search', str(res.data))		

	def test_signup(self):
		# With invalid email:
		with self.client as c:
			res = c.post('/signup', 
				data={
					'username': 'testname', 
					'password': 'password', 
					'confirm': 'password', 
					'email': 'bademail.com'},
					follow_redirects=True)	

		self.assertIsNone(User.query.filter_by(username = 'testname').first())
		self.assertIn('Enter a valid email', str(res.data))		

		# With passwords not matching:
		with self.client as c:
			res = c.post('/signup', 
				data={
					'username': 'testname', 
					'password': 'passwords', 
					'confirm': 'arenotmatching', 
					'email': 'test@email.com'},
					follow_redirects=True)	

		self.assertIsNone(User.query.filter_by(username = 'testname').first())
		self.assertIn('Passwords must match', str(res.data))

		# With already taken username
		with self.client as c:
			res = c.post('/signup', 
				data={
					'username': 'testuser', 
					'password': 'password', 
					'confirm': 'password', 
					'email': 'test@email.com'},
					follow_redirects=True)	

		self.assertIsNone(User.query.filter_by(username = 'testname').first())
		self.assertIn('Username already taken', str(res.data))

		with self.client as c:
			res = c.post('/signup', 
				data={
					'username': 'testname', 
					'password': 'password', 
					'confirm': 'password', 
					'email': 'test@email.com'},
					follow_redirects=True)

			u = User.query.filter_by(username = 'testname').first()

			# Current_user is set to logged in user
			self.assertEqual(current_user, u)

		# User should be redirected to index page.
		self.assertIn('Covid-19 Outbreak Search', str(res.data))	

	def test_logout(self):
		with self.client as c:
			c.post('/login', 
				data={'username': self.testuser.username, 'password': 'password'},
				follow_redirects=True)

			# current_user should be logged in user
			self.assertEqual(current_user, self.testuser)

			res = c.get('/logout', follow_redirects=True)

			# current_user should not be logged in user
			self.assertNotEqual(current_user, self.testuser)
			self.assertIn('Covid-19 Outbreak Search', str(res.data))




