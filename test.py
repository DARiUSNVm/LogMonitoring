import unittest
import pandas as pd
import main

NEW_CSV_NAME = 'unittest_log'
OUTPUT_FILE_NAME = 'unittest_output'


class TestMain(unittest.TestCase):

  def test_check_file_exists(self):
    with open(NEW_CSV_NAME, 'w') as f:
      f.write('00:00:01,This is a description, START,12345\n')
    main.check_file_exists(NEW_CSV_NAME)

  def test_check_file_exists_raises(self):
    with self.assertRaises(FileNotFoundError):
      main.check_file_exists('file_not_found.csv')

  def test_load_data(self):
    with open(NEW_CSV_NAME, 'w') as f:
      f.write('00:00:01,This is a description, START,12345\n')
    data_log = main.load_data(NEW_CSV_NAME)
    self.assertIsInstance(data_log, pd.DataFrame)

  def test_validate_row(self):
    row = pd.Series(['00:00:01', 'This is a description', 'START', '12345'])
    self.assertTrue(main.validate_row(row, 0))

  def test_validate_row_invalid_process_type(self):
    row = pd.Series(['00:00:01', 'This is a description', 'INVALID', '12345'])
    self.assertFalse(main.validate_row(row, 0))

  def test_validate_row_invalid_pid(self):
    row = pd.Series(['00:00:01', 'This is a description', 'START', 'INVALID'])
    self.assertFalse(main.validate_row(row, 0))

  def test_validate_row_invalid_timestamp(self):
    row = pd.Series(['122:12:12', 'This is a description', 'START', '12345'])
    self.assertFalse(main.validate_row(row, 0))

  def test_validate_row_invalid_description(self):
    row = pd.Series(['00:00:01', 123, 'START', '12345'])
    self.assertFalse(main.validate_row(row, 0))

  def test_process_data(self):
    data_log = pd.DataFrame([
        ['00:00:01', 'This is a description', 'START', '12345'],
        ['00:00:02', 'This is a description', 'END', '12345'],
        ['00:00:03', 'This is a description', 'START', '12346'],
        ['00:00:04', 'This is a description', 'END', '12346'],
    ])
    processes = main.process_data(data_log)
    self.assertEqual(processes, {
        '12345': {'START': '00:00:01', 'END': '00:00:02', 'description': 'This is a description'},
        '12346': {'START': '00:00:03', 'END': '00:00:04', 'description': 'This is a description'},
    })

  def test_write_output(self):
    processes = {
        '12345': {'START': '00:00:01', 'END': '00:05:02', 'description': 'This is a description'},
        '12346': {'START': '00:00:03', 'END': '00:10:04', 'description': 'This is a description'},
    }
    main.write_output(processes, OUTPUT_FILE_NAME)
    with open(OUTPUT_FILE_NAME, 'r') as f:
      self.assertEqual(
          f.read(),
          'Warning: The process 12345 took more than 5 minutes to finish. Actual time: 0:05:01.\nError: The process 12346 took more than 10 minutes to finish. Actual time: 0:10:01.\n')


if __name__ == '__main__':
  unittest.main()
