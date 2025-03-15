import hashlib
import hmac
import urllib.parse


def check_initial_data(
    data: str,
    bot_token: str,
) -> bool:
    """
    Validates initial data for the Web App.

    You can read more about this in the official docs:
    https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
    """
    parameters = urllib.parse.parse_qsl(data)

    received_hash = ""
    validation_string = ""

    for key, value in sorted(parameters, key=lambda x: x[0]):
        if key != "hash":
            validation_string += f"{key}={value}\n"
        else:
            received_hash = value

    validation_string = validation_string.strip()

    secret = hmac.new(
        b"WebAppData",
        bot_token.encode(),
        hashlib.sha256,
    )
    expected_hash = hmac.new(
        secret.digest(),
        validation_string.encode(),
        hashlib.sha256,
    )

    return expected_hash.hexdigest() == received_hash
