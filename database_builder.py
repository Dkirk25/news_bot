
import os
from dotenv import load_dotenv
load_dotenv(override=True)


class DatabaseBuilder:
    def __init__(self):
        self._indicator = os.getenv("USE_FIREBASE", "Y")
        self._file_name = os.getenv("DATABASE_FILE", "stock-db")

    def get_db(self):
        if self._indicator == "Y":
            from firebase_db import FirebaseDatabase
            return FirebaseDatabase()
        elif self._indicator == "N":
            from file_db import FileDatabase
            return FileDatabase(self._file_name)
        else:
            return ValueError(self._indicator)
