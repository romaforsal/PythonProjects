import pymongo
from config.settings import MONGODB_URI, DATABASE_NAME # [cite: 30]

class MongoDBDAO:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBDAO, cls).__new__(cls)
            try:
                # Setup connection using .env variables [cite: 9, 24]
                cls._instance.client = pymongo.MongoClient(MONGODB_URI)
                cls._instance.db = cls._instance.client[DATABASE_NAME]
                cls._instance.connection_ok = True # [cite: 42]
            except Exception:
                cls._instance.connection_ok = False
        return cls._instance

    def save_session(self, session_data): # [cite: 14, 31, 41]
        if self.connection_ok:
            return self.db.sessions.insert_one(session_data)

    def save_volume_event(self, event_data): # [cite: 14, 32, 41]
        if self.connection_ok:
            return self.db.volume_events.insert_one(event_data)