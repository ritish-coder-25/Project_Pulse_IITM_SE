import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()


def send_email(first_name: str, last_name: str, email: str):
    try:
        url = "https://smtp.maileroo.com/send-template"
        headers = {"X-API-Key": os.getenv("MAILEROO_API_KEY")}
        data = {
            "from": "support@projectPulse <ea39f45fbd1e6975.maileroo.org>",
            "to": f"{first_name} {last_name} <{email}>",
            "subject": "Welcome to ProjectPulse",
            "template_id": "757",
            "template_data": json.dumps(
                {
                    "username": first_name + " " + last_name,
                }
            ),
        }

        response = requests.post(url, headers=headers, files=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print(response.text)
        return response.status_code

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    send_email("Pranjal", "Kar", "pranjalkar99.work@gmail.com")
