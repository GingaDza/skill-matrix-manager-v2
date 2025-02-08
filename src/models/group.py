"""グループモデル
Created: 2025-02-08 20:44:07
Author: GingaDza
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Group:
    """グループモデル"""
    id: int
    name: str
    description: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
