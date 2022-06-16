#!/bin/sh 


sudo apt install python3-pip
pip install -r requirements.txt

echo "Creating and moving VMDETECT files..."
sudo mkdir /usr/share/vmdetect
sudo cp -r $(pwd)/scripts/ /usr/share/vmdetect/
sudo cp -r $(pwd)/methods/ /usr/share/vmdetect/
sudo cp -r $(pwd)/reports/ /usr/share/vmdetect/

echo "Giving +rwx permission..."
sudo chmod +x /usr/share/vmdetect/scripts/*
sudo chmod 747 /usr/share/vmdetect/reports
