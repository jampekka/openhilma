def default_handler(d, child, **kwargs):
	if child.tag not in d:
		d[child.tag] = []
	d[child.tag].append(etree_to_dict(child, **kwargs))

# A simple module/function to convert an elementtree representation
# to json. Uses badgerfish semantics http://badgerfish.ning.com/, although
# nested elements are always lists to avoid data-driven weirdness by default.
# These can be overriden with the handlers-parameter.
def etree_to_dict(t, gethandler=None):
	def default_handler(d, child):
		if child.tag not in d:
			d[child.tag] = []
		d[child.tag].append(etree_to_dict(child, gethandler))
	if gethandler is None:
		gethandler = lambda el, default: default_handler

	d = {'@' + k: v for k, v in t.attrib.items()}

	for child in t.getchildren():
		handler = gethandler(child, default_handler)
		handler(d, child)
	
	text = t.text if t.text is not None else ""
	text = text.strip()

	if text:
		d['@'] = text
	return d

