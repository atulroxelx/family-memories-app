# ============================================================
# setup_secrets.py - Streamlit Cloud Secrets Helper
# ============================================================
# This script runs before the app starts on Streamlit Cloud
# It reads secrets from Streamlit secrets and writes them
# to local files (client_secrets.json and token.json)
# ============================================================

import json
import os

def setup_credentials():
    """Setup credentials from Streamlit secrets for cloud deployment."""
    try:
        import streamlit as st

        # Write client_secrets.json from secrets
        if "client_secrets" in st.secrets:
            client_secrets = dict(st.secrets["client_secrets"])
            if "installed" in client_secrets:
                client_secrets["installed"] = dict(client_secrets["installed"])
            with open("client_secrets.json", "w") as f:
                json.dump(client_secrets, f)
            print("✅ client_secrets.json written from Streamlit secrets")

        # Write token.json from secrets
        if "token" in st.secrets:
            token_data = dict(st.secrets["token"])
            if "scopes" in token_data:
                token_data["scopes"] = list(token_data["scopes"])
            with open("token.json", "w") as f:
                json.dump(token_data, f)
            print("✅ token.json written from Streamlit secrets")

    except Exception as e:
        print(f"⚠️ Could not setup secrets: {e}")


if __name__ == "__main__":
    setup_credentials()
