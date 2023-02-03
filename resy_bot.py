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



def get_details(venue, date, guests):
    response = requests.get(f'https://api.resy.com/4/find?lat=0&long=0&day={date}&party_size={guests}&venue_id={venue}', headers=headers)

    data = response.json()

    results = data["results"]
    if len(results):
        open_slots = results["venues"][0]["slots"]
        res = [slot["date"]["start"] for slot in open_slots]

    print("AVAILABLE SLOTS\n \n",res)

    return res

def read_config():
    parser = configparser.ConfigParser()
    parser.read("config.ini")

    obj = parser["CONFIG"]

    return obj["Venue"], obj["Date"], obj["Guests"]


def main():
    venue, date, guests = read_config()

    avail_slots = get_details(venue, date, guests)

    login_token, payment_method = login()
    if login_token == "error":
        return



main()
