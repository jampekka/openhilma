# REST API for HILMA data

A quick RESTful API for HILMA data (Finnish public sector bidding registry).
Uses Python (>= 3.1), Mongo, Eve and nasty hacks.

## Usage

(Install dependencies according to breakage along the way.)

### Needed only once

Make a directory for data files

    mkdir data

Scrape HILMA XML data

    ./scrape_hilma.py <HILMA API URL, sort of a secret?> data

Infer datatypes so we can serve nicer JSON from the XML

    ./infer_hilma_schema.py data > hilma_generated.py

Load the scraped data to Mongo

    ./load_hilma.py data

Start the REST server (this should probably go to a startup script or something)

    ./hilma_rest_api.py

Take your browser to the address given by the last command.

### Repeat daily

Scrape HILMA XML data

    ./scrape_hilma.py <HILMA API URL, sort of a secret?> data

Upsert the new data

    ./load_hilma.py data
