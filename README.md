# Clay's GIS Toolbox
This is my Python Toolbox that I use in ArcGIS Pro, and you're free to use it too. This is an ongoing project -- tools will be added and updated as I work on them.

## How to use
Extract all files wherever you like (keeping them all together!), then add the toolbox in your ArcGIS Pro project. The [.pyt file](https://github.com/aJarOfClay/ClaysGISToolbox/blob/main/ClaysPythonToolbox.pyt) is really just ArcGIS Pro's interface to run each of the scripts. If you'd like to use one of the tools in another script, you can copy the tool's standalone .py into your project directory and import it (open the main .pyt to see how each one is used).

I plan to make this also work for QGIS and command-line in the future

## Tools
- Bulk Download
- Difference Between DEMs
- Create Extent Polygon

See [tools.md](https://github.com/aJarOfClay/ClaysGISToolbox/blob/main/tools.md) for how each one is used

## Current and future work
- [ ] Finish up bulk downloader
    - [ ] Skip Existing Files toggle
    - [ ] Add Directory To Project toggle
- [ ] Finish up DEM difference
    - [ ] Make the downsample a temporary file to avoid clutter
    - [ ] Add toggle for upsample vs downsample
    - [ ] Generate histogram and statistics table from the difference
    - [ ] Test edge cases
    - [ ] Function to show each elevation and difference along a provided line
    - [ ] Function to create a local scene for comparing the rasters directly
- [ ] Finish up extent polygon
    - [ ] Allow appending to an existing feature class
    - [ ] Add identifying names to output polygons
    - [ ] Resolve IsNull() quirk - maybe find a way to not rely on spatial analyst
- [ ] Make good plots
- [ ] Make the toolbox's metadata and documentation work
- [ ] Make usable in command line
    - [ ] Disable adding to map & symbology when not run from an active project
    - [ ] Switch for whether to use print() or arcpy.AddMessage() for progress updates
    - [ ] CL interfaces
- [ ] Make usable in QGIS
