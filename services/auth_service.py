import getpass #Used to ask for a password without displaying it on the screen.
import hashlib #Used for hashing the password.
import hmac  #used for safely compare two hashed string 
import json 
from pathlib import Path #Used to work with files and directories.


class AuthService:
    def __init__(self, path="data/users.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._create_default_user()

    @staticmethod
    def _hash(password):
        #sha256 operates on bytes so first we convert/encode utf-8 and then hexdigest convert bytes into redable hexadecimal text 
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def _create_default_user(self):
        # Demo credentials: admin / admin123
        data = {
            "admin": {
                "password_hash": self._hash("Ujjawal123"),
                "role": "admin"
            }
        }
        self.path.write_text(json.dumps(data, indent=4), encoding="utf-8")

    def login(self, attempts=3):
        users = json.loads(self.path.read_text(encoding="utf-8"))
        for attempt in range(attempts):
            print("\n========== ADMIN LOGIN ==========")
            username = input("Username: ").strip()
            password = getpass.getpass("Password: ")
            user = users.get(username)

            if user and hmac.compare_digest(
                user["password_hash"], self._hash(password)
            ):
                print(f"\nLogin successful. Welcome, {username}!")
                return True

            print(f"Invalid credentials. Attempts left: {attempts - attempt - 1}")
        return False
