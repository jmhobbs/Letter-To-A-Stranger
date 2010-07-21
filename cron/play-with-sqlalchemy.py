# -*- coding: utf-8 -*-

# http://www.sqlalchemy.org/docs/ormtutorial.html

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.exc import IntegrityError

from os.path import dirname

# Set up our custom classes
Base = declarative_base()
Session = sessionmaker()

# Set up SQL connection and bind it to the session factory
engine = create_engine( 'sqlite://%s/test.sqlite' % dirname( __file__ ) )
Session.configure( bind=engine )

# Declare our user model
class User ( Base ):
	__tablename__ = 'users'

	email = Column( String, primary_key=True )
	letters_sent = Column( Integer )
	replys_completed = Column( Integer )
	replys_dropped = Column( Integer )

	def __init__( self, email ):
			self.email = email
			self.letters_sent = 0
			self.replys_completed = 0
			self.replys_dropped = 0

	def __repr__(self):
		return "<User('%s')>" % self.email

# Start our session
session = Session()

# Try out some ORM action
try:
	test_user = User( 'john@velvetcache.org' )
	session.add( test_user )
	session.commit()
except IntegrityError:
	session.rollback()
	print "Didn't save user, duplicate primary key!"

# Get that user back!
our_user = session.query( User ).filter_by( email='john@velvetcache.org' ).first()
if our_user:
	print "Email:", our_user.email
else:
	print "Couldn't find that user!"