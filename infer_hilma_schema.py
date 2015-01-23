#!/usr/bin/env python3

from pathlib import Path
import argh
import xml.etree.ElementTree as ET
import json
import sys
import itertools

def always_applies_for(eliter, predicate):
	seen_tags = set()
	not_matching = set()

	for el in eliter:
		seen_tags.add(el.tag)
		if not predicate(el):
			not_matching.add(el.tag)

	return seen_tags - not_matching

def is_trivial_tag(el):
	if next(iter(el.attrib.items()), None) is not None:
		return False
	
	if next(iter(el), None) is not None:
		return False
	
	return True

def is_numeric_tag(el):
	if not is_trivial_tag(el):
		return False
	if el.text is None: return False
	try:
		float(el.text)
	except ValueError:
		return False
	return True

def is_datetime_tag(el):
	if el.attrib:
		return False
	children = list(el)
	if len(children) != 4:
		return False
	
	names = sorted(c.tag for c in children)
	if names == ['DAY', 'MONTH', 'TIME', 'YEAR']:
		return True

	return False

def is_date_tag(el):
	if el.attrib:
		return False
	children = list(el)
	if len(children) != 3:
		return False
	
	names = sorted(c.tag for c in children)
	if names == ['DAY', 'MONTH', 'YEAR']:
		return True

	return False
	

def notices(directory):
	for fpath in directory.glob("*.xml"):
		for entry in ET.parse(str(fpath)).getroot().iterfind('WRAPPED_NOTICE'):
			yield entry

def main(input_directory):
	from pprint import pprint
	directory = Path(input_directory)
	
	def applies_for(predicate):
		all_docs = notices(directory)
		all_elements = itertools.chain(*(root.iter() for root in all_docs))
		return always_applies_for(all_elements, predicate)
	
	trivial_tags = applies_for(is_trivial_tag)
	numeric_tags = applies_for(is_numeric_tag)
	text_tags = trivial_tags - numeric_tags

	print("TEXT_TAGS = " + repr((text_tags)))
	print("NUMERIC_TAGS = " + repr((numeric_tags)))
	print("DATETIME_TAGS = " + repr((applies_for(is_datetime_tag))))
	print("DATE_TAGS = " + repr((applies_for(is_date_tag))))
	
	entries = (etree_to_dict(n) for n in notices(directory))


if __name__ == '__main__':
	argh.dispatch_command(main)
