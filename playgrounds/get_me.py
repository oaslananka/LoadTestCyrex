"""
Module: get_me
Description: Retrieves user information using gRPC.
Author: oaslananka
GitHub: https://github.com/oaslananka
"""

import grpc
import logging
import json
from proto_out import user_service_pb2_grpc as user_service_grpc
from proto_out.user_service_pb2 import GetMeRequest

logging.basicConfig(level=logging.INFO)


class UserServiceClient:
    """
    Client class for user service operations.
    """

    def __init__(self, grpc_server_address):
        self.grpc_server_address = grpc_server_address
        self.channel = grpc.insecure_channel(grpc_server_address)
        self.stub = user_service_grpc.UserServiceStub(self.channel)

    def get_me(self, sub):
        """
        Retrieve user information by ID.

        Args:
            sub (str): The user ID.

        Returns:
            The response from the get me method.
        """
        try:
            request = GetMeRequest(Id=sub)
            response = self.stub.GetMe(request)
            logging.info(f"GetMe successful: {response}")
            return response
        except grpc.RpcError as e:
            logging.error(f"gRPC error: {e.code()} - {e.details()}")
            return None
        except Exception as e:
            logging.error(e)
            return None


def load_user_data(json_file):
    """
    Load user data from JSON file.

    Args:
        json_file (str): The JSON file to load data from.

    Returns:
        list: List of user data.
    """
    try:
        with open(json_file, "r") as file:
            data = json.load(file)
        return data
    except Exception as e:
        logging.error(f"Error loading user data from {json_file}: {e}")
        return []


def main():
    json_file = "signedup_succesfully_users.json"
    grpc_server_address = "vacancies.cyrextech.net:7823"

    user_data = load_user_data(json_file)
    user_service_client = UserServiceClient(grpc_server_address)

    for user in user_data:
        sub = user['decoded_access_token']['sub']
        user_service_client.get_me(sub)


if __name__ == "__main__":
    main()
