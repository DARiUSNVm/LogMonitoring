# Log Monitoring Project

This project monitors processes from a CSV file and generates a report based on their execution time.

## Features

- Reads the CSV file and extracts the jobs data.
- Identifies each job and tracks its start and finish times.
- Logs warning if the job is taking more than 5 minutes to finish.
- Logs error if the job is taking more than 10 minutes to finish.
- Generates a report (`output.txt`)

## File Structure

- `main.py`: The main script that loads data, validates rows, processes data, and writes the results to an output file.
- `test.py`: The script that holds the unit tests.
- `logs.log`: The input CSV file containing the process logs.
- `output.txt`: The output file containing the generated report.

## Usage

1. Clone the repository:
    ```
    git clone https://github.com/DARiUSNVm/LogMonitoring.git
    ```

2. Ensure you have installed all necessary dependencies:
    ```
    pip3 install pandas
    pip3 install unittest
    ```

3. Place the CSV file (`logs.log`) in the same directory as `main.py`.

4. Run the script:
    ```
    python3 main.py
    ```

5. Check the output file (`output.txt`) for the generated report.