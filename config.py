"""generic box configuration"""

import os
import dotenv

dotenv.load_dotenv()


class BoxConfig:
    """generic box configuration"""

    # Webhook keys
    WH_KEY_A = os.getenv("WH_KEY_A", "your webhook primary key")
    WH_KEY_B = os.getenv("WH_KEY_B", "your webhook secondary key")
