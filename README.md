## About this Project

Automatically make reservations on resy.com for hard-to-get restaurants.

TODO (not implemented)
Ability for table selection. Currently grabs the first availability for given day.
Ability to reserve with credit card on file.

## Getting Started

1. Clone this repository

2. Install dependencies

    ```bash
    pipenv install
    ```

3. Create **.env** file in root directory, and create EMAIL and PASSWORD variables based on your resy log in info

    ```
    EMAIL=example@example.com
    PASSWORD=examplePassword000
    ```

4. Insert values into config.ini file

    ```
    Venue: 0000
    Date: 2023-12-31
    Guests: 2
    ```

    Note: Venue Id can be found in the network tab from the restaurant page on resy. Date is in YYYY-MM-DD format

5. Enter virtual environment and run script, or run script directly

    ```bash
    pipenv shell
    python3 resy_bot.py
    ```

    OR

    ```bash
    pipenv run python3 resy_bot.py
    ```

6. Failed attempts will be logged in attempts.csv . Leave script running.
