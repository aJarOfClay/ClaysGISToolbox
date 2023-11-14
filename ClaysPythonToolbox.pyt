# -*- coding: utf-8 -*-

# Clay's GIS Toolbox
# https://github.com/aJarOfClay/ClaysGISToolbox

import arcpy

# ran into an issue during development where we need to make sure we're working the most recent version
# many thanks to the solution found here: https://stackoverflow.com/questions/1517038/python-refresh-reload
# set this to True when changing and testing, False for normal use and published versions
in_development_mode = True
if in_development_mode: from importlib import reload


def print_parameters(parameters):
    for idx, parameter in enumerate(parameters):
        message = "parameter {0}: {1}".format(idx, parameter.valueAsText)
        arcpy.AddMessage(message)


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Clay's Python Toolbox"
        self.alias = "ClaysPythonToolbox"

        # List of tool classes associated with this toolbox
        self.tools = [BulkDownload, DEMDifference, CreateExtentPolygon, ExportTableByLabel, MakeProfiles]


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


class ExportTableByLabel(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Export Table By Label"
        self.description = "Exports separate tables from a single source based on unique values in a field"
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""

        inTable = arcpy.Parameter(
            displayName="Input Table",
            name="table_in",
            datatype=["DETable", "DEFeatureClass", "GPTableView"],
            parameterType="Required",
            direction="Input")

        labelField = arcpy.Parameter(
            displayName="Label Field",
            name="field",
            datatype="Field",
            parameterType="Required",
            direction="Input")
        labelField.parameterDependencies = [inTable.name]

#         FieldsToInclude = arcpy.Parameter(
#             displayName="Fields to Include (do not include OBJECTID, SHAPE, or duplicates)",
#             name="included_fields",
#             datatype="Field",
#             parameterType="Required",
#             direction="Input",
#             multiValue=True)
#         FieldsToInclude.parameterDependencies = [inTable.name]

        excelOut = arcpy.Parameter(
            displayName="Output Excel File",
            name="xlsx_out",
            datatype="DEFile",
            parameterType="Required",
            direction="Output")

        excelOut.filter.list = ['xlsx'] # only allow an excel

        params = [inTable, labelField, excelOut]
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
        feature_class_in = parameters[0].valueAsText
        field_in = parameters[1].valueAsText
#         included_fields = parameters[2].valueAsText.split(';')
        file_out =  parameters[2].valueAsText

        import ExportTableByLabel
        if in_development_mode: reload(ExportTableByLabel)
        ExportTableByLabel.do_everything_to_excel(
            input_table=feature_class_in,
            label_field=field_in,
#             wanted_fields=included_fields,
            output_filename=file_out)

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""

        return


class MakeProfiles(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Make Profiles"
        self.description = "Takes line features and makes profiles along rasters"
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""
        # lines_in: line feature class
        # label_field: field from lines
        # rasters_in: Extract Values type
        # density_type: percentage or distance
        # density: float
        # xlsx_out: Excel doc file

        lines_in = arcpy.Parameter(
            displayName="Line Feature Class",
            name="lines_in",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input",
            category="Input Data")
        lines_in.filter.list = ["Polyline"]
        # todo: figure out how to allow GPFeatureLayer with filter

        label_field = arcpy.Parameter(
            displayName="Label Field",
            name="label_field",
            datatype="Field",
            parameterType="Required",
            direction="Input",
            category="Input Data")
        label_field.parameterDependencies = [lines_in.name]

        rasters_in = arcpy.Parameter(
            displayName="Value Rasters",
            name="rasters_in",
            datatype=["DERasterBand","DERasterDataset", "GPRasterLayer", "DEMosaicDataset", "GPMosaicLayer"],
            # "GPSAExtractValues"? maybe just name fields after rasters
            parameterType="Required",
            direction="Input",
            multiValue=True,
            category="Input Data")

        density_type = arcpy.Parameter(
            displayName="Sample Density Type",
            name="density_type",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            category="Sampling")
        density_type.filter.type = "ValueList"
        density_type.filter.list = ["PERCENTAGE", "DISTANCE"]

        percent_density = arcpy.Parameter(
            displayName="Percent Density Value",
            name="percent_density",
            datatype="GPDouble",
            parameterType="Optional",
            direction="Input",
            category="Sampling")

        distance_density = arcpy.Parameter(
            displayName="Distance Density Value",
            name="distance_density",
            datatype="GPLinearUnit",
            parameterType="Optional",
            direction="Input",
            category="Sampling")

        interpolate = arcpy.Parameter(
            displayName="Interpolate Raster Values",
            name="interpolate",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input",
            category="Sampling")
        interpolate.defaultEnvironmentName = False

        keep_sample_points = arcpy.Parameter(
            displayName="Keep Sample Points",
            name="keep_sample_points",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input",
            category="Sampling")
        keep_sample_points.defaultEnvironmentName = False

        xlsx_out = arcpy.Parameter(
            displayName="Output Excel File",
            name="xlsx_out",
            datatype="DEFile",
            parameterType="Required",
            direction="Output",
            category="Output")
        xlsx_out.filter.list = ['xlsx'] # only allow an Excel

        params = [lines_in, label_field, rasters_in, density_type, percent_density, distance_density, interpolate, keep_sample_points, xlsx_out]
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
        if in_development_mode: print_parameters(parameters)
        import MakeProfiles
        if in_development_mode: reload(MakeProfiles)

        file_feature = parameters[0].valueAsText
        label_field = parameters[1].valueAsText
        rasters = parameters[2].valueAsText.split(';')
        sample_type = parameters[3].valueAsText
        if sample_type == 'PERCENTAGE':
            density = parameters[4].valueAsText
        else:
            density = parameters[5].valueAsText
        interpolate = parameters[6].valueAsText
        if interpolate is None:
            interpolate = False
        keep_sample_points = parameters[7].valueAsText
        if keep_sample_points is None:
            keep_sample_points = False
        output = parameters[8].valueAsText

        MakeProfiles.make_profiles(
            lines_in = file_feature,
            label_field = label_field,
            rasters_in = rasters,
            density_type = sample_type,
            density = density,
            interpolate = interpolate,
            keep_sample_points = keep_sample_points,
            xlsx_out = output)

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""

        return

