import time

from celery import Celery, chain
from celery.result import allow_join_result

from pydantic import BaseModel, UUID4


class TestModel(BaseModel):
    name: str
    uuid: UUID4


broker_uri = "redis://localhost:6379/0"


celery_app = Celery(
    'tester',
    backend='redis',
    broker=broker_uri
)

# When we use the signature without output annotation and `.model_dump()` function this succeeds.

@celery_app.task(bind=True, pydantic=True)
def task1(self, payload: TestModel) -> TestModel:
# def task1(self, payload: TestModel):
    name = payload.name
    print(name)

    payload.name = "task1"
    return payload
    # return payload.model_dump()


@celery_app.task(bind=True, pydantic=True)
def task2(self, payload: TestModel) -> TestModel:
    name = payload.name
    print(name)

    payload.name = "task2"
    return payload


@celery_app.task(bind=True, pydantic=True)
def our_chain(self, payload: TestModel) -> TestModel:
    result = chain(
        task1.s(payload.model_dump()),
        task2.s()
    )()

    while not result.ready():
        print("not ready")
        time.sleep(1)

    print("ready!")

    with allow_join_result():
        res = result.get()
        print(res)

        return res


if __name__ == "__main__":
    celery_app.start()
