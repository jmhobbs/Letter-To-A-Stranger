# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

import models
import config

import datetime

Session = sessionmaker()

engine = create_engine( config.DATABASE )
Session.configure( bind=engine )
session = Session()

## Try out some ORM action
try:
	user = models.User( 'test@example.com' )
	user.joined = datetime.datetime.now()
	session.add( user )
	session.commit()
except IntegrityError:
	session.rollback()
	print "== Didn't save user, duplicate primary key! ==\n"

our_user = session.query( models.User ).filter_by( email='test@example.com' ).first()
if our_user:

	our_user.registrations.append( models.Registration( recieved=datetime.datetime.now(), hash="abcdefg" ) )
	session.add( our_user )
	session.commit()

	print "        Email:", our_user.email
	print "Registrations:", our_user.registrations
else:
	print "== Couldn't find that user! ==\n"