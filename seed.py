from models import User, Search, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()
Search.query.delete()

folke = User.signup('folke', 'folke@gmail.com', 'password')
linda = User.signup('linda', 'linda@gmail.com', 'password')
noel = User.signup('noel', 'noel@gmail.com', 'password')

db.session.commit()

search1 = Search(
  location='Gatlinburg, Tennessee, US',
  date='2020-06-04',
  dates='6-4-20,6-5-20,6-6-20,6-7-20,6-8-20,6-9-20,6-10-20,6-11-20,6-12-20,6-13-20,6-14-20,6-15-20,6-16-20,6-17-20,6-18-20,6-19-20,6-20-20,6-21-20,6-22-20,6-23-20,6-24-20,6-25-20,6-26-20,6-27-20,6-28-20,6-29-20,6-30-20',
  deaths='2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3',
  cases='97,100,109,110,129,158,178,184,206,229,233,248,285,297,342,387,411,420,422,464,489,516,536,549,549,588,608',
  created_at='2020-07-01',
  description='Cases from 2020-06-04 in Gatlinburg, Tennessee',
  user_id=1
   )

db.session.add(search1)
db.session.commit()