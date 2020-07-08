""" User model tests """

import os
from unittest import TestCase
from sqlalchemy import exc
from models import User, login, db

os.environ['DATABASE_URL'] = 'postgresql:///covid-test'

from app import app

db.create_all()

class UserModelTestCase(TestCase):
	""" Test User Model """
	def setUp(self):
		db.drop_all()
		db.create_all()

		u1 = User.signup('testuser', 'user@test.com', 'testpwd')
		uid1 = 1111
		u1.id = uid1

		db.session.commit()

		u1 = User.query.get(uid1)

		self.u1 = u1
		self.uid1 = uid1
	
	def tearDown(self):
		res = super().tearDown()
		db.session.rollback()
		return res
	
	def test_user_model(self):
		""" Does basic model work? """

		u = User(
			email="test@test.com",
			username="tester",
			password="testpassword"
		)

		db.session.add(u)
		db.session.commit()

		# User should have no searches.
		self.assertEqual(len(u.searches), 0)	

#### Signup Tests ####
	def test_valid_signup(self):
		u = User.signup('signupuser', 'user1@test.com', 'testpwd')
		u.id = 1234
		db.session.commit()

		u = User.query.get(1234)

		self.assertIsNotNone(u)
		self.assertEqual(u.username, 'signupuser')
		self.assertEqual(u.email, 'user1@test.com')
		self.assertTrue(u.password.startswith('$2b$'))

	def test_invalid_username_singup(self):
		u = User.signup(None, 'user1@test.com', 'testpwd')
		u.id = 4321
		with self.assertRaises(exc.IntegrityError) as context:
			db.session.commit()
		
	def test_invalid_email_singup(self):
		u = User.signup(None, 'user1@test.com', 'testpwd')
		u.id = 4321
		with self.assertRaises(exc.IntegrityError) as context:
			db.session.commit()

#### Authentication Tests ####

	def test_valid_authentication(self):
		u = User.authenticate(self.u1.username, 'testpwd')
		self.assertIsNotNone(u)
		self.assertEqual(u.id, self.uid1)
	
	def test_invalid_username(self):
		self.assertFalse(User.authenticate('invaliduser', 'password'))

	def test_invalid_password(self):
		self.assertFalse(User.authenticate(self.u1.username, 'invalidpassword'))

#### Save Search Tests ####
