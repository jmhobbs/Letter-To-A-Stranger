# -*- coding: utf-8 -*-

import datetime

import mail
import models
import database

db = database.Database()

server = mail.Inbound( 'register' )

print "New Messages: %d" % server.messages

for i in range( server.messages ):
	message = server.next_message()
	user = session.query( models.User ).filter_by( email=message._from ).first()
	if user:
		try:
			user.registrations.append( models.Registration( recieved=datetime.datetime.now(), hash="TODO-TODO-TODO" ) )
			user.status = 'CONFIRMED'
			db.session.add( user )
			db.session.commit()
		except IntegrityError:
			db.session.rollback()
			continue
	else:
		try:
			user = models.User( message._from )
			user.joined = datetime.datetime.now()
			user.registrations.append( models.Registration( recieved=datetime.datetime.now(), hash="TODO-TODO-TODO" ) )
			db.session.add( user )
			db.session.commit()
		except IntegrityError:
			db.session.rollback()
			continue
	server.delete_message()