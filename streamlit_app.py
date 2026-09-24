"""
Streamlit Community Cloud Deployment Entrypoint for Nassau Candy Profitability Analysis.
"""

import sys
from pathlib import Path

# Add root directory to path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

# Import and execute main app
import dashboard.app
