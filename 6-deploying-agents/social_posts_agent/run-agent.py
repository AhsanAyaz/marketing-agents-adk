import json
import os
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from social_posts_agent.agent import root_agent

# Load environment variables
load_dotenv()

# Get app configuration from environment variables
APP_NAME = os.environ.get("APP_NAME", "social_posts_agent")
USER_ID = os.environ.get("USER_ID", "user123")


def run_agent(query):
    """Execute the marketing campaign assistant with the given query."""
    # Set up session service
    session_service = InMemorySessionService()

    # Create a session
    session = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    user_id = USER_ID
    session_id = session.id

    print("[user]: ", query)
    print("-" * 50)

    # Create content using the proper types from google.genai
    content = types.Content(role="user", parts=[types.Part(text=query)])

    # Set up the runner
    runner = Runner(
        app_name=APP_NAME,
        agent=root_agent,
        session_service=session_service,
    )

    # Run the agent and collect all events
    events = list(
        runner.run(user_id=user_id, session_id=session_id, new_message=content)
    )

    # Process and display intermediate events
    for event in events:
        if not hasattr(event, "content") or not event.content:
            continue

        author = event.author

        # Handle text responses
        if event.content.parts:
            text_parts = [
                part.text
                for part in event.content.parts
                if hasattr(part, "text") and part.text
            ]
            if text_parts:
                text_response = "".join(text_parts)
                print(f"\n[{author}]: {text_response}")

    # Extract the final response from the last event
    if events:
        last_event = events[-1]
        if (
            hasattr(last_event, "content")
            and last_event.content
            and last_event.content.parts
        ):
            final_response = "".join(
                [
                    part.text
                    for part in last_event.content.parts
                    if hasattr(part, "text") and part.text
                ]
            )

            print("\n" + "=" * 50)
            print("FINAL CAMPAIGN BRIEF:")
            print("=" * 50)
            print(final_response)
            print("=" * 50)

            return final_response

    return None


if __name__ == "__main__":
    query = "Create a quick post about the latest trends in AI and machine learning."

    # Allow command line argument to override the default query
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])

    print("Running Social Posts Assistant...")
    run_agent(query)
