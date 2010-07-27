# -*- coding: utf-8 -*-

import poplib
from email.mime.text import MIMEText
from email.parser import Parser
import re

import config
from effbot import unescape

# Build our HTML removal regex.
# TODO: Use lxml or something stronger.
html_remove = re.compile( r'<[^<]*?/?>' )

# HTML comes in wrapped with an "=" on the end of wrapped lines
# This Regex should fix all of those.
# Not sure if this is always needed...
html_unwrap = re.compile( r'=\n' )

def html_to_text ( html ):
	# Unwrap long lines
	html = html_unwrap.sub( '', html )
	# Add newlines when we can
	html = html.replace( '<br>', "\n" )
	html = html.replace( '</br>', "\n" )
	html = html.replace( '</p>', "\n" )
	# Strip remaining tags
	html = html_remove.sub( '', html )
	# Convert remaining entities to plain text
	return unescape( html )

class InboundEmail ( object ):
	""" An e-mail message, parsed from a raw MIME message. """
	_from = None
	date = None
	text = None
	headers = ()

	def __init__ ( self, raw ):
		parsed = Parser().parsestr( raw )
		self._from = email['From']
		self.date = email['Date']
		self.headers = email.items()

		if email.is_multipart():
			for part in email.get_payload():
				if "text/plain" == part.get_content_type():
					self.text = part.get_payload()
					break
				elif "text/html" == part.get_content_type():
					self.text = html_to_text( part.get_payload() )
		else:
			if "text/plain" == email.get_payload().get_content_type():
				self.text = email.get_payload()
			elif "text/html" == email.get_payload().get_content_type():
				self.text = html_to_text( email.get_payload() )

		if None == self.text:
			raise Exception( 'No valid content.' )

class Inbound ( object ):
	""" Defines an inbound email server. Uses POP3 for now. """

	connection = None
	messages = 0
	counter = -1

	def __init__ ( self, account ):
		""" Creates an inbound e-mail reader from an account specifier. """
		if config.POP[account]['ssl']:
			self.connection = poplib.POP3_SSL( config.POP[account]['server'], config.POP[account]['port'] )
		else:
			self.connection = poplib.POP3( config.POP[account]['server'], config.POP[account]['port'] )

		self.connection.user( config.POP[account]['user'] )
		self.connection.pass_( config.POP[account]['password'] )

		self.messages = len( self.connection.list()[1] )

	def __del__ ( self ):
		""" Quits the POP3 connection, ensuring e-mail deletion. """
		if self.connection:
			self.connection.quit()

	def next_message ( self ):
		"""
			Increment the counter and retrieve the next available message.

			Returns None when no messages remain.
		"""
		self.counter += 1
		if self.counter >= self.messages:
			return None
		return self.get_message()

	def get_message ( self ):
		""" Get the current message. """
		message = ""
		for line in self.connection.retr( self.counter + 1 )[1]:
			message += line + "\n"
		return InboundEmail( message )

	def delete_message ( self ):
		""" Delete the current message. """
		self.connection.dele( self.counter + 1 )