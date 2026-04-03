# ============================================================
# setup_secrets.py - Streamlit Cloud Secrets Helper
# ============================================================

import json
import os

def setup_credentials():
    try:
        import streamlit as st
        if "client_secrets" in st.secrets:
            client_secrets = dict(st.secrets["client_secrets"])
            if "installed" in client_secrets:
                client_secrets["installed"] = dict(client_secrets["installed"])
            with open("client_secrets.json", "w") as f:
                json.dump(client_secrets, f)

        if "token" in st.secrets:
            token_data = dict(st.secrets["token"])
            if "scopes" in token_data:
                token_data["scopes"] = list(token_data["scopes"])
            with open("token.json", "w") as f:
                json.dump(token_data, f)
    except Exception as e:
        print(f"Could not setup secrets: {e}")


if __name__ == "__main__":
    setup_credentials()
