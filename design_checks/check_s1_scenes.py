"""Paper 2 design check: Sentinel-1 scenes per year in the flood windows, by satellite."""
import ee

ee.Initialize(project="bd-agri-climate")
AREAS = {"Bangladesh": [88.0, 20.6, 92.7, 26.7], "Haor basin": [90.6, 24.2, 91.9, 25.3]}


def scenes(box, start, end):
    c = (ee.ImageCollection("COPERNICUS/S1_GRD").filterBounds(ee.Geometry.Rectangle(box))
         .filterDate(start, end).filter(ee.Filter.eq("instrumentMode", "IW"))
         .filter(ee.Filter.listContains("transmitterReceiverPolarisation", "VV")))
    return c.aggregate_histogram("platform_number").getInfo()


for name, box in AREAS.items():
    print(name)
    for y in range(2015, 2026):
        print(" ", y, "Apr-May", scenes(box, f"{y}-04-01", f"{y}-06-01"), "| Jan-Mar", scenes(box, f"{y}-01-01", f"{y}-04-01"))
