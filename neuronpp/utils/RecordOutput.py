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

    def get_records_from_time(self, ms, with_time_vector=False):
        """
        Returns records array where time in miliseconds is equal or higher than ms.

        If there were multiple sources of recordings (eg. many segments or many point processes)
        each of them will be stored as a separated dimension of the array.

        :param ms:
            time in ms
        :param with_time_vector:
            Default False. If True it will return tuple of (records, time)
        """
        min_arg = np.min(np.where(self.time >= ms))
        if with_time_vector:
            return self.records[min_arg:], self.time[min_arg:]
        else:
            return self.records[min_arg:]

    def get_records_to_time(self, ms, with_time_vector=False):
        """
        Returns records array where time in miliseconds is lower than ms

        If there were multiple sources of recordings (eg. many segments or many point processes)
        each of them will be stored as a separated dimension of the array.

        :param ms:
            time in ms
        :param with_time_vector:
            Default False. If True it will return tuple of (records, time)
        """
        max_arg = np.max(np.where(self.time <= ms))+1
        if with_time_vector:
            return self.records[:max_arg], self.time[:max_arg]
        else:
            return self.records[:max_arg]

    def get_records_by_time(self, from_ms, to_ms, with_time_vector=False):
        """
        Returns records array where time in miliseconds is between 2 values

        If there were multiple sources of recordings (eg. many segments or many point processes)
        each of them will be stored as a separated dimension of the array.

        :param to_ms:
            time in ms, inclusive (will be higher or equal this time)
        :param from_ms:
            time in ms, exclusive (will be lower than this time)
        :param with_time_vector:
            Default False. If True it will return tuple of (records, time)
        """
        from_arg = np.min(np.where(self.time >= from_ms))
        to_arg = np.max(np.where(self.time <= to_ms))+1
        if with_time_vector:
            return self.records[from_arg:to_arg], self.time[from_arg:to_arg]
        else:
            return self.records[from_arg:to_arg]

    @property
    def size(self):
        return self.records.size

    @property
    def shape(self):
        return self.records.shape
