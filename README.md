Query tool and sample data generator

Requirements:
- Python 3.7
- Dependencies in `requirements.txt`


#### Usage
##### generate.py
`python generate.py /path/to/generate/sample/files/`

Generates sample data files in the following format without header row. One file per minute.
```
1414689783 192.168.1.10 0 87
1414689783 192.168.1.10 1 90
1414689783 192.168.1.11 1 93
...
```
Assumptions:
- We're working within `192.168.0.0/16` network and take first `1000` servers for generation
- Generates sample logs for one day `2014-10-31 00:00:00 utc`
- We're writing to existent directory

##### query.py
`python query.py /path/to/generated/logs/`
It takes some time to start interactive shell. After successful load `>` will appear. 

**Syntax:**

* To query results `QUERY IP cpu_id time_start time_end`, date format `YYYY-MM-DD HH:MM`.
E.g. `QUERY 192.168.0.0 1 2014-10-31 00:00 2014-10-31 00:04`.
Sample output `CPU1 usage on 192.168.0.0:(2014-10-31 23:58, 39%), (2014-10-31 23:59, 73%)`
* To exit type `EXIT`
