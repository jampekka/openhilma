#!/usr/bin/env python3
# A simple script to scrape XML-data from
# the HILMA (Finnish registry of public bids, probably totally
# idiosyntratic, so not very useful for any other purposes) API.

# Argh! When will the standard argument parsing get a sane
# interface? :(
import argh
import time
import datetime
from urllib import request
from pathlib import Path
from shutil import copyfileobj
import xml.etree.ElementTree as ET

def ensure_date(str_or_date, defaulter=lambda: None):
	if str_or_date is None:
		return defaulter()
	
	if isinstance(str_or_date, str):
		# When will the standard date/time/datetime mess
		# be fixed?
		return datetime.date(*map(int, str_or_date.split('-')))

	return date

def fetch_days_data(api_root_url, target_directory, date, force_refresh=False):
	# Ad-hoc, but Python's URL parsing/formatting
	# isn't one of its best library components either :(
	mangled_probe_end = date.strftime("%Y%m%d240000")
	mangled_probe_start = date.strftime("%Y%m%d000000")
	dates_url = "%s?start=%s&end=%s"%(api_root_url, mangled_probe_start, mangled_probe_end)
	
	target_path = target_directory / ("%s.xml"%(date.isoformat()))
	if force_refresh or not target_path.exists():
		# This should be atomic
		try:
			with target_path.open('wb') as target_file, request.urlopen(dates_url) as src_file:
				copyfileobj(src_file, target_file)
		except:
			# Try to make the reading "atomic". Eg. if there's a file,
			# there's all the data there. Can still fail if Python crashes
			# or something. Fix to tmp file and move if this isn't enough.
			target_path.unlink()
			raise
		was_cached = False
	else:
		was_cached = True

	print(str(target_path))
	data = ET.parse(str(target_path)).getroot()
	notices = data.iterfind('WRAPPED_NOTICE')
	is_empty = next(notices, None) is None
	return data, is_empty, was_cached
	#print(target_path)
	#if 

	#data = request.urlopen(dates_url)
	

def main(api_root_url, target_directory,
		newest_date=None, oldest_date=None,
		empty_days_before_giving_up=60, server_mercy_sleep=1.0,
		force_refresh_days=7):
	target_directory = Path(target_directory)
	probe_date = ensure_date(newest_date, datetime.date.today)
	oldest_date = ensure_date(oldest_date, lambda: datetime.date.min)
	one_day = datetime.timedelta(1)
	force_until = probe_date - datetime.timedelta(force_refresh_days)
	empties = 0
	while probe_date >= oldest_date:
		if empties > empty_days_before_giving_up:
			break

		data, is_empty, was_cached = fetch_days_data(api_root_url,
			target_directory,
			probe_date,
			probe_date >= force_until)
		if not was_cached:
			time.sleep(server_mercy_sleep)

		if is_empty:
			empties += 1
		else:
			empties = 0
		probe_date -= one_day
		#print(data.read())


if __name__ == '__main__':
	argh.dispatch_command(main)
