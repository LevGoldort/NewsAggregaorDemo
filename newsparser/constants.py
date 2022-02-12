import os
import pwd

CATEGORIES = frozenset(['sports', 'politics', 'finance', 'weather'])
DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Path to parent folder
USERNAME = pwd.getpwuid(os.getuid())[0]  # System username
