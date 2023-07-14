from boxsdk import JWTAuth, Client


def get_box_client() -> Client:
    """Returns a Box Client object that can be used to make API calls."""
    config = JWTAuth.from_settings_file(".jwt.config.json")
    return Client(config)
