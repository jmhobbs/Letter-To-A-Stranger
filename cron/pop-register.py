# -*- coding: utf-8 -*-

import mail
import models

server = mail.Inbound( 'register' )

print "Messages: %d" % server.messages