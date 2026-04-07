from datetime import datetime

class Session:
    def __init__(self):
        self.start_time = datetime.now()
        self.end_time = None
        self.duration = None

    def to_dict(self):
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_seconds": self.duration
        }