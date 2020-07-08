import os
from unittest import TestCase

from models import db, connect_db, User, Search
from flask_login import current_user, login_user

from datetime import datetime
import json

os.environ['DATABASE_URL'] = 'postgresql:///covid-test'

from app import app

app.config['WTF_CSRF_ENABLED'] = False
app.config['TESTING'] = True

class SearchRouteTestCase(TestCase):
	""" Test views for search """

	def setUp(self):
		db.drop_all()
		db.create_all()

		self.client = app.test_client()
		self.testuser = User.signup(username='testuser', email='user@test.com', password='password') 
		self.testuser.id = 1000

		db.session.commit()

		self.searchObj = {
			'location': 'In-test location',
			'date': '2020-07-07',
			'dates': '6-10-20,6-11-20,6-12-20,6-13-20,6-14-20',
			'cases': '6916,6985,7051,7107,7151',
			'deaths': '402,406,410,416,422',
			'description': 'In-test description'
		}

		self.testsearch = Search.create(self.searchObj)
		self.testsearch.id = 2000
		self.testuser.searches.append(self.testsearch)

		db.session.commit()

	def tearDown(self):
		db.session.rollback()

	def test_valid_search(self):
		# Test valid search
		data = json.dumps({'date': '2020-06-01', 'location': 'Philadelphia, Pennsylvania, US'})
		headers = {'Content-Type': 'application/json'}

		with self.client as c:
			res = c.post('/search', data=data, headers=headers)

		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertIsInstance(data['cases'], list)
		self.assertIsInstance(data['deaths'], list)
		self.assertIsInstance(data['dates'], list)
		self.assertGreater(len(data['cases']), 30)
		self.assertEqual(len(data['cases']), len(data['deaths']))
		self.assertEqual(len(data['cases']), len(data['dates']))

		# Test invalid date
	def test_invalid_date(self):
		data = json.dumps({'date': '2020-10-01', 'location': 'Philadelphia, Pennsylvania, US'})
		headers = {'Content-Type': 'application/json'}

		with self.client as c:
			res = c.post('/search', data=data, headers=headers)

		data = res.data.decode("utf-8")

		self.assertEqual(res.status_code, 200)
		self.assertEqual(data, 'invalid date')

	def test_invalid_location(self):
		data = json.dumps({'date': '2020-10-01', 'location': 'Sweden'})
		headers = {'Content-Type': 'application/json'}

		with self.client as c:
			res = c.post('/search', data=data, headers=headers)

		data = res.data.decode("utf-8")

		self.assertEqual(res.status_code, 200)
		self.assertEqual(data, 'invalid location')
		
	def test_save_search_not_logged_in(self):
		data = json.dumps(self.searchObj)
		headers = {'Content-Type': 'application/json'}

		# Should return 'login' if user is not logged in.
		with self.client as c:
			res = c.post('/search/save', data=data, headers=headers)

		data = res.data.decode("utf-8")
		self.assertEqual(res.status_code, 200)
		self.assertEqual(data, 'login')

		u = User.query.get(1000)

		self.assertEqual(len(u.searches), 1)
		
	def test_save_search_logged_in(self):
		with self.client as c:
			c.post('/login', 
				data={'username': self.testuser.username, 'password': 'password'},
				follow_redirects=True)

		data = json.dumps(self.searchObj)
		headers = {'Content-Type': 'application/json'}

	# Should return 'saved' when user is logged in.
		res = c.post('/search/save', data=data, headers=headers)

		data = res.data.decode("utf-8")
		self.assertEqual(res.status_code, 200)
		self.assertEqual(data, 'saved')

		u = User.query.get(1000)

		self.assertEqual(len(u.searches), 2)

	def test_load_search(self):
		with self.client as c:
			c.post('/login', 
				data={'username': 'testuser', 'password': 'password'},
				follow_redirects=True)

			headers = {'Content-Type': 'application/json'}
			res = c.get('/search/load?id=2000')

		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertIsInstance(data['cases'], list)
		self.assertIsInstance(data['deaths'], list)
		self.assertIsInstance(data['dates'], list)
		self.assertEqual(len(data['cases']), 5)
		self.assertEqual(len(data['cases']), len(data['deaths']))
		self.assertEqual(len(data['cases']), len(data['dates']))
		self.assertEqual(data['location'], 'In-test location')
		self.assertEqual(data['date'], '2020-07-07')

  # def test_delete_search():