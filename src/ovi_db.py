from dotenv import load_dotenv
import os


load_dotenv()
username: str = os.getenv('DB_USERNAME')

print(username)
