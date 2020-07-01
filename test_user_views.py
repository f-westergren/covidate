import os
from unittest import TestCase
from flask import url_for

from models import db, connect_db, User, load_user
from flask_login import current_user, login_user
from bs4 import BeautifulSoup

os.environ['DATABASE_URL'] = 'postgresql:///covid-test'

from app import app

app.config['WTF_CSRF_ENABLED'] = False
app.config['TESTING'] = True

class UserViewTestCase(TestCase):
	""" Test views for users """

	def setUp(self):

		db.drop_all()
		db.create_all()

		self.client = app.test_client()

		self.testuser = User.signup(username='testuser', email='user@test.com', password='password')

		self.testuser_id = 1000
		self.testuser.id = self.testuser_id

		db.session.commit()
	
	def tearDown(self):
		db.session.rollback()
	
	def test_user_searches(self):
		with self.client as c:
			c.post('/login', 
				data={'username': self.testuser.username, 'password': 'password'},
				follow_redirects=True
			)
			
			res = c.get(f'/user/{self.testuser.username}/searches')

			self.assertEqual(res.status_code, 200)
			self.assertIn('Date & Location', str(res.data))

			# Add more tests here
	
	
	def test_edit_profile(self):
		with self.client as c:
			c.post('/login', 
				data={'username': self.testuser.username, 'password': 'password'},
				follow_redirects=True)

			res = c.get(f'/user/{self.testuser.username}/profile')

			self.assertEqual(res.status_code, 200)
			self.assertIn('testuser', str(res.data))
			self.assertIn('user@test.com', str(res.data))

			# Test with valid password
			res = c.post(f'/user/{self.testuser.username}/profile', 
				data={'username': 'changeduser', 'email': 'changeduser@test.com', 'password': 'password'})

			self.assertEqual(res.status_code, 302)
			u = User.query.get(self.testuser_id)

			self.assertEqual(u.username, 'changeduser')
			self.assertEqual(u.email, 'changeduser@test.com')

			# Test with invalid password
			res = c.post(f'/user/{u.username}/profile', 
				data={'username': 'changeduseragain', 'email': 'changeduseragain@test.com', 'password': 'invalid_password'})

			self.assertEqual(res.status_code, 200)
			u = User.query.get(self.testuser_id)
		
			self.assertIn('Invalid credentials.', str(res.data))
			self.assertNotEqual(u.username, 'changeduseragain')
			self.assertNotEqual(u.email, 'changeduseragain@test.com')

			# Test with already taken username


	def test_edit_password(self):
		with self.client as c:
			c.post('/login', 
				data={'username': self.testuser.username, 'password': 'password'},
				follow_redirects=True)

			#Test with valid password
			old_hashed_pwd = User.query.get(self.testuser_id).password

			res = c.post(f'/user/{self.testuser.username}/password', 
				data={'current_password': 'password', 'new_password': 'newpassword', 'confirm': 'newpassword'})
			
			self.assertEqual(res.status_code, 302)
			self.assertNotEqual(old_hashed_pwd, User.query.get(self.testuser_id).password)

			#Test with invalid password
			old_hashed_pwd = User.query.get(self.testuser_id).password

			res = c.post(f'/user/{self.testuser.username}/password', 
				data={'current_password': 'badpassword', 'new_password': 'newpassword', 'confirm': 'newpassword'})

			self.assertEqual(res.status_code, 200)
			self.assertEqual(old_hashed_pwd, User.query.get(self.testuser_id).password)

	def test_save_search(self):
		with self.client as c:
			c.post('/login', 
				data={'username': self.testuser.username, 'password': 'password'},
				follow_redirects=True)
			
			res = c.post(f'/search/{self.testsearch_id}/save')

	# def test_delete_search(self):
	
	# def test_edit_search(self):
