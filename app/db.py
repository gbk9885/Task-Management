import sys
from sqlalchemy import create_engine
# from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import redis
import logging
 
logger = logging.getLogger(__name__)
load_dotenv()
rd = redis.StrictRedis(
            host=os.environ.get("REDIS_URL"),
            port=6379,
            db=0,
        )
ping = rd.ping()
if ping is False:
    print("Connection Error!")
    sys.exit(1)
 
engine = create_engine(os.environ.get("DATABASE_URL"),
                        pool_size=100,        # Adjusted pool size based on needs
                        max_overflow=10,     # Allows extra connections during spikes
                        pool_timeout=30,     # Timeout before throwing error if pool is full
                        # pool_recycle=1800,   # Recycle connections every 30 minutes
                        pool_pre_ping=True   # Ensure connections are alive before use
                    )

SessionLocal  = sessionmaker(bind=engine,autocommit=False,autoflush=False)
 
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        logger.info(f' Closing DB Connection ...! ')
        db.close()