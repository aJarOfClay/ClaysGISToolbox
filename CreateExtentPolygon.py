import arcpy

def MakePolygon(input_raster, feature_class_location):
    arcpy.SetProgressor("step", "Generating Extent Polygon", 0, 3, 1)  # set up progress bar
    # extract parameters and make descriptions for each input raster
    arcpy.SetProgressorLabel("Looking at inputs")

    arcpy.SetProgressorPosition()

    arcpy.SetProgressorLabel("Executing IsNull")
    null_raster = arcpy.sa.IsNull(input_raster)
    arcpy.SetProgressorPosition()

    arcpy.SetProgressorLabel("Executing RasterToPolygon")
    arcpy.conversion.RasterToPolygon(
        in_raster=null_raster,
        out_polygon_features=feature_class_location,
        simplify="NO_SIMPLIFY")
    arcpy.SetProgressorPosition()
