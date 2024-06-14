"""
Module: email_listener
Description: Listens for emails and extracts verification codes.
Author: oaslananka
GitHub: https://github.com/oaslananka
"""

from mailtm import Email
import json
import threading


class EmailListener:
    """
    Listens for verification emails and extracts verification codes.
    """

    def __init__(self, target_address, num_addresses=1, callback=None):
        self.target_address = target_address
        self.num_addresses = num_addresses
        self.email_objects = []
        self.verification_codes = []
        self.callback = callback if callback else self.default_callback
        self.verification_complete = False
        self.lock = threading.Lock()

    def default_callback(self, message):
        """
        Default callback to handle incoming emails.

        Args:
            message (dict): The email message.
        """
        from_address = message['from']['address']
        subject = message['subject']
        text_content = message['text']

        if from_address == self.target_address:
            to_address = message['to'][0]['address']
            verification_code = text_content.split("code: ")[1].split("\n")[0]
            print(f"To: {to_address}, Verification Code: {verification_code}")
            with self.lock:
                self.verification_codes.append({"email": to_address, "verification_code": verification_code})

            # Stop listening to this email address
            for email in self.email_objects:
                if email.address == to_address:
                    threading.Thread(target=email.stop).start()
                    with self.lock:
                        self.email_objects.remove(email)
                    break

            # Check if all email listeners have completed
            with self.lock:
                if not self.email_objects:
                    self.verification_complete = True

    def get_domains(self):
        """
        Get the domain of the email addresses.

        Returns:
            str: The domain of the email addresses.
        """
        return self.email_objects[0].domain if self.email_objects else ""

    def register_new_addresses(self):
        """
        Register new email addresses.

        Returns:
            list: List of registered email addresses.
        """
        for _ in range(self.num_addresses):
            email = Email()
            email.register()
            self.email_objects.append(email)
        return [email.address for email in self.email_objects]

    def start_listening(self):
        """
        Start listening for emails.
        """
        for email in self.email_objects:
            email.start(self.callback)
        print("\nWaiting for new emails...")
