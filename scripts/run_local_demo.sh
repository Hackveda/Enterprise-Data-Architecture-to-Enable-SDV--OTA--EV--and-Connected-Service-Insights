#!/usr/bin/env bash
set -euo pipefail
python -m src.data.generate_dimensions
streamlit run dashboard/app.py
