"""
Module: update_vacancy
Description: Updates a vacancy using gRPC.
Author: oaslananka
GitHub: https://github.com/oaslananka
"""

import grpc
import logging
import json
import uuid
import random
from proto_out import vacancy_service_pb2_grpc as vacancy_service_grpc
from proto_out.rpc_update_vacancy_pb2 import UpdateVacancyRequest

logging.basicConfig(level=logging.INFO)


class VacancyServiceClient:
    """
    Client class for vacancy service operations.
    """

    def __init__(self, grpc_server_address):
        self.grpc_server_address = grpc_server_address
        self.channel = grpc.insecure_channel(grpc_server_address)
        self.stub = vacancy_service_grpc.VacancyServiceStub(self.channel)

    def update_vacancy(self, data):
        """
        Update a vacancy with provided data.

        Args:
            data (dict): Data dictionary for vacancy update.

        Returns:
            The response from the update vacancy method.
        """
        try:
            request = UpdateVacancyRequest(
                Id=data["Id"],
                Title=data["Title"],
                Description=data["Description"],
                Division=data["Division"],
                Country=data["Country"]
            )
            response = self.stub.UpdateVacancy(request)
            logging.info(f"UpdateVacancy successful: {response}")
            return response
        except grpc.RpcError as e:
            logging.error(f"gRPC error: {e.code()} - {e.details()}")
            return None
        except Exception as e:
            logging.error(e)
            return None


def load_vacancy_data(json_file):
    """
    Load vacancy data from JSON file.

    Args:
        json_file (str): The JSON file to load data from.

    Returns:
        list: List of vacancy data.
    """
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        logging.error(f"Error loading vacancy data from {json_file}: {e}")
        return []


def generate_update_data(vacancy):
    """
    Generate update data for a vacancy.

    Args:
        vacancy (dict): The original vacancy data.

    Returns:
        dict: The updated vacancy data.
    """
    random_hex = str(uuid.uuid4().hex[:8])
    return {
        "Id": vacancy["Id"],
        "Title": random_hex,
        "Description": random_hex,
        "Division": random.randint(1, 3),
        "Country": random_hex
    }


def main():
    json_file = "vacancies.json"
    grpc_server_address = "vacancies.cyrextech.net:7823"
    vacancy_service_client = VacancyServiceClient(grpc_server_address)

    vacancies = load_vacancy_data(json_file)
    for vacancy in vacancies:
        update_data = generate_update_data(vacancy)
        response = vacancy_service_client.update_vacancy(update_data)
        if response:
            logging.info(f"Updated vacancy: {update_data}")
        else:
            logging.error(f"Failed to update vacancy: {update_data}")


if __name__ == "__main__":
    main()
