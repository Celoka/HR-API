# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

def convert_to_camel_case(str):
    """Convert String to Camel Case"""
    title_str = str.title().replace("_", "")
    return title_str[0].lower() + title_str[1:]
