from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class Waypoint:
    lat: float
    lon: float
    height: float
    speed: Optional[float] = None
    heading: int = 0
    turn_mode: str = "toPointAndStopWithDiscontinuityCurvature"
    turn_radius: float = 0.2
    actions: List[Dict[str, Any]] = field(default_factory=list)