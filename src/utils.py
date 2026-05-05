import pandas as pd

def load_contacts():
    return pd.read_csv("data/contacts.csv")

def load_reminders():
    return pd.read_csv("data/reminders.csv")

def load_template():
    with open("templates/email.txt") as f:
        return f.read()