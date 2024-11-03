import requests

movement = {
    "connectionId" : "79a7eaac-482a-4cd6-a5ee-596165f47f01",
    "amount" : -9223372036854775786
}

api_base_args = {'API-KEY': '7bcd6334-bc2e-4cbf-b9d4-61cb9e868869'}
start_api = 'http://localhost:8080/api/v1/session/start'
play_api = 'http://localhost:8080/api/v1/play/round'
end_api = 'http://localhost:8080/api/v1/session/end'

# Helpe
# Process server response for demand and penalties



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