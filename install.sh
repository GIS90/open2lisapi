echo 'start========='
source .venv/bin/activate
echo `which python`
echo `which pip`
echo `python --version`
python -m pip install --upgrade pip
pip install setuptools
pip install pbr==3.1.1
pip install -r requirements.txt
echo 'end'