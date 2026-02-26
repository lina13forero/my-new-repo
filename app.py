import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title='vehicles_us.csv', layout='wide')

@st.cache_data
def load_data(path):
 return pd.read_csv(path)
DATA_PATH = 'vehicles_us.csv'

data = load_data(DATA_PATH)

st.header('Analisis Exploratorio del Dataset')

num_cols = data.select_dtypes(include='number').columns.tolist()
cat_cols = data.select_dtypes(exclude='number').columns.tolist()

if not num_cols:
  st.error('No se encontraron columnas numéricas en el dataset. Agrega columnas numéricas para graficar.')
  st.stop()
with st.expander('Vista previa de datos', expanded=False):
  st.dataframe(data.head(50), use_container_width=True)

st.subheader('Histograma')
col_hist = st.selectbox('Columna numérica', options=num_cols, index=0)
bins = st.slider('Numero de bins', 5, 100, 30)
show_hist = st.checkbox('Mostrar histograma', value=True)

st.subheader('Grafico de dispersión')
if len(num_cols) >= 2:
  default_x, default_y = num_cols[0], num_cols[1]
else:
  default_x = default_y = num_cols[0]
x_scatter = st.selectbox('Eje X', options=num_cols, 
index=num_cols.index(default_x))
y_scatter = st.selectbox('Eje Y', options=num_cols, 
index=num_cols.index(default_y))
color_by = st.selectbox('Color (opcional)', options=['(ninguno)'] + cat_cols)
show_scatter = st.checkbox('Mostrar dispersión', value=True)

st.divider()

if show_hist and col_hist:
  st.write(f'Histograma de **{col_hist}**') 
  fig = px.histogram(data, x=col_hist, nbins=bins)
  st.plotly_chart(fig, use_container_width=True)

if show_scatter and x_scatter and y_scatter and x_scatter != '' and y_scatter != '':
  st.write(f'Dispersión: **{x_scatter}** vs **{y_scatter}**')
  color_arg = None if color_by == '(ninguno)' else color_by
  fig2 = px.scatter(data, x=x_scatter, y=y_scatter, color=color_arg)
  st.plotly_chart(fig2, use_container_width=True)
st.caption('Tip: pasa el mouse por los puntos para ver valores y usa el selector para filtrar.')
