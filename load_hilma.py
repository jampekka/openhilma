#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import sys
import pymongo
from bson.objectid import ObjectId
from pathlib import Path
import hashlib

import argh

from xml2json import etree_to_dict
from hilma_conversion import get_handler

hilma_to_dict = lambda notice: etree_to_dict(notice, get_handler)

def hilma_id_to_mongo(hilma_id):
	# A hack to generate a deterministic
	# Mongo objectId from a HILMA-id. Mostly
	# to workaround brainfarts of Eve
	return ObjectId(hashlib.md5(hilma_id.encode('utf-8')).digest()[:12])

def load_hilma_xml(inputfile, collection):
	collection.ensure_index([("$**", "text")])
	root = ET.parse(inputfile).getroot()
	notices = list(root.iterfind('WRAPPED_NOTICE'))
	
	notices = map(hilma_to_dict, notices)
	
	for n in notices:
		# Use a mangled ID as primary key
		n.update({'_id': hilma_id_to_mongo(n['ID'])})
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
