import sys
from pathlib import Path


ROOT = Path(__file__).parent.parent.parent.parent
sys.path.append(str(ROOT))

from api.v2.constants import TIMEZONE_COMPENSATION


# TIMEZONE_COMPENSATION = getenv('DEPARTMENT_ID', None)


print(TIMEZONE_COMPENSATION)