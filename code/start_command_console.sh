#!/bin/bash
# The console call that starts the whole thing

echo "Booting up ILITE Mission Control"

source ./constants.conf

# Show the ILITE Screen saver (in the background) until other stuff happens
python3 display_ilite_logo.py &

# TODO:- Change background IMAGE to Outreach video (booklet)

# Run the button reader
python3 main.py

echo "Shutting down ILITE Mission Control"