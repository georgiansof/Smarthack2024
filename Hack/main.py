import requests
import csv

api_base_args = {'API-KEY': '7bcd6334-bc2e-4cbf-b9d4-61cb9e868869'} #TODO de schimbat
start_api = 'http://localhost:8080/api/v1/session/start' #TODO de schimbat IP / port
play_api = 'http://localhost:8080/api/v1/play/round' #TODO de schimbat IP / port
end_api = 'http://localhost:8080/api/v1/session/end' #TODO de schimbat IP / port


def csvparser(filename):
    fields = []
    rows = []
    with open(filename, "r") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=";")
        fields = next(csvreader)
        for row in csvreader:
            rows.append(row)
            return fields, rows # I only need one valid connectionId
    return fields, rows


connections_csv = "../data/connections.csv"
fields, rows = csvparser(connections_csv)

connId = rows[0][0]

movement = {
    "connectionId" : connId,
    "amount" : -9223372036854775786
}

def process_server_response(response):
    response_data = response.json()
    day = response_data["round"]

    # Print penalties and KPIs for debugging purposes
    penalties = response_data.get("penalties", [])
    delta_kpis = response_data.get("deltaKpis", {})
    total_kpis = response_data.get("totalKpis", {})

    print(f"Day {day} - Penalties: {penalties}")
    print(f"Day {day} - Delta KPIs: {delta_kpis}")
    print(f"Day {day} - Total KPIs: {total_kpis}")


# Initialize session with server
def initialize_session():
    api_call = requests.post(start_api, headers=api_base_args)
    session_id = api_call.content.decode()
    api_base_args['SESSION-ID'] = session_id
    return session_id


def run_simulation():
    session_id = initialize_session()

    day = 0
    max_days = 42

    while day <= max_days:
        print(f"Processing day {day}")

        # Plan movements for the day
        movements = [movement for i in range(975)]


        api_body = {'day': day, 'movements': movements}

        response = requests.post(play_api, headers=api_base_args, json=api_body)

        if response.status_code != 200:
            print(f"Error on day {day}: {response.content}")
            break

        # Process server response to update demands and penalties
        process_server_response(response)

        print("Response:", response.json())
        day += 1

# Run the simulation
run_simulation()