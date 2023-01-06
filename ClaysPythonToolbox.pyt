# -*- coding: utf-8 -*-
import arcpy
import os
from datetime import datetime
import requests
import string

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "Clay's Python Toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [BulkDownload, DEMDifference]  # RasterTesting also exists, but I'm not including it here


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

        # creating target directory if needed
        try:
            os.mkdir(output_directory)
            arcpy.AddMessage("Created new directory " + output_directory)
        except OSError:
            arcpy.AddMessage("Using existing directory " + output_directory)

        # make a list of URLs to look at
        url_list = []
        with open(input_list,'r',encoding='utf8') as f:
            url_list = f.readlines()  # crack apart entries
        for i in range(len(url_list)):
            url_list[i] = url_list[i].replace('\n', '')  # strip off newlines
        url_list = [i for i in url_list if i]  # strip out blank entries


        # function for downloading each file
        def download_file(file_url, target_folder):

            r = requests.get(file_url, headers=headers)  # create HTTP response object
            file_name = get_filename(file_url)
            # send an HTTP request to the server and save the HTTP response in a response object called r
            with open(os.path.join(target_folder, file_name), 'wb') as f:
                # write the contents of the response (r.content) to a new file in binary mode.
                f.write(r.content)
            return 0

        # make a "problem links" list in the output if needed
        problem_url_list = os.path.join(output_directory, datetime.now().strftime('ProblemURLs_%Y-%m-%d_%H-%M-%S.txt'))
        def add_problem_url(problem_url):
            f = open(problem_url_list, "a")
            f.write(problem_url + "\n")
            f.close()

        def get_filename(file_url):
            i = len(file_url) - 1
            first_letter = 0
            while i >= 0:
                if file_url[i] == "/":
                    first_letter = i + 1
                    break
                else:
                    i -= 1
            temp_filename = file_url[first_letter:]
            valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
            true_filename = ''.join(c for c in temp_filename if c in valid_chars)
            return true_filename

        # download each file
        current_url = 0
        total_urls = len(url_list)
        had_problem_urls = False
        headers = {'User-Agent': "Clay's Bulk Downloader (claystestingaddress@gmail.com)"}
        # Wikimedia commons (and probably others) won't allow requests without an identifying header
        arcpy.SetProgressor("step", "Downloading Files", 0, total_urls, 1)
        for url in url_list:
            try:
                current_url += 1
                message =  "Fetching file %d / %d" % (current_url, total_urls)
                arcpy.SetProgressorLabel(message)
                # arcpy.AddMessage(datetime.now().strftime("%H:%M:%S") + " | " + message)
                download_file(url, output_directory)
            # Invalid URL
            except requests.exceptions.MissingSchema:
                arcpy.AddWarning("Invalid URL")
                add_problem_url(url)
                had_problem_urls = True
            except requests.exceptions.InvalidSchema:
                arcpy.AddWarning("Invalid URL")
                add_problem_url(url)
                had_problem_urls = True
            # Trouble connecting
            except requests.exceptions.ConnectionError or socket.gaierror \
                   or urllib3.exceptions.NewConnectionError or urllib3.exceptions.MaxRetryError:
                arcpy.AddWarning("Could not connect")
                add_problem_url(url)
                had_problem_urls = True
            arcpy.SetProgressorPosition()

        # end message
        arcpy.AddMessage("Downloads complete! Check '%s' to see your files." % output_directory)
        if had_problem_urls:
            arcpy.AddWarning("File created at '%s' with a list of problem urls" % problem_url_list)

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""

        return

class RasterTesting(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Raster Testing"
        self.description = "Basic tool for learning how to work with rasters"
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""
        # Location of the raster
        param0 = arcpy.Parameter(
            displayName = "Raster",
            name = "input_raster",
            datatype = ["DERasterDataset", "GPRasterLayer"],
            parameterType = "Required",
            direction = "Input")

        # Select a band. If blank, all will be analyzed.
        param1 = arcpy.Parameter(
            displayName = "Band (set blank or 0 to analyze all)",
            name = "band",
            datatype = "GPLong",
            parameterType = "Optional",
            direction = "Input")

        params = [param0,param1]
        return params

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        input_raster = parameters[0]
        band_filter = parameters[1].filter

        # Update number of bands available based on the input raster dataset
        num_bands = arcpy.Describe(input_raster).bandcount
        band_filter.list = [*range(0,num_bands+1)]
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        input_raster = parameters[0].valueAsText
        # Simply announce what python is actually seeing when the parameters are passed
        # Turns out that all you're getting is the address on disk to the dataset
        arcpy.AddMessage("Data recieved: " + input_raster)
        arcpy.AddMessage("Data Type: " + arcpy.Describe(input_raster).datatype)

        # Announce the number of bands using a Describe object
        num_bands = arcpy.Describe(input_raster).bandcount
        arcpy.AddMessage("Number of bands: %s" % num_bands)

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
        # Raster 2
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
        # extract parameters and make descriptions for each input raster
        input_raster_1 = parameters[0].valueAsText
        input_raster_2 = parameters[1].valueAsText
        output_raster_location = parameters[2].valueAsText
        input_raster_1_desc = arcpy.Describe(input_raster_1)
        input_raster_2_desc = arcpy.Describe(input_raster_2)
        # output raster description is generated later when the raster actually exists

        # todo: need to only allow a single raster band through

        # downsample and snap finer raster to match coarser raster
        # compare meanCellWidth
        input_raster_1_cellSize = input_raster_1_desc.meanCellWidth
        input_raster_2_cellSize = input_raster_2_desc.meanCellWidth
        if input_raster_1_cellSize < input_raster_2_cellSize:  # if input 1 is finer, downsample to match input 2
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
            arcpy.AddMessage("Rasters have the same pixel size, snapping to %s" % input_raster_1)
            raster_1 = input_raster_1
            raster_2 = input_raster_2
            arcpy.env.snapRaster = raster_1

        # generate difference raster -- positive means first is on top, negative means second is on top
        # algebra operations already excludes areas without overlap, so no need to worry about it
        arcpy.AddMessage("Subtracting rasters")
        difference_raster = arcpy.Raster(raster_1) - arcpy.Raster(raster_2)
        difference_raster.save(output_raster_location)
        output_raster_object = arcpy.Raster(output_raster_location)

        # create and update layer in current map
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

        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""

        return

