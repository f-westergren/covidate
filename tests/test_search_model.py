""" Search model tests """

import os
from unittest import TestCase
from sqlalchemy import exc
from models import Search, User, login, db

from datetime import datetime

os.environ['DATABASE_URL'] = 'postgresql:///covid-test'

from app import app

class SearchModelTestCase(TestCase):
  """ Test Search Model """

  def setUp(self):
    db.drop_all()
    db.create_all()
    
    u = User.signup('testuser', 'user@test.com', 'testpwd')
    uid = 1111
    u.id = uid

    db.session.commit()

    s = Search.create({
      'location': 'Test location',
      'date': '2020-07-07',
      'dates': '6-10-20,6-11-20,6-12-20,6-13-20,6-14-20',
      'deaths': '402,406,410,416,422',
      'cases': '6916,6985,7051,7107,7151',
      'change_deaths': '1,2,3,4,5',
      'change_cases': '10,20,30,40,50',
      'created_at': datetime.now(),
      'description': 'Test description'
      })
    
    sid = 2222
    s.id = 2222

    u.searches.append(s)
    db.session.commit()

    self.u = u
    self.s = s

  def tearDown(self):
    res = super().tearDown()
    db.session.rollback()
    return res

  def test_search_model(self):
    """ Does basic model work? """

    testsearch = Search(
      location='test place',
      date='2020-01-01',
      dates='6-10-20',
      deaths='100',
      cases='200',
      change_cases='10',
      change_deaths='1'
      created_at=datetime.now(),
      description='Testing testing 123'
    )

    testsearch.id = 1234
    db.session.add(testsearch)
    db.session.commit()

    # Search should have no user ID.
    self.assertIsNone(testsearch.user_id)

    # Test user relationship
    self.u.searches.append(testsearch)
    db.session.commit()

    # Search should have user ID.
    self.assertEqual(len(self.u.searches), 2)

  def test_create(self):
    testsearch = Search.create({
      'location': 'Test place',
      'date': '2020-07-07',
      'dates': '6-10-20',
      'deaths': '402',
      'cases': '6916',
      'change_deaths': '1',
      'change_cases': '10',
      'description': 'Testing description'
    })

    testsearch.id = 1234
    db.session.add(testsearch)
    db.session.commit()

    testsearch = Search.query.get(1234)

    self.assertIsNotNone(testsearch)
    self.assertEqual(testsearch.location, 'Test place')
    self.assertEqual(testsearch.date, '2020-07-07')
    self.assertEqual(testsearch.dates, '6-10-20')
    self.assertEqual(testsearch.deaths, '402')
    self.assertEqual(testsearch.cases, '6916')
    self.assertEqual(testsearch.description, 'Testing description')
    self.assertIsInstance(testsearch.created_at, datetime)