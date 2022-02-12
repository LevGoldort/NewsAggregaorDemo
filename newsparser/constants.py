import os
import pwd

CATEGORIES = frozenset(['sports', 'politics', 'finance', 'weather'])  # For News categorization and user subscription
DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Path to parent folder
USERNAME = pwd.getpwuid(os.getuid())[0]  # System username
