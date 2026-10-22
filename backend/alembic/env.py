# Add at top of alembic/env.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.session import Base
from app.core.config import settings
from app.models.domain import User, CommunityRequest  # import models

target_metadata = Base.metadata