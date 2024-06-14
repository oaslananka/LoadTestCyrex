"""
Module: auth_client
Description: Provides client class for interacting with authentication service.
Author: oaslananka
GitHub: https://github.com/oaslananka
"""

import grpc
import logging
from proto_out import auth_service_pb2_grpc as auth_service_grpc
from proto_out.rpc_signup_user_pb2 import SignUpUserInput
from proto_out.rpc_signin_user_pb2 import SignInUserInput
from proto_out.auth_service_pb2 import VerifyEmailRequest
from google.protobuf.json_format import ParseDict

logging.basicConfig(level=logging.INFO)


class AuthClient:
    """
    Client class for authentication operations.
    """

    def __init__(self, grpc_server_address):
        self.channel = grpc.insecure_channel(grpc_server_address)
        self.stub = auth_service_grpc.AuthServiceStub(self.channel)

    def create_signup_request(self, data):
        """
        Create a signup request from data dictionary.

        Args:
            data (dict): Data dictionary for signup.

        Returns:
            SignUpUserInput: The signup request message.
        """
        try:
            return ParseDict(data, SignUpUserInput())
        except Exception as e:
            logging.error(f"Error creating signup request: {e}")
            return None

    def signup_user(self, data):
        """
        Signup user with provided data.

        Args:
            data (dict): Data dictionary for signup.

        Returns:
            The response from the signup method.
        """
        try:
            request = self.create_signup_request(data)
            if request:
                response = self.stub.SignUpUser(request)
                logging.info(f"Signup successful: {response}")
                return response
            else:
                logging.error("Failed to create signup request.")
                return None
        except grpc.RpcError as e:
            logging.error(f"gRPC error: {e.code()} - {e.details()}")
            return None
        except Exception as e:
            logging.error(e)
            return None

    def verify_email(self, verification_code):
        """
        Verify user email with provided verification code.

        Args:
            verification_code (str): The verification code.

        Returns:
            The response from the verify email method.
        """
        try:
            request = VerifyEmailRequest(verificationCode=verification_code)
            response = self.stub.VerifyEmail(request)
            logging.info(f"Email verification successful: {response}")
            return response
        except grpc.RpcError as e:
            logging.error(f"gRPC error: {e.code()} - {e.details()}")
            return None
        except Exception as e:
            logging.error(e)
            return None

    def signin_user(self, data):
        """
        Signin user with provided data.

        Args:
            data (dict): Data dictionary for signin.

        Returns:
            The response from the signin method.
        """
        try:
            request = SignInUserInput(email=data["email"], password=data["password"])
            response = self.stub.SignInUser(request)
            logging.info(f"Signin successful: {response}")
            return response
        except grpc.RpcError as e:
            logging.error(f"gRPC error: {e.code()} - {e.details()}")
            return None
        except Exception as e:
            logging.error(e)
            return None
