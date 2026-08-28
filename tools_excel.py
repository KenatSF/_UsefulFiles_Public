
import os
import pandas as pd

######################################              Create dataFrames

def create_xlsx_file(path, df, file_name):
    try:
        if len(df) < 1:
            print("Tabla {} (nula/sin elementos) NO creada!".format(file_name))
        else:
            # Specify the file name and path
            os.chdir(path)

            # Create an ExcelWriter object
            writer = pd.ExcelWriter(file_name + ".xlsx", engine='xlsxwriter')

            # Write the DataFrame to the Excel file
            df.to_excel(writer, sheet_name='Sheet1', index=False)

            # Get the xlsxwriter workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']

            n = len(df.columns.tolist())

            for i in range(n):
                # Set the column width to 25
                worksheet.set_column(0, i, 25)  # [^1^][1]

            # Save and close the Excel file
            writer.close()

            print("File created!: {}".format(file_name + ".xlsx"))
    except:
        print("Hubo un error al crear la tabla con nombre: {}".format(file_name))



def create_xlsx_table(path, df, file_name, sheet_name_in='Sheet1'):
    try:
        if len(df) < 1:
            print("Tabla {} (nula/sin elementos) NO creada!".format(file_name))
        else:
            os.chdir(path)

            # Create a Pandas Excel writer using XlsxWriter as the engine.
            writer = pd.ExcelWriter(file_name + ".xlsx", engine="xlsxwriter")

            # Write the dataframe data to XlsxWriter. Turn off the default header and
            # index and skip one row to allow us to insert a user defined header.
            df.to_excel(writer, sheet_name=sheet_name_in, startrow=1, header=False, index=False)

            # Get the xlsxwriter workbook and worksheet objects.
            workbook = writer.book
            worksheet = writer.sheets[sheet_name_in]

            # Get the dimensions of the dataframe.
            (max_row, max_col) = df.shape

            # Create a list of column headers, to use in add_table().
            column_settings = [{"header": column} for column in df.columns]

            # Add the Excel table structure. Pandas will add the data.
            worksheet.add_table(0, 0, max_row, max_col - 1, {"columns": column_settings})

            # Make the columns wider for clarity.
            worksheet.set_column(0, max_col - 1, 12)

            # Close the Pandas Excel writer and output the Excel file.
            writer.close()

            print("Table created!: {}".format(file_name + ".xlsx"))
    except Exception as e:
        print("Hubo un error al crear la tabla con nombre: {}".format(file_name))
        print(e)



def create_xlsx_table_personalized(path, df, file_name, color_columns):
    try:
        if len(df) < 1:
            print("Tabla {} (nula/sin elementos) NO creada!".format(file_name))
        else:
            os.chdir(path)

            # Create a Pandas Excel writer using XlsxWriter as the engine.
            writer = pd.ExcelWriter(file_name + ".xlsx", engine="xlsxwriter")

            # Write the dataframe data to XlsxWriter. Turn off the default header and
            # index and skip one row to allow us to insert a user defined header.
            df.to_excel(writer, sheet_name="Sheet1", startrow=1, header=False, index=False)

            # Get the xlsxwriter workbook and worksheet objects.
            workbook = writer.book
            worksheet = writer.sheets["Sheet1"]

            # Get the dimensions of the dataframe.
            (max_row, max_col) = df.shape

            # Create a list of column headers, to use in add_table().
            column_settings = [{"header": column} for column in df.columns]

            # Add the Excel table structure. Pandas will add the data.
            worksheet.add_table(0, 0, max_row, max_col - 1, {"columns": column_settings})

            # Make the columns wider for clarity.
            worksheet.set_column(0, max_col - 1, 12)

        ####################        New code            |           _Mucho código por mejorar
            d = {
                'bold': True,
                'text_wrap': True,
                'align': 'vcenter',
                'valign': 'center',
                'fg_color': color_columns,
                'border': 1
            }
            for i, col in enumerate(df.columns.values):
                header_format = workbook.add_format(d)
                worksheet.write(0, i, col, header_format)

            # Autofit the columns
            for i, col in enumerate(df.columns.values):
                # Get the max length of the column
                max_len = max(df[col].astype(str).map(len).max(), len(col)) + 6
                # Set the column width
                worksheet.set_column(i, i, max_len)

            # Close the Pandas Excel writer and output the Excel file.
            writer.close()

            print("Table created!: {}".format(file_name + ".xlsx"))
    except:
        print("Hubo un error al crear la tabla con nombre: {}".format(file_name))




def create_xlsx_multiple_tables(path, dfs, n_space_between_tables, sheet_name, file_name):
    try:
        with pd.ExcelWriter(path + file_name + '.xlsx', engine='xlsxwriter') as writer:
            workbook = writer.book
            worksheet = workbook.add_worksheet(sheet_name)
            writer.sheets[sheet_name] = worksheet

            current_row = n_space_between_tables

            for i, df in enumerate(dfs):
                # Write DataFrame headers and data
                df.to_excel(writer, sheet_name=sheet_name, startrow=current_row, startcol=0, index=False, header=True)

                # Define table range
                rows, cols = df.shape
                col_letters = [chr(65 + j) for j in range(cols)]  # A, B, C...
                table_range = f"A{current_row + 1}:{col_letters[-1]}{current_row + rows}"

                # Add Excel table
                worksheet.add_table(table_range, {
                    'columns': [{'header': col} for col in df.columns],
                    'name': f'Table_{i + 1}',
                    'style': 'Table Style Medium 9'
                })

                current_row += rows + n_space_between_tables  # Move down for next table
        print("Table created!: {}".format(file_name + ".xlsx"))
    except:
        print("Hubo un error al crear la tabla con nombre: {}".format(file_name))
    return 0

##############################################          Load dataframes


def modify_table_all_new_version(df, row_columns, columns_index=0, n_up=0, n_down=0):
    if row_columns is True:
        pre_columns = list(df.iloc[columns_index])
        df.columns = pre_columns

        df = df.tail((len(df) - n_up))
        df = df.head((len(df) - n_down))
        df = df.reset_index()
        df = df.drop(['index'], axis=1)
    else:
        df = df.tail((len(df) - n_up))
        df = df.head((len(df) - n_down))

    return df


def get_database_from_excel_basic_format(path, file_name):
    return pd.read_excel(path + file_name + ".xlsx", dtype=str)

def get_database_from_excel_basic_format_by_sheet(path, file_name, sheet_name):
    return pd.read_excel(path + file_name + ".xlsx", dtype=str, sheet_name=sheet_name)

def get_database_from_excel_asociados_format(path, file_name, n_up=1, n_down=0):
    #   Most of the databases have the first file empty and the last one with no sums at all, so:
    #   Note: If there is a goodd format use only pd.read_excel()
    file_name = file_name.replace(".xlsx", "")
    df = pd.read_excel(path + file_name + ".xlsx", dtype=str)
    df = modify_table_all_new_version(df, True, columns_index=0, n_up=1, n_down=0)
    return df







