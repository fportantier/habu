"""Retrieve details of a HTTP server."""
import requests
import urllib3

urllib3.disable_warnings()


def get_headers(server):
    """Retrieve all HTTP headers"""
    try:
        response = requests.head(
            server, allow_redirects=False, verify=False, timeout=5)
    except requests.exceptions.ConnectionError:
        return False

    return dict(response.headers)


def subjugation(server):
    """Check if the URL is redirected."""
    headers = get_headers(server)
    if 'Location' in headers:
        return {'redirect': headers['Location']}


def get_options(server):
    """Retrieve the available HTTP verbs"""
    try:
        response = requests.options(
            server, allow_redirects=False, verify=False, timeout=5)
    except (requests.exceptions.ConnectionError,
            requests.exceptions.MissingSchema):
        return "Server {} is not available!".format(server)

    try:
        return {'allowed': response.headers['Allow']}
    except KeyError:
        return "Unable to get HTTP methods"
