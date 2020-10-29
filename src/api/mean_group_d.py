import os, sys
import pandas as pd 
import json 

# ----------------------
# $$$$$$$ MEAN OF TOTAL DEATHS $$$$$$$$
# ----------------------

def t_d_mean (url, countries):
    """ Obtiene la media de muertes diarias (total_deaths) de los países del grupo pasado como argumento a la función.

    Argumentos:
        url: la url de donde se extraerá la información (formato csv)
        countries: La lista de códigos de países del grupo (iso_code) de los cuales se desea obtener la media del total de muertes (total_deaths)
    Retorna:
        Json: Un diccionario con una clave denominada "t_d_averages" que contiene a su vez un diccionario cuya clave es las fecha 
         y el valor la media de total de muertes para ese día
        
    """
    covid_general = pd.read_csv(url, sep=",")
    covid_grupoD=covid_general[covid_general.iso_code.isin(countries)]
    covid_grupoD.set_index(["date"],inplace=True)
    covid_no_NaN = covid_grupoD.copy()
    covid_no_NaN.dropna(subset=["total_deaths"],axis=0, inplace=True)
    final_covid_D = covid_no_NaN.groupby("date").mean().total_deaths.to_frame()
    final_covid_D["total_deaths"] = round(final_covid_D["total_deaths"],2)
    final_covid_D.rename(columns={"total_deaths":"t_d_averages"},inplace=True)
    json_d = final_covid_D.to_json()
    return json_d

