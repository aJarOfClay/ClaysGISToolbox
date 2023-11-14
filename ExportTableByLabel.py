import arcpy
import FeatureTabletoDataframe
import pandas as pd


def labels_to_excel_sheets(input_table, included_fields, label_field, output_filename):
    # create a list of unique labels to work with
    list_of_labels = unique_values(input_table, label_field)

    # # create list of fields to output
    # table_fields = arcpy.ListFields(input_table)
    # wanted_fields = []
    # for field in table_fields:
    #     wanted_fields.append(field.name)
    # forbidden_words = ['OBJECTID', 'OID', 'SHAPE', 'Shape']
    # for forbidden_word in forbidden_words:
    #     try:
    #         wanted_fields.remove(forbidden_word)
    #     except ValueError:
    #         pass
    # arcpy.AddMessage("using fields " + str(wanted_fields))

    # for each label, select that subset from the table and write out each selection in its own excel worksheet
    with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
        for label in list_of_labels:
            where_clause = ''' {0} = '{1}' '''.format(label_field, label)
            pd_data_frame = FeatureTabletoDataframe.arcgis_table_to_dataframe(in_fc=input_table,
                                                                              input_fields=included_fields,
                                                                              query=where_clause)
            pd_data_frame.to_excel(writer, sheet_name=label)

    # figure out a way to add the charts automatically
    # column list is everything after the Notes field
    # actually -- maybe capture the original line's fields and compare to point's fields

# returns a list with the unique values in a feature class's field
# shamelessly stolen from https://gis.stackexchange.com/questions/208430/trying-to-extract-a-list-of-unique-values-from-a-field-using-python
def unique_values(table, field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({str(row[0]) for row in cursor})


