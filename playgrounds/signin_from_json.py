"""
Module: signin_from_json
Description: Signs in users from a JSON file using gRPC.
Author: oaslananka
GitHub: https://github.com/oaslananka
"""

import time
import threading
from email_listener import EmailListener
from auth_client import AuthClient
import json
import jwt


def decode_jwt(encoded_jwt, secret_key=None):
    """
    Decodes a JWT token.

    Args:
        encoded_jwt (str): The encoded JWT token.
        secret_key (str, optional): The secret key for decoding.

    Returns:
        dict: The decoded token payload.
    """
    try:
        if secret_key:
            decoded_token = jwt.decode(encoded_jwt, secret_key, algorithms=["HS256"])
        else:
            header_data = jwt.get_unverified_header(encoded_jwt)
            payload_data = jwt.decode(encoded_jwt, options={"verify_signature": False})
            decoded_token = {"header": header_data, "payload": payload_data}
        return decoded_token
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}


def extract_local_part(email):
    """
    Extracts the local part of an email address.

    Args:
        email (str): The email address.

    Returns:
        str: The local part of the email address.
    """
    return email.split('@')[0]


def process_email(email, auth_client, email_listener, results):
    """
    Processes email for signup, verification, and signin.

    Args:
        email (str): The email address.
        auth_client (AuthClient): The authentication client.
        email_listener (EmailListener): The email listener.
        results (dict): Dictionary to store results.
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
        results[email] = {"status": "signup_failed"}
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
        results[email] = {"status": "verification_failed"}
        return

    # Verify email
    verify_response = auth_client.verify_email(verification_code)
    if verify_response:
        print(f"Email verified for {email}")
    else:
        print(f"Email verification failed for {email}")
        results[email] = {"status": "verification_failed"}
        return

    # Signin
    signin_data = {
        "email": email,
        "password": local_part
    }
    signin_response = auth_client.signin_user(signin_data)
    if signin_response:
        print(f"Signin successful for {email}")
        access_token_decoded = decode_jwt(signin_response.access_token)["payload"]
        refresh_token_decoded = decode_jwt(signin_response.refresh_token)["payload"]
        results[email] = {
            "status": "success",
            "email": email,
            "password": local_part,
            "access_token": access_token_decoded,
            "refresh_token": refresh_token_decoded
        }
    else:
        print(f"Signin failed for {email}")
        results[email] = {"status": "signin_failed"}


if __name__ == "__main__":
    target_email = "noreply@cyrextech.net"
    grpc_server_address = "vacancies.cyrextech.net:7823"
    num_addresses = int(input("Enter the number of email addresses to generate: "))

    auth_client = AuthClient(grpc_server_address=grpc_server_address)
    email_listener = EmailListener(target_address=target_email, num_addresses=num_addresses)

    email_addresses = email_listener.register_new_addresses()
    for email_address in email_addresses:
        print("\nEmail Address: " + email_address)

    results = {}
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
