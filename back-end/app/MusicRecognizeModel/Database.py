from sqlalchemy import create_engine, Column, Boolean, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config
from sqlalchemy.exc import ProgrammingError, DatabaseError

Base = declarative_base()


class Songs(Base):
	# Table name:
	__tablename__ = 'Songs'

	# Table structure:
	id = Column(Integer, autoincrement=True, primary_key=True)
	name = Column(String(64))
	filehash = Column(String(512), index=True)
	fingerprinted = Column(Boolean, default=False)


class Fingerprints(Base):
	# Table name:
	__tablename__ = 'Fingerprints'

	# Table structure:
	id = Column(Integer, autoincrement=True, primary_key=True)
	song_id = Column(Integer, index=False)
	# length of string depend on how long your fingerprint is.
	fingerprint = Column(String(64), index=True)
	offset = Column(Integer)


def createTables(conn=config.sqlalchemy_address):
	try:
		engine = create_engine(conn)
		Base.metadata.create_all(engine)
		return True
	except:
		return False


def checkDatabase(conn=config.sqlalchemy_address):
	try:
		engine = create_engine(conn)
		DBSession = sessionmaker(bind=engine)
		dbs = DBSession()
		dbs.query(Songs).first()
		dbs.query(Fingerprints).first()
		return True, 0, ""
	except ProgrammingError as err:
		return False, err.code, err.orig
	except DatabaseError as err:
		return False, err.code, err.orig


def initSession(conn=config.sqlalchemy_address):
	# init connection
	engine = create_engine(conn)
	DBSession = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
	return DBSession, engine
