if [! -e '$venv']
then
    virtualenv -p `which python3` venv
    echo 'venv file is created'
fi
echo 'venv exists!'

sleep 1

source venv/bin/activate

pip3 install -r requirements.txt

export FLASK_APP=timey.py

export FLASK_ENV=development

python3 -m flask run