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



pico searchapp.sh

    !/bin/bash
    # flask settings

    #export MDB_CONN="mongodb+srv://user:2gu5E0NvzUIxGDOM@mdb-search.ajuitpu.mongodb.net/?retryWrites=true&w=majority"
    export MDB_CONN="mongodb+srv://user:2gu5E0NvzUIxGDOM@mdb-search-aws.rthjzes.mongodb.net/?retryWrites=true&w=majority"
    export DB="sample_mflix"
    export COLL="embedded_movies"
    export OPENAI_API_KEY=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
    export SITE_USER="vector"
    export SITE_PASS="search"


    export FLASK_APP=/home/ec2-user/mdb-search-main/app.py
    export FLASK_DEBUG=0



    source /home/ec2-user/mdb-search-main/.venv/bin/activate

    flask run --host=0.0.0.0 --port=8080

chmod +rxw searchapp.sh

sudo vim /etc/systemd/system/searchapp.service
    [Unit]
    Description = flask python command to do useful stuff

    [Service]
    ExecStart = /home/ec2-user/searchapp.sh

    [Install]
    WantedBy = multi-user.target


systemctl enable searchapp.service

