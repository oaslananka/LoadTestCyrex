"""
Module: locust_client
Description: Provides Locust client classes for performance testing with gRPC.
Author: oaslananka
GitHub: https://github.com/oaslananka
"""

import grpc
import grpc.experimental.gevent as grpc_gevent
import time

from grpc_interceptor import ClientInterceptor
from locust import HttpUser, User
from locust.exception import LocustError
from typing import Any, Callable

grpc_gevent.init_gevent()


class LocustInterceptor(ClientInterceptor):
    """
    Intercepts gRPC calls to measure performance metrics.
    """

    def __init__(self, environment, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.env = environment

    def intercept(
        self,
        method: Callable,
        request_or_iterator: Any,
        call_details: grpc.ClientCallDetails,
    ):
        """
        Intercepts gRPC calls to measure performance metrics.

        Args:
            method (Callable): The gRPC method to call.
            request_or_iterator (Any): The request or iterator for the call.
            call_details (grpc.ClientCallDetails): The details of the gRPC call.

        Returns:
            response: The response from the gRPC call.
        """
        response = None
        exception = None
        start_perf_counter = time.perf_counter()
        response_length = 0
        try:
            response = method(request_or_iterator, call_details)
            try:
                response_length = len(list(response))
            except:
                pass
            try:
                response_length = response.result().ByteSize()
            except:
                pass
        except grpc.RpcError as e:
            exception = e

        self.env.events.request.fire(
            request_type="grpc",
            name=call_details.method,
            response_time=(time.perf_counter() - start_perf_counter) * 1000,
            response_length=response_length,
            response=response,
            context=None,
            exception=exception,
        )
        return response


class GrpcUser(HttpUser):
    """
    Abstract user class for Locust performance testing with gRPC.
    """
    abstract = True
    vacancy_service_stub_class = None
    auth_service_stub_class = None

    def __init__(self, environment):
        super().__init__(environment)
        for attr_value, attr_name in ((self.host, "host"), (self.vacancy_service_stub_class, "vacancy_service_stub_class"),  (self.auth_service_stub_class, "auth_service_stub_class")):
            if attr_value is None:
                raise LocustError(f"You must specify the {attr_name}.")

        self._channel = grpc.insecure_channel(self.host)
        self._channel_closed = False
        interceptor = LocustInterceptor(environment=environment)
        self._channel = grpc.intercept_channel(self._channel, interceptor)
        self.client = {
            "authClient": self.auth_service_stub_class(self._channel),
            "vacancyClient": self.vacancy_service_stub_class(self._channel),
        }

    def stop(self, force=False):
        """
        Stops the gRPC user and closes the channel.

        Args:
            force (bool): Force stop the user.
        """
        self._channel_closed = True
        time.sleep(1)
        self._channel.close()
        super().stop(force=True)
