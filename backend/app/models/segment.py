from pydantic import BaseModel
from datetime import date
from enum import Enum

# --- Enums ---
class RoadType(str, Enum):
    AUTOROUTE = "Autoroute"
    NATIONALE = "Nationale"
    REGIONALE = "Régionale"
    URBAINE   = "Urbaine"

class SurfaceType(str, Enum):
    BITUME = "Bitume"
    BETON  = "Béton"
    PAVE   = "Pavé"
    AUTRE  = "Autre"

class SegmentStatus(str, Enum):
    BON          = "Bon"
    DEGRADE      = "Dégradé"
    CRITIQUE     = "Critique"
    HORS_SERVICE = "Hors service"

# --- Models ---
class Geometry(BaseModel):
    lat: float
    lon: float

class Segment(BaseModel):
    id: str
    name: str
    code: str
    length_km: float
    road_type: RoadType        # ← Enum
    surface_type: SurfaceType  # ← Enum
    construction_year: int
    last_maintenance_date: date
    geometry: Geometry