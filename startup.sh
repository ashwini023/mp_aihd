#!/bin/bash

# Install system dependencies
apt update && apt install -y libgl1

# Run your app
python app.py
