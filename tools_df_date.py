import datetime
import pandas as pd
import datetime as dt


#########################################################           single functions
def get_date_string_value(the_date):
    the_date = the_date.split("-")
    fecha_a_filtrar = datetime.date(int(the_date[0]), int(the_date[1]), int(the_date[2]))

    return fecha_a_filtrar

def get_datetime_string_value(the_date):
    the_date = the_date.split("-")
    fecha_a_filtrar = datetime.datetime(int(the_date[0]), int(the_date[1]), int(the_date[2]),
                                        0, 0, 0)

    return fecha_a_filtrar


def get_is_old_enough_by_days(date_str, n_days):
    date_object = dt.datetime.strptime(date_str, "%d/%m/%Y").date()
    fecha_a_filtrar = dt.date.today() - dt.timedelta(days=n_days)

    if date_object <= fecha_a_filtrar:
        return True
    else:
        return False


#########################################################           Otras functions (Get specific days)
def get_first_today_final_month():
    now = dt.date.today()
    first_day = datetime.date(now.year, now.month, 1)
    next_month = now.replace(day=28) + datetime.timedelta(days=4)
    next_month = next_month - datetime.timedelta(days=next_month.day)

    return str(first_day), str(now), str(next_month)

def get_first_and_last_day_from_entrance(date_entrance):
    #####           Format filters must be added to avoid errors
    year = str(date_entrance).split("-")[0]
    month = str(date_entrance).split("-")[1]

    first_day = datetime.date(int(year), int(month), 1)
    last_day = datetime.date(int(year), int(month), 28) + datetime.timedelta(days=4)
    last_day = last_day - datetime.timedelta(days=last_day.day)

    return str(first_day), str(last_day)

def get_first_today_final__last_month():
    now = dt.date.today()

    last_day_last_month = datetime.date(now.year, now.month, 1) - datetime.timedelta(days=1)
    first_day_last_month = last_day_last_month.replace(day=1)


    return str(first_day_last_month), str(now), str(last_day_last_month)

def get_date_plus_n_days(date_entrance, n_days):
    year = str(date_entrance).split("-")[0]
    month = str(date_entrance).split("-")[1]
    day = str(date_entrance).split("-")[2]

    today = datetime.date(int(year), int(month), int(day))

    return str(today + datetime.timedelta(days=int(n_days)))

def get_date_minus_n_days(date_entrance, n_days):
    year = str(date_entrance).split("-")[0]
    month = str(date_entrance).split("-")[1]
    day = str(date_entrance).split("-")[2]

    today = datetime.date(int(year), int(month), int(day))

    return str(today + datetime.timedelta(days=int(n_days) * (-1)))



#########################################################           DF functions



def filtering_by_n_days(df, date_column, operation_type, n_days=0, date_format="mixed"):
    df["date"] = pd.to_datetime(df[date_column], format=date_format)
    fecha_a_filtrar = dt.date.today() - dt.timedelta(days=n_days)
    ##  Nota: Sí n_days = 0; Entonces significa a la fecha actual.
    ##          O también, si no estableces los días. Lo deja como Fecha Actual.
    print("Dentro de def filtered_by_last_n_days():----------> FECHA: {}".format(fecha_a_filtrar))
    if operation_type == "<":       # Menor que
        df = df[df["date"].dt.date < fecha_a_filtrar]
    elif operation_type == "=":
        df = df[df["date"].dt.date == fecha_a_filtrar]
    elif operation_type == ">":     # Mayor que
        df = df[df["date"].dt.date > fecha_a_filtrar]
    else:
        return None

    df[date_column] = df['date'].dt.strftime("%d/%m/%Y")
    df = df.drop(['date'], axis=1)
    return df


def filtered_by_string_date(df, date_column, operation_type, the_date, date_format="mixed"):
    #       Nota: the_date Debe tener el siguiente formato: Year-Month-Day
    df["date"] = pd.to_datetime(df[date_column], format=date_format)
    fecha_a_filtrar = get_date_string_value(the_date)

    print("Dentro de def filtered_by_string_date():----------> FECHA: {}".format(fecha_a_filtrar))
    if operation_type == "MENOR":       # Menor que
        df = df[df["date"].dt.date < fecha_a_filtrar]
    elif operation_type == "IGUAL":
        df = df[df["date"].dt.date == fecha_a_filtrar]
    elif operation_type == "MAYOR":     # Mayor que
        df = df[df["date"].dt.date > fecha_a_filtrar]
    else:
        return None

    df[date_column] = df['date'].dt.strftime("%d/%m/%Y")
    df = df.drop(['date'], axis=1)
    return df

def filtereing_by_string_date_improved(df, date_column, operation_type, the_date, date_format="mixed"):
    #       Nota: the_date Debe tener el siguiente formato: Year-Month-Day
    df["date"] = pd.to_datetime(df[date_column], format=date_format)
    fecha_a_filtrar = get_date_string_value(the_date)

    if operation_type == "MENOR":       # Menor que
        print("Dentro de def filtered_by_string_date():----------> FECHA MENOR A || < : {}".format(fecha_a_filtrar))
        df = df[df["date"].dt.date < fecha_a_filtrar]
    elif operation_type == "MENOR O IGUAL":
        print("Dentro de def filtered_by_string_date():----------> FECHA MENOR O IGUAL A || <= : {}".format(fecha_a_filtrar))
        df = df[df["date"].dt.date <= fecha_a_filtrar]
    elif operation_type == "IGUAL":
        print("Dentro de def filtered_by_string_date():----------> FECHA IGUAL A || = : {}".format(fecha_a_filtrar))
        df = df[df["date"].dt.date == fecha_a_filtrar]
    elif operation_type == "MAYOR":
        print("Dentro de def filtered_by_string_date():----------> FECHA MAYOR A || > : {}".format(fecha_a_filtrar))
        df = df[df["date"].dt.date > fecha_a_filtrar]
    elif operation_type == "MAYOR O IGUAL":
        print("Dentro de def filtered_by_string_date():----------> FECHA MAYOR O IGUAL A || >= : {}".format(fecha_a_filtrar))
        df = df[df["date"].dt.date >= fecha_a_filtrar]
    else:
        return None

    df = df.drop(['date'], axis=1)
    return df

def filtered_by_string_date_add_and_substract_days(df, date_column, operation_type, the_date,
                                                   plus_days=0, minus_days=0, date_format="mixed"):
    #       Nota: the_date Debe tener el siguiente fomrato: Year-Month-Day
    df["date"] = pd.to_datetime(df[date_column], format=date_format)
    fecha_a_filtrar = get_date_string_value(the_date)
    fecha_a_filtrar = fecha_a_filtrar + dt.timedelta(days=plus_days)
    fecha_a_filtrar = fecha_a_filtrar - dt.timedelta(days=minus_days)

    print("Dentro de def filtered_by_string_date():----------> FECHA: {}".format(fecha_a_filtrar))
    if operation_type == "MENOR":       # Menor que
        df = df[df["date"].dt.date < fecha_a_filtrar]
    elif operation_type == "IGUAL":
        df = df[df["date"].dt.date == fecha_a_filtrar]
    elif operation_type == "MAYOR":     # Mayor que
        df = df[df["date"].dt.date > fecha_a_filtrar]
    else:
        return None

    df[date_column] = df['date'].dt.strftime("%d/%m/%Y")
    df = df.drop(['date'], axis=1)
    return df

def filterering_by_string_date_add_and_substract_days_improved(df, date_column, operation_type, the_date,
                                                   plus_days=0, minus_days=0, date_format="mixed"):
    #       Nota: the_date Debe tener el siguiente fomrato: Year-Month-Day
    df["date"] = pd.to_datetime(df[date_column], format=date_format)
    fecha_a_filtrar = get_date_string_value(the_date)
    fecha_a_filtrar = fecha_a_filtrar + dt.timedelta(days=plus_days)
    fecha_a_filtrar = fecha_a_filtrar - dt.timedelta(days=minus_days)

    print("Dentro de def filtered_by_string_date():----------> FECHA: {}".format(fecha_a_filtrar))
    if operation_type == "MENOR":       # Menor que
        df = df[df["date"].dt.date < fecha_a_filtrar]
    elif operation_type == "IGUAL":
        df = df[df["date"].dt.date == fecha_a_filtrar]
    elif operation_type == "MAYOR":     # Mayor que
        df = df[df["date"].dt.date > fecha_a_filtrar]
    else:
        return None

    df = df.drop(['date'], axis=1)
    return df


def get_number_of_days_by_string_date(df, date_column, the_date, new_column_name, date_format="mixed"):
    #       Nota: the_date Debe tener el siguiente fomrato: Year-Month-Day
    df["date"] = pd.to_datetime(df[date_column], format=date_format)
    fecha_a_filtrar = get_date_string_value(the_date)
    fecha_a_filtrar = pd.to_datetime(fecha_a_filtrar)

    df[new_column_name] = fecha_a_filtrar - df['date']
    df[new_column_name] = df[new_column_name].apply(lambda x: str(x).split(" ")[0])

    df[date_column] = df['date'].dt.strftime("%Y/%m/%d")
    df = df.drop(['date'], axis=1)
    return df


def get_index_date_by_year_and_month(df, column_to_use, format_column_to_use):


    df['INDEX_DATE'] = pd.to_datetime(df[column_to_use], format=format_column_to_use)
    df['INDEX_YEAR'] = df['INDEX_DATE'].dt.strftime("%Y")
    df['INDEX_DATE'] = pd.to_datetime(df[column_to_use], format=format_column_to_use)
    df['INDEX_MONTH'] = df['INDEX_DATE'].dt.strftime("%b")

    df['INDEX_DATE'] = pd.to_datetime(df[column_to_use], format=format_column_to_use)

    df['INDEX_DATE'] = df['INDEX_DATE'].dt.strftime("%Y %b")

    return df

def get_index_date_by_year_and_month_hope(df, column_to_use, format_column_to_use):


    df['INDEX_DATE'] = pd.to_datetime(df[column_to_use], format=format_column_to_use)
    df['INDEX_YEAR'] = df['INDEX_DATE'].dt.strftime("%Y")
    df['INDEX_DATE'] = pd.to_datetime(df[column_to_use], format=format_column_to_use)
    df['INDEX_MONTH'] = df['INDEX_DATE'].dt.strftime("%b")

    df['INDEX_DATE'] = pd.to_datetime(df[column_to_use], format=format_column_to_use)
    df['INDEX_DATE'] = df['INDEX_DATE'] + pd.offsets.MonthEnd(0)

    df['INDEX_DATE'] = df['INDEX_DATE'].dt.strftime("%d/%m/%Y")

    return df



def get_dict_meses():
    return {'JANUARY': 'ENERO', 'FEBRUARY': 'FEBRERO', 'MARCH': 'MARZO', 'APRIL': 'ABRIL', 'MAY': 'MAYO', 'JUNE': 'JUNIO', 'JULY': 'JULIO', 'AUGUST': 'AGOSTO', 'SEPTEMBER': 'SEPTIEMBRE', 'OCTOBER': 'OCTUBRE', 'NOVEMBER': 'NOVIEMBRE', 'DECEMBER': 'DICIEMBRE'}

def get_dict_months():
    return {'ENERO': 'JANUARY', 'FEBRERO': 'FEBRUARY', 'MARZO': 'MARCH', 'ABRIL': 'APRIL', 'MAYO': 'MAY', 'JUNIO': 'JUNE', 'JULIO': 'JULY', 'AGOSTO': 'AUGUST', 'SEPTIEMBRE': 'SEPTEMBER', 'OCTUBRE': 'OCTOBER', 'NOVIEMBRE': 'NOVEMBER', 'DICIEMBRE': 'DECEMBER'}

def get_dict_months_formato_three_letters():
    return { "ENE": "Jan", "FEB": "Feb", "MAR": "Mar", "ABR": "Apr", "MAY": "May", "JUN": "Jun", "JUL": "Jul", "AGO": "Aug", "SEP": "Sep", "OCT": "Oct", "NOV": "Nov", "DIC": "Dec" }
def get_dict_numbers_numbers():
    return {'JANUARY': '01', 'FEBRUARY': '02', 'MARCH': '03', 'APRIL': '04', 'MAY': '05', 'JUNE': '06', 'JULY': '07', 'AUGUST': '08', 'SEPTEMBER': '09', 'OCTOBER': '10', 'NOVEMBER': '11', 'DECEMBER': '12'}

def get_dict_numbers_months():
    return {'01': 'JANUARY', '02': 'FEBRUARY', '03': 'MARCH', '04': 'APRIL', '05': 'MAY', '06': 'JUNE', '07': 'JULY', '08': 'AUGUST', '09': 'SEPTEMBER', '10': 'OCTOBER', '11': 'NOVEMBER', '12': 'DECEMBER'}


####        Rango mes a
def rango_mes_fin():
    ## Crear una serie de fechas con el final de cada mes
    finales = pd.date_range(start="2022-01-31", end="2030-12-31", freq="M")
    finales = list(finales)
    finales_cierre = pd.date_range(start="2022-01-31", end="2030-12-31", freq="M") + pd.DateOffset(days=6)
    finales_cierre = list(finales_cierre)


    # Unir las dos series de fechas en una sola columna
    columna_fin_mes = finales
    columna_cierre_mes = finales_cierre

    df_fin_mes = pd.DataFrame(data={'FECHA_VENCIMIENTO': columna_fin_mes, 'FECHA_CIERRE': columna_cierre_mes})
    df_fin_mes = df_fin_mes.sort_values(by='FECHA_VENCIMIENTO')



    df_fin_mes['FECHA_VENCIMIENTO'] = pd.to_datetime(df_fin_mes['FECHA_VENCIMIENTO'], format="%Y-%m-%d %H:%M:%S")
    df_fin_mes['FECHA_VENCIMIENTO'] = df_fin_mes['FECHA_VENCIMIENTO'].dt.strftime("%Y/%m/%d")
    df_fin_mes['FECHA_CIERRE'] = pd.to_datetime(df_fin_mes['FECHA_CIERRE'], format="%Y-%m-%d %H:%M:%S")
    df_fin_mes['FECHA_CIERRE'] = df_fin_mes['FECHA_CIERRE'].dt.strftime("%Y/%m/%d")
    df_fin_mes.drop_duplicates(subset=['FECHA_VENCIMIENTO'], keep='first', inplace=True)


    df_fin_mes.reset_index(inplace=True)
    df_fin_mes.drop(columns=['index'], inplace=True)
    df_fin_mes.reset_index(inplace=True)



    df_fin_mes['index'] = df_fin_mes['index'] + 1


    return df_fin_mes

###     Rango mes b (Complemento)
def select_row_date_to_filter(date_to_filter):
    df_mes = rango_mes_fin()
    df_mes['FECHA_VENCIMIENTO'] = pd.to_datetime(df_mes['FECHA_VENCIMIENTO'], format="%Y/%m/%d")
    df_mes = filtereing_by_string_date_improved(df_mes,
                                                'FECHA_VENCIMIENTO',
                                                'MENOR O IGUAL',
                                                date_to_filter,
                                                date_format="%Y/%m/%d")
    df_mes['FECHA_VENCIMIENTO'] = df_mes['FECHA_VENCIMIENTO'].dt.strftime("%Y/%m/%d")

    df_mes = df_mes[['index', 'FECHA_VENCIMIENTO']]

    return df_mes

