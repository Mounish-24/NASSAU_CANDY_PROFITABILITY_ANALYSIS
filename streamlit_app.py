"""
Streamlit Community Cloud Deployment Entrypoint for Nassau Candy Profitability Analysis.
"""

import sys
import runpy
from pathlib import Path

# Add root directory to path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

# Run main dashboard app cleanly
app_path = root_dir / "dashboard" / "app.py"
runpy.run_path(str(app_path), run_name="__main__")

