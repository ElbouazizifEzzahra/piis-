from models.segment import Segment, Geometry, RoadType, SurfaceType
from datetime import date

MOCK_SEGMENTS = [
    Segment(
        id="segment-001",
        name="Route N1 - Rabat",
        code="RN1-001",
        length_km=12.5,
        road_type=RoadType.NATIONALE,
        surface_type=SurfaceType.BITUME,
        construction_year=1990,
        last_maintenance_date=date(2021, 3, 15),
        geometry=Geometry(lat=33.9716, lon=-6.8498)   # Rabat — normal
    ),
    Segment(
        id="segment-002",
        name="Route Sahara - Ouarzazate",
        code="SAH-002",
        length_km=3.8,
        road_type=RoadType.REGIONALE,
        surface_type=SurfaceType.BETON,
        construction_year=2010,
        last_maintenance_date=date(2024, 1, 10),
        geometry=Geometry(lat=30.9335, lon=-6.9370)   # Ouarzazate — désert, chaud, sec
    ),
    Segment(
        id="segment-003",
        name="Autoroute Nord - Tanger",
        code="A3-003",
        length_km=45.0,
        road_type=RoadType.AUTOROUTE,
        surface_type=SurfaceType.BITUME,
        construction_year=2000,
        last_maintenance_date=date(2020, 7, 22),
        geometry=Geometry(lat=35.7595, lon=-5.8340)   # Tanger — côte, humide, venteux
    ),
     Segment(
        id="segment-002",
        name="Desert Road - Dubai",
        code="UAE-D1-002",
        length_km=18.0,
        road_type=RoadType.NATIONALE,
        surface_type=SurfaceType.BETON,
        construction_year=2005,
        last_maintenance_date=date(2023, 3, 20),
        geometry=Geometry(lat=25.2048, lon=55.2708)   # Dubai — chaleur extrême, sec
    ),
    Segment(
        id="segment-004",
        name="Route Nationale - Paris",
        code="FR-RN7-003",
        length_km=35.0,
        road_type=RoadType.NATIONALE,
        surface_type=SurfaceType.BITUME,
        construction_year=1995,
        last_maintenance_date=date(2022, 11, 5),
        geometry=Geometry(lat=48.8566, lon=2.3522)    # Paris — pluie modérée
    ),
    Segment(
    id="segment-005",
    name="Highway BR-101 - Manaus",
    code="BR-101-004",
    length_km=60.0,
    road_type=RoadType.AUTOROUTE,
    surface_type=SurfaceType.PAVE,
    construction_year=1978,
    last_maintenance_date=date(2019, 2, 10),
    geometry=Geometry(lat=-3.1190, lon=-60.0217)  # Manaus Brésil — forêt amazonienne
)

]