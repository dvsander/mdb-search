sudo yum install python3 unzip

python3 --version
python3 -m ensurepip --upgrade

curl -LO https://github.com/dvsander/mdb-search/archive/refs/heads/main.zip
unzip main.zip

cd mdb-search-main
python3 -m venv .venv
. .venv/bin/activate

pip3 install -r requirements.txt

export FLASK_APP=app.py

flask run --host=0.0.0.0 --port=8080
