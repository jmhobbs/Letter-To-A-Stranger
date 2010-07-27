# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config

class Database ( object ):

	session = None
	engine = None

	def __init__ ( self ):
		Session = sessionmaker()
		self.engine = create_engine( config.DATABASE )
		Session.configure( bind=self.engine )
		self.session = Session()