from time import sleep
from habu.lib.tomorrow3 import threads
import requests

@threads(50)
def __threaded_request(url):
    return requests.get(url)


def threaded_request(urls):

    answers = [__threaded_request(url) for url in urls]

    while True:
        if all([ a.done() for a in answers]):
            break
        sleep(1)




    return answers
