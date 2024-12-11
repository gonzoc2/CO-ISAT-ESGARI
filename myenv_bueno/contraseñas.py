import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import requests
from io import BytesIO
import plotly.graph_objects as go
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from streamlit_option_menu import option_menu
import calendar
import io
from streamlit_cookies_manager import EncryptedCookieManager
from st_aggrid import JsCode
import numpy as np

# Configurar las cookies (debes proporcionar la contraseña para cifrar las cookies)
cookies = EncryptedCookieManager(prefix="mi_aplicacion_", password="mi_contrasena_secreta_123")
if not cookies.ready():
    st.stop()

# Diccionario de usuarios y contraseñas
usuarios = {
    "admin": "adminpass",
    "Presidencia": "Bolsa2030",
    "Salvador": "dslegari",
    "Amendieta": "Mat0710",
    "Antonio":"esgaridc",
    "Ernesto":"dirgenesg",
    "Octavio":"Montenegro.1",
    "Karla":"Esgari.2024",
    "Luis":"Esgari2030!"
}

# Revisar si el usuario ya está autenticado
if 'autenticado' in cookies and cookies['autenticado'] == 'true':
    st.sidebar.success(f"Bienvenido, {cookies['usuario']}!")
    

    # Botón para cerrar sesión (en la barra lateral)
    if st.sidebar.button("Cerrar sesión"):
        cookies['autenticado'] = 'false'
        cookies['usuario'] = ''
        cookies.save()
        st.rerun()

else:
    # Formulario de inicio de sesión
    st.title("Iniciar sesión CO-ISAT")
    usuario_input = st.text_input("Usuario", placeholder="Ingresa tu usuario")
    contrasena_input = st.text_input("Contraseña", placeholder="Ingresa tu contraseña", type="password")

    if st.button("Iniciar sesión"):
        if usuario_input in usuarios and usuarios[usuario_input] == contrasena_input:
            st.success(f"Bienvenido, {usuario_input}!")
            
            # Guardar cookies para la sesión persistente
            cookies['autenticado'] = 'true'
            cookies['usuario'] = usuario_input
            cookies.save()
            
            st.rerun()  # Recargar la página para aplicar la sesión
        else:
            st.error("Nombre de usuario o contraseña incorrectos")



if 'autenticado' in cookies and cookies['autenticado'] == 'true':

    
    # URLs de las hojas de cálculo
    url = "https://docs.google.com/spreadsheets/d/18YVl2KDL14rObiOrEQZAAHajGsQankML/export?format=xlsx"
    url_ly = 'https://docs.google.com/spreadsheets/d/1bgCv6wmTI0mosaW1Gd2PKNiXhRwDqmWz/export?format=xlsx'

    url_ppt = 'https://docs.google.com/spreadsheets/d/1U0NGtYXB2Z2rDBL2useDzM1jIg8MF031/export?format=xlsx'

    fecha_actualizacion = 'https://docs.google.com/spreadsheets/d/1loPFsSZ3agTRuUAYWCDXFYtGMjvp6lh8/export?format=xlsx'

    cuadro_financiero = 'https://docs.google.com/spreadsheets/d/1utsKHn7V9fPPFrY3W4Ks6olIV8OMKQLm/export?format=xlsx'

    info_pro = 'https://docs.google.com/spreadsheets/d/1r5yTZl2wubp9gu5K_kiF-CEHxjhZF3K7/export?format=xlsx'

    # Configuración de la página
    

    # Función para descargar datos con cacheo
    @st.cache_data
    def cargar_datos(url):
        response = requests.get(url)
        response.raise_for_status()  # Verifica si hubo algún error en la descarga
        archivo_excel = BytesIO(response.content)
        return pd.read_excel(archivo_excel, engine="openpyxl")

    # Descargar las hojas de cálculo
    df = cargar_datos(url)
    df_ly = cargar_datos(url_ly)
    df_ppt = cargar_datos(url_ppt)
    fecha_actualizacion= cargar_datos(fecha_actualizacion)
    cuadro_financiero = cargar_datos(cuadro_financiero)

    info_pro_url = 'https://docs.google.com/spreadsheets/d/1r5yTZl2wubp9gu5K_kiF-CEHxjhZF3K7/export?format=xlsx'

    @st.cache_data
    def cargar_datos_hoja(url, nombre_hoja=None):
        """Función para cargar una hoja específica de un archivo de Excel desde una URL"""
        response = requests.get(url)
        response.raise_for_status()  # Verifica si hubo algún error en la descarga
        archivo_excel = BytesIO(response.content)
        # Si se especifica un nombre de hoja, se carga esa hoja; de lo contrario, se carga la primera por defecto
        return pd.read_excel(archivo_excel, engine="openpyxl", sheet_name=nombre_hoja)


    st.title('ESGARI CO-ISAT')
    fecha_actualizacion_texto = fecha_actualizacion.iloc[0, 0]
    fecha_actualizacion = fecha_actualizacion.iloc[0, 0]
    if isinstance(fecha_actualizacion_texto, pd.Timestamp):  # Verifica si es un Timestamp
        fecha_actualizacion_texto = fecha_actualizacion_texto.strftime('%d de %B de %Y')  # Formato español
    else:
        fecha_actualizacion_texto = str(fecha_actualizacion_texto) 
    fecha_actualizacion_texto = fecha_actualizacion_texto.replace('January', 'enero').replace('February', 'febrero') \
                                                        .replace('March', 'marzo').replace('April', 'abril') \
                                                        .replace('May', 'mayo').replace('June', 'junio') \
                                                        .replace('July', 'julio').replace('August', 'agosto') \
                                                        .replace('September', 'septiembre').replace('October', 'octubre') \
                                                        .replace('November', 'noviembre').replace('December', 'diciembre')

    st.write(f'Datos hasta el {fecha_actualizacion_texto}')
    # Menú interactivo
    
    if cookies['usuario'] == 'Presidencia' or cookies['usuario'] == 'Karla' or cookies['usuario'] == 'Octavio' or cookies['usuario'] == 'Ernesto' or cookies['usuario'] == 'admin':
        selected = option_menu(
            menu_title=None,  # Sin título
            options=["Resumen", "Estado de Resultado", "Comparativa", "Análisis", "Comparativa CeCo", "Proyeccion", "Cuadro financiero"],
            icons=["house", "clipboard-data", "file-earmark-bar-graph", "bar-chart", "graph-up", "building"],
            default_index=0,
            orientation="horizontal",
        )
    else:
        selected = option_menu(
            menu_title=None,  # Sin título
            options=["Resumen", "Estado de Resultado", "Comparativa", "Análisis", "Comparativa CeCo", "Proyeccion"],
            icons=["house", "clipboard-data", "file-earmark-bar-graph", "bar-chart", "graph-up", "building"],
            default_index=0,
            orientation="horizontal",
        )

    orden_meses = {
            'ene.': 1, 'feb.': 2, 'mar.': 3, 'abr.': 4,
            'may.': 5, 'jun.': 6, 'jul.': 7, 'ago.': 8,
            'sep.': 9, 'oct.': 10, 'nov.': 11, 'dic.': 12
        }
    meses_archivo = df['Mes_A'].unique().tolist()
    meses_archivo_ordenados = sorted(meses_archivo, key=lambda mes: orden_meses[mes])
    todos_los_meses = ['ene.', 'feb.', 'mar.', 'abr.', 'may.','jun.','jul.','ago.','sep.','oct.','nov.','dic.']
    oh = [8004,8002]
    oh_p = [8002,8003, 8004, 7501]
    p_7501_8003 = [8003, 7501]
    p_8003 = [8003]
    gastos_fin = ['COMISIONES BANCARIAS', 'INTERESES', 'PERDIDA CAMBIARIA', 'PAGO POR FACTORAJE']
    ingreso_fin = ['INGRESO POR REVALUACION CAMBIARIA ', 'INGRESO POR INTERESES', 'INGRESO POR REVALUACION DE ACTIVOS', 'INGRESO POR FACTORAJE']
    in_gasfin = ['INGRESO', 'GASTOS FINANCIEROS']
    proyectos_activos_oh_p = [5001, 3201, 3002, 2003, 7901, 1001, 1003, 2001, 7806, 8002, 8003, 8004]
    nombre_proyectos_oh_p = ['MANZANILLO', 'CONTINENTAL', 'CENTRAL OTROS', 'FLEX SPOT', 'WH', 'CHALCO', 'ARRAYANES', 
                            'FLEX DEDICADO', 'INTERNACIONAL FWD', 'OFICINAS LUNA', 'PATIO', 'OFICINAS ANDARES']
    proyecto_dict_oh_p = dict(zip(proyectos_activos_oh_p, nombre_proyectos_oh_p))
    proyectos_activos = [5001, 3201, 3002, 2003, 7901, 1001, 1003, 2001, 7806]
    nombre_proyectos_activos = ['MANZANILLO', 'CONTINENTAL', 'CENTRAL OTROS', 'FLEX SPOT', 'WH', 'CHALCO', 'ARRAYANES', 
                            'FLEX DEDICADO', 'INTERNACIONAL FWD']
    empresas = [0, 10, 20, 30, 40, 50]

    nombre_empresas = ['ESGARI','ESGARI HOLDING MEXICO, S.A. DE C.V.', 'RESA MULTIMODAL, S.A. DE C.V', 
                    'UBIKARGA S.A DE C.V', 'ESGARI FORWARDING SA DE CV', 
                    'ESGARI WAREHOUSING & MANUFACTURING, S DE R.L DE C.V']

    empresas_dict = dict(zip(nombre_empresas, empresas))
    proyecto_dict = dict(zip(proyectos_activos, nombre_proyectos_activos))
    cecos_ytd = sorted(df['CeCo_A'].dropna().unique().tolist())
    cecos_ly = sorted(df_ly['CeCo_A'].dropna().unique().tolist())
    cecos_ppt = sorted(df_ppt['CeCo_A'].dropna().unique().tolist())
    cecos = sorted(set(cecos_ytd + cecos_ly + cecos_ppt))

    # Diccionario de valores con códigos y nombres
    valores = {
                50: "INTEREMPRESAS",
                100: "DIRECCION",
                200: "TI",
                300: "ADMINISTRACION",
                400: "CONTRALORIA",
                500: "RH",
                600: "SEGURIDAD",
                700: "CONTABILIDAD Y FINANZAS",
                800: "CREDITO Y COBRANZA",
                900: "SOLUCIONES LOGISTICAS",
                1000: "PRODUCTIVIDAD Y FLOTAS",
                1100: "OPERACIONES",
                1200: "OPERACIONES INTERNACIONALES",
                1300: "DESARROLLO DE TRANSPORTE",
                1500: "PRESIDENCIA",
                1600: "DO",
                1650: "COMPLIANCE",
                1700: "COMERCIAL",
                1800: "EXCELENCIA OPERATIVA",
                1900: "SOSTENIBILIDAD E INVERSION SOCIAL",
                2000: "FACTURACION",
                2100: "DESARROLLO ESTRATEGICO",
                2200: "FINANZAS"
            }

            # Crear lista combinada de opciones
    opciones = []

            # Agregar valores del diccionario con formato "NOMBRE (CÓDIGO)"
    for codigo in cecos:
        if codigo in valores:
            opciones.append(f"{valores[codigo]} ({codigo})")
        else:
            opciones.append(f"{codigo}")  # Mostrar solo el código si no está en el diccionario

    proyectos_archivo = sorted(df['Proyecto_A'].unique().tolist())
    proyectos_archivo_ly = sorted(df_ly['Proyecto_A'].unique().tolist())
    proyectos_archivo_ppt = sorted(df_ppt['Proyecto_A'].unique().tolist())
    # Lista de opciones de proyecto
    opciones_proyecto = ["Todos los proyectos"]
    for proyecto in proyectos_archivo:
        if proyecto in proyecto_dict_oh_p:
            opciones_proyecto.append(f"{proyecto_dict_oh_p[proyecto]} ({proyecto})")
        else:
            opciones_proyecto.append(str(proyecto))
    categorias_felx_com = ['COSTO DE PERSONAL', 'GASTO DE PERSONAL', 'NOMINA ADMINISTRATIVOS']
    da = ['AMORT ARRENDAMIENTO', 'AMORTIZACION', 'DEPRECIACION ']


    def meses ():
        usar_rango = st.checkbox("¿Quieres seleccionar un rango de meses?")
        if usar_rango:
            # Selector de mes inicial y final
            mes_inicio = st.selectbox("Selecciona el mes inicial", meses_archivo_ordenados, key="mes_inicio")
            mes_fin = st.selectbox("Selecciona el mes final", meses_archivo_ordenados, key="mes_fin")

            # Convertir los meses a índices
            indice_inicio = meses_archivo_ordenados.index(mes_inicio)
            mes_inicio = [mes_inicio]
            indice_fin = meses_archivo_ordenados.index(mes_fin)
            mes_unico = mes_fin
            # Generar la lista de meses dentro del rango
            if indice_inicio <= indice_fin:
                rango_meses = meses_archivo_ordenados[indice_inicio:indice_fin + 1]
            else:
                # Si el rango cruza el límite del año
                rango_meses = meses_archivo_ordenados[indice_inicio:] + meses_archivo_ordenados[:indice_fin + 1]
        else:
            # Selector de un único mes
            mes_unico = st.selectbox("Selecciona un mes", meses_archivo_ordenados, key="mes_unico")
            rango_meses = [mes_unico]  # La salida sigue siendo una lista con un único mes
            mes_inicio = rango_meses
        return rango_meses, mes_unico, mes_inicio


    @st.cache_data
    def calcular_oh_pro_totales(df, mes, pro, oh):
            oh_pro_total = 0
            oh_pro_da = 0
            for i in mes:
                # Ingreso total excluyendo overhead
                ingreso_total = df[df['Categoria_A'] == 'INGRESO']
                ingreso_total = ingreso_total[~ingreso_total['Proyecto_A'].isin(oh)]
                ingreso_total = ingreso_total[ingreso_total['Mes_A'] == i]['Neto_A'].sum()

                # Ingreso del proyecto actual
                ingreso_pro = df[df['Categoria_A'] == 'INGRESO']
                ingreso_pro = ingreso_pro[ingreso_pro['Mes_A'] == i]
                ingreso_pro = ingreso_pro[ingreso_pro['Proyecto_A'].isin(pro)]['Neto_A'].sum()

                # Calcular porcentaje del ingreso
                porcentaje_ingreso = ingreso_pro / ingreso_total if ingreso_total > 0 else 0

                # Overhead total
                oh_t = df[df['Proyecto_A'].isin(oh)]
                oh_t = oh_t[oh_t['Clasificacion_A'].isin(['COSS', 'G.ADMN'])]
                oh_t = oh_t[oh_t['Mes_A'] == i]['Neto_A'].sum()
                oh_t_da = df[df['Proyecto_A'].isin(oh)]
                oh_t_da = oh_t_da[oh_t_da['Categoria_A'].isin(da)]
                oh_t_da = oh_t_da[oh_t_da['Mes_A'] == i]['Neto_A'].sum()

                oh_pro_da += porcentaje_ingreso * oh_t_da
                oh_pro_total += porcentaje_ingreso * oh_t

            return oh_pro_total, oh_pro_da
    @st.cache_data   
    def tabla_resumen(pro, mes, dataframe):
            pro_origi = pro 
            if isinstance(pro, list):
                pro_no_lista = pro[0]  # Acceder al primer elemento si es una lista
            else:
                pro_no_lista = pro 
            
            # Asegurar que 'pro' sea siempre una lista
            if isinstance(pro, int):
                pro = [pro]
            lineas = {}
            
            if pro == proyectos_archivo or pro == proyectos_archivo_ly or pro == proyectos_archivo_ppt:  # Todos los proyectos
                df_pro = dataframe[dataframe['Mes_A'].isin(mes)]

                # Ingreso total
                ingreso = df_pro[df_pro['Categoria_A'] == 'INGRESO']['Neto_A'].sum()
                lineas['INGRESO'] = ingreso

                # Overhead total
                oh_t = dataframe[dataframe['Proyecto_A'].isin(oh)]
                oh_t = oh_t[oh_t['Mes_A'].isin(mes)]
                oh_t_da = 0
                oh_t = oh_t[oh_t['Clasificacion_A'].isin(['COSS', 'G.ADMN'])]['Neto_A'].sum()
                
                

                # Patio
                patio = dataframe[dataframe['Mes_A'].isin(mes)]
                patio = patio[patio['Proyecto_A'].isin(p_7501_8003)]
                patio_da = 0
                patio = patio[~patio['Clasificacion_A'].isin(in_gasfin)]['Neto_A'].sum()
                
                df_pro = df_pro[~df_pro['Proyecto_A'].isin(oh_p)]
            elif pro_origi == 3002 or pro_no_lista == 3002:
                df_pro = dataframe[dataframe['Proyecto_A'].isin(pro)]
                df_pro = df_pro[df_pro['Mes_A'].isin(mes)]

                # Ingreso
                ingreso = df_pro[df_pro['Categoria_A'] == 'INGRESO']['Neto_A'].sum()
                lineas['INGRESO'] = ingreso

                # Overhead
                oh_t, _ = calcular_oh_pro_totales(dataframe, mes, pro, oh)
                _, oh_t_da = calcular_oh_pro_totales(dataframe, mes, pro, oh)
                # Patio
                patio = dataframe[dataframe['Proyecto_A'].isin([8003])]
                patio = patio[patio['Mes_A'].isin(mes)]
                patio_da = patio[patio['Categoria_A']. isin(da)]['Neto_A'].sum()
                patio = patio[~patio['Clasificacion_A'].isin(in_gasfin)]['Neto_A'].sum()      
                    
            else:  # Proyecto individual
                df_pro = dataframe[dataframe['Proyecto_A'].isin(pro)]
                df_pro = df_pro[df_pro['Mes_A'].isin(mes)]

                # Ingreso
                ingreso = df_pro[df_pro['Categoria_A'] == 'INGRESO']['Neto_A'].sum()
                lineas['INGRESO'] = ingreso

                # Overhead
                oh_t, _ = calcular_oh_pro_totales(dataframe, mes, pro, oh)
                _, oh_t_da = calcular_oh_pro_totales(dataframe, mes, pro, oh)

                # Patio (siempre 0 para proyectos individuales)
                patio = 0
                patio_da = 0

            # Costo
            costo = df_pro[df_pro['Clasificacion_A'] == 'COSS']['Neto_A'].sum()
            if selected == "Análisis":
                lineas['COSS'] = costo
            else: 
                lineas['COSS'] = costo + patio
            lineas['PATIO'] = patio
            lineas['% PATIO'] = patio / lineas['INGRESO']*100
            
            lineas['Ut. Bruta'] = lineas['INGRESO'] - lineas['COSS']
            lineas['MG. bruto'] = lineas['Ut. Bruta']/ lineas['INGRESO']*100
            # Gasto Administrativo
            if pro_origi == 2001:
                g_admn = df_pro[df_pro['Clasificacion_A'] == 'G.ADMN']['Neto_A'].sum()
                g_admn = g_admn - df_pro[df_pro['Categoria_A'].isin(categorias_felx_com)]['Neto_A'].sum()*.15
            elif pro_origi == 2003:
                g_admn = dataframe[dataframe['Proyecto_A'].isin([2001])]
                g_admn = g_admn[g_admn['Mes_A'].isin(mes)]
                g_admn = g_admn[g_admn['Categoria_A'].isin(categorias_felx_com)]['Neto_A'].sum()*.15
            else:
                g_admn = df_pro[df_pro['Clasificacion_A'] == 'G.ADMN']['Neto_A'].sum()



            lineas['G.ADMN'] = g_admn
            
            lineas['UO'] = lineas['INGRESO'] - lineas['COSS'] - g_admn
            lineas['MG. OP.'] = lineas['UO']/lineas['INGRESO']*100
            lineas['OH'] = oh_t
            lineas['% OH'] = lineas['OH']/lineas['INGRESO']*100
            # EBIT
            lineas['EBIT'] = lineas['INGRESO'] - lineas['COSS'] - g_admn - lineas['OH']
            lineas['MG. EBIT'] = lineas['EBIT']/lineas['INGRESO']*100
            #ajuste df_pro
            if pro == proyectos_archivo or pro == proyectos_archivo_ppt or pro == proyectos_archivo_ly:
                df_pro = dataframe[dataframe['Mes_A'].isin(mes)]
            # Gastos Financieros
            gfin = df_pro[df_pro['Categoria_A'].isin(gastos_fin)]['Neto_A'].sum()
            
            
            # Ingresos Financieros
            ifin = df_pro[df_pro['Categoria_A'].isin(ingreso_fin)]['Neto_A'].sum()
            
            resultado_fin = gfin - ifin
            lineas['RESULTADO FINANCIERO'] = resultado_fin
            lineas['GASTOS FINANCIEROS'] = gfin
            lineas['INGRESO FINANCIERO'] = ifin


            # EBT
            lineas['EBT'] = lineas['EBIT'] - gfin + ifin
            #EBITDEA 
            lineas['MG. EBT'] = lineas['EBT']/lineas['INGRESO']*100
            
            lineas['EBITDA'] = lineas['EBIT'] + oh_t_da + patio_da + df_pro[df_pro['Categoria_A'].isin(da)]['Neto_A'].sum()
            lineas['MG. EBITDA'] = lineas['EBITDA']/lineas['INGRESO']*100

            return lineas


    # Función para calcular ingresos y egresos mensuales
    @st.cache_data   
    def in_egre_mes_a_mes(pro, df, meses_archivo_ordenados):
        ingreso_mes_a_mes = {}
        egreso_mes_a_mes = {}
        if isinstance(pro, int):
            pro = [pro]
        for i in meses_archivo_ordenados:
            ingreso = df[df['Mes_A'] == i]
            ingreso = ingreso[ingreso['Clasificacion_A'] == 'INGRESO']
            ingreso = ingreso[ingreso['Proyecto_A'].isin(pro)]['Neto_A'].sum()
            ingreso_mes_a_mes[i] = ingreso
            egreso = df[df['Mes_A'] == i]
            egreso = egreso[egreso['Clasificacion_A'].isin(['COSS','G.ADMN','GASTOS FINANCIEROS'])]
            egreso = egreso[egreso['Proyecto_A'].isin(pro)]['Neto_A'].sum()
            egreso_mes_a_mes[i] = egreso
        return ingreso_mes_a_mes, egreso_mes_a_mes

    # Función para crear el gráfico de ingresos y egresos
    @st.cache_data   
    def crear_grafico_in_egre(ingreso_mes_a_mes, egreso_mes_a_mes, meses_ordenados):
        # Crear DataFrame para combinar ingresos y egresos
        data = {
            'Mes': list(ingreso_mes_a_mes.keys()),
            'Ingresos': list(ingreso_mes_a_mes.values()),
            'Egresos': list(egreso_mes_a_mes.values())
        }
        df_combined = pd.DataFrame(data)

        # Asegurarnos de que los meses estén ordenados correctamente
        df_combined['Mes'] = pd.Categorical(df_combined['Mes'], categories=meses_ordenados, ordered=True)
        df_combined = df_combined.sort_values('Mes').set_index('Mes')

        # Crear el gráfico
        fig = go.Figure()

        # Línea de Ingresos
        fig.add_trace(go.Scatter(
            x=df_combined.index,
            y=df_combined['Ingresos'],
            mode='lines+markers+text',
            line=dict(color='#4CAF50', width=2),
            marker=dict(size=8, color='#FFA726'),
            text=df_combined['Ingresos'].apply(lambda x: f"${x:,.0f}"),
            texttemplate="%{text}",
            textposition="top center",
            name='Ingresos'
        ))

        # Línea de Egresos
        fig.add_trace(go.Scatter(
            x=df_combined.index,
            y=df_combined['Egresos'],
            mode='lines+markers+text',
            line=dict(color='#FF5733', width=2),
            marker=dict(size=8, color='#FFC300'),
            text=df_combined['Egresos'].apply(lambda x: f"${x:,.0f}"),
            texttemplate="%{text}",
            textposition="bottom center",
            name='Egresos'
        ))

        # Personalización del gráfico
        fig.update_layout(
            title='Ingresos y Egresos Mensuales',
            xaxis_title='Mes',
            yaxis_title='Monto ($)',
            title_font=dict(size=20, color='white'),
            xaxis=dict(
                tickangle=-45,
                color='white',
                tickvals=df_combined.index,
                ticktext=df_combined.index
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=0.5,
                gridcolor='#444444',
                color='white'
            ),
            plot_bgcolor='#333333',
            paper_bgcolor='#0e1117',
            font=dict(color='white', size=14)
        )

        return fig

    # Función para crear el gráfico de ingresos por proyecto
    @st.cache_data   
    def crear_grafico_egre(ingreso_por_proyecto, meses_ordenados):
        # Crear el gráfico
        fig = go.Figure()

        # Iterar sobre los proyectos y agregar una traza por cada uno
        for proyecto, ingreso_mes_a_mes in ingreso_por_proyecto.items():
            # Crear DataFrame para el proyecto actual
            data = {
                'Mes': list(ingreso_mes_a_mes.keys()),
                'Ingresos': list(ingreso_mes_a_mes.values()),
            }
            df_combined = pd.DataFrame(data)

            # Asegurarnos de que los meses estén ordenados correctamente
            df_combined['Mes'] = pd.Categorical(df_combined['Mes'], categories=meses_ordenados, ordered=True)
            df_combined = df_combined.sort_values('Mes').set_index('Mes')

            # Agregar la línea del proyecto al gráfico
            fig.add_trace(go.Scatter(
                x=df_combined.index,
                y=df_combined['Ingresos'],
                mode='lines+markers+text',
                line=dict(width=2),
                marker=dict(size=8),
                text=df_combined['Ingresos'].apply(lambda x: f"${x:,.0f}"),
                texttemplate="%{text}",
                textposition="top center",
                name=f"Proyecto {proyecto}"
            ))

        # Personalización del gráfico
        fig.update_layout(
            title='Ingresos por Proyecto',
            xaxis_title='Mes',
            yaxis_title='Monto ($)',
            title_font=dict(size=20, color='white'),
            xaxis=dict(
                tickangle=-45,
                color='white',
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=0.5,
                gridcolor='#444444',
                color='white'
            ),
            plot_bgcolor='#333333',
            paper_bgcolor='#0e1117',
            font=dict(color='white', size=14)
        )

        return fig
    def tabla_expandible(df, cat, mes, pro, dic, key_prefix):
            if not isinstance(pro, list):
                pro = [pro]

            if cat == 'INGRESO':
                df_tabla = df[df['Categoria_A'] == cat]
                df_tabla = df_tabla[df_tabla['Proyecto_A'].isin(pro)]
                df_tabla = df_tabla[df_tabla['Mes_A'].isin(mes)]
                df_tabla = df_tabla.groupby(columnas, as_index=False).agg({"Neto_A": "sum"})
            elif cat == 'INGRESO FINANCIERO':
                df_tabla = df[df['Categoria_A'].isin(ingreso_fin)]
                df_tabla = df_tabla[df_tabla['Proyecto_A'].isin(pro)]
                df_tabla = df_tabla[df_tabla['Mes_A'].isin(mes)]
                df_tabla = df_tabla.groupby(columnas, as_index=False).agg({"Neto_A": "sum"})
            else:
                df_tabla = df[df['Clasificacion_A'] == cat]
                df_tabla = df_tabla[df_tabla['Proyecto_A'].isin(pro)]
                df_tabla = df_tabla[df_tabla['Mes_A'].isin(mes)]
                df_tabla = df_tabla.groupby(columnas, as_index=False).agg({"Neto_A": "sum"})
            
            # Limpiar el DataFrame (muy importante para evitar errores en AgGrid)
            df_tabla = df_tabla.fillna("")  # Reemplazar NaN por cadenas vacías
            df_tabla.reset_index(drop=True, inplace=True)  # Reiniciar índices

            # Configurar AgGrid
            gb = GridOptionsBuilder.from_dataframe(df_tabla)
            gb.configure_default_column(groupable=True)
            gb.configure_column("Categoria_A", rowGroup=True, hide=True)  # Ocultar columna pero hacerla agrupable
            gb.configure_column(
                "Neto_A",
                aggFunc="sum",  # Configurar la función de agregación como suma
                valueFormatter="`$${value.toLocaleString()}`",  # Mostrar como formato de moneda
            )
            grid_options = gb.build()
            num = dic[f'{cat}']
            # Mostrar la tabla dentro de un expander
            if cat == 'COSS':
                with st.expander(f"{cat}: ${num:,.2f}"):
                    st.write(f"PATIO: ${dic[f'PATIO']:,.2f}")
                    st.write(f"Tabla {cat}")
                                # Use a unique key for the AgGrid instance
                    AgGrid(
                        df_tabla,
                        gridOptions=grid_options,
                        enable_enterprise_modules=True,  # Activar módulos avanzados
                        height=400,  # Altura de la tabla
                        theme="streamlit",  # Tema de la tabla
                        key=f"{key_prefix}_aggrid_{cat}"  # Unique key for AgGrid
                    )

                    # Convertir el DataFrame a un archivo Excel en memoria
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                        df_tabla.to_excel(writer, index=False, sheet_name=f"Tabla_{cat}")
                        output.seek(0)  # Regresar el puntero al inicio del flujo de datos

                    # Agregar el botón de descarga para Excel con un unique key
                    st.download_button(
                        label=f"Descargar tabla {cat}",
                        data=output,
                        file_name=f"tabla_{cat}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"{key_prefix}_download_{cat}"  # Unique key for download button
                    )            
            else: 
                with st.expander(f"{cat}: ${num:,.2f}"):
                    st.write(f"Tabla {cat}")
                                # Use a unique key for the AgGrid instance
                    AgGrid(
                        df_tabla,
                        gridOptions=grid_options,
                        enable_enterprise_modules=True,  # Activar módulos avanzados
                        height=400,  # Altura de la tabla
                        theme="streamlit",  # Tema de la tabla
                        key=f"{key_prefix}_aggrid_{cat}"  # Unique key for AgGrid
                    )

                    # Convertir el DataFrame a un archivo Excel en memoria
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                        df_tabla.to_excel(writer, index=False, sheet_name=f"Tabla_{cat}")
                        output.seek(0)  # Regresar el puntero al inicio del flujo de datos

                    # Agregar el botón de descarga para Excel con un unique key
                    st.download_button(
                        label=f"Descargar tabla {cat}",
                        data=output,
                        file_name=f"tabla_{cat}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"{key_prefix}_download_{cat}"  # Unique key for download button
                    )


    def tabla_expandible_comp(df,df_ly,df_ppt, cat, mes, pro, dic, dic_ly, dic_ppt, key_prefix):
            if not isinstance(pro, list):
                pro = [pro]
            
            if cat == 'INGRESO':
                df_tabla = df[df['Categoria_A'] == cat]
                df_tabla = df_tabla[df_tabla['Proyecto_A'].isin(pro)]
                df_tabla = df_tabla[df_tabla['Mes_A'].isin(mes)]
                df_tabla = df_tabla.groupby(columnas, as_index=False).agg({"Neto_A": "sum"})

                df_tabla_ly = df_ly[df_ly['Categoria_A'] == cat]
                df_tabla_ly = df_tabla_ly[df_tabla_ly['Proyecto_A'].isin(pro)]
                df_tabla_ly = df_tabla_ly[df_tabla_ly['Mes_A'].isin(mes)]
                df_tabla_ly = df_tabla_ly.groupby(columnas, as_index=False).agg({"Neto_A": "sum"})

                df_tabla_ppt = df_ppt[df_ppt['Categoria_A'] == cat]
                df_tabla_ppt = df_tabla_ppt[df_tabla_ppt['Proyecto_A'].isin(pro)]
                df_tabla_ppt = df_tabla_ppt[df_tabla_ppt['Mes_A'].isin(mes)]
                df_tabla_ppt = df_tabla_ppt.groupby(columnas, as_index=False).agg({"Neto_A": "sum"})

            elif cat == 'INGRESO FINANCIERO':
                df_tabla = df[df['Categoria_A'].isin(ingreso_fin)]
                df_tabla = df_tabla[df_tabla['Proyecto_A'].isin(pro)]
                df_tabla = df_tabla[df_tabla['Mes_A'].isin(mes)]
                df_tabla = df_tabla.groupby(columnas, as_index=False).agg({"Neto_A": "sum"})

                df_tabla_ly = df_ly[df_ly['Categoria_A'].isin(ingreso_fin)]
                df_tabla_ly = df_tabla_ly[df_tabla_ly['Proyecto_A'].isin(pro)]
                df_tabla_ly = df_tabla_ly[df_tabla_ly['Mes_A'].isin(mes)]
                df_tabla_ly = df_tabla_ly.groupby(columnas, as_index=False).agg({"Neto_A": "sum"})

                df_tabla_ppt = df_ppt[df_ppt['Categoria_A'].isin(ingreso_fin)]
                df_tabla_ppt = df_tabla_ppt[df_tabla_ppt['Proyecto_A'].isin(pro)]
                df_tabla_ppt = df_tabla_ppt[df_tabla_ppt['Mes_A'].isin(mes)]
                df_tabla_ppt = df_tabla_ppt.groupby(columnas, as_index=False).agg({"Neto_A": "sum"})
                
            else:
                df_tabla = df[df['Clasificacion_A'] == cat]
                df_tabla = df_tabla[df_tabla['Proyecto_A'].isin(pro)]
                df_tabla = df_tabla[df_tabla['Mes_A'].isin(mes)]
                df_tabla = df_tabla.groupby(columnas, as_index=False).agg({"Neto_A": "sum"})

                df_tabla_ly = df_ly[df_ly['Clasificacion_A'] == cat]
                df_tabla_ly = df_tabla_ly[df_tabla_ly['Proyecto_A'].isin(pro)]
                df_tabla_ly = df_tabla_ly[df_tabla_ly['Mes_A'].isin(mes)]
                df_tabla_ly = df_tabla_ly.groupby(columnas, as_index=False).agg({"Neto_A": "sum"})

                df_tabla_ppt = df_ppt[df_ppt['Clasificacion_A'] == cat]
                df_tabla_ppt = df_tabla_ppt[df_tabla_ppt['Proyecto_A'].isin(pro)]
                df_tabla_ppt = df_tabla_ppt[df_tabla_ppt['Mes_A'].isin(mes)]
                df_tabla_ppt = df_tabla_ppt.groupby(columnas, as_index=False).agg({"Neto_A": "sum"})
            


            # Paso 1: Realizamos las uniones de las tablas
            df_combinado = pd.merge(df_tabla, df_tabla_ly, on=['Cuenta_Nombre_A', 'Categoria_A'], how='outer', suffixes=('', '_ly'))
            df_combinado = pd.merge(df_combinado, df_tabla_ppt, on=['Cuenta_Nombre_A', 'Categoria_A'], how='outer', suffixes=('', '_ppt'))

            # Paso 2: Llenamos las columnas faltantes con ceros
            df_combinado['YTD'] = df_combinado['Neto_A'].fillna(0)
            df_combinado['LY'] = df_combinado['Neto_A_ly'].fillna(0)
            df_combinado['PPT'] = df_combinado['Neto_A_ppt'].fillna(0)

            # Paso 3: Calculamos las nuevas columnas para Alcance_LY y Alcance_PPT
            df_combinado['Alcance_LY'] = df_combinado['YTD'] / df_combinado['LY'].replace(0, float('nan'))
            df_combinado['Alcance_PPT'] = df_combinado['YTD'] / df_combinado['PPT'].replace(0, float('nan'))

            # Paso 4: Reemplazamos los valores NaN con 0 en las divisiones
            df_combinado['Alcance_LY'] = df_combinado['Alcance_LY'].fillna(0)
            df_combinado['Alcance_PPT'] = df_combinado['Alcance_PPT'].fillna(0)
            df_combinado = df_combinado.loc[:, ~df_combinado.columns.str.contains('Neto')]
            cols_alcance = df_combinado.columns[df_combinado.columns.str.contains('Alcance')]
            df_combinado[cols_alcance] = df_combinado[cols_alcance] * 100


            # Limpiar el DataFrame (muy importante para evitar errores en AgGrid)
            df_combinado = df_combinado.fillna("")  # Reemplazar NaN por cadenas vacías
            df_combinado.reset_index(drop=True, inplace=True)  # Reiniciar índices

            # Precalcular las columnas Alcance_LY y Alcance_PPT en el DataFrame
            # Calcular las columnas con validación para evitar divisiones por cero
            df_combinado["Alcance_LY"] = df_combinado.apply(
                lambda row: (row["YTD"] / row["LY"] * 100) if row["YTD"] > 0 and row["LY"] != 0 else 0, axis=1
            )
            df_combinado["Alcance_PPT"] = df_combinado.apply(
                lambda row: (row["YTD"] / row["PPT"] * 100) if row["YTD"] > 0 and row["PPT"] != 0 else 0, axis=1
            )

            # Crear valores precalculados para las filas agrupadas
            df_grouped = df_combinado.groupby("Categoria_A", as_index=False).agg({
                "YTD": "sum",
                "LY": "sum",
                "PPT": "sum"
            })

            # Calcular las columnas en el DataFrame agrupado con validación para evitar divisiones por cero
            df_grouped["Alcance_LY"] = df_grouped.apply(
                lambda row: (row["YTD"] / row["LY"] * 100) if row["YTD"] > 0 and row["LY"] != 0 else 0, axis=1
            )
            df_grouped["Alcance_PPT"] = df_grouped.apply(
                lambda row: (row["YTD"] / row["PPT"] * 100) if row["YTD"] > 0 and row["PPT"] != 0 else 0, axis=1
            )


            # Combinar los datos originales con los valores agrupados
            df_combinado_or = df_combinado
            df_combinado = pd.concat([df_combinado, df_grouped], ignore_index=True)
            
            # Configurar AgGrid
            gb = GridOptionsBuilder.from_dataframe(df_combinado)
            gb.configure_default_column(groupable=True)

            # Ocultar columna pero hacerla agrupable
            gb.configure_column("Categoria_A", rowGroup=True, hide=True)

            # Configurar columnas principales
            js_code_value_formatter_currency = JsCode("""
            function(params) {
                return `$${params.value.toLocaleString()}`;
            }
            """)

            gb.configure_column(
                "YTD",
                aggFunc="last",  # Suma para filas agrupadas
                valueFormatter=js_code_value_formatter_currency,
            )

            gb.configure_column(
                "LY",
                aggFunc="last",  # Suma para filas agrupadas
                valueFormatter=js_code_value_formatter_currency,
            )

            gb.configure_column(
                "PPT",
                aggFunc="last",  # Suma para filas agrupadas
                valueFormatter=js_code_value_formatter_currency,
            )

            # Mostrar valores precalculados en Alcance_LY y Alcance_PPT
            gb.configure_column(
                "Alcance_LY",
                aggFunc="last",  # Usar el último valor precalculado
                valueFormatter="`${value.toFixed(2)}%`",
            )

            gb.configure_column(
                "Alcance_PPT",
                aggFunc="last",  # Usar el último valor precalculado
                valueFormatter="`${value.toFixed(2)}%`",
            )

            # Construir las opciones de la tabla
            grid_options = gb.build()
            if cat == 'COSS':
                # Mostrar la tabla dentro de un expander
                with st.expander(f"{cat}: YTD ${dic[f'{cat}']:,.2f} vs LY {dic_ly[f'{cat}']:,.2f} vs PPT {dic_ppt[f'{cat}']:,.2f}"):
                    st.write(f"PATIO: YTD ${dic['PATIO']:,.2f} vs LY {dic_ly['PATIO']:,.2f} vs PPT {dic_ppt['PATIO']:,.2f}")
                    st.write(f"Alcance LY {dic[f'{cat}']/dic_ly[f'{cat}']*100:,.2f}%")
                    st.write(f"Alcance PPT {dic[f'{cat}']/dic_ppt[f'{cat}']*100:,.2f}%")
                    AgGrid(
                        df_combinado,  # El DataFrame que estás usando
                        gridOptions=grid_options,  # Opciones de la tabla
                        enable_enterprise_modules=True,  # Módulos avanzados de AgGrid
                        allow_unsafe_jscode=True,  # Permite usar JsCode personalizado
                        height=400,  # Altura de la tabla
                        theme="streamlit",  # Tema de la tabla
                        key=f"{key_prefix}_aggrid_{cat}"  # Llave única para evitar conflictos
                    )

                    # Convertir el DataFrame a un archivo Excel en memoria
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                        df_combinado_or.to_excel(writer, index=False, sheet_name=f"Tabla_{cat}")
                        output.seek(0)  # Regresar el puntero al inicio del flujo de datos

                    # Agregar el botón de descarga para Excel con un unique key
                    st.download_button(
                        label=f"Descargar tabla {cat}",
                        data=output,
                        file_name=f"tabla_{cat}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"{key_prefix}_download_{cat}"  # Unique key for download button
                    )
            else:

                # Mostrar la tabla dentro de un expander
                with st.expander(f"{cat}: YTD ${dic[f'{cat}']:,.2f} vs LY {dic_ly[f'{cat}']:,.2f} vs PPT {dic_ppt[f'{cat}']:,.2f}"):
                    st.write(f"Alcance LY {dic[f'{cat}']/dic_ly[f'{cat}']*100:,.2f}%")
                    st.write(f"Alcance PPT {dic[f'{cat}']/dic_ppt[f'{cat}']*100:,.2f}%")
                    AgGrid(
                        df_combinado,  # El DataFrame que estás usando
                        gridOptions=grid_options,  # Opciones de la tabla
                        enable_enterprise_modules=True,  # Módulos avanzados de AgGrid
                        allow_unsafe_jscode=True,  # Permite usar JsCode personalizado
                        height=400,  # Altura de la tabla
                        theme="streamlit",  # Tema de la tabla
                        key=f"{key_prefix}_aggrid_{cat}"  # Llave única para evitar conflictos
                    )

                    # Convertir el DataFrame a un archivo Excel en memoria
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                        df_combinado_or.to_excel(writer, index=False, sheet_name=f"Tabla_{cat}")
                        output.seek(0)  # Regresar el puntero al inicio del flujo de datos

                    # Agregar el botón de descarga para Excel con un unique key
                    st.download_button(
                        label=f"Descargar tabla {cat}",
                        data=output,
                        file_name=f"tabla_{cat}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"{key_prefix}_download_{cat}"  # Unique key for download button
                    )




    def filtro_pro():
            if selected != 'Proyeccion':
                nombre_proyectos_oh_p = ['MANZANILLO', 'CONTINENTAL', 'CENTRAL OTROS', 'FLEX SPOT', 'WH', 'CHALCO', 'ARRAYANES', 
                                'FLEX DEDICADO', 'INTERNACIONAL FWD', 'OFICINAS LUNA', 'PATIO', 'OFICINAS ANDARES']
            else:
                nombre_proyectos_oh_p = ['MANZANILLO', 'CONTINENTAL', 'CENTRAL OTROS', 'FLEX SPOT', 'CHALCO', 'ARRAYANES', 
                                'FLEX DEDICADO', 'INTERNACIONAL FWD']
            nombre_a_codigo = {nombre: codigo for codigo, nombre in proyecto_dict_oh_p.items()}
            
            nombre_proyectos_oh_p = ['ESGARI'] + nombre_proyectos_oh_p
            
            # Selección de proyecto en Streamlit
            pro = st.selectbox('Selecciona el proyecto a visualizar', nombre_proyectos_oh_p)

            # Obtener el código del proyecto seleccionado
            if pro == 'ESGARI':
                codigo_proyecto = proyectos_archivo
            else:
                codigo_proyecto = nombre_a_codigo.get(pro)
            return pro, codigo_proyecto


    def filtro_emp():
        emp = st.selectbox('Selecciona la empresa',empresas_dict)
        if emp == 'ESGARI':
            codigo_emp = empresas
        else:
            codigo_emp = empresas_dict.get(emp)
            codigo_emp = [codigo_emp]
        return emp, codigo_emp
    def filtrar_cecos(df, cecos, valores):
            
            opciones = ["Todos"]  # Agregar la opción "Todos" al inicio
            for codigo in cecos:
                if codigo in valores:
                    opciones.append(f"{valores[codigo]} ({codigo})")
                else:
                    opciones.append(f"{codigo}")

            # Visualización en Streamlit
            seleccionados = st.selectbox("Selecciona un Centro de Costo (CeCo):", opciones)

            # Manejo de la opción "Todos"
            if seleccionados == "Todos":
                # Si "Todos" está seleccionado, usar todos los valores disponibles
                cecos_seleccionados = cecos
            else:
                # Extraer los códigos seleccionados quitando el texto adicional
                cecos_seleccionados = [
                    int(seleccionados.split("(")[-1].strip(")"))
                ]

            # Filtrar el DataFrame
            return df[df["CeCo_A"].isin(cecos_seleccionados)], cecos_seleccionados

    def expander(dic,va, por_var):
                if va ==  'PATIO':
                    with st.expander(f"{va} ${dic[f'{va}']:,.2f}"):
                        st.write("")
                else:
                    with st.expander(f"{va} ${dic[f'{va}']:,.2f}  | {dic[f'{por_var}']:,.2f}% "):
                        st.write("")

    def expander_com(dic, dic_ly, dic_ppt, va):
        with st.expander(f"{va}: YTD ${dic[f'{va}']:,.2f} vs LY {dic_ly[f'{va}']:,.2f} vs PPT {dic_ppt[f'{va}']:,.2f}"):
            st.write(f"Alcance_LY: {dic[f'{va}']/dic_ly[f'{va}']*100:,.2f}%")
            st.write(f"Alcance_PPT: {dic[f'{va}']/dic_ppt[f'{va}']*100:,.2f}%")

    def expander_ceco(dic, dic_ppt, va):
        with st.expander(f"{va}: YTD ${dic[f'{va}']:,.2f} vs PPT {dic_ppt[f'{va}']:,.2f}"):
            st.write(f"Alcance_PPT: {dic[f'{va}']/dic_ppt[f'{va}']*100:,.2f}%")

    def calcular_meses_anteriores(mes_seleccionado):
            if isinstance(mes_seleccionado, list):
                mes_seleccionado = mes_seleccionado[0]  # Tomar el primer mes si es una lista
            # Encontrar el número del mes seleccionado
            num_mes_seleccionado = orden_meses[mes_seleccionado]
            
            # Generar los meses anteriores en orden
            meses_anteriores = [mes for mes, num in orden_meses.items() if num < num_mes_seleccionado]
            
            # Ordenar los meses anteriores en el orden correcto
            meses_anteriores.sort(key=lambda m: orden_meses[m])
            
            return meses_anteriores

    @st.cache_data 
    def calcular_estadisticas(data, metricas):
            # Crear un DataFrame vacío
            df_resultado = pd.DataFrame()

            for mes, valores in data.items():
                # Convertir cada mes en DataFrame
                df_mes = pd.DataFrame(valores)
                df_mes['MES'] = mes
                df_resultado = pd.concat([df_resultado, df_mes], ignore_index=True)

            # Filtrar solo las métricas seleccionadas
            df_resultado = df_resultado[metricas + ['MES']]
            
            # Calcular estadísticas
            estadisticas = df_resultado.describe().T[['mean', 'std']]  # Media y desviación estándar
            estadisticas['LIMITE_INFERIOR'] = estadisticas['mean'] - estadisticas['std']
            estadisticas['LIMITE_SUPERIOR'] = estadisticas['mean'] + estadisticas['std']
            estadisticas = estadisticas.reset_index().rename(columns={'index': 'METRICA'})
            return estadisticas
    @st.cache_data 
    def er_analisis (df, codigo_proyecto, meses_antes):
            er_analisis = {}
            for x in meses_antes:
                er_analisis[x] = [tabla_resumen(codigo_proyecto, [x], df)]
            return er_analisis
    def analisis(df_c, df_cat, df_cla, llave_unica):
            # Combinar DataFrames y procesar
            
            df_experimento = pd.concat([df_c, df_cat], ignore_index=True)
            df_experimento =df_experimento.drop(columns='Clasificacion_A')
            df_experimento[df_experimento.select_dtypes(include='number').columns] *= 100
            df_cla[df_cla.select_dtypes(include='number').columns] *= 100
            # Función para aplicar estilos condicionales
            def resaltar_filas(df):
                def aplicar_estilo(val, limite_inf, limite_sup):
                    if val > limite_sup:
                        return "background-color: red; color: white"
                    elif val < limite_inf:
                        return "background-color: yellow; color: black"
                    return None

                return df.style.applymap(
                    lambda val: aplicar_estilo(val, df["Límite_Inferior"].iloc[0], df["Límite_Superior"].iloc[0]),
                    subset=["Neto_Porcentual"]
                )

            # Aplicar formato de porcentaje y estilos
            df_estilizado = resaltar_filas(df_cla).format({
                "Media": "{:.2f}%",
                "Desviación_Estándar": "{:.2f}%",
                "Límite_Inferior": "{:.2f}%",
                "Límite_Superior": "{:.2f}%",
                "Neto_Porcentual": "{:.2f}%"
            })

            st.dataframe(df_estilizado)

            # Lógica de estilos en JavaScript
            row_style_js = JsCode("""
            function(params) {
                // Verificar si la fila es agrupada
                if (params.node.group) {
                    const aggregatedValue = params.node.aggData['Neto_Porcentual'];  // Valor agregado de la fila agrupada
                    const limiteSuperior = params.node.aggData['Límite_Superior'];  // Límite superior agregado
                    const limiteInferior = params.node.aggData['Límite_Inferior'];  // Límite inferior agregado

                    if (aggregatedValue > limiteSuperior) {
                        return { backgroundColor: 'red', color: 'white' };
                    } else if (aggregatedValue < limiteInferior) {
                        return { backgroundColor: 'yellow', color: 'black' };
                    }
                }

                // Aplicar estilos condicionales a las demás filas
                if (params.data) {
                    if (params.data['Neto_Porcentual'] > params.data['Límite_Superior']) {
                        return {backgroundColor: 'red', color: 'white'};
                    } else if (params.data['Neto_Porcentual'] < params.data['Límite_Inferior']) {
                        return {backgroundColor: 'yellow', color: 'black'};
                    }
                }

                return null;  // Sin estilos si no cumple las condiciones
            }
            """)

            # Configuración de opciones para AgGrid
            gb = GridOptionsBuilder.from_dataframe(df_experimento)

            # Permitir filtros, orden y agrupación
            gb.configure_default_column(filter=True, sortable=True, resizable=True)

            # Configuración de agrupación (primero por Clasificacion_A, luego por Categoria_A)
            gb.configure_column("Categoria_A", rowGroup=True, hide=True)       # Segunda agrupación (nivel inferior)

            # Aplicar lógica de estilos condicionales
            gb.configure_grid_options(getRowStyle=row_style_js)

            gb.configure_column(
                "Media",
                aggFunc="last",  # Usar el último valor precalculado
                valueFormatter="`${value.toFixed(2)}%`",
            )

            gb.configure_column(
                "Desviación_Estándar",
                aggFunc="last",
                valueFormatter="`${value.toFixed(2)}%`",
            )

            gb.configure_column(
                "Límite_Inferior",
                aggFunc="last",
                valueFormatter="`${value.toFixed(2)}%`",
            )

            gb.configure_column(
                "Límite_Superior",
                aggFunc="last",
                valueFormatter="`${value.toFixed(2)}%`",
            )

            gb.configure_column(
                "Neto_Porcentual",
                aggFunc="last",
                valueFormatter="`${value.toFixed(2)}%`",
            )

            # Generar opciones para la tabla
            grid_options = gb.build()

            # Mostrar la tabla interactiva en Streamlit
            AgGrid(
                df_experimento,
                gridOptions=grid_options,
                height=500,
                theme="streamlit",
                allow_unsafe_jscode=True,
                key=f"{llave_unica}_aggrid"
            )

            # Crear archivo para descarga
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_experimento.to_excel(writer, index=False, sheet_name="Datos")
            processed_data = output.getvalue()

            # Botón de descarga
            st.download_button(
                label="Descargar Excel",
                data=processed_data,
                file_name=f"df_cos_{llave_unica}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


    def tabla_expandible_ceco(df,df_ppt, cat, mes, pro, dic, dic_ppt, key_prefix):
            if not isinstance(pro, list):
                pro = [pro]
            columnas = ['Cuenta_Nombre_A', 'Categoria_A']
            if cat == 'INGRESO':
                df_tabla = df[df['Categoria_A'] == cat]
                df_tabla = df_tabla[df_tabla['Proyecto_A'].isin(pro)]
                df_tabla = df_tabla[df_tabla['Mes_A'].isin(mes)]
                df_tabla = df_tabla.groupby(columnas, as_index=False).agg({"Neto_A": "sum"})

                df_tabla_ppt = df_ppt[df_ppt['Categoria_A'] == cat]
                df_tabla_ppt = df_tabla_ppt[df_tabla_ppt['Proyecto_A'].isin(pro)]
                df_tabla_ppt = df_tabla_ppt[df_tabla_ppt['Mes_A'].isin(mes)]
                df_tabla_ppt = df_tabla_ppt.groupby(columnas, as_index=False).agg({"Neto_A": "sum"})

            elif cat == 'INGRESO FINANCIERO':
                df_tabla = df[df['Categoria_A'].isin(ingreso_fin)]
                df_tabla = df_tabla[df_tabla['Proyecto_A'].isin(pro)]
                df_tabla = df_tabla[df_tabla['Mes_A'].isin(mes)]
                df_tabla = df_tabla.groupby(columnas, as_index=False).agg({"Neto_A": "sum"})


                df_tabla_ppt = df_ppt[df_ppt['Categoria_A'].isin(ingreso_fin)]
                df_tabla_ppt = df_tabla_ppt[df_tabla_ppt['Proyecto_A'].isin(pro)]
                df_tabla_ppt = df_tabla_ppt[df_tabla_ppt['Mes_A'].isin(mes)]
                df_tabla_ppt = df_tabla_ppt.groupby(columnas, as_index=False).agg({"Neto_A": "sum"})
                
            else:
                df_tabla = df[df['Clasificacion_A'] == cat]
                df_tabla = df_tabla[df_tabla['Proyecto_A'].isin(pro)]
                df_tabla = df_tabla[df_tabla['Mes_A'].isin(mes)]
                df_tabla = df_tabla.groupby(columnas, as_index=False).agg({"Neto_A": "sum"})

                df_tabla_ppt = df_ppt[df_ppt['Clasificacion_A'] == cat]
                df_tabla_ppt = df_tabla_ppt[df_tabla_ppt['Proyecto_A'].isin(pro)]
                df_tabla_ppt = df_tabla_ppt[df_tabla_ppt['Mes_A'].isin(mes)]
                df_tabla_ppt = df_tabla_ppt.groupby(columnas, as_index=False).agg({"Neto_A": "sum"})
            


            # Paso 1: Realizamos las uniones de las tablas
            df_combinado = pd.merge(df_tabla, df_tabla_ppt, on=['Cuenta_Nombre_A', 'Categoria_A'], how='outer', suffixes=('', '_ppt'))
            
            # Paso 2: Llenamos las columnas faltantes con ceros
            df_combinado['YTD'] = df_combinado['Neto_A'].fillna(0)
            df_combinado['PPT'] = df_combinado['Neto_A_ppt'].fillna(0)

            # Paso 3: Calculamos las nuevas columnas para Alcance_LY y Alcance_PPT

            df_combinado['Alcance_PPT'] = df_combinado['YTD'] / df_combinado['PPT'].replace(0, float('nan'))

            # Paso 4: Reemplazamos los valores NaN con 0 en las divisiones
            df_combinado['Alcance_PPT'] = df_combinado['Alcance_PPT'].fillna(0)
            df_combinado = df_combinado.loc[:, ~df_combinado.columns.str.contains('Neto')]
            cols_alcance = df_combinado.columns[df_combinado.columns.str.contains('Alcance')]
            df_combinado[cols_alcance] = df_combinado[cols_alcance] * 100


            # Limpiar el DataFrame (muy importante para evitar errores en AgGrid)
            df_combinado = df_combinado.fillna("")  # Reemplazar NaN por cadenas vacías
            df_combinado.reset_index(drop=True, inplace=True)  # Reiniciar índices

            # Precalcular las columnas Alcance_LY y Alcance_PPT en el DataFrame
            df_combinado["Alcance_PPT"] = df_combinado.apply(
                lambda row: (row["YTD"] / row["PPT"] * 100) if row["PPT"] > 0 else 0, axis=1
            )

            # Crear valores precalculados para las filas agrupadas
            df_grouped = df_combinado.groupby("Categoria_A", as_index=False).agg({
                "YTD": "sum",
                "PPT": "sum"
            })
            df_grouped["Alcance_PPT"] = df_grouped.apply(
                lambda row: (row["YTD"] / row["PPT"] * 100) if row["PPT"] > 0 else 0, axis=1
            )

            # Combinar los datos originales con los valores agrupados
            df_combinado_or = df_combinado
            df_combinado = pd.concat([df_combinado, df_grouped], ignore_index=True)
            
            # Configurar AgGrid
            gb = GridOptionsBuilder.from_dataframe(df_combinado)
            gb.configure_default_column(groupable=True)

            # Ocultar columna pero hacerla agrupable
            gb.configure_column("Categoria_A", rowGroup=True, hide=True)

            # Configurar columnas principales
            js_code_value_formatter_currency = JsCode("""
            function(params) {
                return `$${params.value.toLocaleString()}`;
            }
            """)

            gb.configure_column(
                "YTD",
                aggFunc="last",  # Suma para filas agrupadas
                valueFormatter=js_code_value_formatter_currency,
            )

            gb.configure_column(
                "PPT",
                aggFunc="last",  # Suma para filas agrupadas
                valueFormatter=js_code_value_formatter_currency,
            )

            gb.configure_column(
                "Alcance_PPT",
                aggFunc="last",  # Usar el último valor precalculado
                valueFormatter="`${value.toFixed(2)}%`",
            )

            # Construir las opciones de la tabla
            grid_options = gb.build()
            if cat == 'COSS':
                # Mostrar la tabla dentro de un expander
                with st.expander(f"{cat}: YTD ${dic[f'{cat}']:,.2f} vs PPT {dic_ppt[f'{cat}']:,.2f}"):
                    st.write(f"Alcance PPT {dic[f'{cat}']/dic_ppt[f'{cat}']*100:,.2f}%")
                    AgGrid(
                        df_combinado,  # El DataFrame que estás usando
                        gridOptions=grid_options,  # Opciones de la tabla
                        enable_enterprise_modules=True,  # Módulos avanzados de AgGrid
                        allow_unsafe_jscode=True,  # Permite usar JsCode personalizado
                        height=400,  # Altura de la tabla
                        theme="streamlit",  # Tema de la tabla
                        key=f"{key_prefix}_aggrid_{cat}"  # Llave única para evitar conflictos
                    )

                    # Convertir el DataFrame a un archivo Excel en memoria
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                        df_combinado_or.to_excel(writer, index=False, sheet_name=f"Tabla_{cat}")
                        output.seek(0)  # Regresar el puntero al inicio del flujo de datos

                    # Agregar el botón de descarga para Excel con un unique key
                    st.download_button(
                        label=f"Descargar tabla {cat}",
                        data=output,
                        file_name=f"tabla_{cat}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"{key_prefix}_download_{cat}"  # Unique key for download button
                    )
            else:

                # Mostrar la tabla dentro de un expander
                with st.expander(f"{cat}: YTD ${dic[f'{cat}']:,.2f} vs PPT {dic_ppt[f'{cat}']:,.2f}"):
                    st.write(f"Alcance PPT {dic[f'{cat}']/dic_ppt[f'{cat}']*100:,.2f}%")
                    AgGrid(
                        df_combinado,  # El DataFrame que estás usando
                        gridOptions=grid_options,  # Opciones de la tabla
                        enable_enterprise_modules=True,  # Módulos avanzados de AgGrid
                        allow_unsafe_jscode=True,  # Permite usar JsCode personalizado
                        height=400,  # Altura de la tabla
                        theme="streamlit",  # Tema de la tabla
                        key=f"{key_prefix}_aggrid_{cat}"  # Llave única para evitar conflictos
                    )

                    # Convertir el DataFrame a un archivo Excel en memoria
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                        df_combinado_or.to_excel(writer, index=False, sheet_name=f"Tabla_{cat}")
                        output.seek(0)  # Regresar el puntero al inicio del flujo de datos

                    # Agregar el botón de descarga para Excel con un unique key
                    st.download_button(
                        label=f"Descargar tabla {cat}",
                        data=output,
                        file_name=f"tabla_{cat}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"{key_prefix}_download_{cat}"  # Unique key for download button
                    )

    #pagina resumen
    if selected == "Resumen":
        st.title("Resumen")
        
        meses_seleccionados, mes, _ = meses()
        resumen_proyectos = {proyecto: tabla_resumen(proyecto, meses_seleccionados, df) for proyecto in proyectos_activos}
    
        resumen_todos = tabla_resumen(proyectos_archivo, meses_seleccionados, df)
    

        # Convertir resumen_proyectos a DataFrame
        df_resumen_proyectos = pd.DataFrame.from_dict(resumen_proyectos, orient='index')
        df_resumen_proyectos.reset_index(inplace=True)
        df_resumen_proyectos.rename(columns={'index': 'Proyecto'}, inplace=True)

        # Convertir resumen_todos a DataFrame y añadir columna "Proyecto" con el valor "Todos"
        df_resumen_todos = pd.DataFrame([resumen_todos])
        df_resumen_todos['Proyecto'] = "ESGARI"

        # Combinar ambos DataFrames
        df_combinado = pd.concat([df_resumen_proyectos, df_resumen_todos], ignore_index=True)
            # Reemplazar los códigos de proyecto por sus nombres
        df_combinado['Proyecto'] = df_combinado['Proyecto'].replace(proyecto_dict_oh_p)
        
        # Transponer el DataFrame combinado
        df_transpuesto = df_combinado.set_index("Proyecto").transpose()
        
        eliminar = ['PATIO', 'INGRESO FINANCIERO', 'GASTOS FINANCIEROS', '% PATIO']
        df_transpuesto = df_transpuesto.drop(eliminar, axis= 0)
    
    # Función para formatear celdas en pesos
        def formatear_pesos(valor):
            try:
                return f"${valor:,.0f}"
            except (ValueError, TypeError):
                return valor  # Si no es numérico, devolver el valor tal cual

        # Función para formatear celdas en porcentaje
        def formatear_porcentaje(valor):
            try:
                return f"{float(valor):.2f}%"
            except (ValueError, TypeError):
                return valor  # Si no es numérico, devolver el valor tal cual

        # Especificar las filas que se deben formatear como porcentaje (índices o nombres)
        filas_porcentaje = [
        'MG. bruto',
        'MG. OP.',
        '% OH',
        'MG. EBIT',
        'MG. EBT',
        'MG. EBITDA'
    ]


        # Aplicar formato según las filas
        def aplicar_formato_personalizado(fila):
            if fila.name in filas_porcentaje:  # Si la fila está en las especificadas
                return fila.apply(formatear_porcentaje)  # Formatear como porcentaje
            else:
                return fila.apply(formatear_pesos)  # Formatear como pesos

        # Aplicar la función personalizada a las filas del DataFrame transpuesto
        df_transpuesto_formateado = df_transpuesto.apply(aplicar_formato_personalizado, axis=1)

        # Mostrar el DataFrame transpuesto y formateado en Streamlit
        st.subheader("Resumen de Proyectos")
  

        def generar_tabla_con_estilo(df):
            # Lista de nombres de las filas que deseas marcar con el color azul marino
            filas_destacadas = ['MG. bruto', 'MG. OP.', '% OH', 'MG. EBIT', 'MG. EBT', 'MG. EBITDA']

            # Función para aplicar estilos a todo el DataFrame
            def aplicar_estilos(data):
                # Crear un DataFrame vacío con la misma forma que el DataFrame de entrada
                estilos = pd.DataFrame('', index=data.index, columns=data.columns)
                
                for row_index in data.index:
                    if row_index in filas_destacadas:
                        # Si la fila está en filas destacadas, aplica azul marino y texto blanco
                        estilos.loc[row_index, :] = 'background-color: #001f3f; color: white;'
                    else:
                        # Filas normales: alternar entre blanco y gris
                        estilos.loc[row_index, :] = 'background-color: white; color: black;'
                        if data.index.get_loc(row_index) % 2 == 1:  # Filas pares en gris
                            estilos.loc[row_index, :] = 'background-color: #f9f9f9; color: black;'
                return estilos

            # Crear estilos para encabezados
            estilos_filas = [
                {'selector': 'thead th', 'props': 'background-color: #001f3f; color: white; font-weight: bold; font-size: 14px;'},
            ]

            # Aplicar estilos y convertir el DataFrame en HTML
            html = (
                df.style.apply(aplicar_estilos, axis=None)  # Aplica los estilos a todo el DataFrame
                .set_table_styles(estilos_filas)           # Estilo para encabezados
                .set_properties(**{'font-size': '12px'})   # Configurar tamaño de fuente general
                .format(na_rep='-', precision=2)           # Formatear valores numéricos
                .render()
            )

            return html









        # Generar la tabla con estilo
        tabla_estilizada = generar_tabla_con_estilo(df_transpuesto_formateado)

        # Mostrar en Streamlit
    
        st.markdown(tabla_estilizada, unsafe_allow_html=True)



        # Convertir el DataFrame a Excel en memoria
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            df_transpuesto_formateado.to_excel(writer, index=True, sheet_name='Sheet1')

        # Botón de descarga
        st.download_button(
            label="Descargar Resumen en Excel",
            data=excel_buffer.getvalue(),
            file_name="dataframe.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )



        # Calcular ingresos y egresos
        ingreso, egreso = in_egre_mes_a_mes(proyectos_archivo, df, meses_archivo_ordenados)

        # Crear y mostrar el gráfico
        fig = crear_grafico_in_egre(ingreso, egreso, meses_archivo_ordenados)
        st.plotly_chart(fig)

        # Seleccionar los proyectos
        pro = st.multiselect('Selecciona el proyecto', options=opciones_proyecto, default='CHALCO (1001)')

        #prediccion lineal
        prediccion = st.checkbox('Ver prediccion lineal para cierre de mes')
        
        # Calcular ingresos por proyecto
        ingreso_por_proyecto = {}

        # Comprobar si "Todos los proyectos" está seleccionado
        if "Todos los proyectos" in pro:
            # Calcular la suma de ingresos de todos los proyectos
            ingreso_total, _ = in_egre_mes_a_mes(proyectos_archivo, df, meses_archivo_ordenados)
            ingreso_por_proyecto['Todos los proyectos'] = ingreso_total

            # Filtrar los proyectos seleccionados (sin incluir "Todos los proyectos")
            proyectos_seleccionados = [int(p.split()[-1].strip("()")) for p in pro if p != "Todos los proyectos"]
        else:
            # Si no se seleccionó "Todos los proyectos", incluir los proyectos seleccionados
            proyectos_seleccionados = [int(p.split()[-1].strip("()")) for p in pro]

        # Calcular ingresos para los proyectos seleccionados
        for codigo in proyectos_seleccionados:
            ingreso, _ = in_egre_mes_a_mes([codigo], df, meses_archivo_ordenados)
            ingreso_por_proyecto[codigo] = ingreso

        if prediccion:
            # Calcular días transcurridos y días totales
            dias_transcurridos = fecha_actualizacion.day
            dias_totales = calendar.monthrange(fecha_actualizacion.year, fecha_actualizacion.month)[1]

            # Ajustar el ingreso del último mes
            ultimo_mes = list(meses_archivo_ordenados)[-1]  # Obtener el último mes

            ingresos_ajustados = {}

            for proyecto, ingresos_mensuales in ingreso_por_proyecto.items():
                # Verificar que el último mes está en el diccionario
                if ultimo_mes in ingresos_mensuales:
                    # Hacer una copia de los datos del proyecto
                    ingresos_ajustados[proyecto] = ingresos_mensuales.copy()
                    # Ajustar el ingreso del último mes
                    ingresos_ajustados[proyecto][ultimo_mes] = (
                        ingresos_mensuales[ultimo_mes] / dias_transcurridos
                    ) * dias_totales
                else:
                    st.warning(f"El proyecto {proyecto} no tiene datos para el mes {ultimo_mes}.")

        # Si no hay predicción, usar los ingresos originales
        else:
            ingresos_ajustados = ingreso_por_proyecto

            
            # Crear el gráfico con todas las líneas
        fig_egreso = crear_grafico_egre(ingresos_ajustados, meses_archivo_ordenados)

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig_egreso)


        # Token de API directamente en el archivo
        API_KEY = 'eef020dafff1667cc5fb4dc1de10cf314857367cbd5c881511679bb2e7a7433a'

            # URL base para obtener el índice de precios al consumidor (IPC)
        URL_BASE = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SP1/datos/"

            # Diccionario de meses para seleccionar en la barra lateral
        mes_seleccionado = orden_meses[mes]  # Convierte el nombre del mes al número correspondiente
        @st.cache_data   
        def obtener_ipc_mensual(fecha_fin):
                """
                Obtiene el IPC mensual hasta la fecha fin especificada.
                """
                # Definir la fecha de inicio para tener un año de datos
                anio_inicio = fecha_fin.year - 1
                fecha_inicio = f"{anio_inicio}-{fecha_fin.month:02d}-01"
                fecha_fin_str = fecha_fin.strftime("%Y-%m-%d")
                
                # Construir URL completa
                url = f"{URL_BASE}{fecha_inicio}/{fecha_fin_str}?token={API_KEY}"

                # Solicitar datos a la API de Banxico
                response = requests.get(url)
                if response.status_code != 200:
                    st.write("Error al obtener datos de Banxico:", response.status_code)
                    st.write("Mensaje de respuesta:", response.text)
                    raise Exception("Error al obtener datos de Banxico:", response.status_code)
                
                # Procesar datos en formato JSON
                datos = response.json()['bmx']['series'][0]['datos']
                df = pd.DataFrame(datos)
                df['fecha'] = pd.to_datetime(df['fecha'], format='%d/%m/%Y')
                df['dato'] = pd.to_numeric(df['dato'], errors='coerce')
                
                return df
        @st.cache_data   
        def calcular_inflacion_anual(mes_seleccionado):
                """
                Calcula la inflación anual hasta el mes seleccionado.
                """
                # Fecha actualizada hasta el mes seleccionado en el año actual
                fecha_fin = datetime(datetime.now().year, mes_seleccionado, 1)
                
                # Obtener el IPC mensual hasta el mes seleccionado
                ipc_df = obtener_ipc_mensual(fecha_fin)
                
                # Verificar si el último dato disponible es anterior al mes seleccionado
                ultima_fecha_disponible = ipc_df['fecha'].max()
                if fecha_fin > ultima_fecha_disponible:
                    st.write(f"Los datos para el resumen de este mes aún no están completos.")
                    st.subheader(f'Resumen parcial al {fecha_actualizacion_texto} ESGARI')
                    resumen = tabla_resumen(proyectos_archivo,meses_hasta_seleccionado, df)
                    resumen_ly = tabla_resumen(proyectos_archivo_ly,meses_hasta_seleccionado,df_ly)
                    resumen_ppt = tabla_resumen(proyectos_archivo_ppt,meses_hasta_seleccionado,df_ppt)
                    
            # Ingresos YTD
                    st.write(f"Los ingresos YTD alcanzaron **${resumen['INGRESO']:,.2f}**. "
                            f"Comparado con el año pasado (LY), la diferencia es de **{(resumen['INGRESO'] / resumen_ly['INGRESO']) * 100 - 100:,.2f}%**. "
                            f"Frente al presupuesto (PPT), la diferencia es de **{(resumen['INGRESO'] / resumen_ppt['INGRESO']) * 100 - 100:,.2f}%**.")

                    # EBITDA
                    st.write(f"El EBITDA alcanzó un valor de **${resumen['EBITDA']:,.2f}**, comparado con el año pasado: **{resumen_ly['EBITDA']:,.2f}**. "
                            f"El cambio porcentual respecto al año anterior es de **{resumen['EBITDA'] / resumen_ly['EBITDA'] * 100 - 100:,.2f}%**.")

                    # Costos y Gastos Administrativos
                    st.write(f"El costo de los servicios vendidos representó un **{(resumen['COSS']) / resumen['INGRESO'] * 100:,.2f}%** de los ingresos. "
                            f"El gasto administrativo fue del **{resumen['G.ADMN'] / resumen['INGRESO'] * 100:,.2f}%** de los ingresos.")

                    # Utilidad de Operación
                    st.write(f"La utilidad de operación fue de **${resumen['UO']:,.2f}**, representando un **{resumen['UO'] / resumen['INGRESO'] * 100:,.2f}%** de los ingresos. ")
                    st.write(f"- Utilidad operativa esperada: 26%. ")        
                    st.write(f"- Diferencia respecto a lo esperado: **{resumen['UO'] / resumen['INGRESO'] * 100 - 26:,.2f}%**.")      

                    # Overhead
                    st.write(f"El overhead representó un **{resumen['OH'] / resumen['INGRESO'] * 100:,.2f}%** de los ingresos. ")
                    st.write(f"- Porcentaje esperado de overhead: 11.5%. ")       
                    st.write( f"- Diferencia respecto a lo esperado: **{resumen['OH'] / resumen['INGRESO'] * 100 - 11.5:,.2f}%**.")          
                    # Inicializar un diccionario vacío para guardar los resultados
                    resumen = {}
                    
                    # Iterar sobre cada proyecto activo
                    for pro in proyectos_activos:
                        # Calcular el resumen para el proyecto actual
                        resumen[pro] = tabla_resumen(pro, meses_hasta_seleccionado, df)

                    # Umbral de utilidad operativa esperada
                    utilidad_esperada = 23.0

                    # Clasificar los proyectos
                    arriba_utilidad = []
                    debajo_utilidad = []
                    en_perdida = []

                    for proyecto, datos in resumen.items():
                        mg_op = datos["MG. OP."]
                        nombre = proyecto_dict_oh_p.get(proyecto, f"Proyecto {proyecto}")
                        if mg_op > utilidad_esperada:
                            arriba_utilidad.append((nombre, mg_op))
                        elif mg_op > 0:
                            debajo_utilidad.append((nombre, mg_op))
                        else:
                            en_perdida.append((nombre, mg_op))

                    # Generar el texto mejorado con nombres de proyectos
                    texto = (
                        "De acuerdo con el análisis, los proyectos con una utilidad operativa superior al "
                        "23% esperado son: "
                    )
                    texto += ", ".join(
                        [f"{nombre} con {mg_op:.2f}%" for nombre, mg_op in arriba_utilidad]
                    )
                    texto += ".\n\nPor otro lado, los proyectos con utilidad operativa positiva, pero por "
                    texto += "debajo del umbral esperado, incluyen: "
                    texto += ", ".join(
                        [f"{nombre} con {mg_op:.2f}%" for nombre, mg_op in debajo_utilidad]
                    )
                    texto += ".\n\nFinalmente, los proyectos que actualmente presentan pérdidas son: "
                    texto += ", ".join(
                        [f"{nombre} con {mg_op:.2f}%" for nombre, mg_op in en_perdida]
                    )
                    

                    # Mostrar el resultado
                    st.write(texto)
                    return None
                
                # Obtener el IPC del mes seleccionado del año actual y del año anterior
                ipc_actual = ipc_df[ipc_df['fecha'] == fecha_fin]['dato'].values[0]
                fecha_anio_anterior = fecha_fin.replace(year=fecha_fin.year - 1)
                ipc_anterior = ipc_df[ipc_df['fecha'] == fecha_anio_anterior]['dato'].values[0]
                
                # Calcular la inflación anual
                inflacion_anual = ((ipc_actual - ipc_anterior) / ipc_anterior) * 100
                return inflacion_anual

            # Calcular y mostrar la inflación anual en la aplicación de Streamlit
        mes_seleccionado = st.selectbox('Resumen de ESGARI hasta mes', meses_archivo_ordenados)
        mes_seleccionado_ori = mes_seleccionado
        # Buscar la posición del mes seleccionado  
        indice_mes = meses_archivo_ordenados.index(mes_seleccionado)

        # Crear una sublista con el mes seleccionado y los anteriores
        meses_hasta_seleccionado = meses_archivo_ordenados[:indice_mes + 1]

        
        mes_seleccionado_num = orden_meses[mes_seleccionado] 
        try:
                inflacion_anual = calcular_inflacion_anual(mes_seleccionado_num)
                if inflacion_anual is not None:
                    resumen = tabla_resumen(proyectos_archivo,meses_hasta_seleccionado, df)
                    resumen_ly = tabla_resumen(proyectos_archivo_ly,meses_hasta_seleccionado,df_ly)
                    resumen_ppt = tabla_resumen(proyectos_archivo_ppt,meses_hasta_seleccionado,df_ppt)
                    st.write(f"Inflación anual hasta el mes de {mes_seleccionado_ori}: {inflacion_anual:.2f}%")
                    st.subheader(f'Resumen cierre de {mes_seleccionado_ori} ESGARI')
                    st.write(f"""
                    Los ingresos YTD alcanzaron **${resumen['INGRESO']:,.2f}**. Comparado con el año pasado (LY), 
                    la diferencia es de **{(resumen['INGRESO'] / resumen_ly['INGRESO'] - 1) * 100:,.2f}%**, y 
                    ajustando por la inflación del año pasado, el cambio real es de **{(resumen['INGRESO'] / resumen_ly['INGRESO'] - 1) * 100 - inflacion_anual:,.2f}%**.

                    Frente al presupuesto (PPT), la diferencia en INGRESOS es de **{(resumen['INGRESO'] / resumen_ppt['INGRESO'] - 1) * 100:,.2f}%**. 
                    """)


                    # EBITDA
                    st.write(f"El EBITDA alcanzó un valor de **${resumen['EBITDA']:,.2f}**, comparado con el año pasado: **{resumen_ly['EBITDA']:,.2f}**. "
                            f"El cambio porcentual respecto al año anterior es de **{resumen['EBITDA'] / resumen_ly['EBITDA'] * 100 - 100:,.2f}%**.")

                    # Costos y Gastos Administrativos
                    st.write(f"El costo de los servicios vendidos representó un **{(resumen['COSS']) / resumen['INGRESO'] * 100:,.2f}%** de los ingresos. "
                            f"El gasto administrativo fue del **{resumen['G.ADMN'] / resumen['INGRESO'] * 100:,.2f}%** de los ingresos.")

                    # Utilidad de Operación
                    st.write(f"La utilidad de operación fue de **${resumen['UO']:,.2f}**, representando un **{resumen['UO'] / resumen['INGRESO'] * 100:,.2f}%** de los ingresos. ")
                    st.write(f"- Utilidad operativa esperada: 26%. ")        
                    st.write(f"- Diferencia respecto a lo esperado: **{resumen['UO'] / resumen['INGRESO'] * 100 - 26:,.2f}%**.")      

                    # Overhead
                    st.write(f"El overhead representó un **{resumen['OH'] / resumen['INGRESO'] * 100:,.2f}%** de los ingresos. ")
                    st.write(f"- Porcentaje esperado de overhead: 11.5%. ")       
                    st.write( f"- Diferencia respecto a lo esperado: **{resumen['OH'] / resumen['INGRESO'] * 100 - 11.5:,.2f}%**.")          
                    # Inicializar un diccionario vacío para guardar los resultados
                    resumen = {}
                    
                    # Iterar sobre cada proyecto activo
                    for pro in proyectos_activos:
                        # Calcular el resumen para el proyecto actual
                        resumen[pro] = tabla_resumen(pro, meses_hasta_seleccionado, df)

                    # Umbral de utilidad operativa esperada
                    utilidad_esperada = 23.0

                    # Clasificar los proyectos
                    arriba_utilidad = []
                    debajo_utilidad = []
                    en_perdida = []

                    for proyecto, datos in resumen.items():
                        mg_op = datos["MG. OP."]
                        nombre = proyecto_dict_oh_p.get(proyecto, f"Proyecto {proyecto}")
                        if mg_op > utilidad_esperada:
                            arriba_utilidad.append((nombre, mg_op))
                        elif mg_op > 0:
                            debajo_utilidad.append((nombre, mg_op))
                        else:
                            en_perdida.append((nombre, mg_op))

                    # Generar el texto mejorado con nombres de proyectos
                    texto = (
                        "De acuerdo con el análisis, los proyectos con una utilidad operativa superior al "
                        "23% esperado son: "
                    )
                    texto += ", ".join(
                        [f"{nombre} con {mg_op:.2f}%" for nombre, mg_op in arriba_utilidad]
                    )
                    texto += ".\n\nPor otro lado, los proyectos con utilidad operativa positiva, pero por "
                    texto += "debajo del umbral esperado, incluyen: "
                    texto += ", ".join(
                        [f"{nombre} con {mg_op:.2f}%" for nombre, mg_op in debajo_utilidad]
                    )
                    texto += ".\n\nFinalmente, los proyectos que actualmente presentan pérdidas son: "
                    texto += ", ".join(
                        [f"{nombre} con {mg_op:.2f}%" for nombre, mg_op in en_perdida]
                    )
                    texto += ".\n\nEste análisis permite identificar las áreas de oportunidad y los proyectos que están superando las expectativas."

                    # Mostrar el resultado
                    st.write(texto)
                    
        except Exception as e:
                st.write("Ocurrió un error:", e)


    elif selected == "Estado de Resultado":
        st.title("Estado de Resultado")
        
        pro, codigo_proyecto = filtro_pro()
        df_er, cecos_seleccionados = filtrar_cecos(df, cecos, valores)
        meses_seleccionados, mes, _ = meses()
        columnas = ['Cuenta_Nombre_A', 'Categoria_A']
        er = tabla_resumen(codigo_proyecto,meses_seleccionados,df_er)
        # Llamar a la función con expanders para las tablas
        tabla_expandible(df_er, 'INGRESO', meses_seleccionados, codigo_proyecto, er, key_prefix="ingreso")
        tabla_expandible(df_er, 'COSS', meses_seleccionados, codigo_proyecto, er, key_prefix="coss")
        expander(er,'Ut. Bruta','MG. bruto')
        tabla_expandible(df_er, 'G.ADMN', meses_seleccionados, codigo_proyecto, er, key_prefix="g.admn")
        expander(er,'UO','MG. OP.')
        expander(er,'OH','% OH')
        expander(er,'EBIT','MG. EBIT')
        tabla_expandible(df_er, 'GASTOS FINANCIEROS', meses_seleccionados, codigo_proyecto, er, key_prefix="gfin")
        tabla_expandible(df_er, 'INGRESO FINANCIERO', meses_seleccionados, codigo_proyecto, er, key_prefix="ifin")
        expander(er,'EBT','MG. EBT')
        expander(er,'EBITDA','MG. EBITDA')

        
    elif selected == "Comparativa":
        tabs = ['Comparativa Horizontal', 'Comparativa Vertical']
        st.tabs(tabs)
        st.title("Comparativa")
        pro, codigo_proyecto = filtro_pro()
        df_er, cecos_seleccionados = filtrar_cecos(df, cecos, valores)
        df_er_ly = df_ly[df_ly['CeCo_A'].isin(cecos_seleccionados)]
        df_er_ppt = df_ppt[df_ppt['CeCo_A'].isin(cecos_seleccionados)]
        meses_seleccionados, mes, _ = meses()
        
        columnas = ['Cuenta_Nombre_A', 'Categoria_A']
        er_ly = tabla_resumen(codigo_proyecto,meses_seleccionados,df_er_ly)
        er_ppt = tabla_resumen(codigo_proyecto,meses_seleccionados,df_er_ppt)
        er = tabla_resumen(codigo_proyecto,meses_seleccionados,df_er)
        tabla_expandible_comp(df_er,df_er_ly,df_er_ppt,'INGRESO',meses_seleccionados,codigo_proyecto, er, er_ly, er_ppt,  key_prefix="ing")
        tabla_expandible_comp(df_er,df_er_ly,df_er_ppt,'COSS',meses_seleccionados,codigo_proyecto, er, er_ly, er_ppt,  key_prefix="coss")
        expander_com(er, er_ly, er_ppt, 'Ut. Bruta')
        tabla_expandible_comp(df_er,df_er_ly,df_er_ppt,'G.ADMN',meses_seleccionados,codigo_proyecto, er, er_ly, er_ppt,  key_prefix="g.admn")
        expander_com(er, er_ly, er_ppt, 'UO')
        expander_com(er, er_ly, er_ppt, 'OH')
        expander_com(er, er_ly, er_ppt, 'EBIT')
        tabla_expandible_comp(df_er,df_er_ly,df_er_ppt,'GASTOS FINANCIEROS',meses_seleccionados,codigo_proyecto, er, er_ly, er_ppt,  key_prefix="gfin")
        tabla_expandible_comp(df_er,df_er_ly,df_er_ppt,'INGRESO FINANCIERO',meses_seleccionados,codigo_proyecto, er, er_ly, er_ppt,  key_prefix="ingf")
        expander_com(er, er_ly, er_ppt, 'EBT')
        expander_com(er, er_ly, er_ppt, 'EBITDA')


    elif selected == "Análisis":
        st.subheader("Análisis Historíco")
        emp, cod_emp = filtro_emp()
        pro, codigo_proyecto = filtro_pro()
        if isinstance(codigo_proyecto, int):
                codigo_proyecto = [codigo_proyecto]
        meses_seleccionados, mes, mes_ini = meses()
        
        if mes_ini == ['ene.'] or mes_ini == ['feb.']:
            opciones_analisis = ['LY']
        else:
            opciones_analisis = ['YTD', 'LY']
        # Crear el radio
        seleccionada_analisis = st.radio('Analisis contra:', opciones_analisis)


        df_analisis_ly = df_ly[df_ly['Empresa_A'].isin(cod_emp)]

        df_analisis = df[df['Empresa_A'].isin(cod_emp)]
        
        df_analisis = df_analisis[df_analisis['Proyecto_A'].isin(codigo_proyecto)]
        df_analisis_ly = df_analisis_ly[df_analisis_ly['Proyecto_A'].isin(codigo_proyecto)]

        df_analisis_ing = df_analisis[df_analisis['Categoria_A'] == 'INGRESO']
        df_analisis_ing_ly = df_analisis_ly[df_analisis_ly['Categoria_A'] == 'INGRESO']
        df_analisis_ing = df_analisis_ing.groupby('Mes_A', as_index=False).agg({'Neto_A':'sum'})
        df_analisis_ing_ly = df_analisis_ing_ly.groupby('Mes_A', as_index=False).agg({'Neto_A':'sum'})

        df_analisis = df_analisis[~(df_analisis['Categoria_A'] == 'INGRESO')]
        df_analisis_ly = df_analisis_ly[~(df_analisis_ly['Categoria_A'] == 'INGRESO')]

        columnas = ['Cuenta_Nombre_A', 'Categoria_A', 'Mes_A', 'Clasificacion_A']
        df_analisis = df_analisis.groupby(columnas, as_index=False).agg({"Neto_A": "sum"})
        df_analisis_ly = df_analisis_ly.groupby(columnas, as_index=False).agg({"Neto_A": "sum"})

        df_analisis_cat = df_analisis.groupby(['Categoria_A', 'Clasificacion_A','Mes_A'], as_index=False).agg({"Neto_A":"sum"})
        df_analisis_cat_ly = df_analisis_ly.groupby(['Categoria_A', 'Clasificacion_A','Mes_A'], as_index=False).agg({"Neto_A":"sum"})

        df_analisis_cla = df_analisis.groupby(['Clasificacion_A', 'Mes_A'], as_index=False).agg({"Neto_A":"sum"})
        df_analisis_cla_ly = df_analisis_ly.groupby(['Clasificacion_A', 'Mes_A'], as_index=False).agg({"Neto_A":"sum"})

        # Crear un diccionario para mapear 'Mes_A' a 'Neto_A' en df_analisis_ing
        neto_mes_ing = df_analisis_ing.set_index('Mes_A')['Neto_A'].to_dict()
        neto_mes_ing_ly = df_analisis_ing_ly.set_index('Mes_A')['Neto_A'].to_dict()


        # Mantener la columna original y agregar una columna para el Neto porcentual
        df_analisis['Neto_Porcentual'] = df_analisis.apply(
            lambda row: row['Neto_A'] / neto_mes_ing[row['Mes_A']] if row['Mes_A'] in neto_mes_ing else None,
            axis=1
        )
        df_analisis_ly['Neto_Porcentual'] = df_analisis_ly.apply(
            lambda row: row['Neto_A'] / neto_mes_ing_ly[row['Mes_A']] if row['Mes_A'] in neto_mes_ing_ly else None,
            axis=1
        )
        df_analisis_cat['Neto_Porcentual'] = df_analisis_cat.apply(
            lambda row: row['Neto_A'] / neto_mes_ing[row['Mes_A']] if row['Mes_A'] in neto_mes_ing else None,
            axis=1
        )
        df_analisis_cat_ly['Neto_Porcentual'] = df_analisis_cat_ly.apply(
            lambda row: row['Neto_A'] / neto_mes_ing_ly[row['Mes_A']] if row['Mes_A'] in neto_mes_ing_ly else None,
            axis=1
        )
        df_analisis_cla['Neto_Porcentual'] = df_analisis_cla.apply(
            lambda row: row['Neto_A'] / neto_mes_ing[row['Mes_A']] if row['Mes_A'] in neto_mes_ing else None,
            axis=1
        )
        df_analisis_cla_ly['Neto_Porcentual'] = df_analisis_cla_ly.apply(
            lambda row: row['Neto_A'] / neto_mes_ing_ly[row['Mes_A']] if row['Mes_A'] in neto_mes_ing_ly else None,
            axis=1
        )

        meses_antes = calcular_meses_anteriores(mes_ini)
        if seleccionada_analisis == 'YTD':

            df_analisis_std = df_analisis[df_analisis['Mes_A'].isin(meses_antes)]
            df_analisis_cat_std = df_analisis_cat[df_analisis_cat['Mes_A'].isin(meses_antes)]
            df_analisis_cla_std = df_analisis_cla[df_analisis_cla['Mes_A'].isin(meses_antes)]
        else:
            df_analisis_std = df_analisis_ly
            df_analisis_cat_std = df_analisis_cat_ly
            df_analisis_cla_std = df_analisis_cla_ly

        df_analisis_mes = df_analisis[df_analisis['Mes_A'].isin(meses_seleccionados)]
        df_analisis_cat_mes = df_analisis_cat[df_analisis_cat['Mes_A'].isin(meses_seleccionados)]
        df_analisis_cla_mes = df_analisis_cla[df_analisis_cla['Mes_A'].isin(meses_seleccionados)]

        # Cálculo de estadísticas agrupadas por Cuenta_Nombre_A y Categoria_A
        df_analisis_std = df_analisis_std.groupby(['Cuenta_Nombre_A', 'Categoria_A','Clasificacion_A']).agg(
            Media=('Neto_Porcentual', 'mean'),
            Desviación_Estándar=('Neto_Porcentual', 'std')
        ).reset_index()
        df_analisis_cat_std = df_analisis_cat_std.groupby(['Categoria_A','Clasificacion_A']).agg(
            Media=('Neto_Porcentual', 'mean'),
            Desviación_Estándar=('Neto_Porcentual', 'std')
        ).reset_index()
        df_analisis_cla_std = df_analisis_cla_std.groupby(['Clasificacion_A']).agg(
            Media=('Neto_Porcentual', 'mean'),
            Desviación_Estándar=('Neto_Porcentual', 'std')
        ).reset_index()
        
        # Calcular límites superior e inferior
        df_analisis_std['Límite_Inferior'] = df_analisis_std['Media'] - df_analisis_std['Desviación_Estándar']
        df_analisis_std['Límite_Superior'] = df_analisis_std['Media'] + df_analisis_std['Desviación_Estándar']

        df_analisis_cat_std['Límite_Inferior'] = df_analisis_cat_std['Media'] - df_analisis_cat_std['Desviación_Estándar']
        df_analisis_cat_std['Límite_Superior'] = df_analisis_cat_std['Media'] + df_analisis_cat_std['Desviación_Estándar']

        df_analisis_cla_std['Límite_Inferior'] = df_analisis_cla_std['Media'] - df_analisis_cla_std['Desviación_Estándar']
        df_analisis_cla_std['Límite_Superior'] = df_analisis_cla_std['Media'] + df_analisis_cla_std['Desviación_Estándar']
        
        df_combined = pd.merge(
            df_analisis_std,
            df_analisis_mes[['Cuenta_Nombre_A', 'Categoria_A','Neto_Porcentual']],
            on=['Cuenta_Nombre_A', 'Categoria_A'],
            how='left'
        )
        df_combined_cat = pd.merge(
            df_analisis_cat_std,
            df_analisis_cat_mes[['Categoria_A','Clasificacion_A','Neto_Porcentual']],
            on=['Categoria_A','Clasificacion_A'],
            how='left'
        )
        df_combined_cla = pd.merge(
            df_analisis_cla_std,
            df_analisis_cla_mes[['Clasificacion_A','Neto_Porcentual']],
            on=['Clasificacion_A'],
            how='left'
        )
        df_combined = df_combined.fillna(0)
        df_combined_cat = df_combined_cat.fillna(0)
        df_combined_cla = df_combined_cla.fillna(0)
        # Crear DataFrames filtrados
        df_cos = df_combined[df_combined['Clasificacion_A'] == 'COSS']
        df_gadmn = df_combined[df_combined['Clasificacion_A'] == 'G.ADMN']
        df_gfin = df_combined[df_combined['Clasificacion_A'] == 'GASTOS FINANCIEROS']
        df_ingfin = df_combined[df_combined['Clasificacion_A'] == 'INGRESO']

        df_cos_cat = df_combined_cat[df_combined_cat['Clasificacion_A'] == 'COSS']
        df_gadmn_cat = df_combined_cat[df_combined_cat['Clasificacion_A'] == 'G.ADMN']
        df_gfin_cat = df_combined_cat[df_combined_cat['Clasificacion_A'] == 'GASTOS FINANCIEROS']
        df_ingfin_cat = df_combined_cat[df_combined_cat['Clasificacion_A'] == 'INGRESO']

        df_cos_cla = df_combined_cla[df_combined_cla['Clasificacion_A'] == 'COSS']
        df_gadmn_cla = df_combined_cla[df_combined_cla['Clasificacion_A'] == 'G.ADMN']
        df_gfin_cla = df_combined_cla[df_combined_cla['Clasificacion_A'] == 'GASTOS FINANCIEROS']
        df_ingfin_cla = df_combined_cla[df_combined_cla['Clasificacion_A'] == 'INGRESO']

            # Llenar el DataFrame con los resultados de tabla_resumen
        
        if seleccionada_analisis == 'YTD':
            er_analisis = er_analisis (df, codigo_proyecto, meses_antes)
        else: 
            er_analisis = er_analisis (df_ly, codigo_proyecto, todos_los_meses)

        # Métricas seleccionadas
        metricas_seleccionadas = ["% PATIO", "MG. bruto", "MG. OP.", "% OH", "MG. EBIT", "MG. EBT", "MG. EBITDA"]

        # Calcular estadísticas
        estadisticas_df = calcular_estadisticas(er_analisis, metricas_seleccionadas)

        # Mostrar tabla de resultados
        er_mes = tabla_resumen(codigo_proyecto, meses_seleccionados, df)
        er_mes_df = pd.DataFrame([er_mes]).T.reset_index()
        er_mes_df = er_mes_df[er_mes_df['index'].isin(metricas_seleccionadas)]
        estadisticas_df['Neto_Porcentual'] = er_mes_df[0].reset_index(drop=True)

        def resaltar_filas(row):
            if row['Neto_Porcentual'] > row['LIMITE_SUPERIOR']:
                return ['background-color: red'] * len(row)
            elif row['Neto_Porcentual'] < row['LIMITE_INFERIOR']:
                return ['background-color: yellow'] * len(row)
            else:
                return [''] * len(row)

        def expander_analisis(va, df):
            with st.expander(f'{va}'):
                df_va = df[df['METRICA'] == va]
            
                # Aplicar formato condicional y de porcentaje
                styled_df = (df_va.style
                            .apply(resaltar_filas, axis=1)  # Aplicar formato condicional
                            .format({
                                'Neto_Porcentual': '{:.2f}%', 
                                'LIMITE_SUPERIOR': '{:.2f}%', 
                                'LIMITE_INFERIOR': '{:.2f}%'
                            }))  # Formato de porcentaje
                st.write(styled_df)

        # Mostrar cada DataFrame en un expander con tabs
        with st.expander("COSS"):
            analisis(df_cos, df_cos_cat, df_cos_cla, 'coss')
        expander_analisis('% PATIO', estadisticas_df)
        expander_analisis('MG. bruto', estadisticas_df)
        with st.expander("G.ADMN"):
            analisis(df_gadmn, df_gadmn_cat,df_gadmn_cla, 'g.admn')
        expander_analisis('MG. OP.', estadisticas_df)
        expander_analisis('% OH', estadisticas_df)
        expander_analisis('MG. EBIT', estadisticas_df)
        with st.expander("GASTOS FINANCIEROS"):
            analisis(df_gfin, df_gfin_cat,df_gfin_cla, 'gfin')
        with st.expander("INGRESOS FINANCIEROS"):
            analisis(df_ingfin, df_ingfin_cat,df_ingfin_cla, 'ingfin')
        expander_analisis('MG. EBT', estadisticas_df)
        expander_analisis('MG. EBITDA', estadisticas_df)
                    

    elif selected == "Comparativa CeCo":
        st.title("Comparativa Centro de Costos")
    
        df_er, cecos_seleccionados = filtrar_cecos(df, cecos, valores)
        df_er_ppt = df_ppt[df_ppt['CeCo_A'].isin(cecos_seleccionados)]
        
        meses_seleccionados, mes, _ = meses()
        codigo_proyecto = proyectos_activos_oh_p
        
        er_ppt = tabla_resumen(codigo_proyecto,meses_seleccionados,df_er_ppt)
        er = tabla_resumen(codigo_proyecto,meses_seleccionados,df_er)

        tabla_expandible_ceco(df_er,df_er_ppt, "INGRESO", meses_seleccionados, codigo_proyecto ,er, er_ppt, "ingreso")
        tabla_expandible_ceco(df_er,df_er_ppt, "COSS", meses_seleccionados, codigo_proyecto ,er, er_ppt, "coss")
        tabla_expandible_ceco(df_er,df_er_ppt, "G.ADMN", meses_seleccionados, codigo_proyecto ,er, er_ppt, "gadmn")
        tabla_expandible_ceco(df_er,df_er_ppt, "GASTOS FINANCIEROS", meses_seleccionados, codigo_proyecto ,er, er_ppt, "gfin")
        tabla_expandible_ceco(df_er,df_er_ppt, "INGRESO FINANCIERO", meses_seleccionados, codigo_proyecto ,er, er_ppt, "ifin")
        


    elif selected ==  "Proyeccion":
        st.subheader('Proyeccion')
        pro, codigo_proyecto = filtro_pro()


        meses_proyeccion = st.selectbox('Cuantos meses usar', ['Ultimo mes','Ultimos 3 meses'])
        dias_transcurridos = fecha_actualizacion.day
        dias_totales = calendar.monthrange(fecha_actualizacion.year, fecha_actualizacion.month)[1]
        # Ajustar el ingreso del último mes
        ultimo_mes = [list(meses_archivo_ordenados)[-1]]  # Obtener el último mes
        if meses_proyeccion == 'Ultimo mes':
            ultimos_meses = [list(meses_archivo_ordenados)[-2]]
            numero_meses = len(ultimos_meses)
        else:
            ultimos_meses = [list(meses_archivo_ordenados)[-2],list(meses_archivo_ordenados)[-3],list(meses_archivo_ordenados)[-4]]
            numero_meses = len(ultimos_meses)
        opciones_proyeccion = ['Ingreso Lineal', 'Llenar ingreso manualmente.']


        def pe(df, codigo_pro, ultimos_meses, pro, ultimo_mes):
            if not isinstance(codigo_pro, list):
                codigo_pro = [codigo_pro]
            
            # Filtrar DataFrame por proyecto y meses seleccionados
            if codigo_pro == proyectos_archivo:
                df_pe_ohp = df[df['Proyecto_A'].isin(oh_p)]
                df_pe_meses_ohp = df_pe_ohp[df_pe_ohp['Mes_A'].isin(ultimos_meses)]
                df_pe = df[~df['Proyecto_A'].isin(oh_p)]
                df_pe = df_pe[df_pe['Proyecto_A'].isin(codigo_pro)]
                df_pe_meses = df_pe[df_pe['Mes_A'].isin(ultimos_meses)]
            else:
                df_pe = df[df['Proyecto_A'].isin(codigo_pro)]
                df_pe_meses = df_pe[df_pe['Mes_A'].isin(ultimos_meses)]

            df_pe_mes = df[df['Proyecto_A'].isin(codigo_pro)]
            df_pe_mes = df_pe_mes[df_pe_mes['Mes_A'].isin(ultimo_mes)]
            
            # Calcular costos fijos y variables
            df_pe_meses_fijos = df_pe_meses.groupby(['Categoria_A', 'Clasificacion_A', 'Cuenta_Nombre_A', 'Mes_A'])['Neto_A'].sum().reset_index()
            df_pe_meses_variables = df_pe_meses.groupby(['Categoria_A', 'Clasificacion_A', 'Cuenta_Nombre_A'])['Neto_A'].sum().reset_index()
            
            
            df_pe_meses_variables_mes = df_pe_mes.groupby(['Categoria_A', 'Clasificacion_A', 'Cuenta_Nombre_A'])['Neto_A'].sum().reset_index()
            # Lógica para cada proyecto
            if codigo_pro == [2003]:
                categorias_variables = ['FLETES']
                costo_variable = (
                    df_pe_meses_variables[df_pe_meses_variables['Categoria_A'].isin(categorias_variables)]['Neto_A'].sum() / 
                    df_pe_meses_variables[df_pe_meses_variables['Categoria_A'] == 'INGRESO']['Neto_A'].sum()
                )
                costo_variable_mes = (
                    df_pe_meses_variables_mes[df_pe_meses_variables_mes['Categoria_A'].isin(categorias_variables)]['Neto_A'].sum() / 
                    df_pe_meses_variables_mes[df_pe_meses_variables_mes['Categoria_A'] == 'INGRESO']['Neto_A'].sum()
                )
                
                df_pe = df[df['Proyecto_A'].isin([2001])]
                df_pe_meses_fs = df_pe[df_pe['Mes_A'].isin(ultimos_meses)]
                fijos_fs = (df_pe_meses_fs[df_pe_meses_fs['Categoria_A'].isin(categorias_felx_com)]['Neto_A'].sum()*.15) /numero_meses
                
                df_pe_meses_fijos = df_pe_meses.groupby(['Categoria_A', 'Clasificacion_A', 'Cuenta_Nombre_A', 'Mes_A'])['Neto_A'].sum().reset_index()
                categorias_fijos = ['OTROS COSS', 'RENTA DE REMOLQUES','NOMINA OPERADORES']
                clasificaciones_fijos = ['G.ADMN']
    
                costos_fijos = (
                    df_pe_meses_fijos[
                        (df_pe_meses_fijos['Categoria_A'].isin(categorias_fijos))
                    ]['Neto_A'].sum()
                ) / numero_meses + fijos_fs

            elif codigo_pro == [1003]:
                                
                categorias_variables = ['FLETES', 'CASETAS', 'COMBUSTIBLE', 'OTROS COSS']
                costo_variable = (
                    df_pe_meses_variables[df_pe_meses_variables['Categoria_A'].isin(categorias_variables)]['Neto_A'].sum() / 
                    df_pe_meses_variables[df_pe_meses_variables['Categoria_A'] == 'INGRESO']['Neto_A'].sum()
                )
                costo_variable_mes = (
                    df_pe_meses_variables_mes[df_pe_meses_variables_mes['Categoria_A'].isin(categorias_variables)]['Neto_A'].sum() / 
                    df_pe_meses_variables_mes[df_pe_meses_variables_mes['Categoria_A'] == 'INGRESO']['Neto_A'].sum()
                )
                
                categorias_fijos = ['AMORT ARRENDAMIENTO', 'NOMINA OPERADORES', 'INTERESES']
                clasificaciones_fijos = ['G.ADMN']
            
                
                costos_fijos = (
                    df_pe_meses_fijos[
                        (df_pe_meses_fijos['Categoria_A'].isin(categorias_fijos)) | 
                        (df_pe_meses_fijos['Clasificacion_A'].isin(clasificaciones_fijos))
                    ]['Neto_A'].sum()
                ) / numero_meses

            elif codigo_pro == [3201]:
                
                categorias_variables = ['FLETES', 'COMBUSTIBLE', 'OTROS COSS']
                costo_variable = (
                    df_pe_meses_variables[df_pe_meses_variables['Categoria_A'].isin(categorias_variables)]['Neto_A'].sum() / 
                    df_pe_meses_variables[df_pe_meses_variables['Categoria_A'] == 'INGRESO']['Neto_A'].sum()
                )
                costo_variable_mes = (
                    df_pe_meses_variables_mes[df_pe_meses_variables_mes['Categoria_A'].isin(categorias_variables)]['Neto_A'].sum() / 
                    df_pe_meses_variables_mes[df_pe_meses_variables_mes['Categoria_A'] == 'INGRESO']['Neto_A'].sum()
                )
                
                categorias_fijos = ['AMORT ARRENDAMIENTO', 'NOMINA OPERADORES', 'INTERESES', 'RENTA DE CONTENEDOR', 'RENTA DE REMOLQUES']
                clasificaciones_fijos = ['G.ADMN']
                
                costos_fijos = (
                    df_pe_meses_fijos[
                        (df_pe_meses_fijos['Categoria_A'].isin(categorias_fijos)) | 
                        (df_pe_meses_fijos['Clasificacion_A'].isin(clasificaciones_fijos))
                    ]['Neto_A'].sum()
                ) / numero_meses
            
            elif codigo_pro == [1001]:
                
                categorias_variables = ['CASETAS', 'COMBUSTIBLE', 'OTROS COSS']
                costo_variable = (
                    df_pe_meses_variables[df_pe_meses_variables['Categoria_A'].isin(categorias_variables)]['Neto_A'].sum() / 
                    df_pe_meses_variables[df_pe_meses_variables['Categoria_A'] == 'INGRESO']['Neto_A'].sum()
                )
                costo_variable_mes = (
                    df_pe_meses_variables_mes[df_pe_meses_variables_mes['Categoria_A'].isin(categorias_variables)]['Neto_A'].sum() / 
                    df_pe_meses_variables_mes[df_pe_meses_variables_mes['Categoria_A'] == 'INGRESO']['Neto_A'].sum()
                )
                
                categorias_fijos = ['AMORT ARRENDAMIENTO', 'NOMINA OPERADORES', 'INTERESES']
                clasificaciones_fijos = ['G.ADMN']
                
                costos_fijos = (
                    df_pe_meses_fijos[
                        (df_pe_meses_fijos['Categoria_A'].isin(categorias_fijos)) | 
                        (df_pe_meses_fijos['Clasificacion_A'].isin(clasificaciones_fijos))
                    ]['Neto_A'].sum()
                ) / numero_meses

            elif codigo_pro == [5001]:
                # Cálculo para proyecto 5001
                categorias_variables = ['FLETES', 'CASETAS', 'COMBUSTIBLE', 'OTROS COSS']
                costo_variable = (
                    df_pe_meses_variables[df_pe_meses_variables['Categoria_A'].isin(categorias_variables)]['Neto_A'].sum() / 
                    df_pe_meses_variables[df_pe_meses_variables['Categoria_A'] == 'INGRESO']['Neto_A'].sum()
                )
                costo_variable_mes = (
                    df_pe_meses_variables_mes[df_pe_meses_variables_mes['Categoria_A'].isin(categorias_variables)]['Neto_A'].sum() / 
                    df_pe_meses_variables_mes[df_pe_meses_variables_mes['Categoria_A'] == 'INGRESO']['Neto_A'].sum()
                )
                
                categorias_fijos = ['AMORT ARRENDAMIENTO', 'RENTA DE REMOLQUES', 'NOMINA OPERADORES', 'INTERESES']
                clasificaciones_fijos = ['G.ADMN']
                
                costos_fijos = (
                    df_pe_meses_fijos[
                        (df_pe_meses_fijos['Categoria_A'].isin(categorias_fijos)) | 
                        (df_pe_meses_fijos['Clasificacion_A'].isin(clasificaciones_fijos))
                    ]['Neto_A'].sum()
                ) / numero_meses
            
            elif codigo_pro == [3002]:
                # Cálculo para proyecto 5001
                categorias_variables = ['FLETES', 'COMBUSTIBLE', 'CASETAS', 'OTROS COSS']
                er_pe = {}
                for x in ultimos_meses:
                    er_pe[x] = tabla_resumen(codigo_pro, [x], df)
                
                # Calcular el promedio de % patio
                patio_values = [mes["% PATIO"] for mes in er_pe.values()]
                patio_promedio = (sum(patio_values) / len(patio_values)) / 100
                costo_variable = (
                    df_pe_meses_variables[df_pe_meses_variables['Categoria_A'].isin(categorias_variables)]['Neto_A'].sum() / 
                    df_pe_meses_variables[df_pe_meses_variables['Categoria_A'] == 'INGRESO']['Neto_A'].sum()
                ) + patio_promedio
                
                er_pe_mes = tabla_resumen(codigo_pro, ultimo_mes, df)
                
                # Calcular el promedio de % patio
                patio_values_mes = er_pe_mes['% PATIO'] /100
                costo_variable_mes = (
                    df_pe_meses_variables_mes[df_pe_meses_variables_mes['Categoria_A'].isin(categorias_variables)]['Neto_A'].sum() / 
                    df_pe_meses_variables_mes[df_pe_meses_variables_mes['Categoria_A'] == 'INGRESO']['Neto_A'].sum()
                ) + patio_values_mes
                
                
                
                categorias_fijos = ['AMORT ARRENDAMIENTO', 'NOMINA OPERADORES', 'INTERESES', 'RENTA DE REMOLQUES']
                clasificaciones_fijos = ['G.ADMN']
                
                costos_fijos = (
                    df_pe_meses_fijos[
                        (df_pe_meses_fijos['Categoria_A'].isin(categorias_fijos)) | 
                        (df_pe_meses_fijos['Clasificacion_A'].isin(clasificaciones_fijos))
                    ]['Neto_A'].sum()
                ) / numero_meses

            elif codigo_pro == proyectos_archivo:
                categorias_variables = ['COMBUSTIBLE', 'CASETAS', 'FLETES', 'OTROS COSS']
                er_pe = {}
                for x in ultimos_meses:
                    er_pe[x] = tabla_resumen(codigo_pro, [x], df)
                
                # Calcular el promedio de % patio
                patio_values = [mes["PATIO"] for mes in er_pe.values()]
                patio_promedio = (sum(patio_values) / len(patio_values))
                costo_variable = (
                    df_pe_meses_variables[df_pe_meses_variables['Categoria_A'].isin(categorias_variables)]['Neto_A'].sum() / 
                    df_pe_meses_variables[df_pe_meses_variables['Categoria_A'] == 'INGRESO']['Neto_A'].sum()
                )
                
                costo_variable_mes = (
                    df_pe_meses_variables_mes[df_pe_meses_variables_mes['Categoria_A'].isin(categorias_variables)]['Neto_A'].sum() / 
                    df_pe_meses_variables_mes[df_pe_meses_variables_mes['Categoria_A'] == 'INGRESO']['Neto_A'].sum()
                ) 
                
                
                
                categorias_fijos = ['NOMINA OPERADORES', 'AMORT ARRENDAMIENTO', 'COSTO OPERADORES', 'RENTA DE CONTENEDORES', 'RENTA DE REMOLQUES']
                clasificaciones_fijos = ['G.ADMN', 'GASTOS FINANCIEROS']
                df_pe_meses_ohp = df_pe_meses_ohp[df_pe_meses_ohp['Clasificacion_A'] == 'GASTOS FINANCIEROS']['Neto_A'].sum()
                
                costos_fijos = (
                    df_pe_meses_fijos[
                        (df_pe_meses_fijos['Categoria_A'].isin(categorias_fijos)) | 
                        (df_pe_meses_fijos['Clasificacion_A'].isin(clasificaciones_fijos))
                    ]['Neto_A'].sum()
                ) / numero_meses + patio_promedio + df_pe_meses_ohp

            elif codigo_pro == [2001]:
                
                # Cálculo para proyecto 5001
                categorias_variables = ['COSS']
                costo_variable = (
                    df_pe_meses_variables[df_pe_meses_variables['Clasificacion_A'].isin(categorias_variables)]['Neto_A'].sum() / 
                    df_pe_meses_variables[df_pe_meses_variables['Categoria_A'] == 'INGRESO']['Neto_A'].sum()
                )
                costo_variable_mes = (
                    df_pe_meses_variables_mes[df_pe_meses_variables_mes['Clasificacion_A'].isin(categorias_variables)]['Neto_A'].sum() / 
                    df_pe_meses_variables_mes[df_pe_meses_variables_mes['Categoria_A'] == 'INGRESO']['Neto_A'].sum()
                )
                
                
                categorias_fijos = ['INTERESES']
                clasificaciones_fijos = ['G.ADMN']
                
                costos_fijos = (
                    df_pe_meses_fijos[
                        (df_pe_meses_fijos['Categoria_A'].isin(categorias_fijos)) | 
                        (df_pe_meses_fijos['Clasificacion_A'].isin(clasificaciones_fijos))
                    ]['Neto_A'].sum() -
                    (df_pe_meses_fijos[df_pe_meses_fijos['Categoria_A'].isin(categorias_felx_com)]['Neto_A'].sum()*.15)
                ) / numero_meses


            elif codigo_pro == [7806]:
                # Cálculo para proyecto 7806
                costo_variable = (
                    df_pe_meses_variables[df_pe_meses_variables['Categoria_A'] == 'FLETES']['Neto_A'].sum() / 
                    df_pe_meses_variables[df_pe_meses_variables['Categoria_A'] == 'INGRESO']['Neto_A'].sum()
                )
                costo_variable_mes = (
                    df_pe_meses_variables_mes[df_pe_meses_variables_mes['Categoria_A'] == 'FLETES']['Neto_A'].sum() / 
                    df_pe_meses_variables_mes[df_pe_meses_variables_mes['Categoria_A'] == 'INGRESO']['Neto_A'].sum()
                )
                
                # Calcular costos fijos como promedio de los últimos 3 meses
                df_g_admn = df_pe_meses_fijos[df_pe_meses_fijos['Clasificacion_A'] == 'G.ADMN']
                suma_por_mes = df_g_admn.groupby('Mes_A')['Neto_A'].sum().reset_index()
                
                if meses_proyeccion == 'Último mes':
                    costos_fijos = suma_por_mes[suma_por_mes['Mes_A'] == list(meses_archivo_ordenados)[-2]]['Neto_A'].sum()
                else:
                    costos_fijos = suma_por_mes['Neto_A'].mean() if not suma_por_mes.empty else 0

            # Otros cálculos
            oh_obj = 0.115  # Overhead
            er_pe = {}
            for x in ultimos_meses:
                er_pe[x] = tabla_resumen(codigo_pro, [x], df)
            
            pe_pro = costos_fijos / (1 - (costo_variable + oh_obj))
            ventas_ut = costos_fijos / (1 - (costo_variable + oh_obj + 0.115))
            
            # Calcular el promedio de % OH
            oh_values = [mes["% OH"] for mes in er_pe.values()]
            oh_promedio = (sum(oh_values) / len(oh_values)) / 100

            # Cálculos con el promedio de OH
            pe_pro_prom = costos_fijos / (1 - (costo_variable + oh_promedio))
            ventas_ut_prom = costos_fijos / (1 - (costo_variable + oh_promedio + 0.115))
            
            # Generar la tabla
            table_html = f"""
            <style>
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    text-align: center;
                }}
                th, td {{
                    border: 1px solid black;
                    padding: 8px;
                    font-size: 14px;
                }}
                th {{
                    background-color: #001f3f;
                    color: white;
                    font-weight: bold;
                }}
                .header {{
                    text-align: center;
                    font-size: 16px;
                    font-weight: bold;
                    background-color: #001f3f;
                    color: white;
                    padding: 10px;
                    border: 1px solid black;
                }}
            </style>
            <div class="header">{pro}</div>
            <table>
                <tr>
                    <th>Descripción</th>
                    <th>VARIABLES</th>
                    <th>GASTOS FIJOS</th>
                    <th>OH</th>
                    <th>ventas PE</th>
                    <th>ventas ut 11.5%</th>
                </tr>
                <tr>
                    <td>Calculo de PE con OH ojetivo</td>
                    <td>{costo_variable:.1%}</td>
                    <td>${costos_fijos:,.2f}</td>
                    <td>{oh_obj:.2%}</td>
                    <td>${pe_pro:,.2f}</td>
                    <td>${ventas_ut:,.2f}</td>
                </tr>
                <tr>
                    <td>Calculo de PE con OH historico</td>
                    <td>{costo_variable:.1%}</td>
                    <td>${costos_fijos:,.2f}</td>
                    <td>{oh_promedio*100:.2f}%</td>
                    <td>${pe_pro_prom:,.2f}</td>
                    <td>${ventas_ut_prom:,.2f}</td>
                </tr>
            </table>
            """
            
            # Renderizar la tabla en Streamlit
            st.markdown(table_html, unsafe_allow_html=True)
            if ventas_ut_prom < 0:
                reduccion = ((costo_variable + oh_promedio + 0.115) - 1) * 100
                st.write(f'''Alcanzar la utilidad objetivo es imposible,
                            se debe reducir la proporción de costos u OH en un {reduccion:,.2f}% para alcanzar el objetivo.''')
            proyeccion = st.radio('', opciones_proyeccion)
            if proyeccion == 'Llenar ingreso manualmente.':
                ingreso_lineal = st.number_input(
                    label="Introduce un número:",
                    value=1000000,
                    step=500000,
                )

            
            elif proyeccion == 'Ingreso Lineal':
                st.write('Proyección Lineal')
                dias_transcurridos = fecha_actualizacion.day
                dias_totales = calendar.monthrange(fecha_actualizacion.year, fecha_actualizacion.month)[1]

                # Ajustar el ingreso del último mes
                ultimo_mes = list(meses_archivo_ordenados)[-1]  # Obtener el último mes
                
                ingreso = df[df['Mes_A'] == ultimo_mes]
                ingreso = ingreso[ingreso['Categoria_A'] == 'INGRESO']
                ingreso = ingreso[ingreso['Proyecto_A'].isin(codigo_pro)]['Neto_A'].sum()
                ingreso_lineal = ingreso/dias_transcurridos * dias_totales
                
            # **Cálculos para la primera fila (meses anteriores)**
            ingreso_total = ingreso_lineal
            costos_variables = ingreso_total * costo_variable
            costos_fijos_totales = costos_fijos
            oh_total = ingreso_total * oh_obj
            utilidad_antes_impuestos = ingreso_total - costos_variables - costos_fijos_totales - oh_total

            # **Cálculos para la segunda fila (mes actual)**
            costo_variable_mes_total = ingreso_total * costo_variable_mes
            costos_fijos_totales_mes_actual = costos_fijos  # Si es el mismo costo fijo, se usa la misma variable
            oh_total_mes_actual = ingreso_total * oh_promedio
            utilidad_antes_impuestos_mes_actual = ingreso_total - costo_variable_mes_total - costos_fijos_totales_mes_actual - oh_total_mes_actual

            # **Generar la tabla de ingresos lineales**
            tabla_ingresos_html = f"""
            <style>
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    text-align: center;
                }}
                th, td {{
                    border: 1px solid black;
                    padding: 8px;
                    font-size: 14px;
                }}
                th {{
                    background-color: #001f3f;
                    color: white;
                    font-weight: bold;
                }}
            </style>
            <table>
                <tr>
                    <th>Descripción</th>
                    <th>Ingresos</th>
                    <th>Costos Variables</th>
                    <th>Costos Fijos</th>
                    <th>OH</th>
                    <th>Utilidad Antes de Impuestos</th>
                    <th>MG. EBT</th>
                </tr>
                <tr>
                    <td>Cálculo meses anteriores con OH objetivo</td>
                    <td>${ingreso_total:,.2f}</td>
                    <td>${costos_variables:,.2f}</td>
                    <td>${costos_fijos_totales:,.2f}</td>
                    <td>${oh_total:,.2f}</td>
                    <td>${utilidad_antes_impuestos:,.2f}</td>
                    <td>{utilidad_antes_impuestos/ingreso_total*100:,.2f}%</td>
                </tr>
                <tr>
                    <td>Costos variables del mes actual con OH promedio</td>
                    <td>${ingreso_total:,.2f}</td>
                    <td>${costo_variable_mes_total:,.2f}</td>
                    <td>${costos_fijos_totales_mes_actual:,.2f}</td>
                    <td>${oh_total_mes_actual:,.2f}</td>
                    <td>${utilidad_antes_impuestos_mes_actual:,.2f}</td>
                    <td>{utilidad_antes_impuestos_mes_actual/ingreso_total*100:,.2f}%</td>
                </tr>
            </table>
            """

            # **Renderizar la tabla en Streamlit**
            st.markdown(tabla_ingresos_html, unsafe_allow_html=True)




        st.write('Punto de equilibrio')
        pe(df, codigo_proyecto, ultimos_meses, pro, ultimo_mes)

        
    elif selected == "Cuadro financiero":

        # Cuadro financiero (sin cambios)
        st.subheader('Cuadro financiero')

        html_table_financiera = """
        <style>
            .financial-table {
                border-collapse: collapse;
                width: 100%;
                margin-bottom: 20px;
            }
            .financial-table th, .financial-table td {
                border: 1px solid black;
                padding: 8px;
                font-size: 14px;
                text-align: right;
            }
            .financial-table th {
                background-color: #001f3f;
                color: white;
                font-weight: bold;
                text-align: center;
            }
            .financial-table .header {
                text-align: center;
                font-size: 16px;
                font-weight: bold;
                background-color: #001f3f;
                color: white;
                padding: 10px;
            }
            .financial-table .highlight {
                background-color: #FFDC00;
                font-weight: bold;
            }
            .financial-table .subtitle {
                background-color: #0074D9;
                color: white;
                font-weight: bold;
                text-align: center;
            }
        </style>

        <table class="financial-table">
            <tr>
                <th colspan="2" class="header">NOVIEMBRE</th>
                <th colspan="3" class="header">CUADRO FINANCIERO</th>
            </tr>
            <tr>
                <td colspan="2" class="subtitle">DEL 01 AL 30 DE NOVIEMBRE 2024</td>
                <td colspan="3"></td>
            </tr>
            <tr>
                <td>Cuentas por cobrar</td>
                <td>$121,786,943.00</td>
                <td>Presupuesto ingresos</td>
                <td>$95,929,922.00</td>
                <td>100%</td>
            </tr>
            <tr>
                <td>Cuentas por pagar</td>
                <td>$66,577,119.00</td>
                <td>Ingreso real</td>
                <td>$87,528,895.00</td>
                <td>91%</td>
            </tr>
            <tr>
                <td>Diferencial</td>
                <td>$55,209,824.00</td>
                <td>Proyección de cierre</td>
                <td>$95,928,922.00</td>
                <td>100%</td>
            </tr>
            <tr>
                <td>Flujo</td>
                <td class="highlight">$2,720,050.00</td>
                <td>Presupuesto gastos</td>
                <td>$85,663,454.00</td>
                <td>100%</td>
            </tr>
            <tr>
                <td></td>
                <td></td>
                <td>Gastos reales</td>
                <td>$80,800,097.00</td>
                <td>94%</td>
            </tr>
            <tr>
                <td></td>
                <td></td>
                <td>Proyección de cierre</td>
                <td>$85,663,454.00</td>
                <td>100%</td>
            </tr>
        </table>
        """
        st.markdown(html_table_financiera, unsafe_allow_html=True)

        # Nombres de las pestañas
        tabs = ['CAMIONES', 'OPERADORES', 'CAMIONES SC', 'REMOLQUES', 'CHASIS & DOLLY', 'CONTENEDORES']

        # Crear las pestañas
        tab_objects = st.tabs(tabs)

        # Cargar y mostrar los datos en cada pestaña
        for i, tab in enumerate(tab_objects):
            with tab:
                st.subheader(f"INFORMACIÓN {tabs[i]}")

                # Cargar la hoja correspondiente (el nombre de la hoja debe coincidir con la pestaña)

                info_pro_ca = cargar_datos_hoja(info_pro_url, nombre_hoja=tabs[i]) 

                # CSS exclusivo para las tablas en las pestañas
                st.markdown(f"""
                <style>
                .tab-table-{i} {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 15px 0;
                    font-size: 18px;
                    text-align: left;
                }}
                .tab-table-{i} th {{
                    background-color: #003366; /* Azul marino */
                    color: white;
                    text-transform: uppercase;
                    padding: 10px;
                }}
                .tab-table-{i} td {{
                    padding: 8px;
                }}
                .tab-table-{i} tr:nth-child(even) {{
                    background-color: #003366; /* Azul marino para filas pares */
                    color: white; /* Texto blanco */
                }}
                .tab-table-{i} tr:nth-child(odd) {{
                    background-color: white; /* Blanco para filas impares */
                    color: black; /* Texto negro */
                }}
                .tab-table-{i} tr:hover {{
                    background-color: #00509E; /* Azul más claro */
                    color: white;
                }}
                </style>
                """, unsafe_allow_html=True)

                # Convertir el DataFrame a HTML con clase única por pestaña
                html_table = info_pro_ca.to_html(index=False, escape=False, classes=f"tab-table-{i}")
                st.markdown(html_table, unsafe_allow_html=True)