# Clay's GIS Toolbox
This is my Python Toolbox that I use in ArcGIS Pro, and you're free to use it too. This is an ongoing project -- tools will be added and updated as I work on them.

How to use: extract all files wherever you like, then add the toolbox in your ArcGIS Pro project. I plan to make this also work for QGIS and command-line in the future


## Tool Documentation
### Bulk Download
Download a bunch of files without all the hassle of clicking around!

**Input List**: txt file containing a list of URLs on separate lines. e.g:
```
https://www.example.com/image.jpg
https://www.example.com/index.html
... 
```
**Output Directory**: target folder for the downloaded files. This (should) default to a folder within the current active project once an input file is selected.


### Difference Between DEMs
Need to know how two DEMs differ? Look no further! It even symbolizes the output for you!

**Input Rasters 1 & 2**: the rasters to compare, either a raster (or mosaic) layer or a raster on disk. If the cell sizes differ, the finer one will be downsampled to match the first and stored in the workspace

**Output Raster**: where to store the output raster. This is created by subtracting raster 2 from raster 1 -- positive values mean raster 1 was on top, negative values mean raster 2 was on top.



## Current and future work
- [ ] Finish up bulk downloader
    - [ ] Skip Existing Files toggle
    - [ ] Add Directory To Project toggle
    - [ ] Add toggle for upsample vs downsample
- [ ] Finish up DEM difference
    - [ ] Make the downsample a temporary file to avoid clutter
    - [ ] Generate histogram and statistics table from the difference
    - [ ] Test edge cases
    - [ ] Function to show each elevation and difference along a provided line
    - [ ] Function to create a local scene for comparing the rasters directly
- [ ] Make good plots
- [ ] Make the toolbox's metadata and documentation work
- [ ] Make usable in QGIS
- [ ] Make usable in command line
