from Partner import Partner
from Country import Country
#installed using python-dateutil
from dateutil.parser import parse
import datetime
#installed using python-requests
import requests
import json


"""
    Performs a get request at the indicated HubSpot api
"""
def get_json():
    data = requests.get('https://candidate.hubteam.com/candidateTest/v2/partners?userKey=cc77851c9d677bffec6e915c5fc1')
    return data.json()

def parse_json(json_in):
    country_result = []
    country_dict = dict()

    """
         Adds a country to the dictionary if it does not already exist
    """
    for p in json_in['partners']:
        employee = Partner(p)
        if employee.country not in country_dict:
            country_dict[employee.country] = dict()

        """
            Sets an employee under the subdictionary to hold the available dates
        """
        for available in employee.dates_available:
            if available not in country_dict[employee.country]:
                country_dict[employee.country][available] = set()
            country_dict[employee.country][available].add(employee)


        for country, dates in country_dict.items():
            sorted_dates = sorted(dates.keys())
            min_attendees = 0
            min_days = None
            max_attendees = set()

            """
                Parses all date formats to a readable form that can be used to compare. This is how to find two
                dates that are consecutive
            """
            for i in range(len(sorted_dates[:-1])):

                current_date = sorted_dates[i]
                current_tomorrow = sorted_dates[i+1]
                current_date_formatted = parse(current_date)
                current_tomorrow_formatted = parse(current_tomorrow)

                date_attendees = dates[current_date]
                tomorrow_attendees = dates[current_tomorrow]

                if current_tomorrow_formatted - current_date_formatted != datetime.timedelta(1):
                    continue
                attendees = date_attendees & tomorrow_attendees
                attend_total = len(attendees)

                """
                    Sets a new date if the total number of attendees for a given date is greater than the already
                    existing max date
                """
                if attend_total > min_attendees:
                    min_attendees = attend_total
                    min_days = current_date
                    max_attendees = attendees
            """
                Creates Country objects to hold the correct format able to be put into JSON
            """
            country = Country()
            country.name = country
            if min_attendees > 0:
                country.final_start_date = min_attendees
            for attendee in max_attendees:
                country.add(attendee)
            country_result.append(country)
            return country_result

def get_final(countries):
    final = dict()
    final['countries'] = list(map(lambda result: result.get_final(), countries))
    return final

"""
    Posts the final list of countries w/ dates and attendees to the HubSpot api
"""
def json_out(final_send):
    r = requests.post('https://candidate.hubteam.com/candidateTest/v2/results?userKey=cc77851c9d677bffec6e915c5fc1', data=json.dumps(final_send))
    print(r)

def main():
    json_in = get_json()
    countries = parse_json(json_in)
    final_send = get_final(countries)
    json_out(final_send)
if __name__ == '__main__':
    main()