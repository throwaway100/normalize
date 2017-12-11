import csv
import datetime
import decimal
import sys

import pytz

def read_from_stdin():
	input_bytes = sys.stdin.buffer.read()
	decoded_input = input_bytes.decode('utf-8', errors='replace')
	return decoded_input

def parse_csv(blob):
	split = blob.splitlines()
	reader = csv.DictReader(split)
	for record in reader:
		yield record

def transform_timestamp(timestamp):
	# convert from pacific to eastern and to iso8601
	# input format e.g., 12/31/16 11:59:59 PM
	input_format = '%m/%d/%y %I:%M:%S %p'
	dt = datetime.datetime.strptime(timestamp, input_format)
	dt_pacific = pytz.timezone('US/Pacific').localize(dt)
	dt_eastern = dt_pacific.astimezone(tz=pytz.timezone('US/Eastern'))
	return dt_eastern.isoformat()

def transform_zipcode(zipcode):
	# convert to 5 digit with zero prefix
	if not zipcode.isdigit():
		raise ValueError('ZIP must be digit')
	return zipcode.zfill(5)

def transform_name(name):
	# uppercase
	return name.upper()

def _duration_to_timedelta(duration):
	hours, minutes, seconds_and_milliseconds = duration.split(':')
	seconds, milliseconds = seconds_and_milliseconds.split('.')
	hours, minutes, seconds, milliseconds = list(map(int, [hours, minutes, seconds, milliseconds]))
	return datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)

def transform_duration(duration):
	# convert from millisecond to floating-point seconds
	# input format e.g., 1:23:32.123
	duration_timedelta = _duration_to_timedelta(duration)
	return str(duration_timedelta.total_seconds())

def sum_durations(duration1, duration2):
	# sums two durations
	# durations must be strings because durations can have precision greater than 1
	# and floats do not have exact representations
	try:
		assert type(duration1) is str
		assert type(duration2) is str
	except AssertionError:
		raise ValueError('Duration must be string')
	try:
		return str(decimal.Decimal(duration1) + decimal.Decimal(duration2))
	except decimal.InvalidOperation as e:
		raise ValueError(e)

def write_to_stdout(list_of_ordered_dicts):
	fieldnames = list_of_ordered_dicts[0].keys()
	writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
	writer.writeheader()
	for row in list_of_ordered_dicts:
		writer.writerow(row)

def main():
	input_as_string = read_from_stdin()
	transformed_csv = []
	for record in parse_csv(input_as_string):
		try:
			record['Timestamp'] = transform_timestamp(record['Timestamp'])
			record['ZIP'] = transform_zipcode(record['ZIP'])
			record['FullName'] = transform_name(record['FullName'])
			record['FooDuration'] = transform_duration(record['FooDuration'])
			record['BarDuration'] = transform_duration(record['BarDuration'])
			record['TotalDuration'] = sum_durations(record['FooDuration'], record['BarDuration'])
		except ValueError as e:
			sys.stderr.write("Failed to parse line {} with error: {}\n".format(",".join(record.values()), e))
			continue
		transformed_csv.append(record)
	write_to_stdout(transformed_csv)

if __name__ == '__main__':
	main()
