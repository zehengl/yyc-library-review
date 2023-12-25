from os import getenv
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

cpl_username = getenv("cpl_username")
cpl_password = getenv("cpl_password")

assert cpl_username
assert cpl_password

output = Path("output")
output.mkdir(exist_ok=True)
