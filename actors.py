from pulsar import arbiter, task, command, spawn, send
import random


@command()
def actor1(request, message):
    act2 = yield from spawn(name='actor2')
    r = send(act2, 'actor2', dict(message="Important data"))
    r.add_done_callback(lambda resolved_promise: print(resolved_promise))
    return "Message sent"


@command()
def actor2(request, message):
    print("Got the message")


class MC:

    def __init__(self):
        a = arbiter()
        self._loop = a._loop
        self._loop.call_later(1, self)
        a.start()

    @task
    def __call__(self, a=None):
        act1 = yield from spawn(name='actor1')
        r = send(act1, 'actor1', dict(data=[1, 2, 4]))
        r.add_done_callback(lambda resolved_promise: print(resolved_promise.result()))
        arbiter().stop()

MC()
