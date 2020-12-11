#!/bin/bash

# you should run this inside a tmux window so it stays running after logout
# to create one: tmux new -s cellrc -d
# to attach: tmux a -t cellrc
# to detach: ^b d
# to list: tmux ls

export PYTHONPATH=.

if [ "$1" = "server" ]; then
  echo "Launching server"
  python3 server/main.py

elif [ "$1" = "vehicle" ]; then
  echo "Launching vehicle"
  python3 vehicle/main.py

else
  echo "Unknown target $1"
fi


