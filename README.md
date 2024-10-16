To reproduce:

* run a redis server with default config: `docker run -p 6379:6379 redis`
* create an environment using poetry: `poetry install`
* run `poetry shell` and then `celery -A celery_test.testworker worker`
* run `poetry shell` and then `python testme.py`
