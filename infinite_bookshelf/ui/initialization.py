"""
Function to initialize streamlit session states and environment variables
"""

import streamlit as st
from dotenv import load_dotenv
from typing import List, Dict, Any
import os

# load .env file to environment
load_dotenv()


def load_return_env(variables: List[str]) -> Dict[str, str]:
    return {var: os.getenv(var, None) for var in variables}


def ensure_states(state_dict: Dict[str, Any]) -> None:
    """
    Define key values in session state
    if key not already defined
    """
    for key, default_value in state_dict.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
