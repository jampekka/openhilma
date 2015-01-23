#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import sys
import pymongo
from pathlib import Path

import argh

from xml2json import etree_to_dict
from hilma_conversion import get_handler

hilma_to_dict = lambda notice: etree_to_dict(notice, get_handler)

def load_hilma_xml(inputfile, collection):
	root = ET.parse(inputfile).getroot()
	notices = list(root.iterfind('WRAPPED_NOTICE'))
	
	notices = map(hilma_to_dict, notices)
	
	for n in notices:
		# Use the ID as primary key
		n.update({'_id': n['ID']})
		collection.save(n)
	
def sync_hilma_xml_directory(directory, mongo_uri=None, mongo_db='openhilma'):
	if mongo_uri is None:
		client = pymongo.MongoClient()
	else:
		client = pymongo.MongoClient(mongo_uri)
	
	db = client[mongo_db]
	collection = db.notices
	paths = sorted(Path(directory).glob("*.xml"))
	for fpath in paths:
		load_hilma_xml(fpath.open(), collection)

if __name__ == '__main__':
	argh.dispatch_command(sync_hilma_xml_directory)
