import arcpy

def difference(input_raster_1, input_raster_2, output_raster_location):
    # set up progress bar
    arcpy.SetProgressor("step", "Finding Difference Between DEMs", 0, 4, 1)

    # extract parameters and make descriptions for each input raster
    arcpy.SetProgressorLabel("Looking at inputs")

    input_raster_1_desc = arcpy.Describe(input_raster_1)
    input_raster_2_desc = arcpy.Describe(input_raster_2)
    # output raster description is generated later when the raster actually exists
    arcpy.SetProgressorPosition()

    # todo: need to only allow a single raster band through

    # downsample and snap finer raster to match coarser raster
    input_raster_1_cellSize = input_raster_1_desc.meanCellWidth
    input_raster_2_cellSize = input_raster_2_desc.meanCellWidth
    if input_raster_1_cellSize < input_raster_2_cellSize:  # if input 1 is finer, downsample to match input 2
        arcpy.SetProgressorLabel("Downsampling %s" % input_raster_1_desc.baseName)
        raster_2 = input_raster_2
        raster_1 = input_raster_1_desc.baseName + "_downsample"
        arcpy.AddMessage("Downsampling %s as %s to match %s" % (input_raster_1, raster_1, input_raster_2))
        arcpy.env.snapRaster = raster_2
        arcpy.Resample_management(
            in_raster=input_raster_1,
            out_raster=raster_1,
            cell_size=input_raster_2_cellSize,
            resampling_type="BILINEAR")
    elif input_raster_1_cellSize > input_raster_2_cellSize:  # if input 2 is finer, downsample to match input 1
        arcpy.SetProgressorLabel("Downsampling %s" % input_raster_2_desc.baseName)
        raster_1 = input_raster_1
        raster_2 = input_raster_2_desc.baseName + "_downsample"
        arcpy.AddMessage("Downsampling %s as %s to match %s" % (input_raster_2, raster_2, input_raster_1))
        arcpy.env.snapRaster = raster_1
        arcpy.Resample_management(
            in_raster=input_raster_2,
            out_raster=raster_2,
            cell_size=input_raster_1_cellSize,
            resampling_type="BILINEAR")
    else:  # rasters are the same size - don't change them, just snap to raster 1
        arcpy.SetProgressorLabel("Rasters appear to match, not downsampling")
        arcpy.AddMessage("Rasters have the same pixel size, snapping to %s" % input_raster_1)
        raster_1 = input_raster_1
        raster_2 = input_raster_2
        arcpy.env.snapRaster = raster_1
    arcpy.SetProgressorPosition()

    # generate difference raster -- positive means first is on top, negative means second is on top
    # algebra operations already excludes areas without overlap, so no need to worry about it
    arcpy.SetProgressorLabel("Subtracting rasters")
    arcpy.AddMessage("Subtracting rasters")
    difference_raster = arcpy.Raster(raster_1) - arcpy.Raster(raster_2)
    difference_raster.save(output_raster_location)
    output_raster_object = arcpy.Raster(output_raster_location)
    arcpy.SetProgressorPosition()

    # create and update layer in current map
    arcpy.SetProgressorLabel("Adding and symbolizing raster layer")
    p = arcpy.mp.ArcGISProject("current")
    m = p.activeMap
    m.addDataFromPath(output_raster_object.catalogPath)  # add the data as a new layer
    l = m.listLayers(output_raster_object.name)[0]
    sym = l.symbology  # start symbolizing
    sym.updateColorizer('RasterStretchColorizer')
    sym.colorizer.classificationField = 'Value'
    sym.colorizer.stretchType = 'PercentClip'
    sym.colorizer.minPercent = 1.0
    sym.colorizer.maxPercent = 1.0
    sym.colorizer.colorRamp = p.listColorRamps("Orange-Purple (Continuous)")[0]
    # some conditions for labeling based on min/max value
    min_difference = arcpy.Raster(output_raster_location).minimum
    max_difference = arcpy.Raster(output_raster_location).maximum
    if min_difference >= 0:  # raster 1 is always on top
        sym.colorizer.maxLabel = input_raster_1_desc.baseName + " on top by " + str(round(max_difference, 4))
        sym.colorizer.minLabel = input_raster_1_desc.baseName + " on top by " + str(round(min_difference, 4))
    elif (max_difference < 0):  # raster 2 is always on top
        sym.colorizer.maxLabel = input_raster_2_desc.baseName + " on top by " + str(round(max_difference * -1, 4))
        sym.colorizer.minLabel = input_raster_2_desc.baseName + " on top by " + str(round(min_difference * -1, 4))
    else:  # rasters go back and forth
        sym.colorizer.maxLabel = input_raster_1_desc.baseName + " on top by " + str(round(max_difference, 4))
        sym.colorizer.minLabel = input_raster_2_desc.baseName + " on top by " + str(round(min_difference * -1, 4))
    l.symbology = sym
    arcpy.SetProgressorPosition()

if __name__ == '__main__':  # executed on its own
    try:  # if arguments are given, use those
        raster_1 = sys.argv[1]
        raster_2 = sys.argv[2]
        raster_out = sys.argv[3]
        difference(raster_1, raster_2, raster_out)
    except IndexError:  # otherwise, ask and verify through command line
        print("Sorry, this doesn't work on command line yet")
