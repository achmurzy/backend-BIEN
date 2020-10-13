# backend-BIEN

INSTALLATION:
sudo apt-get update
sudo apt-get install python3-venv python3-pip
sudo apt-get install python-celery-common redis-server
sudo apt-get install libsqlite3-mod-spatialite
python3 -m venv venv
source ./venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt

FIRST-TIME STARTUP OR REBOOT:
#Delete migrations folder
#Delete old SQLite .db file
source ./venv/bin/activate
./build_server.sh	
	flask db init
	flask db migrate
	flask db upgrade
	python3 initialize.py

Celery start workers:
celery -A tasks worker --loglevel=INFO

Azure set-up:
ssh -i HDR.test_key.pem achmurzy@104.40.87.231
sudo rsync -uavz -e "ssh -i HDR.test_key.pem" richness.hdf5 achmurzy@104.40.87.231:~
