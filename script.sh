sudo yum install python3 unzip

python3 --version
python3 -m ensurepip --upgrade

curl -LO https://github.com/dvsander/mdb-search/archive/refs/heads/main.zip
unzip main.zip

cd mdb-search-main
python3 -m venv .venv
. .venv/bin/activate

pip3 install -r requirements.txt

export MDB_CONN=
export DB=
export COLL=
export OPENAI_API_KEY=

python3 app.py
