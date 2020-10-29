import pandas as pd



def world(df):
    
    """ DF Mundial sin los datos globales (continent is Nan) o de países Nan y con la fecha en formato datetime"""
    
    df = df[~((df.continent.isnull()) | (df.iso_code.isnull()))]
    df["date"]=pd.to_datetime(df["date"],format="%Y-%m-%d")
    if len (df[df["date"] == df["date"].max()].index)< len (df.groupby('iso_code')['date'].max()):
        df.drop(df[df["date"] == df["date"].max()].index, axis =0, inplace = True)
    return df
 
 
def crear_rank(df):
    
    """
    Agrega las columnas correspondientes al ranking diario por países considerando 
    número de casos totales (i.e. Total Infected), número de muertes (i.e. Total Deaths), número de casos totales por millon 
    de hab.(i.e. total_cases_per_million) y el número de muertes totales por millon de hab (i.e. total_deaths_per_million)
    Agrega el  Ratio de mortalidad por pais considerando total_deaths / total_cases
    """
    
    df["rank_TC"] = df.groupby(["date"])["total_cases"].rank(method = "dense", ascending = False)
    df["rank_TD"] = df.groupby(["date"])["total_deaths"].rank(method = "dense", ascending = False)
    df["rank_TCxM"] = df.groupby(["date"])["total_cases_per_million"].rank(method = "dense", ascending = False)
    df["rank_TDxM"] = df.groupby(["date"])["total_deaths_per_million"].rank(method = "dense", ascending = False)
    df["mortality_rate"] = round((df['total_deaths']/df['total_cases'])*100, 2)
    return df

def crear_df_grupo (df, paises):
    
    """ Crea el DF con los datos de los países indicados en la lista 
        Si hay algun país que no ha reportado casos para la última fecha elimina los registros del último día para todos los 
        países (de manera que los datos sean consistentes para el análisis)
    """
    
    df = df[df.iso_code.isin(paises)]
    if len (df[df["date"] == df["date"].max()].index)< len (paises):
        df.drop(df[df["date"] == df["date"].max()].index, axis =0, inplace = True)
    return df

def limpiar_grupo(df, col):
    
    """ Elimina del DF las filas sin información relevante del COVID19 y las columnas indicadas que no aportan información """
    
    df.drop(df[(df["new_cases"]==0) & (df["total_cases"] ==0)].index)
    df.drop(columns=[col], axis = 1, inplace=True)
    df.reset_index(inplace=True)
    return df

def crear_sidx_df (df):
    
    """ Retorna un DF con el Stringency Index promedio mensual por país """
    
    df = df[(df.stringency_index>0)]
    df = df.groupby([df.date.dt.month, "iso_code"]).stringency_index.mean().to_frame()
    df.reset_index(inplace=True)
    df['date'] = pd.to_datetime('2020-' + df.date.astype(int).astype(str) + '-1', format = '%Y-%m')
    return df
