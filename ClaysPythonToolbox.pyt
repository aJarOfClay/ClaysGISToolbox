# -*- coding: utf-8 -*-

# Clay's GIS Toolbox
# https://github.com/aJarOfClay/ClaysGISToolbox

import arcpy

# ran into an issue during development where we need to make sure we're working the most recent version
# many thanks to the solution found here: https://stackoverflow.com/questions/1517038/python-refresh-reload
# set this to True when changing and testing, False for normal use and published versions
in_development_mode = True
if in_development_mode: from importlib import reload


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "Clay's Python Toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [BulkDownload, DEMDifference, CreateExtentPolygon]


class BulkDownload(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Bulk Download"
        self.description = """Download from a list a links to avoid all that clicking around! \nInput: list of URLs formatted as a line-separated .txt \nOutput: the requested files in a specified folder, with a list of any 'problem urls' if they occur"""
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""
        # Location of the list
        param0 = arcpy.Parameter(
            displayName = "Input List (line-separated .txt)",
            name = "input_list",
            datatype = "DEFile",
            parameterType = "Required",
            direction = "Input")
        
        # Download directory
        param1 = arcpy.Parameter(
            displayName = "Output Directory",
            name = "output_directory",
            datatype = "DEFolder",
            parameterType = "Required",
            direction = "Output")

        # TODO: add toggle for overwriting existing files
        # TODO: add toggle for preserving directory structure

        param0.filter.list = ['txt']

        params = [param0, param1]
        return params

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        input_list = parameters[0].valueAsText
        output_directory = parameters[1].valueAsText

        import BulkDownload
        if in_development_mode: reload(BulkDownload)
        BulkDownload.download(input_list, output_directory)

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""

        return


class DEMDifference(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Difference Between DEMs"
        self.description = "Find the elevation difference in the overlap between two DEMs. Produces a difference raster, table with stats, and histogram. The finer-resolution will be downsampled and snapped to match the coarser one. Ensure both are using the same projection and units"
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""
        # Raster 1
        param0 = arcpy.Parameter(
            displayName = "First Raster",
            name = "raster_1",
            datatype = ["GPRasterLayer", "DERasterDataset", "GPMosaicLayer", "DEMosaicDataset", "DERasterBand"],
            parameterType = "Required",
            direction = "Input")

        # Raster 2
        param1 = arcpy.Parameter(
            displayName = "Second Raster",
            name = "raster_2",
            datatype = ["GPRasterLayer", "DERasterDataset", "GPMosaicLayer", "DEMosaicDataset", "DERasterBand"],
            parameterType = "Required",
            direction = "Input")

        # Output Raster
        param2 = arcpy.Parameter(
            displayName = "Difference Raster",
            name = "raster_out",
            datatype = "DERasterDataset",
            parameterType = "Required",
            direction = "Output")

        params = [param0, param1, param2]
        return params

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        # check number of bands in the rasters provided (skip if raster band is selected)
        # if there's more than one band, require user to select a band

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # set up progress bar
        arcpy.SetProgressor("step", "Finding Difference Between DEMs", 0, 4, 1)

        # extract parameters and make descriptions for each input raster
        arcpy.SetProgressorLabel("Looking at inputs")
        input_raster_1 = parameters[0].valueAsText
        input_raster_2 = parameters[1].valueAsText
        output_raster_location = parameters[2].valueAsText
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
                in_raster = input_raster_1,
                out_raster = raster_1,
                cell_size = input_raster_2_cellSize,
                resampling_type = "BILINEAR")
        elif input_raster_1_cellSize > input_raster_2_cellSize:  # if input 2 is finer, downsample to match input 1
            arcpy.SetProgressorLabel("Downsampling %s" % input_raster_2_desc.baseName)
            raster_1 = input_raster_1
            raster_2 = input_raster_2_desc.baseName + "_downsample"
            arcpy.AddMessage("Downsampling %s as %s to match %s" % (input_raster_2, raster_2, input_raster_1))
            arcpy.env.snapRaster = raster_1
            arcpy.Resample_management(
                in_raster = input_raster_2,
                out_raster = raster_2,
                cell_size = input_raster_1_cellSize,
                resampling_type = "BILINEAR")
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

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""

        return


class CreateExtentPolygon(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Create Extent Polygon"
        self.description = "Create a polygon representing the extent of a raster"
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""
        # Input raster
        param0 = arcpy.Parameter(
            displayName = "Input Raster",
            name = "raster",
            datatype = ["GPRasterLayer", "DERasterDataset", "GPMosaicLayer", "DEMosaicDataset", "DERasterBand"],
            parameterType = "Required",
            direction = "Input")

        # Output feature class
        param1 = arcpy.Parameter(
            displayName = "Feature Class",
            name = "feature_class",
            datatype = ["DEFeatureClass"],
            parameterType = "Required",
            direction = "Output")

        # Identifying name for the resulting polygon
        param2 = arcpy.Parameter(
            displayName = "Polygon Identifier",
            name = "polygon_name",
            datatype = ["GPString"],
            parameterType = "Optional",
            direction = "Output")

        # param1.filter.list = ["Polygon"]  # only allow a polygon

        params = [param0, param1]
        return params

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        # check number of bands in the rasters provided (skip if raster band is selected)
        # if there's more than one band, require user to select a band

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        arcpy.SetProgressor("step", "Generating Extent Polygon", 0, 3, 1)  # set up progress bar
        # extract parameters and make descriptions for each input raster
        arcpy.SetProgressorLabel("Looking at inputs")
        input_raster = parameters[0].valueAsText
        feature_class_location = parameters[1].valueAsText
        arcpy.SetProgressorPosition()

        arcpy.SetProgressorLabel("Executing IsNull")
        null_raster = arcpy.sa.IsNull(input_raster)
        arcpy.SetProgressorPosition()

        arcpy.SetProgressorLabel("Executing RasterToPolygon")
        arcpy.conversion.RasterToPolygon(
            in_raster = null_raster,
            out_polygon_features = feature_class_location,
            simplify = "NO_SIMPLIFY")
        arcpy.SetProgressorPosition()
        
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""

        return
