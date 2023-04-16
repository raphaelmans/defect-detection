### Installation
`pip install virtualenv`
`python -m venv env`
`pip install -r requirements.txt`

### Start Env
`source env/bin/activate`

### Start App
`python -m streamlit run main.py`


### Local Database access
`docker exec -it pwbclassification-db bash -c "mysql -uroot -p"`