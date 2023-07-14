"""sample code for rename on upload wbehook"""

import json
import logging
from box_jwt_client import get_box_client
from flask import Flask, request

from rename_file import rename_file
from webhook import webhook_signature_check


app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logging.getLogger("boxsdk").setLevel(logging.CRITICAL)


@app.route("/box/rename-upload", methods=["POST"])
def event_webhook():
    request_body = request.data
    request_headers = request.headers
    request_data = request.get_json()
    webhook_id = request_data["webhook"]["id"]
    webhook_trigger = request_data["trigger"]

    is_valid = webhook_signature_check(webhook_id, request_body, request_headers)

    # print(
    #     "#############################################################################################################"
    # )
    print(
        f"Webhook {webhook_id}:{webhook_trigger} with is_valid: {is_valid} {request_data['source']['name']}"
    )
    # print("----------------------------------------")
    # print(f"JSON: {request_data}")
    # print("----------------------------------------")

    if not is_valid:
        return (
            json.dumps({"success": False, "message": "Invalid request"}),
            400,
            {"ContentType": "application/json"},
        )

    try:
        service_client = get_box_client()
        me = service_client.user(user_id="18622116055").get()
        client = service_client.as_user(me)
        folder_id = request_data["source"]["parent"]["id"]
        file = client.file(request_data["source"]["id"]).get()

        rename_file(client, folder_id, file, "file.txt")

    except Exception as e:
        print(f"Error processing webhook: {e.message}")
        if e.code == "trashed":
            return (
                json.dumps({"success": True}),
                201,
                {"ContentType": "application/json"},
            )
        return (
            json.dumps({"success": False, "message": "Internal error"}),
            500,
            {"ContentType": "application/json"},
        )

    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


# run the app
if __name__ == "__main__":
    app.run(port=8000)
