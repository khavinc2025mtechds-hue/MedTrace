"""SQLite default or explicit PostgreSQL. Never silently downgrade a failed DB."""
import os
from functools import lru_cache
from sqlalchemy import create_engine,event
from sqlalchemy.orm import sessionmaker
from config.settings import path
from src.database.models import Base
@lru_cache(maxsize=1)
def engine():
    url=os.getenv('DATABASE_URL','sqlite:///data/medtrace.db')
    if url.startswith('sqlite:///') and url!='sqlite:///:memory:':
        file=path(url[len('sqlite:///'):]);file.parent.mkdir(parents=True,exist_ok=True);url='sqlite:///'+file.as_posix()
    eng=create_engine(url,connect_args={'check_same_thread':False} if url.startswith('sqlite') else {},pool_pre_ping=True)
    if url.startswith('sqlite'):
        @event.listens_for(eng,'connect')
        def enable_foreign_keys(connection,record):connection.execute('PRAGMA foreign_keys=ON')
    Base.metadata.create_all(eng);return eng

def session():return sessionmaker(bind=engine(),expire_on_commit=False)()
