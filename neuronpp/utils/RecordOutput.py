import numpy as np


class RecordOutput:
    def __init__(self, variable: str, records: np.array, time: np.array):
        """
        :param variable:
            a variable name of the records
        :param records:
            a numpy array contains records for the selected variable. If there were multiple sources
             of recordings (eg. many segments or many point processes) each of them will be stored
             as a separated dimension of the array
        :param time:
            a numpy array contains time records
        """
        self.variable = variable
        self.records = records
        self.time = time

    def get_records_from_time(self, ms):
        """
        Returns records array where time in miliseconds is higher than ms.

        If there were multiple sources of recordings (eg. many segments or many point processes)
        each of them will be stored as a separated dimension of the array.

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
