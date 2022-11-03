#!/bin/bash
mkdir -p dependencies
touch requirements.txt
cd dependencies
python3 -m pip download -r ../requirements.txt
