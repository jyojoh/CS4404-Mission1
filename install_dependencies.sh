#!/bin/bash
mkdir -p dependencies
touch requirements.txt
python3 -m pip install --no-index --find-links ./dependencies/ -r requirements.txt
