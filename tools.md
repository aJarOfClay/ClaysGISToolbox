# Tool Documentation
## Bulk Download
Download a bunch of files without all the hassle of clicking around!

**Input List**: txt file containing a list of URLs on separate lines. e.g:
```
https://www.example.com/image.jpg
https://www.example.com/index.html
... 
```
**Output Directory**: target folder for the downloaded files. This (should) default to a folder within the current active project once an input file is selected.


## Difference Between DEMs
Need to know how two DEMs differ? Look no further! It even symbolizes the output for you!

**Input Rasters 1 & 2**: the rasters to compare, either a raster (or mosaic) layer or a raster on disk. If the cell sizes differ, the finer one will be downsampled to match the first and stored in the workspace

**Output Raster**: where to store the output raster. This is created by subtracting raster 2 from raster 1 -- positive values mean raster 1 was on top, negative values mean raster 2 was on top.


## Create Extent Polygon
Want to see how far your raster goes without loading the whole thing? Now you can turn it into a single polygon!

**Input Raster**: Any raster dataset or layer.

**Feature Class**: Where to store the resulting polygon. Can either be a new feature class, or an existing one to be overwritten

Known quirk: when a raster has been clipped / extracted, the removed cells are replaced with NoData instead of Null, which leaves artifacts when using IsNull(). This tool still works, it just generates 2 polygons showing the current and previous extent.
