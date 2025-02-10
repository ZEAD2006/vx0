#!/bin/bash

echo " Install tool requirements..."
sudo apt update && sudo apt install python3 -y
pip install -r requirements.txt

echo " Installation Successful! To run the tool use"
echo "python3 vx0.py"
