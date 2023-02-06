import requests
import configparser
import os
from dotenv import load_dotenv

#date in YYYY-MM-DD format

headers = {
    'authorization': 'ResyAPI api_key="VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"',
    'content-type': 'application/x-www-form-urlencoded'
}

def login():
    print('Logging in.....')
    load_dotenv()

    body = {"email": os.getenv('EMAIL'), "password": os.getenv("PASSWORD")}
    response = requests.post('https://api.resy.com/3/auth/password', headers=headers, data=body)
    response_data = response.json()

    if response.status_code == 200:
        print("Successfully logged in")
    else:
        print("ERROR LOGGING IN", "status code: ", response_data["status"], "message: ", response_data["message"])
        return "error", "error"


    login_token = response_data["token"]
    payment_method = response_data["payment_method_id"]


    return login_token, payment_method



def get_config_token(venue, date, guests):
    response = requests.get(f'https://api.resy.com/4/find?lat=0&long=0&day={date}&party_size={guests}&venue_id={venue}', headers=headers)

    data = response.json()

    results = data.get("results")

    if results == None:
        print("Incorrect values in config file.")
        return

    open_slots = results["venues"][0]["slots"]
    avail_times = [slot["date"]["start"] for slot in open_slots]
    print("AVAILABLE SLOTS\n", avail_times, "\n")

    res = [slot for slot in open_slots]
    if res:
        config_data = res[0].get("config") #currently getting first avail time, TODO make dynamic
        return config_data.get("token")

def make_reservation(login_token, date, guests, config_id):

    params = {
        'config_id': config_id,
        'day': date,
        'party_size': guests
    }

    response = requests.get('https://api.resy.com/3/details', headers=headers, params=params)
    booking_details = response.json()
    print(booking_details)
    if not booking_details.get("book_token"):
        return
    else:
        booking_token = booking_details["book_token"].get("value")

        data = {'book_token': booking_token}

        headers['X-Resy-Auth-Token'] = login_token
        response = requests.post('https://api.resy.com/3/book', headers=headers, data=data)

        res = response.json()
        print(res)

def read_config():
    parser = configparser.ConfigParser()
    parser.read("config.ini")

    obj = parser["CONFIG"]

    return obj["Venue"], obj["Date"], obj["Guests"]


def main():
    venue, date, guests = read_config()


    login_token, payment_method = login()
    if login_token == "error":
        return

    config_id = get_config_token(venue, date, guests)
    print(config_id)

    make_reservation(login_token, date, guests, config_id)



main()
