class WriteWorklogsRequest:
    def __init__(self, year: int, month: int, date: int):
        self.date = date
        self.month = month
        self.year = year

    @staticmethod
    def deserialize(payload):
        year = payload['year']
        month = payload['month']
        date = payload['day']
        return WriteWorklogsRequest(year, month, date)
