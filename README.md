Query tool and sample data generator

Requirements:
- Python 3.7
- dependencies in `requirements.txt`


#### Usage
##### generate.py
`python ./generate.py /path/to/generate/sample/files/`

Assumptions:
- we're working within `192.168.0.0/16` network and take first `1000` servers for generation
- Generates sample logs for one day `2014-10-31`
- We're writing to existent directory

##### query.py
