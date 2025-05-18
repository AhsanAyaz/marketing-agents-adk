import os
import sys
import time
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "./..")))

import vertexai
from social_posts_agent.agent import root_agent
from vertexai import agent_engines
from vertexai.preview import reasoning_engines

# Get deployment settings from environment variables
PROJECT_ID = os.environ.get("PROJECT_ID", "multiversity-418607")
LOCATION = os.environ.get("LOCATION", "us-central1")
STAGING_BUCKET = os.environ.get("STAGING_BUCKET", "gs://marketing-campaign-assistant")

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)

# Uncomment the following code to create a new agent engine
app = reasoning_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True,
)

remote_app = agent_engines.create(
    agent_engine=app,
    requirements=[
        "google-cloud-aiplatform[adk,agent_engines]",
    ],
    extra_packages=["./social_posts_agent"],
)
print(f"Remote app created: {remote_app.resource_name}")
