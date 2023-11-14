import arcpy
import ExportTableByLabel
import MakeExcelCharts
import string

def make_profiles(lines_in, label_field, rasters_in, density_type, density, interpolate, keep_sample_points, xlsx_out):
    # lines_in: line feature class
    # label_field: field from lines
    # rasters_in: Extract Values type
    # density_type: percentage or distance
    # density: float or linear unit
    # xlsx_out: Excel doc file

    arcpy.SetProgressor("step", "Making Profiles", 0, 5, 1)

    # process input
    arcpy.SetProgressorLabel("Processing Input")
    arcpy.SetProgressorPosition()
    raster_mapping = []
    valid_fieldname_chars = "%s%s_" % (string.ascii_letters, string.digits)
    for raster in rasters_in:
        desc = arcpy.Describe(raster)
        field_name = ''.join(c for c in desc.name if c in valid_fieldname_chars)
        raster_mapping.append([desc.catalogPath,field_name])

    if keep_sample_points:
        points_fc = "{0}_SamplePoints".format(arcpy.Describe(lines_in).catalogPath)
    else:
        points_fc = "in_memory/pointsAlongLines"

    # make table
    arcpy.SetProgressorLabel("Generating Points")
    arcpy.SetProgressorPosition()
    if density_type == 'PERCENTAGE':
        arcpy.management.GeneratePointsAlongLines(Input_Features=lines_in,
                                                  Output_Feature_Class=points_fc,
                                                  Point_Placement=density_type,
                                                  Percentage=density,
                                                  Include_End_Points=True,
                                                  Add_Chainage_Fields=True)
    elif density_type == 'DISTANCE':
        arcpy.management.GeneratePointsAlongLines(Input_Features=lines_in,
                                                  Output_Feature_Class=points_fc,
                                                  Point_Placement=density_type,
                                                  Distance=density,
                                                  Include_End_Points=True,
                                                  Add_Chainage_Fields=True)
    else:
        arcpy.AddError("Point density doesn't work")
        return 1
    arcpy.SetProgressorLabel("Extracting Values to Points")
    arcpy.SetProgressorPosition()
    arcpy.sa.ExtractMultiValuesToPoints(in_point_features=points_fc,
                                        in_rasters=raster_mapping,
                                        bilinear_interpolate_values=interpolate)

    # export to excel
    # set wanted fields
    arcpy.SetProgressorLabel("Exporting Table")
    arcpy.SetProgressorPosition()
    wanted_fields = [label_field, 'ORIG_SEQ', 'ORIG_LEN']
    for raster in raster_mapping:
        wanted_fields.append(raster[1])
    ExportTableByLabel.labels_to_excel_sheets(input_table=points_fc,
                                              included_fields=wanted_fields,
                                              label_field=label_field,
                                              output_filename=xlsx_out)

    # make charts in Excel
    arcpy.SetProgressorLabel("Drawing Charts")
    arcpy.SetProgressorPosition()
    label_list = ExportTableByLabel.unique_values(points_fc, label_field)
    y_cols = []
    col_name = 'E'
    for field in wanted_fields[3:]:
        y_cols.append(col_name)
        col_name = chr(ord(col_name)+1)
    MakeExcelCharts.chart_for_each_sheet(filename=xlsx_out,
                                         list_of_sheets=label_list,
                                         x_axis_label_column='C',
                                         y_axis_columns=y_cols,
                                         split_axes = True)
    return



