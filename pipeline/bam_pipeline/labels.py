"""The curated label list. Keep it short: the buildings draw the region.

City positions come from Overture locality points (OpenStreetMap). Water labels sit at
the visual center of the named Overture water polygon, unless a hand-placed point is
given (a cartographic choice, not a fact).

Tiers set the first zoom at which a label may appear (see src/map/style.ts):
1 = regional view, 2 = subregional, 3 = local.
"""

# (name as in Overture, county as in Overture hierarchies, tier)
CITIES: list[tuple[str, str, int]] = [
    ("San Francisco", "San Francisco", 1),
    ("Oakland", "Alameda County", 1),
    ("San Jose", "Santa Clara County", 1),
    ("Berkeley", "Alameda County", 2),
    ("Richmond", "Contra Costa County", 2),
    ("Vallejo", "Solano County", 2),
    ("Concord", "Contra Costa County", 2),
    ("Antioch", "Contra Costa County", 2),
    ("Fremont", "Alameda County", 2),
    ("Hayward", "Alameda County", 2),
    ("Palo Alto", "Santa Clara County", 2),
    ("San Mateo", "San Mateo County", 2),
    ("San Rafael", "Marin County", 2),
    ("Santa Rosa", "Sonoma County", 2),
    ("Napa", "Napa County", 2),
    ("Fairfield", "Solano County", 2),
    ("Walnut Creek", "Contra Costa County", 3),
    ("Alameda", "Alameda County", 3),
    ("Brisbane", "San Mateo County", 3),
    ("Daly City", "San Mateo County", 3),
    ("Menlo Park", "San Mateo County", 3),
    ("Redwood City", "San Mateo County", 3),
    ("Mountain View", "Santa Clara County", 3),
    ("Sunnyvale", "Santa Clara County", 3),
    ("Santa Clara", "Santa Clara County", 3),
    ("Cupertino", "Santa Clara County", 3),
    ("Suisun City", "Solano County", 3),
    ("Petaluma", "Sonoma County", 3),
    ("Sausalito", "Marin County", 3),
    ("San Leandro", "Alameda County", 3),
    ("Livermore", "Alameda County", 3),
    ("Pittsburg", "Contra Costa County", 3),
]

# (name, tier, hand-placed [lon, lat] or None to use the polygon's visual center)
WATER: list[tuple[str, int, tuple[float, float] | None]] = [
    ("Pacific Ocean", 1, (-122.66, 37.62)),
    ("San Francisco Bay", 1, None),
    ("San Pablo Bay", 2, None),
    ("Suisun Bay", 2, None),
    ("Carquinez Strait", 3, None),
]
