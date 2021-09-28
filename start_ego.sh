#!/usr/bin/env bash
# --------------------------------
# Start MongoDB service
# --------------------------------
sudo service mongod start

# --------------------------------
# Start Ego service with virtualenv
# --------------------------------
./ego_virtualenv/bin/python ./src/start.py

# --------------------------------
# Stop MongoDB service
# --------------------------------
sudo service mongod stop