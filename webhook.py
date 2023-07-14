from box_jwt_client import get_box_client
from config import BoxConfig

config = BoxConfig()


def webhook_signature_check(
    webhook_id,
    body: bytes,
    header: dict,
) -> bool:
    client = get_box_client()
    webhook = client.webhook(webhook_id)

    key_a = config.WH_KEY_A
    key_b = config.WH_KEY_B

    return webhook.validate_message(body, header, key_a, key_b)
