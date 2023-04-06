"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests


def main(param_dict):
    databaseName = "dealerships"

    try:
        client = Cloudant.iam(
            account_name=param_dict["32826014-9f9f-469a-bb30-55d0a2051bbd-bluemix"],
            api_key=param_dict["V0PPkzOLLhz4YlrwSnIFDjptkuHbv3_4hxu-XRJUTSKi"],
            connect=True,
        )
        print(f"Databases: {client.all_dbs()}")
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}
