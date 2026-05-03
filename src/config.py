"""
Configuration and logging setup for the Music Recommender Agent.

Provides centralized logging, configuration management, and constants.
"""

import logging
import os
import json
from datetime import datetime
from typing import Optional

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


def setup_logging(run_id: Optional[str] = None) -> tuple[logging.Logger, str]:
    """
    Initialize logging with timestamps and unique run ID.
    
    Args:
        run_id: Optional custom run ID. If None, generates one from timestamp.
    
    Returns:
        tuple: (logger instance, run_id)
    
    Examples:
        >>> logger, run_id = setup_logging()
        >>> logger.info("Agent started")
    """
    if run_id is None:
        run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    logger = logging.getLogger("recommender_agent")
    logger.setLevel(logging.DEBUG)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # File handler - logs everything
    log_file = os.path.join(LOG_DIR, f"agent_run_{run_id}.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    # Console handler - logs INFO and above
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info(f"Logging initialized for run: {run_id}")
    
    return logger, run_id


class AgentConfig:
    """Configuration constants for the agent workflow."""
    
    # Fuzzy matching threshold for genres/moods
    FUZZY_MATCH_THRESHOLD = 0.7
    
    # Default number of recommendations
    DEFAULT_K_RECOMMENDATIONS = 5
    
    # Energy scale explanation
    ENERGY_SCALE = {
        "low": (0.0, 0.3, "Chill, background music"),
        "medium": (0.3, 0.65, "Balanced energy"),
        "high": (0.65, 1.0, "Energetic, intense"),
    }
    
    # Suggested mood options from the catalog
    EXAMPLE_MOODS = ["chill", "focused", "happy", "intense", "relaxed", "moody", "joyful"]
    
    # Suggested genres from the catalog
    EXAMPLE_GENRES = ["lofi", "pop", "rock", "ambient", "jazz", "synthwave", "indie pop", "electronic"]
    
    # Weight adjustment increments
    WEIGHT_ADJUSTMENT = 0.1


def save_session_data(run_id: str, user_profile: dict, recommendations: list, logger: logging.Logger) -> str:
    """
    Save session data to JSON for reproducibility.
    
    Args:
        run_id: Unique session identifier
        user_profile: The UserProfile as a dict
        recommendations: List of recommendation tuples
        logger: Logger instance
    
    Returns:
        str: Path to saved JSON file
    """
    session_file = os.path.join(LOG_DIR, f"session_{run_id}.json")
    
    session_data = {
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(),
        "user_profile": user_profile,
        "recommendations": [
            {
                "title": rec[0]["title"],
                "artist": rec[0]["artist"],
                "score": rec[1],
                "explanation": rec[2]
            }
            for rec in recommendations
        ]
    }
    
    try:
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        logger.info(f"Session data saved to {session_file}")
        return session_file
    except Exception as e:
        logger.error(f"Failed to save session data: {e}")
        return ""
