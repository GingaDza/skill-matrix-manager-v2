"""グループモデル
Created: 2025-02-08 22:13:49
Author: GingaDza
"""
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Group:
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime