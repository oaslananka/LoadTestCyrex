"""
Module: service_client
Description: Provides client classes for interacting with gRPC services.
Author: oaslananka
GitHub: https://github.com/oaslananka
"""

from abc import ABC

import src.protos.auth_service_pb2_grpc as auth_service_grpc
import src.protos.vacancy_service_pb2_grpc as vacancy_service_grpc


class BaseClient(ABC):
    """
    Abstract base client class for gRPC service clients.
    """

    def __init__(self, channel):
        self.channel = channel


class AuthServiceClient(BaseClient):
    """
    Client class for the authentication service.
    """

    def __init__(self, channel):
        super().__init__(channel)
        self.stub = auth_service_grpc.AuthServiceStub(self.channel)

    def sign_in_user(self, credentials):
        """
        Signs in a user.

        Args:
            credentials: The user credentials.

        Returns:
            The response from the sign-in method.
        """
        return self.stub.SignInUser(credentials)

    def sign_out_user(self):
        """
        Signs out a user.
        """
        pass

    def verify_email(self):
        """
        Verifies a user's email.
        """
        pass


class VacancyServiceClient(BaseClient):
    """
    Client class for the vacancy service.
    """

    def __init__(self, channel):
        super().__init__(channel)
        self.stub = vacancy_service_grpc.VacancyServiceStub(self.channel)

    def create_vacancy(self, message):
        """
        Creates a vacancy.

        Args:
            message: The create vacancy request message.

        Returns:
            The response from the create vacancy method.
        """
        return self.stub.CreateVacancy(message)

    def get_vacancy(self, message):
        """
        Gets a vacancy.

        Args:
            message: The get vacancy request message.

        Returns:
            The response from the get vacancy method.
        """
        return self.stub.GetVacancy(message)

    def get_vacancies(self, message):
        """
        Gets a list of vacancies.

        Args:
            message: The get vacancies request message.

        Returns:
            The response from the get vacancies method.
        """
        return self.stub.GetVacancies(message)

    def update_vacancy(self, message):
        """
        Updates a vacancy.

        Args:
            message: The update vacancy request message.

        Returns:
            The response from the update vacancy method.
        """
        return self.stub.UpdateVacancy(message)

    def delete_vacancy(self, message):
        """
        Deletes a vacancy.

        Args:
            message: The delete vacancy request message.

        Returns:
            The response from the delete vacancy method.
        """
        return self.stub.DeleteVacancy(message)
