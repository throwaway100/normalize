import pytest

import normalize

def test_transform_timestamp():
	# AM/PM
	assert normalize.transform_timestamp('12/9/17 4:20:00 AM') == '2017-12-09T07:20:00-05:00'
	assert normalize.transform_timestamp('12/9/17 4:20:00 PM') == '2017-12-09T19:20:00-05:00'

	# Year boundary
	assert normalize.transform_timestamp('12/31/17 09:00:00 PM') == '2018-01-01T00:00:00-05:00'

	# DST boundary 
	assert normalize.transform_timestamp('11/5/17 12:00:00 AM') == '2017-11-05T02:00:00-05:00'
	assert normalize.transform_timestamp('3/12/17 12:00:00 AM') == '2017-03-12T04:00:00-04:00'
	# invalid input
	with pytest.raises(ValueError):
		normalize.transform_timestamp('3/12/17 12:�0:00 AM')

def test_transform_zipcode():
	assert normalize.transform_zipcode('12345') == '12345'
	assert normalize.transform_zipcode('1') == '00001'
	assert normalize.transform_zipcode('12') == '00012'
	# invalid chars
	with pytest.raises(ValueError):
		normalize.transform_zipcode('941�4')

def test_transform_name():
	# all ascii
	assert normalize.transform_name('cran mcberry') == 'CRAN MCBERRY'
	# CJK
	assert normalize.transform_name('孟小祥') == '孟小祥'
	# diacritic
	assert normalize.transform_name('california über alles') == 'CALIFORNIA ÜBER ALLES'
	# unicode replacement char OK
	assert normalize.transform_name('Mysterious���Person') == 'MYSTERIOUS���PERSON'

def test_transform_duration():
	assert normalize.transform_duration('00:00:01.0') == '1.0'
	with pytest.raises(ValueError):
		normalize.transform_duration('00:00:01.�1')
	with pytest.raises(ValueError):
		normalize.transform_duration('blahblah')

def test_sum_floats():
	assert normalize.sum_durations('0.1', '0.0') == '0.1'
	assert normalize.sum_durations('401012.123', '5553.123') == '406565.246'
	with pytest.raises(ValueError):
		normalize.sum_durations('0.�1', '0.0')
	with pytest.raises(ValueError):
		normalize.sum_durations(100, 200)
