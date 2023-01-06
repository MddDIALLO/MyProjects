import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from constants import URL
from utils import parse_html