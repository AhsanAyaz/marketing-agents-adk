import os
import sys
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "./..")))

import vertexai
from deployment.actions import delete_all_sessions, delete_session
from google.api_core import exceptions
from vertexai import agent_engines

# Get deployment settings from environment variables
PROJECT_ID = os.environ.get("PROJECT_ID", "multiversity-418607")
LOCATION = os.environ.get("LOCATION", "us-central1")
STAGING_BUCKET = os.environ.get("STAGING_BUCKET", "gs://marketing-campaign-assistant")

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)

if __name__ == "__main__":
    # Example usage
    print("Listing deployments...")
    from deployment.actions import list_deployments

    deployments = list_deployments()

    if not deployments:
        print("No deployments found. Exiting.")
        sys.exit(1)

    remote_app = deployments[0]
    resource_id = remote_app.resource_name
    user_id = "123"

    print("\nCleaning up: Deleting all sessions...")
    delete_all_sessions(resource_id, user_id)

    print("Cleanup finished!")
    print("-" * 50)
