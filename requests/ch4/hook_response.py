# _*_ coding: utf-8 _*_
import requests


def get_key_info(response, *args, **kwargs):
    print response.header['Content-Type']


def main():
    requests.get('https://api.github.com', hooks=dict(response=get_key_info))


main()
