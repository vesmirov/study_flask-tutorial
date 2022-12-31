Flaskr
======

The basic blog app built in the Flask `tutorial`.

The tutorial can be found on the [official project website](https://flask.palletsprojects.com/tutorial/).


Install
-------
Make sure that poetry is installed on your machine:  
python-poetry [installation guide](https://python-poetry.org/docs/#installation)

Clone the repository:
```bash
git clone git@github.com:vesmirov/study_flask-tutorial.git flask-tutorial
```

Go to the cloned directory:
```bash
cd flask-tutorial
```

Init poetry environment:
```bash
poetry install
```

Activate postry shell:
```bash
poetry shell
```

Run
---
Init project database:
```bash
flask --app flaskr init-db
```

Run the app:
```shell
flask --app flaskr --debug run
```

Open your localhost in browser with port 5000:  
http://127.0.0.1:5000


Test
----
With active poetry environment run tests:
```shell
pytest
```

Run with coverage report:
```shell
coverage run -m pytest
coverage report
coverage html # open htmlcov/index.html in a browser
```
