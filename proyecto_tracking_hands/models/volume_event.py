from datetime import datetime

class VolumeEvent:
    def __init__(self, old_vol, new_vol, distance):
        self.timestamp = datetime.now()
        self.old_volume = old_vol
        self.new_volume = new_vol
        self.finger_distance = distance

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "old_volume": self.old_volume,
            "new_volume": self.new_volume,
            "distance": self.finger_distance
        }