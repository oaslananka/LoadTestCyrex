"""
Module: get_vacancies
Description: Retrieves a list of vacancies using gRPC.
Author: oaslananka
GitHub: https://github.com/oaslananka
"""

import grpc
import logging
from proto_out import vacancy_service_pb2_grpc as vacancy_service_grpc
from proto_out.vacancy_service_pb2 import GetVacanciesRequest

logging.basicConfig(level=logging.INFO)


class VacancyServiceClient:
    """
    Client class for vacancy service operations.
    """

    def __init__(self, grpc_server_address):
        self.grpc_server_address = grpc_server_address
        self.channel = grpc.insecure_channel(grpc_server_address)
        self.stub = vacancy_service_grpc.VacancyServiceStub(self.channel)

    def get_vacancies(self, page, limit):
        """
        Retrieve a list of vacancies.

        Args:
            page (int): The page number for pagination.
            limit (int): The number of vacancies to retrieve.

        Returns:
            list: List of retrieved vacancies.
        """
        try:
            request = GetVacanciesRequest(page=page, limit=limit)
            response_stream = self.stub.GetVacancies(request)
            logging.info("GetVacancies successful.")
            vacancies = []
            for response in response_stream:
                vacancies.append(response)
            return vacancies
        except grpc.RpcError as e:
            logging.error(f"gRPC error: {e.code()} - {e.details()}")
            return []
        except Exception as e:
            logging.error(e)
            return []


def main():
    grpc_server_address = "vacancies.cyrextech.net:7823"
    vacancy_service_client = VacancyServiceClient(grpc_server_address)

    page = 1
    limit = 20

    vacancies = vacancy_service_client.get_vacancies(page, limit)
    for vacancy in vacancies:
        logging.info(f"Vacancy: {vacancy}")


if __name__ == "__main__":
    main()
