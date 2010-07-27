# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
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
	status = Column( Enum( 'PENDING', 'CONFIRMED', 'DORMANT', 'BAD_ADDRESS' ) )
	spam_threshold = Column( Integer )
	vulgarity_threshold = Column( Integer )

	def __init__( self, email ):
		self.email = email
		self.status = 'PENDING'
		self.letters_sent = 0
		self.replys_completed = 0
		self.replys_dropped = 0
		self.spam_threshold = 25
		self.vulgarity_threshold = 25

	def __repr__( self ):
		return "<User('%s', '%s')>" % ( self.id, self.email )

class LetterChain ( Base ):
	__tablename__ = 'letter_chains'

	id = Column( Integer, primary_key=True )
	slug = Column( String( 40 ) )
	origin_id = Column( Integer, ForeignKey( 'users.id' ) )
	replier_id = Column( Integer, ForeignKey( 'users.id' ) )
	started = Column( DateTime )
	linked = Column( DateTime )
	drop_count = Column( Integer )
	state = Column( Enum( 'PENDING', 'LINKED', 'FAILED', 'SPAM' ) )

	# TODO: Figure out how to make these relationships work...
	#origin_user = relationship( User, backref="origin_letter_chains", primaryjoin=origin_id, foreign_keys=[ origin_id ] )
	#reply_user = relationship( User, backref="reply_letter_chains", primaryjoin=replier_id, foreign_keys=[ replier_id ] )

	def __repr__( self ):
		return "<LetterChain('%s')>" % self.id

class Letter ( Base ):
	__tablename__ = 'letters'

	id = Column( Integer, primary_key=True )
	letter_chain_id = Column( Integer, ForeignKey( 'letter_chains.id' ) )
	user_id = Column( Integer, ForeignKey( 'users.id' ) )
	hash = Column( String( 40 ) )
	recieved = Column( DateTime )
	spam_weight = Column( Integer )
	vulgarity_weight = Column( Integer )

	letter_chain = relationship( LetterChain, backref="letters" )
	user = relationship( User, backref="letters" )

	def __repr__( self ):
		return "<Letter('%s', '%s')>" % ( self.id, self.hash )

class AttemptedLink ( Base ):
	__tablename__ = 'attempted_links'

	letter_chain_id = Column( Integer, ForeignKey( 'letter_chains.id' ), primary_key=True )
	user_id = Column( Integer, ForeignKey( 'users.id' ), primary_key=True )
	link_sent = Column( DateTime )
	link_expires = Column( DateTime )
	link_result = Column( Enum( 'PENDING', 'LINKED', 'DROPPED', 'FAILED', 'VULGARED', 'SPAMMED' ) )
	result_time = Column( DateTime )

	letter_chain = relationship( LetterChain, backref="attempted_links" )
	user = relationship( User, backref="attempted_links" )

	def __repr__( self ):
		return "<AttemptedLink('%s', '%s')>" % ( self.letter_chain_id, self.user_id )

class LetterSend ( Base ):
	__tablename__ = 'letter_sends'

	id = Column( Integer, primary_key=True )
	letter_id = Column( Integer, ForeignKey( 'letters.id' ) )
	user_id = Column( Integer, ForeignKey( 'users.id' ) )
	sent = Column( DateTime )
	failure = Column( Enum( 'NONE', 'BAD_ADDRESS' ) )
	failure_time = Column( DateTime )

	letter = relationship( Letter, backref="sends" )
	user = relationship( User, backref="letters_sent_to" )

	def __repr__( self ):
		return "<LetterSend('%s')>" % self.id

class VulgarLog ( Base ):
	__tablename__ = 'vulgar_logs'

	id = Column( Integer, primary_key=True )
	letter_id = Column( Integer, ForeignKey( 'letters.id' ) )
	marker_id = Column( Integer, ForeignKey( 'users.id' ) )
	marked_at = Column( DateTime )

	letter = relationship( Letter )
	user = relationship( User )

	def __repr__ ( self ):
		return "<VulgarLog('%d')>" % self.id

class SpamLog ( Base ):
	__tablename__ = 'spam_logs'

	id = Column( Integer, primary_key=True )
	letter_id = Column( Integer, ForeignKey( 'letters.id' ) )
	marker_id = Column( Integer, ForeignKey( 'users.id' ) )
	marked_at = Column( DateTime )

	letter = relationship( Letter )
	user = relationship( User )

	def __repr__ ( self ):
		return "<SpamLog('%d')>" % self.id

class Registration ( Base ):
	__tablename__ = 'registrations'

	id = Column( Integer, primary_key=True )
	user_id = Column( Integer, ForeignKey( 'users.id' ) )
	recieved = Column( DateTime )
	hash = Column( String( 40 ) )

	user = relationship( User, backref="registrations" )

	def __repr__ ( self ):
		return "<Registration('%d', '%s')>" % ( self.id, self.recieved )

class Quit ( Base ):
	__tablename__ = 'quits'

	id = Column( Integer, primary_key=True )
	user_id = Column( Integer, ForeignKey( 'users.id' ) )
	recieved = Column( DateTime )
	hash = Column( String( 40 ) )

	user = relationship( User, backref="quits" )

	def __repr__ ( self ):
		return "<Quit('%d')>" % self.id