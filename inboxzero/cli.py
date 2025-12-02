from .screen import InboxZeroApp
from .db import init_db

def main():
    init_db()  # Initialize the database when the CLI starts
    app = InboxZeroApp()
    app.run()