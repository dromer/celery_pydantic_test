import time
from uuid import uuid4

from celery_test.testworker import task2, our_chain, TestModel


test = TestModel(
    name='new',
    uuid=uuid4()
)

result = our_chain(test.model_dump())
print(result)


result = task2(test)
print(result)
