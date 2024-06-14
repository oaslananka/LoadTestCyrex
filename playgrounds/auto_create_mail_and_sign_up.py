"""
Module: auto_create_mail_and_sign_up
Description: Automates email creation and user signup process.
Author: oaslananka
GitHub: https://github.com/oaslananka
"""

import time
import threading
from email_listener import EmailListener
from auth_client import AuthClient
import json
import jwt


def extract_local_part(email):
    """
    Extracts the local part of an email address.

    Args:
        email (str): The email address.

    Returns:
        str: The local part of the email address.
    """
    return email.split('@')[0]


def decode_jwt(token):
    """
    Decodes a JWT token.

    Args:
        token (str): The JWT token.

    Returns:
        dict: The decoded token payload.
    """
    try:
        decoded = jwt.decode(token, options={"verify_signature": False})
        return decoded
    except Exception as e:
        print(f"Error decoding token: {e}")
        return None


def process_email(email, auth_client, email_listener, results):
    """
    Processes email for signup, verification, and signin.

    Args:
        email (str): The email address.
        auth_client (AuthClient): The authentication client.
        email_listener (EmailListener): The email listener.
        results (list): List to store results.
    """
    local_part = extract_local_part(email)

    # Signup
    signup_data = {
        "name": local_part,
        "email": email,
        "password": local_part,
        "passwordConfirm": local_part
    }
    signup_response = auth_client.signup_user(signup_data)
    if signup_response:
        print(f"Signup successful for {email}")
    else:
        print(f"Signup failed for {email}")
        results.append({"email": email, "status": "signup_failed"})
        return

    # Verification
    email_listener.start_listening()
    while not email_listener.verification_complete:
        time.sleep(1)

    verification_code = None
    for verification in email_listener.verification_codes:
        if verification['email'] == email:
            verification_code = verification['verification_code']
            break

    if not verification_code:
        print(f"Verification failed for {email}")
        results.append({"email": email, "status": "verification_failed"})
        return

    # Verify email
    verify_response = auth_client.verify_email(verification_code)
    if verify_response:
        print(f"Email verified for {email}")
    else:
        print(f"Email verification failed for {email}")
        results.append({"email": email, "status": "verification_failed"})
        return

    # Signin
    signin_data = {
        "email": email,
        "password": local_part
    }
    signin_response = auth_client.signin_user(signin_data)
    if signin_response:
        print(f"Signin successful for {email}")
        decoded_access_token = decode_jwt(signin_response.access_token)
        decoded_refresh_token = decode_jwt(signin_response.refresh_token)
        results.append({
            "email": email,
            "password": local_part,
            "decoded_access_token": decoded_access_token,
            "decoded_refresh_token": decoded_refresh_token
        })
    else:
        print(f"Signin failed for {email}")
        results.append({"email": email, "status": "signin_failed"})


if __name__ == "__main__":
    target_email = "noreply@cyrextech.net"
    grpc_server_address = "vacancies.cyrextech.net:7823"
    num_addresses = int(input("Enter the number of email addresses to generate: "))

    auth_client = AuthClient(grpc_server_address=grpc_server_address)
    email_listener = EmailListener(target_address=target_email, num_addresses=num_addresses)

    email_addresses = email_listener.register_new_addresses()
    for email_address in email_addresses:
        print("\nEmail Address: " + email_address)

    results = []
    threads = []
    for email in email_addresses:
        t = threading.Thread(target=process_email, args=(email, auth_client, email_listener, results))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    with open("signedup_succesfully_users.json", "w") as file:
        json.dump(results, file, indent=4)
    print("Results saved to signedup_succesfully_users.json")
    print("All processes complete.")
