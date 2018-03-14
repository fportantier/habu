from habu.lib.tomorrow3 import threads
import dns.resolver
import dns.zone
from time import sleep


@threads(50)
def __threaded_query(hostname):
    try:
        answer = dns.resolver.query(hostname)
        return answer
    except Exception:
        return None


def query_bulk(names):

    answers = [__threaded_query(name) for name in names]

    while True:
        if all([ a.done() for a in answers]):
            break
        sleep(1)

    return [answer.result() for answer in answers]

    #for answer in answers:
    #    print(answer.result())

