# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User ( Base ):
	__tablename__ = 'users'

	id = Column( Integer, primary_key=True )
	joined = Column( DateTime )
	email = Column( String( 255 ) )
	letters_sent = Column( Integer )
	replys_completed = Column( Integer )
	replys_dropped = Column( Integer )
	status = Column( Enum( 'CONFIRMED', 'DORMANT', 'BAD_ADDRESS' ) )

	def __init__( self, email ):
		self.email = email
		self.letters_sent = 0
		self.replys_completed = 0
		self.replys_dropped = 0

	def __repr__( self ):
		return "<User('%s', '%s')>" % ( self.id, self.email )

class LetterChain ( Base ):
	__tablename__ = 'letter_chains'

	id = Column( Integer, primary_key=True )
	slug = Column( String( 40 ) )
	origin_id = Column( Integer )
	replier_id = Column( Integer )
	started = Column( DateTime )
	linked = Column( DateTime )

	def __repr__( self ):
		return "<LetterChain('%s')>" % self.id

class AttemptedLink ( Base ):
	__tablename__ = 'attempted_links'

	letter_id = Column( Integer, primary_key=True )
	user_id = Column( Integer, primary_key=True )
	link_sent = Column( DateTime )
	link_expires = Column( DateTime )
	link_result = Column( Enum( 'PENDING', 'LINKED', 'DROPPED', 'FAILED', 'VULGARED', 'SPAMMED' ) )
	result_time = Column( DateTime )

	def __repr__( self ):
		return "<AttemptedLink('%s', '%s')>" % ( self.letter_id, self.user_id )

class Letter ( Base ):
	__tablename__ = 'letters'

	id = Column( Integer, primary_key=True )
	letter_chain_id = Column( Integer )
	user_id = Column( Integer )
	hash = Column( String( 40 ) )
	recieved = Column( DateTime )

	def __repr__( self ):
		return "<Letter('%s', '%s')>" % ( self.id, self.hash )

class LetterSend ( Base ):
	__tablename__ = 'letter_sends'

	id = Column( Integer, primary_key=True )
	letter_id = Column( Integer )
	user_id = Column( Integer )
	sent = Column( DateTime )
	failure = Column( Enum( 'NONE', 'BAD_ADDRESS' ) )
	failure_time = Column( DateTime )

	def __repr__( self ):
		return "<LetterSend('%s')>" % self.id