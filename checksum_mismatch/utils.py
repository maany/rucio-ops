import pandas as pd
import requests

def load_csv(file_path: str) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame."""
    return pd.read_csv(file_path)


def load_x509_protected_page(page, url):
    """Load a page that is protected by X.509 client certificate."""
    requests.get(url, verify='pat', cert=('/path/to/cert.pem', '/path/to/key.pem'))