import os

DEFAULT_SYSTEM_PROMPT: str = "You are a helpful assistant."

USER_PROFILE_SUB_DIRECTORY: str = os.path.join(os.getcwd(), "profiles")
USER_PROFILE_FILE_NAME: str = "profile.json"
USER_PROFILE_MATCHES_FILE_NAME: str = "matches.json"
USER_PROFILE_IMAGE_FILE_NAME: str = "profile.png"
USER_PROFILE_SUMMARY_KEY: str = "profile_summary"
USER_PROFILE_PREFERENCES_SUMMARY_KEY: str = "preferences_summary"
USER_PROFILE_USER_ID_KEY: str = "user_id"

USER_MATCH_RETRIEVED_KEY: str = "retrieved"
USER_MATCH_RANKED_KEY: str = "ranked"

CHROMA_DISTANCE_KEY: str = "hnsw:space"
CHROMA_PERSISTENT_PATH: str = ".chroma"
CHROMA_USER_PROFILES_COLLECTION_NAME: str = "user_profiles"
CHROMA_DISTANCE: str = "cos"

OPENAI_RATE_LIMIT_SLEEP_SECONDS: int = 10
