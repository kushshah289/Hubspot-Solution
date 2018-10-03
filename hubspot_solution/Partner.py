class Partner:
    def __init__(self, json_in):
        self.first_name = json_in['firstName']
        self.last_name = json_in['lastName']
        self.email = json_in['email']
        self.country = json_in['country']
        self.dates_available = json_in['availableDates']