import os
import sys
import time

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "./..")))

import vertexai
from deployment.actions import (
    create_session,
    delete_all_sessions,
    delete_session,
    get_session,
    list_deployments,
    list_sessions,
    send_message,
)

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
    print("Listing deployments...")
    deployments = list_deployments()

    if not deployments:
        print("No deployments found. Exiting.")
        sys.exit(1)

    remote_app = deployments[0]
    resource_id = remote_app.resource_name
    user_id = "123"
    session_id = None

    try:
        # Create a new session
        print("\nCreating session...")
        session = create_session(resource_id, user_id)
        if not session:
            print("Failed to create session. Skipping session operations.")
        else:
            session_id = session["id"]

            # List all sessions
            print("\nListing sessions...")
            time.sleep(1)  # Small delay to ensure session is registered
            list_sessions(resource_id, user_id)

            # Get session details
            print("\nGetting session details...")
            session_info = get_session(resource_id, user_id, session_id)
            if not session_info:
                print(
                    "Failed to get session details. Continuing with other operations."
                )

            # Send a message
            print("\nSending message...")
            send_message(
                resource_id,
                user_id,
                session_id,
                "Create a post about latest news about Google Agent Development Kit (ADK).",
            )

            # Delete the session we created
            print("\nDeleting session...")
            delete_session(resource_id, user_id, session_id)

    except Exception as e:
        print(f"An error occurred during testing: {e}")

    finally:
        # Clean up: delete all sessions for this user
        print("\nCleaning up: Deleting all sessions...")
        delete_all_sessions(resource_id, user_id)

        print("Testing deployment finished!")
        print("-" * 50)
