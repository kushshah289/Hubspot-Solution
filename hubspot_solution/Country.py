class Country:
    def __init__(self):
        self.attendees = []
        self.name = None
        self.final_start_date = None

    def add(self, partner):
        self.attendees.append(partner.email)

    def get_final(self):
        final = dict()
        final['attendeeCount'] = len(self.attendees)
        final['attendees'] = sorted(self.attendees)
        final['name'] = self.name
        final['startDate'] = self.final_start_date
        return final