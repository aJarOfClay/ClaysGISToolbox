import arcpy

def generateSlice(input_rasters, slice_line):
    template_points = arcpy.GeneratePointsAlongLines_management(
        Input_Features = slice_line,
        Output_Feature_Class = "in_memory/PointTemplate",
        Point_Placement = "PERCENTAGE",
        Percentage = 0.5)

    for dem in input_rasters:
        arcpy.sa.ExtractValuesToPoints(
            in_point_features = template_points,
            in_raster = dem,
            out_point_features = "points" + arcpy.Describe(dem).basename,
            interpolate_values = True)
