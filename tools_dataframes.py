import pandas as pd
import tools_excel
import numpy as np

##########################################################              Paths and Files
def get_a_correct_path(path):
    # Para un correcto uso usar get_a_correct_path(r"path")
    path_b = str(path).replace("\\", "/")
    last_character = list(path)
    if last_character[(len(last_character) - 1)] != "/":
        return path_b + "/"

    return path_b


##########################################################              Columns Format





##########################################################              More Functions

def get_specific_row_df_from_a_condition_in_a_column(df, column_name, condition):
    return df.loc[df.loc[:, column_name] == condition, ]

def get_specific_row_array_from_a_condition_in_a_column(df, column_name, condition):
    return df.loc[df.loc[:, column_name] == condition, ].values[0]

def get_specific_value_from_a_condition_in_a_column(df, column_name, condition, column_value):
    return df.loc[df.loc[:, column_name] == condition, [column_value]].values[0]

def get_specific_value_from_a_condition_in_a_column_improved(df, column_name, condition, column_value):
    return df.loc[df.loc[:, column_name] == condition, [column_value]].values[0][0]


################################################################3                   Nuevas funciones
def fill_df_with_df_values(df_to_fill, df_data, key_column_both, df_to_fill_column, df_data_column):

    df_intersection = pd.merge(df_to_fill, df_data, on=key_column_both, how='inner')
    array_index = df_intersection[key_column_both]

    for i in array_index:
        valor = get_specific_value_from_a_condition_in_a_column(df_data,
                                                                                 key_column_both,
                                                                                 i,
                                                                                 df_data_column)
        df_to_fill.loc[df_to_fill[key_column_both] == i, [df_to_fill_column]] = valor

    return df_to_fill



def fill_df_with_df_multiple_columns_values(df_to_fill, df_data, key_column_both, df_to_fill_column, df_array_columns):

    df_intersection = pd.merge(df_to_fill, df_data, on=key_column_both, how='inner')
    array_index = df_intersection[key_column_both]

    for i in array_index:
        for j in df_array_columns:
            valor = get_specific_value_from_a_condition_in_a_column(df_data,
                                                                    key_column_both,
                                                                    i,
                                                                    j)
            df_to_fill.loc[df_to_fill[key_column_both] == i, [df_to_fill_column]] = valor

    return df_to_fill



def df_split_by_groups_of_rows(df, n_groups, directory_to_save_new_dfs, main_df_name):
    n = len(df)
    k = int(n/n_groups)

    for i in range(k):
        inicio = i * n_groups
        fin = (i + 1) * n_groups
        sub_df = df.iloc[inicio:fin]
        sub_df_name = main_df_name + "_" + str(i)

        tools_excel.create_xlsx_table(directory_to_save_new_dfs, sub_df, sub_df_name)

    if n % n_groups != 0:
        inicio = k * n_groups
        sub_df = df.iloc[inicio:]
        sub_df_name = main_df_name + "_" + str(k)

        tools_excel.create_xlsx_table(directory_to_save_new_dfs, sub_df, sub_df_name)




def get_function_from_columns(df, key_column, array_columns):
    ########################################       ->  9.- Obtener el Min de las comisiones en la Plantilla
    ##            Nota: Si n_NAs <= 2 Entonces es COMISIONES, en cualquier otro caso es ADELANTO
    ##                  En este caso ese trabajador tiene dos registros, es decir, su RFC se repite.
    df_format = df[array_columns]
    df_format = df_format.T
    df_format = df_format.rename_axis(key_column, axis=1)
    pre_columns = list(df_format.iloc[0])
    df_format = df_format.tail(len(df_format) - 1)
    df_format.columns = pre_columns
    df_format = df_format.replace(0, np.nan)

    rfc_lista = []
    na_amount = []

    for i in pre_columns:
        df_format[i] = df_format[i].astype(str)
        df_format[i] = df_format[i].replace('0', np.nan)
        df_format[i] = df_format[i].astype(float)
        rfc_lista.append(df_format[i].min(skipna=True))
        na_amount.append(df_format[i].isna().sum())

    new_row = pd.Series(rfc_lista, index=df_format.columns.tolist())
    new_row_1 = pd.Series(na_amount, index=df_format.columns.tolist())
    df_format = df_format._append(new_row, ignore_index=True)
    df_format = df_format._append(new_row_1, ignore_index=True)

    df_format = df_format.T
    df_format = df_format.reset_index().rename(columns={"index": "RFC"})

    #df_format.columns = ['RFC', 'QNA02', 'QNA04', 'QNA06', 'QNA08', 'QNA10', 'FINAL', 'n_NAs']
    #df_plantilla_new_format.columns = ['RFC', 'QNA02', 'QNA04', 'QNA06', 'QNA08', 'QNA10', 'FINAL']
    return df_format