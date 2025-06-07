#!/bin/bash
python -m pip install --no-cache-dir -r requirements.txt
export PYTHONPATH=$PYTHONPATH:/app
python -m app.main