"""
Module: messages_client
Description: Provides message creation utilities for gRPC requests.
Author: oaslananka
GitHub: https://github.com/oaslananka
"""

import src.protos.rpc_create_vacancy_pb2 as rpc_create_vacancy
import src.protos.rpc_signin_user_pb2 as rpc_signin_user
import src.protos.rpc_update_vacancy_pb2 as rpc_update_vacancy
import src.protos.vacancy_service_pb2 as vacancy_service


class Messages:
    """
    A utility class for creating gRPC request messages.
    """
    @classmethod
    def sign_in_user(cls, email: str, password: str):
        """
        Creates a sign-in user request message.

        Args:
            email (str): User email.
            password (str): User password.

        Returns:
            rpc_signin_user.SignInUserInput: The sign-in user request message.
        """
        return rpc_signin_user.SignInUserInput(
            email=email,
            password=password
        )

    @classmethod
    def create_vacancy(cls, country: str, description: str, division: int, title: str):
        """
        Creates a create vacancy request message.

        Args:
            country (str): Country of the vacancy.
            description (str): Description of the vacancy.
            division (int): Division of the vacancy.
            title (str): Title of the vacancy.

        Returns:
            rpc_create_vacancy.CreateVacancyRequest: The create vacancy request message.
        """
        return rpc_create_vacancy.CreateVacancyRequest(
            Country=country,
            Description=description,
            Division=division,
            Title=title
        )

    @classmethod
    def get_vacancy(cls, id: str):
        """
        Creates a get vacancy request message.

        Args:
            id (str): ID of the vacancy.

        Returns:
            vacancy_service.VacancyRequest: The get vacancy request message.
        """
        return vacancy_service.VacancyRequest(
            Id=id
        )

    @classmethod
    def get_vacancies(cls, page: int = None, limit: int = None):
        """
        Creates a get vacancies request message.

        Args:
            page (int, optional): Page number for pagination.
            limit (int, optional): Limit for pagination.

        Returns:
            vacancy_service.GetVacanciesRequest: The get vacancies request message.
        """
        message = vacancy_service.GetVacanciesRequest()
        if page is not None:
            message.page = page
        if limit is not None:
            message.limit = limit
        return message

    @classmethod
    def update_vacancy(cls, id: str = None, country: str = None, description: str = None, division: int = None, title: str = None, views: int = None):
        """
        Creates an update vacancy request message.

        Args:
            id (str, optional): ID of the vacancy.
            country (str, optional): Country of the vacancy.
            description (str, optional): Description of the vacancy.
            division (int, optional): Division of the vacancy.
            title (str, optional): Title of the vacancy.
            views (int, optional): Views of the vacancy.

        Returns:
            rpc_update_vacancy.UpdateVacancyRequest: The update vacancy request message.
        """
        message = rpc_update_vacancy.UpdateVacancyRequest()

        if id is None:
            return "id cannot be null, must be a string"

        if division is not None:
            if division < 0 or division > 3:
                return "division must be between 0 - 3"

        message.Id = id

        if country is not None:
            message.Country = country

        if description is not None:
            message.Description = description

        if division is not None:
            message.Division = division

        if title is not None:
            message.Title = title

        if views is not None:
            message.Views = views

        return message

    @classmethod
    def delete_vacancy(cls, id: str):
        """
        Creates a delete vacancy request message.

        Args:
            id (str): ID of the vacancy.

        Returns:
            vacancy_service.VacancyRequest: The delete vacancy request message.
        """
        return vacancy_service.VacancyRequest(
            Id=id
        )
