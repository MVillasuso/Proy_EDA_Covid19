import os, sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly
import plotly.graph_objs as go
import plotly.express as px 
import plotly.io as pio
import folders_tb as ftb

def graf_grupo (x_val, y_val, hue_val, df, inv_y): 

    """ Crea un gráfico ESTÁTICO (de todos los países del grupo) con el valor de una columna de datos en un gráfico de líneas
        Guarda el gráfico (.png) en el directorio TOT_D """

    g = sns.relplot(x =x_val, y = y_val, hue = hue_val, kind = "line", data = df, palette = "Paired")
    g._legend.texts[0].set_text("")
    g._legend.set_title("Country")
    plt.xticks(rotation = "vertical")
    tit = y_val.replace("_"," ").title() + " by Date and Country - Group D"
    plt.title(tit)

    file_name = y_val+ "_x_C_D" +  ".png"
    ftb.salvar_plot ( "../resources/plots/TOT_D/", file_name)

    if inv_y:
        plt.gca().invert_yaxis()
    plt.show()

def grafI_grupo (x_val, y_val, hue_val, df, inv_y): 

    """ Crea un gráfico INTERACTIVO (de todos los paises del grupo) con el valor de una columna de datos en un gráfico de líneas
        Guarda el gráfico (.html) en el directorio TOT_D"""

    tit = y_val.replace("_"," ").title() + " by Date and Country - Group D"
    fig = px.line(df, x=x_val, y=y_val, color=hue_val, line_group=hue_val, hover_name=hue_val,
        line_shape="spline", render_mode="svg")
    fig.update_layout(     
            title = {"text" : tit, "x":0.5, "xanchor":"center"}, 
            xaxis_title = x_val.title(),
            yaxis_title = y_val.replace("_"," ").title(),
            legend=dict(title= "Country", y=0.5, font_size=12)
                    )
    file_name = y_val+ "_x_C_D"
    ftb.salvarI_plot(fig,"../resources/plots/TOT_D/", file_name)
    fig.show()

def graf_pais (ccode,col_dat, cname,cdf, y_maximo, adf):

    """ Crea un gráfico estático por cada columna de datos indicada (col_dat)
        Muestra con líneas verticales las fechas del estado de alarma del país
        Guarda cada gráfico (png) en un directorio con el nombre del país indicado en iso_code
    """

    if y_maximo:
        eje_y = cdf.total_cases.max()
        tit =  " Covid19  Totals - " + cname.title()
        filen= "Tot_"
    else:
        eje_y = cdf.rank_TCxM.max()
        tit =  " COVID19  Ranking - " + cname.title()
        filen= "Rank_"
    fg = cdf.plot(x="date", y= col_dat, kind="line", figsize=(12,8))
    fg.set_title(tit, fontsize=20)
    fg.legend(bbox_to_anchor=(1.3, 0.5))
    plt.vlines(adf.alarm_init[adf.iso_code == ccode].to_frame().iloc[0,0], ymin=0, ymax=eje_y, color = "r", linestyles =":")
    plt.vlines(adf.alarm_end[adf.iso_code == ccode].to_frame().iloc[0,0], ymin=0, ymax=eje_y, color = "r", linestyles =":")
    filen=filen+ ccode+".png"
    dirn = "../resources/plots/"+ ccode+ "/"
    ftb.salvar_plot(dirn, filen)
    plt.show()


def grafI_pais (ccode,col_dat, cname,cdf, y_maximo,adf):

    """ Crea un gráfico dinámico por cada columna de datos indicada (col_dat)
        Muestra con líneas verticales las fechas del estado de alarma del país
        Guarda cada gráfico (html) en un directorio con el nombre del país indicado en ccode
    """

    if y_maximo:
        eje_y = cdf.total_cases.max()
        tit =  " Covid19  Totals - " + cname.title()
        filen= "Tot_"
    else:
        eje_y = cdf.rank_TCxM.max()
        tit =  " COVID19  Ranking - " + cname.title()
        filen= "Rank_"

    fig = px.line(cdf, x="date", y=col_dat, line_shape="spline", render_mode="svg")

    fig.add_annotation(x=adf.alarm_init[adf.iso_code==ccode].fillna("01-03-2020").values[0], y=eje_y, text="start alarm")
       
    fig.add_annotation(x=adf.alarm_end[adf.iso_code==ccode].fillna("31-12-2020").values[0], y=eje_y, text="end alarm")
    fig.update_annotations(dict(xref="x", yref="y", showarrow=True, arrowhead=7, ax=-20, ay=20))

    fig.update_layout(     
            title = {"text" : tit, "x":0.4, "xanchor":"center"}, 
            xaxis_title = "Date",
            yaxis_title = "Totals",
            legend=dict(title= " ", y=0.5, font_size=12)
                    )
    fig.add_shape(
        dict(
        type= "line",
        x0 = adf.alarm_init[adf.iso_code==ccode].fillna("01-03-2020").values[0],
        y0 = 0,
        x1 = adf.alarm_init[adf.iso_code==ccode].fillna("01-03-2020").values[0],
        y1 = eje_y, 
        line  = dict (color = "Purple", width = 2, dash = "dot")
        ))
    fig.add_shape(
        dict(
        type= "line",
        x0 = adf.alarm_end[adf.iso_code==ccode].fillna("31-12-2020").values[0],
        y0 = 0,
        x1 = adf.alarm_end[adf.iso_code==ccode].fillna("31-12-2020").values[0],
        y1 = eje_y, 
        line  = dict (color = "Purple", width = 2, dash = "dot")
        ))

    filen=filen+ ccode
    dirn = "../resources/plots/"+ ccode+ "/"
    ftb.salvarI_plot(fig, dirn, filen)
    fig.show()

def graf_daily(n1,c1,n2,c2,ccode,df, cname,adf):

    """ Crea un gráfico dinámico con la información diaria (casos y muertes) 
        Muestra con líneas verticales las fechas del estado de alarma del país
        Guarda el gráfico (html) en un directorio con el nombre del país indicado en ccode
    """

    fig = go.Figure(data=[
        go.Bar(name= n1, x=df['date'], y=df[c1]),
        go.Bar(name= n2, x=df['date'], y=df[c2])])

    fig.add_annotation(x=adf.alarm_init[adf.iso_code==ccode].fillna("01-03-2020").values[0], y=df[c1].max(), text="start alarm")
       
    fig.add_annotation(x=adf.alarm_end[adf.iso_code==ccode].fillna("31-12-2020").values[0], y=df[c1].max(), text="end alarm")
    fig.update_annotations(dict(xref="x", yref="y", showarrow=True, arrowhead=7, ax=-20, ay=20))    
    fig.update_layout(
                    barmode='overlay', 
                    title={ "text":"Covid19  Daily Cases and Daily Deaths - " + cname.title(), "x":0.42, "xanchor": "center"},
                    xaxis_title = "Date",
                    yaxis_title = "Totals",
                    legend=dict(title= " ", y=0.5, font_size=12)
                    )
    fig.add_shape(
        dict(
        type= "line",
        x0 = adf.alarm_init[adf.iso_code==ccode].fillna("01-03-2020").values[0],
        y0 = 0,
        x1 = adf.alarm_init[adf.iso_code==ccode].fillna("01-03-2020").values[0],
        y1 = df[c1].max(),
        line  = dict (color = "Purple", width = 2, dash = "dot")
        ))
    fig.add_shape(
        dict(
        type= "line",
        x0 = adf.alarm_end[adf.iso_code==ccode].fillna("31-12-2020").values[0],
        y0 = 0,
        x1 = adf.alarm_end[adf.iso_code==ccode].fillna("31-12-2020").values[0],
        y1 = df[c1].max(),
        line  = dict (color = "Purple", width = 2, dash = "dot")
        ))

    filen="Daily_"+ ccode
    dirn = "../resources/plots/"+ ccode+ "/"
    ftb.salvarI_plot(fig, dirn, filen)
    fig.show()

def graf_dailyd(n2,c2,ccode,df, cname):

    """ Crea un gráfico dinámico con la información de muertes diarias 
        Muestra con líneas verticales las fechas en que las muertes crecen (rojo) o decrecen (verde)
        Guarda el gráfico (html) en un directorio con el nombre del país indicado en ccode
    """

    fig = go.Figure(data=[
        go.Bar(name= n2, x=df['date'], y=df[c2])])
    fig.update_layout(
                barmode='overlay', 
                title={ "text":"Covid19  Daily Deaths - " + cname.title(), "x":0.42, "xanchor": "center"},
                xaxis_title = "Date",
                yaxis_title = "Totals",
                legend=dict(title= " ", y=0.5, font_size=12)
                )
    if ccode == "ESP":
        df= df[(df.new_deaths > 0) & (df.date<"2020-05-24")]
    else:
        df = df[(df.new_deaths > 0)]
    fig.add_shape(
        dict(
        type= "line",
        x0 = df["date"][(df[c2] == df[c2].min())].max(),
        y0 = 0,
        x1 = df["date"][(df[c2] == df[c2].min())].max(),
        y1 = df[c2].max(),
        line  = dict (color = "Red", width = 3, dash = "dashdot")
    ))
    fig.add_shape(
        dict(
        type= "line",
        x0 = df["date"][(df[c2] == df[c2].max())].min(),
        y0 = 0,
        x1 = df["date"][(df[c2] == df[c2].max())].min(),
        y1 = df[c2].max(),
        line  = dict (color = "Green", width = 3, dash = "dashdot")
    ))
    filen="Deaths_"+ ccode
    dirn = "../resources/plots/"+ ccode+ "/"
    ftb.salvarI_plot(fig, dirn, filen)
    fig.show()

def grafI_area (df,xval,yval,colval,gval):

    """ Gráfico interactivo tipo area con la información por continente
        Guarda el gráfico (.html) en el directorio TOT_CONT """

    fig = px.area(df,x=xval,y=yval,color=colval,line_group=gval)
    fig.update_layout(
    title = {"text" :yval.replace("_", " ").title() + " per continent - Area Graph", "x":0.4, "xanchor": "center"},
    xaxis_title=xval.title(),
    yaxis_title= yval.replace("_", " ").title(),
    legend_title=colval.title(),
    font=dict(
        size=12))
    file_name = yval+ "_x_cont_area"
    ftb.salvarI_plot(fig,"../resources/plots/TOT_CONT/", file_name)
    fig.show()

def grafI_bar(df,xval,yval,col,mod, tit):

    """ Gráfico interactivo tipo barra con los países del grupo D 
        Guarda el gráfico (.html) en el directorio TOT_D """

    fig = px.bar(df,x = xval,y = yval , color= col, barmode= mod,color_discrete_sequence=["red","purple","blue","green","orange"])
    fig.update_layout(
        title = {"text" : tit, "x":0.5, "xanchor": "center"},
        xaxis_title=  xval.title(),
        yaxis_title= yval.replace("_", " ").title(),
        legend_title= " ",
        font=dict(
            size=12))
    file_name = yval+ "_gD_bar"
    ftb.salvarI_plot(fig,"../resources/plots/TOT_D/", file_name)
    fig.show()

def grafI_mm (df,wdf,col,mod,hov,sca):

    """ Gráfico interactivo tipo mapa mundi con las cifras de Casos o Muertes para todos los países 
        Guarda el gráfico (.html) en el directorio TOT_W """

    fig = px.choropleth(df, locations=wdf[hov],
                    color=df[col],locationmode=mod, 
                    hover_name=df[hov], 
                    color_continuous_scale=sca,
                    template='plotly_white')

    fig.update_layout(
        title = {"text" : col.replace("_", " ").title() + " per Country - World Map", "x":0.5, "xanchor": "center"},
        font=dict(
            size=12
        )
    )
    file_name = col+ "_World_map"
    ftb.salvarI_plot(fig,"../resources/plots/TOT_W/", file_name)
    fig.show()

def grafI_pie (df, col, val):

    """ Gráfico interactivo tipo pie con los principales países del mundo 
        Guarda el gráfico (.html) en el directorio TOT_W """

    df2= df[df.date==df.date.max()]
    df2.loc[(df2[col] < val), 'location'] = "Others"
    fig = px.pie(df2, values=col, names='location', title="WORLD "+ col.replace("_", " ").title() + " - Covid19")
    file_name = col+ "_World_pie"
    ftb.salvarI_plot(fig,"../resources/plots/TOT_W/", file_name)
    fig.show()

def grafI_pieD_O(df, col,paises):

    """ Gráfico interactivo tipo pie con los países del grupo D en contraste con el resto del mundo 
        Guarda el gráfico (.html) en el directorio TOT_D """

    df2 = df[df.date==df.date.max()]
    df2.loc[~df2["iso_code"].isin(paises), 'location'] = "Other countries"
    fig = px.pie(df2, values=col, names='location')
    fig.update_layout(     
            title = {"text" : "Group D and Others "+ col.replace("_"," ").title() + " - Covid19", "x": 0.7, "xanchor":"center"})
    file_name = col+ "_gDO_pie"
    ftb.salvarI_plot(fig,"../resources/plots/TOT_D/", file_name)    
    fig.show()

def grafI_pieD(df, col):

    """ Gráfico interactivo tipo pie con los países del grupo D 
        Guarda el gráfico (.html) en el directorio TOT_D """

    df2 = df[df.date==df.date.max()]
    fig = px.pie(df2, values= col, names='location', title=col.replace("_"," ").title() + " - Group D")
    file_name = col+ "_gD_pie"
    ftb.salvarI_plot(fig,"../resources/plots/TOT_D/", file_name)
    fig.show()


def graf_rank_D(datf):

    """ Crea un gráfico interactivo con la posición de los países del grupo D en el ranking mundial
        Guarda el gráfico (.html) en el directorio TOT_D """

    df = datf[datf.date==datf.date.max()]
    fig = go.Figure(data=[
        go.Bar(name='Total Cases', x=df['location'], y=df['rank_TC']),
        go.Bar(name='Total Deaths', x=df['location'], y=df['rank_TD']),
        go.Bar(name='Total Cases x million', x=df['location'], y=df['rank_TCxM']),
        go.Bar(name='Total Deaths x million', x=df['location'], y=df['rank_TDxM'])
        ])
    fig.update_layout(barmode='group', title='Group D Position World Ranking  - Covid19')
    file_name = "rank_gD_bar"
    ftb.salvarI_plot(fig,"../resources/plots/TOT_D/", file_name)
    fig.show()


def graf_outlD(datf, col):

    """ Gráfico de outliers 
        Guarda el gráfico (.png) en el directorio TOT_D """

    sns.set(style="ticks", palette="vlag")
    sns.boxplot(x="location", y=col,
                palette=["b", "r","g","m","orange"],
                data=datf)
    file_name = col+ "_gD_box"
    ftb.salvar_plot("../resources/plots/TOT_D/", file_name)
    sns.despine(offset=10, trim=True)
    plt.show()

def grafI_line(df, xval, yval,col):

    """ Gráfico interactivo para mostrar la rata de mortalidad entre los países del grupo
        Guarda el gráfico (.html) en el directorio TOT_D """

    fig = px.line(df, x=xval, y=yval, color=col, line_group=col, hover_name=col,
        line_shape="spline", render_mode="svg")

    fig.update_layout(
        title = {"text" : yval.replace("_", " ").title() + " per country - Group D", "x":0.4, "xanchor": "center"},
        xaxis_title="Date",
        yaxis_title="Mortality rate (%)",
        legend_title="Country",
        font=dict(
            size=12
        )
    )
    file_name = yval+ "_gD_line"
    ftb.salvarI_plot(fig,"../resources/plots/TOT_D/", file_name)
    fig.show()

def grafI_prog(df,xval,yval, tit,t):

    """ Gráfico interactivo de progresión de los valores cada 10 días
        Guarda el gráfico (.html) en el directorio TOT_W o TOT_D  según sea mundial o de grupo respectivamente """

    fig = px.line(df, x=xval, y= yval)
    fig.update_layout(
        title = {"text" : tit, "x":0.5, "xanchor": "center"},
        xaxis_title=  xval.title(),
        yaxis_title= yval.replace("_", " ").title(),
        font=dict(
            size=12))
    file_name = yval+ "_" + t + "_"+ "prog"
    if t == "W":
        ftb.salvarI_plot(fig,"../resources/plots/TOT_W/", file_name)
    else:
        ftb.salvarI_plot(fig,"../resources/plots/TOT_D/", file_name)
    fig.show()

def graf_corr (df, col, t):

    """ Gráfico estático tipo mapa de calor (Heatmap) con las correlación entre las principales variables
        Guarda el gráfico (.html) en el directorio TOT_W o TOT_D  según sea mundial o de grupo respectivamente  """ 

    plt.subplots(figsize=(16, 12)) 
    corr = df.corr() 
    sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool),  cmap= col, square=True,  annot=True)
    if t =="W":
        plt.title ("COVID19 World - Heatmap")
        file_name = t+"_heatmap" +  ".png"
        ftb.salvar_plot ( "../resources/plots/TOT_W/", file_name)
    elif t=="gD":
        plt.title ("COVID19 Group D - Heatmap")
        file_name = t + "_heatmap" +  ".png"
        ftb.salvar_plot ( "../resources/plots/TOT_D/", file_name)
    else:
        plt.title (t+" COVID19 - Heatmap")
        file_name = t+"_heatmap" +  ".png"
        ftb.salvar_plot ( "../resources/plots/" + t + "/", file_name)
    plt.show()