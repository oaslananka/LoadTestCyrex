"""
Module: main
Description: Main script for running performance tests using Locust with gRPC.
Author: oaslananka
GitHub: https://github.com/oaslananka
"""

import logging
import time
import os
from dotenv import load_dotenv

from locust import task, SequentialTaskSet, constant
from src.clients.service_client import AuthServiceClient, VacancyServiceClient
from src.clients.messages_client import Messages
from src.utils.utils import RandomText, get_user

from src.clients.locust_client import GrpcUser

# Load environment variables from .env file
load_dotenv()

# Get the host address from environment variables
host = os.getenv("HOST")

vacancy_id = None


class LoginWithUsers(SequentialTaskSet):
    """
    A task set for logging in with multiple users.
    """
    wait_time = constant(30)
    email = "NOT_FOUND"
    password = "NOT_FOUND"

    def on_start(self):
        """
        Runs when the task set starts. Retrieves user credentials and logs in.
        """
        self.email, self.password = get_user()

        credentials = Messages.sign_in_user(email=self.email, password=self.password)
        self.client["authClient"].sign_in_user(credentials=credentials)
        logging.info('Login with %s email and %s password', self.email, self.password)

    @task
    class VacancyLoad(SequentialTaskSet):
        """
        A task set for creating, updating, fetching, and deleting vacancies.
        """
        @task
        def create_vacancy(self):
            """
            Creates a vacancy and logs the result.
            """
            global vacancy_id
            create_vacancy_message = Messages.create_vacancy(
                country=RandomText.lowercase(8),
                description=RandomText.lowercase(8),
                division=2,
                title=RandomText.lowercase(8)
            )
            res = self.client["vacancyClient"].create_vacancy(create_vacancy_message)
            vacancy_id = res.vacancy.Id
            logging.info("Vacancy is created with { %s }", res.vacancy)

        @task
        def update_vacancy(self):
            """
            Updates the vacancy and logs the result.
            """
            global vacancy_id
            update_vacancy_message = Messages.update_vacancy(id=vacancy_id, title=RandomText.lowercase(8))
            res = self.client["vacancyClient"].update_vacancy(update_vacancy_message)
            logging.info("Vacancy is updated with { %s }", res.vacancy)

        @task
        def fetch_vacancy(self):
            """
            Fetches the vacancy and logs the result.
            """
            global vacancy_id
            get_vacancy_message = Messages.get_vacancy(id=vacancy_id)
            res = self.client["vacancyClient"].get_vacancy(get_vacancy_message)
            logging.info("Vacancy is fetched { %s }", res.vacancy)

        @task
        def delete_vacancy(self):
            """
            Deletes the vacancy and logs the result.
            """
            global vacancy_id
            delete_vacancy_message = Messages.delete_vacancy(id=vacancy_id)
            res = self.client["vacancyClient"].delete_vacancy(delete_vacancy_message)
            logging.info("Vacancy is deleted { %s }", res.success)
            self.interrupt(reschedule=False)


class FetchVacancies(GrpcUser):
    """
    A Locust user class for fetching multiple vacancies.
    """
    host = host
    vacancy_service_stub_class = VacancyServiceClient
    auth_service_stub_class = AuthServiceClient
    wait_time = constant(44)
    weight = 1

    @task
    def fetch_vacancies(self):
        """
        Fetches a list of vacancies and logs the result.
        """
        if not self._channel_closed:
            get_vacancies_message = Messages.get_vacancies(limit=100)
            res = self.client["vacancyClient"].get_vacancies(get_vacancies_message)
            logging.info("Vacancies are fetched : {%s} ", str(res))
        time.sleep(1)


class LoginWithUniqueUsersTest(GrpcUser):
    """
    A Locust user class for logging in with unique users and performing vacancy operations.
    """
    host = host
    tasks = [LoginWithUsers]
    weight = 3
    vacancy_service_stub_class = VacancyServiceClient
    auth_service_stub_class = AuthServiceClient

# Command to run the Locust test
# locust -f src/main.py --config config/task.config
