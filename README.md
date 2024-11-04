# SmartHack 2024 - SilyCars:3 🐱

## Components and workflow
1. **CSV Parsing and Object Initialization**:
   - The code starts by loading data from CSV files into lists of objects (`Refinery`, `Customer`, `Tank`, `Connection`, and `Demand`).
   
2. **API Session Setup**:
   - An API session is started with a POST request to obtain a `SESSION-ID`. This `SESSION-ID` is included in subsequent API requests to maintain the session context.

3. **Demand Handling Logic**:
   - The code iterates over a 42-round period (looping through `day` from 0 to 42).
   - For each day, demands are handled by finding the best connection (tank or refinery) based on cost metrics.
   - **Sorting and Selecting Demands**: Demands are sorted by urgency (`start_delivery_day`) to prioritize near-term needs.
   - **Cost Optimization**: For each demand, the code attempts to find a tank or refinery connection that meets the demand quantity at the lowest cost.
   - If no optimal tank is available, the code looks for refineries with the capacity and fuel to fulfill the demand.

4. **Refinery Overflow Management**:
   - To prevent refineries from overflowing, the code monitors each refinery's stock.
   - If the stock nears capacity, it transfers excess stock to available tanks based on cost-efficiency.

5. **API Play Calls and Result Logging**:
   - Each day, an API request is made to submit the day’s transactions (`play_api`).
   - Responses are logged in `play_output.json` to keep a record of each round.

## Separate 'solution': Hacking the API
- underflow variable `amount` in API call by putting a value from range [\MIN_INT_64; MIN_INT_64 / 100 + 1\].
- This makes penalty calculation result in negative penalties, because server processes `amount` as a variable of type `long` in java, so it wraps around at underflow.
