# -*- coding: utf-8 -*-

import config

import re

import poplib
import smtplib

from email.mime.text import MIMEText
from email.parser import Parser

from effbot import unescape

# Build our POP3 connection
if config.POP_IS_SSL:
	pop = poplib.POP3_SSL( config.POP_SERVER, config.POP_PORT )
else:
	pop = poplib.POP3( config.POP_SERVER, config.POP_PORT )

pop.user( config.POP_USER )
pop.pass_( config.POP_PASSWORD )

# Build out SMTP connection

#smtp = smtplib.SMTP( config.SMTP_SERVER )
#smtp.set_debuglevel( 1 )
#smtp.sendmail( fromaddr, toaddrs, msg )
#smtp.quit()

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

def print_part ( part ):
	if "text/plain" == part.get_content_type():
		print "==[ text/plain ]========================"
		print part.get_payload()
		print "=" * 40
	elif "text/html" == part.get_content_type():
		print "==[ text/html ]========================="
		print html_to_text( part.get_payload() )
		print "=" * 40

# Start working on messages!
messages = len( pop.list()[1] )

print "You have %d new messages." % messages

for i in range( messages ):
	message = ""
	for j in pop.retr( i + 1 )[1]:
		message += j + "\n"
	email = Parser().parsestr( message )
	print '-' * 40
	print "From:", email['From']
	print " MID:", email['Message-ID']
	print "Date:", email['Date']
	print
	print "Is Multipart?",
	if email.is_multipart():
		print "Yes"
		print
		for part in email.get_payload():
			print_part( part )
	else:
		print "No"
		print
		print_part( email.get_payload() )
	#pop.dele( i + 1 )
pop.quit()
print '-' * 40