import datetime

from hilma_generated import *

def text_converter(d, t, **kwargs):
	text = t.text if t.text is not None else ""
	text = text.strip()
	d[t.tag] = text

def numeric_converter(d, t, **kwargs):
	d[t.tag] = float(t.text)

def date_converter(d, t, **kwargs):
	d[t.tag] = datetime.datetime(
		int(t.find('YEAR').text),
		int(t.find('MONTH').text),
		int(t.find('DAY').text))

def datetime_converter(d, t, **kwargs):
	time = map(int, t.find('TIME').text.split(':'))
	d[t.tag] = datetime.datetime(
		int(t.find('YEAR').text),
		int(t.find('MONTH').text),
		int(t.find('DAY').text),
		*time)

handlers = {}
for tag in TEXT_TAGS: handlers[tag] = text_converter
for tag in NUMERIC_TAGS: handlers[tag] = numeric_converter
for tag in DATE_TAGS: handlers[tag] = date_converter
for tag in DATETIME_TAGS: handlers[tag] = datetime_converter

def get_handler(el, default):
	return handlers.get(el.tag, default)

