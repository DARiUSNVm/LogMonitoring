import pandas as pd
import os
from datetime import datetime, timedelta

CSV_FILE_NAME = 'logs.log'
OUTPUT_FILE_NAME = 'output.txt'


def check_file_exists(file_name):
  '''Check if the file exists'''
  if not os.path.exists(file_name):
    raise FileNotFoundError(f'The CSV file {file_name} doesn\'t exist.')


def load_data(file_name):
  '''Load the data from the csv file'''
  if os.path.getsize(file_name) == 0:
    raise ValueError('The csv file is empty.')
  data_log = pd.read_csv(file_name, header=None)
  return data_log.dropna()


def validate_row(row, index):
  '''Validate the row data. Return True if the row is valid, otherwise return False'''
  if not isinstance(row.iloc[0], str):
    print(f'Error on line {index+1} of the csv file: The timestamp parameter type must be string.')
    return False
  try:
    datetime.strptime(row.iloc[0], '%H:%M:%S')
  except ValueError:
    print(
        f'Error on line {index+1} of the csv file: The timestamp parameter doesn\'t follow the HH:MM:SS format. Actual value: {row.iloc[0]}. Skip this row.')
    return False

  if not isinstance(row.iloc[1], str):
    print(f'Error on line {index+1} of the csv file: The description parameter type must be string. Skip this row.')
    return False

  if row.iloc[2].strip() not in ['START', 'END']:
    print(
        f'Error on line {index+1} of the csv file: "{row.iloc[1]}" is not a "START" or "END" process. Actual value: {row.iloc[2]}. Skip this row.')
    return False

  try:
    int(row.iloc[3])
  except ValueError:
    print(
        f'Error on line {index+1} of the csv file: "{row.iloc[1]}" doesn\'t have a valid PID. Actual value: {row.iloc[3]}. Skip this row.')
    return False
  return True


def process_data(data_log):
  '''Process the data and return a dictionary with the processes'''
  processes = {}
  skipping_list = []
  for index, row in data_log.iterrows():
    if not validate_row(row, index):
      skipping_list.append(row.iloc[3])
      continue
    if not processes.get(row.iloc[3]):
      processes[row.iloc[3]] = {}
    processes[row.iloc[3]][row.iloc[2].strip()] = row.iloc[0]  # Add "START" or "END" process time for the PID
    if not processes[row.iloc[3]].get('description'):
      processes[row.iloc[3]]['description'] = row.iloc[1]
  for pid in skipping_list:
    if pid in processes:
      processes.pop(pid)
  return processes


def write_output(processes, output_file_name):
  '''Write the output to a file with the processes status'''
  with open(output_file_name, 'w') as f:
    for pid, process_dct in processes.items():
      if not process_dct.get('START'):
        f.write(f'The "{process_dct["description"]}" with PID {pid} hasn\'t started yet.\n')
      elif not process_dct.get('END'):
        f.write(f'The "{process_dct["description"]}" with PID {pid} hasn\'t finished yet.\n')
      else:
        END_TIME = datetime.strptime(process_dct['END'], '%H:%M:%S')
        START_TIME = datetime.strptime(process_dct['START'], '%H:%M:%S')
        if END_TIME < START_TIME:
          f.write(f'The process {pid} has the "END" process before the "START" process.\n')
        elif END_TIME - START_TIME > timedelta(minutes=10):
          f.write(f'Error: The process {pid} took more than 10 minutes to finish. Actual time: {END_TIME - START_TIME}.\n')
        elif timedelta(minutes=5) < END_TIME - START_TIME < timedelta(minutes=10):
          f.write(f'Warning: The process {pid} took more than 5 minutes to finish. Actual time: {END_TIME - START_TIME}.\n')
    else:
      f.close()


def main():
  check_file_exists(CSV_FILE_NAME)
  data_log = load_data(CSV_FILE_NAME)
  processes = process_data(data_log)
  write_output(processes, OUTPUT_FILE_NAME)


if __name__ == '__main__':
  main()
