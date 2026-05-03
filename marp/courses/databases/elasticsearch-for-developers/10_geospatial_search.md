---
tags:
  - databases:elasticsearch
  - databases:geospatial
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Geospatial Search

---

## Geospatial Capabilities

![geo_capabilities](svg/courses/databases/elasticsearch-for-developers/10_geospatial_search/geo_capabilities.svg)

---
## What This Chapter Covers

- geo_point and geo_shape
- Distance queries
- Bounding boxes
- Polygons
- Geo aggregations
- Distance sort

---
## Geospatial Features

![geo_features](svg/courses/databases/elasticsearch-for-developers/10_geospatial_search/geo_features.svg)

---
## geo_point

- Single lat/lon
- Stored efficiently
- Distance queries fast

---
## Geo Point Example

```json
"location": { "lat": 40.7, "lon": -73.9 }
```

- Or as GeoJSON, geohash, string

---
## Distance Query

```json
{
  "geo_distance": {
    "distance": "5km",
    "location": { "lat": 40.7, "lon": -73.9 }
  }
}
```

- "Within 5km of point"
- Common: stores near me

---
## Bounding Box

```json
{
  "geo_bounding_box": {
    "location": {
      "top_left": {...},
      "bottom_right": {...}
    }
  }
}
```

- Map-view queries
- Faster than distance

---
## Polygon

```json
{
  "geo_polygon": {
    "location": {
      "points": [...]
    }
  }
}
```

- Arbitrary shapes
- Cities, regions
- Slower than bounding box

---
## geo_shape

- Lines, polygons, multi-shapes
- Larger than geo_point
- Use for: regions, routes, areas

---
## Geo Aggregations

- geohash_grid: bucket by geohash
- geotile_grid: bucket by tile
- Used for heat maps

---
## Distance Sort

- Sort by distance from a point
- Combined with relevance
- "Nearest restaurants" with score boost

---
## Geo Distance Aggregation

- "How many in each radius"
- 1km, 5km, 10km buckets

---
## Performance

- geo_point much faster than geo_shape
- Use the smallest data type that works
- Pre-filter heavily

---
## Geo Decay

- Function score with linear / gauss / exp decay
- Boost results closer to user
- Combined with full-text relevance

---
## Geo Indexing

- Lat/lon coords from frontend
- Validate before indexing
- Common: MapBox, Google Maps for display

---
## Common Geo Mistakes

- geo_shape when geo_point would do
- Lat/lon swapped (longitude first in GeoJSON!)
- No bounding box pre-filter (slow)
- Sorting by distance without filtering first
- Forgetting that the earth is curved (great circle distance)
