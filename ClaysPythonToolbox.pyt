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
        self.tools = [BulkDownload, DEMDifference, CreateExtentPolygon, ViewVerticalSlice]


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
        input_raster_1 = parameters[0].valueAsText
        input_raster_2 = parameters[1].valueAsText
        output_raster_location = parameters[2].valueAsText

        import DEMDifference
        if in_development_mode: reload(DEMDifference)
        DEMDifference.difference(input_raster_1, input_raster_2, output_raster_location)

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

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        input_raster = parameters[0].valueAsText
        feature_class_location = parameters[1].valueAsText

        import CreateExtentPolygon
        if in_development_mode: reload(CreateExtentPolygon)
        CreateExtentPolygon.MakePolygon(input_raster, feature_class_location)
        
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""

        return


class ViewVerticalSlice(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "View Vertical Slice"
        self.description = "Create a plot representing the height of one or more DEMs"
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""
        # Input rasters
        param0 = arcpy.Parameter(
            displayName = "Input DEMs",
            name = "rasters",
            datatype = ["GPRasterLayer", "DERasterDataset", "GPMosaicLayer", "DEMosaicDataset", "DERasterBand"],
            parameterType = "Required",
            direction = "Input",
            multiValue = True)

        # Line to follow
        param1 = arcpy.Parameter(
            displayName = "Line to slice through",
            name = "line",
            datatype = ["DEFeatureClass", "GPFeatureLayer"],
            parameterType = "Required",
            direction = "Input")

        # param1.filter.list = ["Line"]  # only allow a line

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
        input_rasters = parameters[0].valueAsText
        raster_list = input_rasters.split(";")
        line = parameters[1].valueAsText

        arcpy.AddMessage("Recieved Data: ")
        arcpy.AddMessage(raster_list)
        
        # import ViewVerticalSlice
        # if in_development_mode: reload(ViewVerticalSlice)
        # ViewVerticalSlice.MakePlot(input_rasters, line)
        
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""

        return
