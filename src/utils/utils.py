"""
Module: utils
Description: Provides utility functions for random text generation and environment variable handling.
Author: oaslananka
GitHub: https://github.com/oaslananka
"""

import os
import random
import string

from dotenv import load_dotenv


class RandomText:
    """
    Utility class for generating random text strings.
    """
    @classmethod
    def lowercase(cls, length: int, repeated: bool = False):
        """
        Generates a random lowercase string.

        Args:
            length (int): Length of the string.
            repeated (bool, optional): Allow repeated characters.

        Returns:
            str: Random lowercase string.
        """
        if repeated:
            result = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
        else:
            result = ''.join(random.sample(string.ascii_lowercase, length))
        return result

    @classmethod
    def uppercase(cls, length: int, repeated: bool = False):
        """
        Generates a random uppercase string.

        Args:
            length (int): Length of the string.
            repeated (bool, optional): Allow repeated characters.

        Returns:
            str: Random uppercase string.
        """
        if repeated:
            result = ''.join(random.choice(string.ascii_uppercase) for _ in range(length))
        else:
            result = ''.join(random.sample(string.ascii_uppercase, length))
        return result

    @classmethod
    def randomcase(cls, length: int, repeated: bool = False):
        """
        Generates a random case string (mixed uppercase and lowercase).

        Args:
            length (int): Length of the string.
            repeated (bool, optional): Allow repeated characters.

        Returns:
            str: Random case string.
        """
        if repeated:
            result = ''.join(random.choice(string.ascii_letters) for _ in range(length))
        else:
            result = ''.join(random.sample(string.ascii_letters, length))
        return result

    @classmethod
    def fromstr(cls, length: int, base_str: str):
        """
        Generates a random string from a given base string.

        Args:
            length (int): Length of the string.
            base_str (str): Base string to choose characters from.

        Returns:
            str: Random string from the base string.
        """
        result = ''.join((random.choice(base_str) for _ in range(length)))
        return result


counter = 1


def get_user():
    """
    Retrieves user credentials from environment variables.

    Returns:
        tuple: A tuple containing email and password.
    """
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    dotenv_path = os.path.join(root_dir, ".env")
    load_dotenv(dotenv_path)
    global counter
    USER_CREDENTIALS = [
        (os.getenv("TestUser_1_Email"), os.getenv("TestUser_1_Password")),
        (os.getenv("TestUser_2_Email"), os.getenv("TestUser_2_Password")),
        (os.getenv("TestUser_3_Email"), os.getenv("TestUser_3_Password"))
    ]
    user = USER_CREDENTIALS[counter % 3 - 1]
    counter += 1
    return user
