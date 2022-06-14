from data.get_data import get_covid_data, DATA_DICT
import streamlit as st
from matplotlib import pyplot as plt
from datetime import date

current_month = date.today().month
current_year = date.today().year


st.title("Visualisations Covid-19 2020/2021 France")

CONFIG = {'title_fontsize':20, 'x_fontsize':18, 'y_fontsize':16}

def plot_figure(x,y, *args, config=CONFIG, title='mytitle', xlabel='xlabel', ylabel='ylabel'):
    fig = plt.figure()
    fig.suptitle(title, fontsize=config['title_fontsize'])
    plt.xlabel(xlabel, fontsize=config['x_fontsize'])
    plt.ylabel(ylabel, fontsize=config['y_fontsize'])
    plt.plot(x, y, *args)
    plt.xticks(x, rotation='vertical')
    st.pyplot(fig)

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')


# chargement données
covid_data = get_covid_data()
covid_data['year'] = covid_data.apply(lambda x: int(x['jour'].split('-')[0]), axis=1)
covid_data['month'] = covid_data.apply(lambda x: int(x['jour'].split('-')[1]), axis=1)
with st.sidebar:
    st.sidebar.title("Periode")
    year_select = st.selectbox('Année', covid_data['year'].sort_values().unique(), index=list(covid_data['year'].sort_values().unique()).index(current_year))
    month_select = st.selectbox('Mois', covid_data['month'].sort_values().unique(), index=list(covid_data['month'].sort_values().unique()).index(current_month))
    kpi_select = st.radio("Mesure", ("Reanimation", "Hospitalisation", "décès"))
    if kpi_select == 'Reanimation':
        value_select = 'rea'
    elif kpi_select == 'Hospitalisation':
        value_select = 'hosp'
    else:
        value_select = "dc"

column_select = ['jour', 'year', 'month', 'sexe', value_select]
covid_data = covid_data[covid_data['year']==year_select]
covid_data = covid_data[covid_data['month']==month_select]
covid_data = covid_data[column_select]

# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')
st.subheader('Covid-19 données hospitalières 2020/2021 France')
st.table(covid_data.describe())


# Nbre de rea par jour homme vs femme
data_to_plot = covid_data.groupby(['jour', 'sexe'])[value_select].sum().reset_index()

fig = plt.figure()
fig.suptitle('Nombre de {rea} par jour homme vs femme'.format(rea=DATA_DICT[value_select]), fontsize=CONFIG['title_fontsize'])
plt.xlabel('Jour', fontsize=CONFIG['x_fontsize'])
plt.ylabel('Nbre {}'.format(value_select), fontsize=CONFIG['y_fontsize'])
x = data_to_plot[data_to_plot['sexe']==1]['jour']
rea_homme = data_to_plot[data_to_plot['sexe']==1][value_select].values
rea_femme = data_to_plot[data_to_plot['sexe']==2][value_select].values
g1 = plt.plot(x, rea_homme, 'b', label='{} homme'.format(value_select))
plt.xticks(x, rotation='vertical')

x = data_to_plot[data_to_plot['sexe']==2]['jour']
g2 = plt.plot(x, rea_femme, 'r', label='{} femme'.format(value_select))
plt.legend()
st.pyplot(fig)