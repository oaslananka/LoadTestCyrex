"""
Module: delete_vacancy
Description: Deletes a vacancy using gRPC.
Author: oaslananka
GitHub: https://github.com/oaslananka
"""

import grpc
import logging
import json
from proto_out import vacancy_service_pb2_grpc as vacancy_service_grpc
from proto_out.vacancy_service_pb2 import VacancyRequest

logging.basicConfig(level=logging.INFO)


class VacancyServiceClient:
    """
    Client class for vacancy service operations.
    """

    def __init__(self, grpc_server_address):
        self.grpc_server_address = grpc_server_address
        self.channel = grpc.insecure_channel(grpc_server_address)
        self.stub = vacancy_service_grpc.VacancyServiceStub(self.channel)

    def delete_vacancy(self, vacancy_id):
        """
        Delete a vacancy by ID.

        Args:
            vacancy_id (str): The ID of the vacancy to delete.

        Returns:
            The response from the delete vacancy method.
        """
        try:
            request = VacancyRequest(Id=vacancy_id)
            response = self.stub.DeleteVacancy(request)
            logging.info(f"DeleteVacancy successful: {response}")
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


def main():
    json_file = "vacancies.json"
    grpc_server_address = "vacancies.cyrextech.net:7823"
    vacancy_service_client = VacancyServiceClient(grpc_server_address)

    vacancies = load_vacancy_data(json_file)
    for vacancy in vacancies:
        vacancy_id = vacancy.get("Id")
        if vacancy_id:
            response = vacancy_service_client.delete_vacancy(vacancy_id)
            if response:
                logging.info(f"Deleted vacancy ID: {vacancy_id}")
            else:
                logging.error(f"Failed to delete vacancy ID: {vacancy_id}")


if __name__ == "__main__":
    main()
