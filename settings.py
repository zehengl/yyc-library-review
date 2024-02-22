from os import getenv
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)

cpl_username = getenv("cpl_username")
cpl_password = getenv("cpl_password")
cutoff_year = getenv("cutoff_year")
early_exit = getenv("early_exit")
browser = getenv("browser") or "chrome"

assert cpl_username
assert cpl_password

if cutoff_year:
    try:
        cutoff_year = int(cutoff_year)
    except:
        assert False

if early_exit:
    early_exit = early_exit in ["yes", "1", "true"]

output = Path("output")
output.mkdir(exist_ok=True)
