#!/bin/bash
python3 -m pip install --no-cache-dir -r requirements.txt
export PYTHONPATH=$PYTHONPATH:/app
python3 -m app.main