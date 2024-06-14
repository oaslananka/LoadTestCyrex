"""
Module: create_vacancy
Description: Creates a new vacancy using gRPC.
Author: oaslananka
GitHub: https://github.com/oaslananka
"""

import grpc
import logging
import uuid
import random
import json
from proto_out import vacancy_service_pb2_grpc as vacancy_service_grpc
from proto_out.rpc_create_vacancy_pb2 import CreateVacancyRequest

logging.basicConfig(level=logging.INFO)


class VacancyServiceClient:
    """
    Client class for vacancy service operations.
    """

    def __init__(self, grpc_server_address):
        self.grpc_server_address = grpc_server_address
        self.channel = grpc.insecure_channel(grpc_server_address)
        self.stub = vacancy_service_grpc.VacancyServiceStub(self.channel)

    def create_vacancy_request(self, data):
        """
        Create a vacancy request from data dictionary.

        Args:
            data (dict): Data dictionary for vacancy.

        Returns:
            CreateVacancyRequest: The vacancy request message.
        """
        try:
            return CreateVacancyRequest(**data)
        except Exception as e:
            logging.error(f"Error creating vacancy request: {e}")
            return None

    def create_vacancy(self, data):
        """
        Create a new vacancy.

        Args:
            data (dict): Data dictionary for vacancy.

        Returns:
            The response from the create vacancy method.
        """
        try:
            request = self.create_vacancy_request(data)
            if request:
                response = self.stub.CreateVacancy(request)
                logging.info(f"Vacancy created: {response}")
                return response
            else:
                logging.error("Failed to create vacancy request.")
                return None
        except grpc.RpcError as e:
            logging.error(f"gRPC error: {e.code()} - {e.details()}")
            return None
        except Exception as e:
            logging.error(e)
            return None


def generate_sample_data():
    """
    Generate sample data for vacancy.

    Returns:
        dict: Sample data dictionary for vacancy.
    """
    random_hex = str(uuid.uuid4().hex[:8])
    return {
        "Title": random_hex,
        "Description": random_hex,
        "Division": random.randint(1, 3),
        "Country": random_hex
    }


def vacancy_response_to_dict(response):
    """
    Convert vacancy response to dictionary.

    Args:
        response: The vacancy response message.

    Returns:
        dict: The response as dictionary.
    """
    return {
        "Id": response.vacancy.Id,
        "Title": response.vacancy.Title,
        "Description": response.vacancy.Description,
        "Division": response.vacancy.Division,
        "Country": response.vacancy.Country,
        "created_at": {
            "seconds": response.vacancy.created_at.seconds,
            "nanos": response.vacancy.created_at.nanos
        },
        "updated_at": {
            "seconds": response.vacancy.updated_at.seconds,
            "nanos": response.vacancy.updated_at.nanos
        }
    }


def load_vacancies_from_json(filename):
    """
    Load vacancies from JSON file.

    Args:
        filename (str): The filename to load from.

    Returns:
        list: List of vacancies.
    """
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_vacancy_to_json(vacancies, filename):
    """
    Save vacancies to JSON file.

    Args:
        vacancies (list): List of vacancies.
        filename (str): The filename to save to.
    """
    try:
        with open(filename, 'w') as file:
            json.dump(vacancies, file, indent=4)
        logging.info(f"Vacancies saved to {filename}")
    except Exception as e:
        logging.error(f"Error saving vacancies to JSON: {e}")


def main():
    grpc_server_address = "vacancies.cyrextech.net:7823"
    vacancy_service_client = VacancyServiceClient(grpc_server_address)

    sample_data = generate_sample_data()
    response = vacancy_service_client.create_vacancy(sample_data)

    if response:
        vacancy_dict = vacancy_response_to_dict(response)
        vacancies = load_vacancies_from_json("vacancies.json")
        vacancies.append(vacancy_dict)
        save_vacancy_to_json(vacancies, "vacancies.json")


if __name__ == "__main__":
    main()
