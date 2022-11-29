import requests

import config

token = config.api_token


def get_result(conv_to: str, conv_from: str, amount: str) -> float:
    """
    Request to API, get the response.
    :param conv_to: currency to convert to
    :param conv_from: currency to convert from
    :param amount: the amount to be converted
    :return: conversion result
    """
    url = f"https://api.apilayer.com/currency_data/convert?to={conv_to}&from={conv_from}&amount={amount}"
    response = requests.request("GET", url, headers={"apikey": token}).json()
    result = round(response['result'], 2)
    return result

