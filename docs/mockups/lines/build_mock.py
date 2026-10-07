import json, heapq, sys
from shapely.geometry import shape, LineString, Point, mapping
from shapely.ops import linemerge, unary_union, substring
S = sys.argv[1]  # folder holding ntad_jpbx.geojson (fetched from NTAD) and receiving lines-mock.geojson
d = json.load(open(f'{S}/ntad_jpbx.geojson'))
lines = [shape(f['geometry']) for f in d['features'] if f['properties'].get('PASSNGR') and not f['properties'].get('YARDNAME')]
segs = []
for g in lines:
    for l in (g.geoms if g.geom_type == 'MultiLineString' else [g]):
        segs.append(list(l.coords))
# graph on rounded endpoints
adj = {}; pos = {}
for f in d['features']:
    pr = f['properties']
    if pr.get('NET') == 'Y': continue
    g = shape(f['geometry']); c = list((linemerge(g) if g.geom_type == 'MultiLineString' else g).coords)
    a, b = pr['FRFRANODE'], pr['TOFRANODE']; L = LineString(c).length
    pos[a] = c[0]; pos[b] = c[-1]
    adj.setdefault(a, []).append((b, L, c)); adj.setdefault(b, []).append((a, L, c[::-1]))
nodes = list(adj)
near = lambda p: min(nodes, key=lambda n: (pos[n][0]-p[0])**2 + (pos[n][1]-p[1])**2)
start = near((-122.3946, 37.7764))             # 4th & King (end of the Peninsula line)
end = near((-121.902394, 37.330656))            # San Jose Diridon (VTA GTFS)
dist = {start: 0}; prev = {}; pq = [(0, start)]
while pq:
    dd, u = heapq.heappop(pq)
    if u == end: break
    if dd > dist[u]: continue
    for v, L, s in adj[u]:
        if dd + L < dist.get(v, 1e9): dist[v] = dd + L; prev[v] = (u, s); heapq.heappush(pq, (dd + L, v))
parts = []; n = end
while n != start:
    u, s = prev[n]; parts.insert(0, s); n = u
coords = [c for i, s in enumerate(parts) for c in (s if i == 0 else s[1:])]
hsr = LineString(coords)
print('hsr km', round(hsr.length * 111 * 0.85, 1), 'start', start, file=sys.stderr)
K = hsr.coords[0]
def F(geom, **p): return {'type': 'Feature', 'properties': p, 'geometry': mapping(geom)}
stc = (-122.396038, 37.790065)
feats = [
  F(hsr, project='cahsr-sf-sj', stage='entitled', kind='line', segment='shared', name='HSR San Francisco–San José (shares Caltrain tracks)'),
  # Schematic for style only: The Portal tunnel from 4th & King to Salesforce Transit Center.
  F(LineString([K, (-122.3925, 37.7790), (-122.3935, 37.7850), stc]), project='the-portal', stage='entitled', kind='line', segment='tunnel', name='The Portal (schematic)'),
  # Schematic for style only: BART Silicon Valley Phase II, Berryessa to Santa Clara.
  F(LineString([(-121.874681, 37.368473), (-121.8700, 37.3560), (-121.8735, 37.3500), (-121.8860, 37.3370), (-121.902394, 37.330656), (-121.93735, 37.352956)]),
    project='bart-silicon-valley-phase-2', stage='infrastructure', kind='line', segment='tunnel', name='BART Silicon Valley Phase II (schematic)'),
]
for name, c, proj, stage in [
  ('Salesforce Transit Center', stc, 'the-portal', 'entitled'),
  ('4th and King', K, 'cahsr-sf-sj', 'entitled'),
  ('Millbrae', (-122.386757, 37.600237), 'cahsr-sf-sj', 'entitled'),
  ('San José Diridon', (-121.902394, 37.330656), 'cahsr-sf-sj', 'entitled'),
  ('Santa Clara', (-121.93735, 37.352956), 'bart-silicon-valley-phase-2', 'infrastructure'),
]:
  feats.append(F(Point(c), project=proj, stage=stage, kind='station', name=name))
  # Mock footprint for option B only: a 60 m circle, not a traced station.
  from shapely.affinity import scale
  import math
  fp = scale(Point(c).buffer(60 / 110540), xfact=1 / math.cos(math.radians(c[1])), yfact=1)
  feats.append(F(fp, project=proj, stage=stage, kind='station-footprint', name=name))
json.dump({'type': 'FeatureCollection', 'features': feats}, open(f'{S}/lines-mock.geojson', 'w'))
