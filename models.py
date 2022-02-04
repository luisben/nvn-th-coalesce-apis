from typing import Dict
from dataclasses import dataclass


@dataclass
class MemberRecord:
    deductible: int
    stop_loss: int
    oop_max: int


@dataclass
class APIConfig:
    id: str
    hostname: str
    headers: Dict