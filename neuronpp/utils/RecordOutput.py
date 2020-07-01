import numpy as np


class RecordOutput:
    def __init__(self, records, time):
        self.records = records
        self.time = time

    def get_records_from_time(self, ms):
        """
        Returns records array where time in miliseconds is higher than ms
        :param ms:
            time in ms
        """
        min_arg = np.min(np.where(self.time > ms))
        return self.records[min_arg:]

    def get_records_to_time(self, ms):
        """
        Returns records array where time in miliseconds is lower than ms
        :param ms:
            time in ms
        """
        max_arg = np.max(np.where(self.time > ms))
        return self.records[:max_arg]

    @property
    def size(self):
        return self.records.size

    @property
    def shape(self):
        return self.records.shape
