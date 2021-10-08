import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import calendar
import streamlit as st
from data import *

def sidebar_section():
    st.sidebar.header('settings')
    st.session_state.conceptarium_url = st.sidebar.text_input(
        'What\'s the URL of your conceptarium?')
    
    timezone = st.sidebar.number_input(
        'What timezone are you in? (UTC+...)', step=1)
    if timezone >= 0:
        st.session_state.timezone = 'Etc/GMT-' + str(int(abs(timezone)))
    else:
        st.session_state.timezone = 'Etc/GMT+' + str(int(abs(timezone)))

def header_section():
    st.title('🔬 ideoscope')
    st.markdown('An instrument for quantifying, understanding, and optimizing your thinking, split into three sections:')

    col1, col2, col3 = st.columns(3)
    col1.markdown('''#### 🌿 memetics
    - 🐣 birth rate
    - 🐇 population size
    - 🐋 variability
    - 🍃 drift
    - 🦅 fitness
    ''')
    col2.markdown('''#### 📗 linguistics
    - ⏱️ conciseness
    - 📰 readability
    - 📏 objectivity
    - 💚 sentiment
    - 🎨 interests
    ''')
    col3.markdown('''#### 🖼️ semantics
    - 🔭 discovery
    - 🌌 projection
    ''')

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def birth_rate_subsection():
    st.markdown('---')
    st.header('🌿 memetics / 🐣 birth rate')
    st.caption('The rate at which new ideas get saved to your conceptarium.')
    col1, col2, col3, col4 = st.columns(4)

    value, delta = birth_rate_over_past_day()
    col1.metric(label='birth rate over past day', value=value, delta=delta)

    value, delta = birth_rate_over_past_week()
    col2.metric(label='birth rate over past week', value=value, delta=delta)

    value, delta = birth_rate_over_past_month()
    col3.metric(label='birth rate over past month', value=value, delta=delta)

    value, delta = birth_rate_over_past_year()
    col4.metric(label='birth rate over past year', value=value, delta=delta)

    col1, col2 = st.columns(2)

    data = daily_birth_rate()
    fig = px.line(data, color_discrete_sequence=['#228b22'], title='daily birth rate', line_shape='spline')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='days ago', autorange='reversed')
    fig.update_yaxes(title_text='birth rate')
    fig.update_xaxes(showline=True, linewidth=1, linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)

    
    data = birth_rate_by_day_of_week()
    fig = px.histogram(data, x='weekday', nbins=12, color_discrete_sequence=['#228b22'], category_orders={'weekday': calendar.day_abbr[0:7]}, title='birth rate by day of the week')
    fig.update_layout(bargap=0.2)
    fig.update_xaxes(title_text='day of the week')
    fig.update_yaxes(title_text='birth rate')
    fig.update_xaxes(showline=True, linewidth=1, linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='#474539', mirror=True)
    col2.plotly_chart(fig)

    data = birth_rate_by_time_of_day()
    fig = px.histogram(data, nbins=12, color_discrete_sequence=['#228b22'], title='birth rate by time of day')
    fig.update_layout(bargap=0.2, showlegend=False)
    fig.update_xaxes(title_text='time of day', tickformat='%H:%M')
    fig.update_yaxes(title_text='birth rate')
    fig.update_xaxes(showline=True, linewidth=1, linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)

    data = birth_rate_by_time_of_day_and_day_of_week()
    fig = px.density_heatmap(data, x='weekday', y='time', category_orders={'weekday': calendar.day_abbr[0:7]}, color_continuous_scale=['#fffffd', '#228b22'], title='birth rate by day of the week and time of day')
    fig.update_layout(bargap=0.2, xaxis={'side': 'top'})
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='time of day', autorange='reversed', tickformat='%H:%M')
    fig.update_xaxes(showline=True, linewidth=1, linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='#474539', mirror=True)
    col2.plotly_chart(fig)

def population_size_subsection():
    st.markdown('---')
    st.header('🌿 memetics / 🐇 population size')
    st.caption('A measure of how large the ecology of your mind is in terms of individual thoughts.')

    col1, col2 = st.columns(2)

    data = population_size_per_day()
    fig = px.line(data, color_discrete_sequence=['#228b22'], title='population size per day', line_shape='spline')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='days ago', autorange='reversed')
    fig.update_yaxes(title_text='population size')
    fig.update_xaxes(showline=True, linewidth=1, linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)

    data = population_pyramid_of_fittest_quartile()
    layout = go.Layout(yaxis=go.layout.YAxis(title='age (weeks)', showline=True, linewidth=1, linecolor='#474539', mirror=True),
                       xaxis=go.layout.XAxis(
                           range=[-15, 15], title='count', showline=True, linewidth=1, linecolor='#474539', mirror=True),
                       barmode='overlay',
                       bargap=0.1,
                       title='population pyramid of fittest quartile')
    data = [go.Bar(x=data[0],
                   y=list(range(len(data[0]))),
                   orientation='h',
                   name='language',
                   hoverinfo='x',
                   marker=dict(color='#42D142')
                   ),
            go.Bar(x=data[1],
                   y=list(range(len(data[1]))),
                   orientation='h',
                   name='imagery',
                   marker=dict(color='seagreen')
                   )]

    col2.plotly_chart(dict(data=data, layout=layout))


def variability_subsection():
    st.markdown('---')
    st.header('🌿 memetics / 🐋 variability')
    st.caption(
        'A measure of how diverse your thinking is at any given time, the biodiversity of your ideas.')
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(label='variability over past week', value='6.3', delta='+1.2')
    col2.metric(label='variability over past month',
                value='4.6', delta='-0.5')
    col3.metric(label='aggregate variability', value='5.8')
    col4.metric(label='variability of fittest quartile', value='2.3')

    col1, col2 = st.columns(2)
    memetic_variability_per_week = np.random.uniform(5, 3, (20))
    fig = px.line(memetic_variability_per_week, color_discrete_sequence=[
        '#228b22'], title='variability per week', line_shape='spline')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='weeks ago', autorange='reversed')
    fig.update_yaxes(title_text='variability')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)

    memetic_variability_per_month = np.random.uniform(5, 3, (5))
    fig = px.line(memetic_variability_per_month, color_discrete_sequence=[
        '#228b22'], title='variability per month', line_shape='spline')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='months ago', autorange='reversed')
    fig.update_yaxes(title_text='variability')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col2.plotly_chart(fig)


def drift_subsection():
    st.markdown('---')
    st.header('🌿 memetics / 🍃 drift')
    st.caption(
        'A measure of how much you\'re shifting your focus from one period to the next.')
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(label='drift over past week', value='6.3', delta='+1.2')
    col2.metric(label='drift over past week (% of max)',
                value='57.3%', delta='+5.2%')
    col3.metric(label='drift over past month',
                value='4.6', delta='-0.5')
    col4.metric(label='drift over past month (% of max)',
                value='83.6%', delta='-12.5%')

    col1, col2 = st.columns(2)
    memetic_variability_per_week = np.random.uniform(5, 3, (20))
    fig = px.line(memetic_variability_per_week, color_discrete_sequence=[
        '#228b22'], title='drift per week', line_shape='spline')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='weeks ago', autorange='reversed')
    fig.update_yaxes(title_text='drift')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)

    memetic_variability_per_month = np.random.uniform(5, 3, (5))
    fig = px.line(memetic_variability_per_month, color_discrete_sequence=[
        '#228b22'], title='drift per month', line_shape='spline')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='months ago', autorange='reversed')
    fig.update_yaxes(title_text='drift')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col2.plotly_chart(fig)


def fitness_subsection():
    st.markdown('---')
    st.header('🌿 memetics / 🦅 fitness')
    st.caption(
        'The fitness of a thought is equated with how active it is in your mind. Powerful, catchy, gripping ideas are the ones on which you reflect most.')
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(label='mean fitness', value='11.9')
    col2.metric(label='median fitness',
                value='8.3')
    col3.metric(label='mean age of fittest quartile (weeks)',
                value='3.2')
    col4.metric(label='memetic load',
                value='0.73')

    col1, col2 = st.columns(2)
    memetic_fitness = pd.DataFrame(
        np.random.normal(20, 10, 200))
    fig = px.histogram(memetic_fitness, nbins=50, color_discrete_sequence=[
        '#228b22'], labels={'count': '', 'Time': ''}, title='fitness distribution')
    fig.update_layout(bargap=0.2, showlegend=False)
    fig.update_xaxes(title_text='fitness')
    fig.update_yaxes(title_text='thought count')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)

    memetic_fitness = np.abs(np.random.normal(0.1, 0.05, 20))
    fig = px.box(memetic_fitness, color_discrete_sequence=[
        '#228b22'], title='fitness distribution')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='fitness')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col2.plotly_chart(fig)


def conciseness_subsection():
    st.markdown('---')
    st.header('📗 linguistics / ⏱️ conciseness')
    st.caption(
        'The average length of language thoughts.')
    col1, col2 = st.columns(2)

    memetic_variability_per_week = np.random.uniform(5, 3, (20))
    fig = px.line(memetic_variability_per_week, color_discrete_sequence=[
        '#228b22'], title='conciseness per week', line_shape='spline')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='weeks ago', autorange='reversed')
    fig.update_yaxes(title_text='conciseness')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)

    weekly_discovery_rates = np.abs(np.random.normal(0.1, 0.05, 20))
    fig = px.box(weekly_discovery_rates, color_discrete_sequence=[
        '#228b22'], title='conciseness distribution over past month')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='conciseness')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col2.plotly_chart(fig)


def readability_subsection():
    st.markdown('---')
    st.header('📗 linguistics / 📰 readability')
    st.caption(
        'A measure based on the average word length and average sentence length.')
    col1, col2 = st.columns(2)

    memetic_variability_per_week = np.random.uniform(5, 3, (20))
    fig = px.line(memetic_variability_per_week, color_discrete_sequence=[
        '#228b22'], title='readability per week', line_shape='spline')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='weeks ago', autorange='reversed')
    fig.update_yaxes(title_text='readability')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)

    weekly_discovery_rates = np.abs(np.random.normal(0.1, 0.05, 20))
    fig = px.box(weekly_discovery_rates, color_discrete_sequence=[
        '#228b22'], title='readability distribution over past month')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='readability')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col2.plotly_chart(fig)


def objectivity_subsection():
    st.markdown('---')
    st.header('📗 linguistics / 📏 objectivity')
    st.caption(
        'A measure of how much your language thoughts appear to describe facts, rather than opinions.')
    col1, col2 = st.columns(2)

    memetic_variability_per_week = np.random.uniform(5, 3, (20))
    fig = px.line(memetic_variability_per_week, color_discrete_sequence=[
        '#228b22'], title='objectivity per week', line_shape='spline')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='weeks ago', autorange='reversed')
    fig.update_yaxes(title_text='objectivity')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)

    weekly_discovery_rates = np.abs(np.random.normal(0.1, 0.05, 20))
    fig = px.box(weekly_discovery_rates, color_discrete_sequence=[
        '#228b22'], title='objectivity distribution over past month')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='objectivity')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col2.plotly_chart(fig)


def sentiment_subsection():
    st.markdown('---')
    st.header('📗 linguistics / 💚 sentiment')
    st.caption(
        'A measure of how positive your language thoughts are.')
    col1, col2 = st.columns(2)

    memetic_variability_per_week = np.random.uniform(5, 3, (20))
    fig = px.line(memetic_variability_per_week, color_discrete_sequence=[
        '#228b22'], title='sentiment per week', line_shape='spline')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='weeks ago', autorange='reversed')
    fig.update_yaxes(title_text='sentiment')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)

    weekly_discovery_rates = np.abs(np.random.normal(0.1, 0.05, 20))
    fig = px.box(weekly_discovery_rates, color_discrete_sequence=[
        '#228b22'], title='sentiment distribution over past month')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='sentiment')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col2.plotly_chart(fig)


def interests_subsection():
    st.markdown('---')
    st.header('📗 linguistics / 🎨 interests')
    st.caption(
        'Keywords derived from your language thoughts.')
    col1, col2 = st.columns(2)

    df = pd.DataFrame([
        dict(Task="solarpunk", Start='2021-01-01', Finish='2021-02-28'),
        dict(Task="Dune", Start='2021-02-05', Finish='2021-04-15'),
        dict(Task="conceptarium", Start='2021-02-20', Finish='2021-05-30'),
        dict(Task="conceptors", Start='2021-03-01', Finish='2021-04-02'),
        dict(Task="lighting", Start='2021-04-01', Finish='2021-05-10'),
    ])

    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color_discrete_sequence=[
                      '#228b22'], text='Task', title='timeline of interests')
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='', showticklabels=False)
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)

    birth_rate_by_day_of_the_week = np.random.choice(
        ['solarpunk', 'Dune', 'conceptarium', 'conceptors', 'lighting'], 200)
    df = pd.DataFrame(birth_rate_by_day_of_the_week, columns=['Time'])
    fig = px.histogram(df, x='Time', nbins=12, category_orders={'Time': ['solarpunk', 'Dune', 'conceptarium', 'conceptors', 'lighting']}, color_discrete_sequence=[
        '#228b22'], title='thoughts by interest')
    fig.update_layout(bargap=0.2)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='count')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col2.plotly_chart(fig)


def discovery_subsection():
    st.markdown('---')
    st.header('🖼️ semantics / 🔭 discovery')
    st.caption(
        'A measure of how much of the semantic space you\'ve explored through your ideas.')

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(label='dicovery over past week', value='0.21%', delta='+0.02%')
    col2.metric(label='dicovery over past month',
                value='0.87%', delta='-0.09%')
    col3.metric(label='explored proportion of semantic volume',
                value='12.52%')
    col4.metric(label='ETA complete semantic coverage',
                value='67.3 YRS')

    col1, col2 = st.columns(2)

    fig = px.pie(pd.DataFrame([['unexplored', 87.5], ['explored', 12.5]], columns=['name', 'value']), names='name', values='value', color_discrete_sequence=[
        '#228b22'], title='explored portion of semantic space')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='weekly discovery rates')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)

    weekly_discovery_rates = np.abs(np.random.normal(0.1, 0.05, 20))
    fig = px.box(weekly_discovery_rates, color_discrete_sequence=[
        '#228b22'], title='weekly discovery rate distribution')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='weekly discovery rates')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col2.plotly_chart(fig)

    weekly_discovery_rates = np.abs(np.random.normal(0.1, 0.05, 20))
    weekly_discovery_rates = [
        sum(weekly_discovery_rates[e:]) for e in range(len(weekly_discovery_rates))]
    fig = px.line(weekly_discovery_rates, color_discrete_sequence=[
        '#228b22'], title='cumulative discovery rate', line_shape='spline')
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text='weeks ago', autorange='reversed')
    fig.update_yaxes(title_text='explored proportion of semantic volume')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)


def projection_subsection():
    st.markdown('---')
    st.header('🖼️ semantics / 🌌 projection')
    st.caption(
        'Low-dimensional visualizations of the high-dimensional semantics of your thoughts.')
    col1, col2 = st.columns(2)

    embeddings = [np.append(e, 0.5) for e in np.random.rand(300, 3)]
    fig = px.scatter(pd.DataFrame(embeddings, columns=['x', 'y', 'z', 'size']), x='x', y='y', size='size', size_max=5, color_discrete_sequence=[
        '#228b22'], title='2D projection')
    fig.update_layout(showlegend=False, margin=dict(l=0, r=0, b=0))
    fig.update_xaxes(title_text='')
    fig.update_yaxes(title_text='')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col1.plotly_chart(fig)

    embeddings = [np.append(e, 0.5) for e in np.random.rand(300, 3)]
    fig = px.scatter_3d(pd.DataFrame(embeddings, columns=['x', 'y', 'z', 'size']), x='x', y='y', z='z', size='size', size_max=5, color_discrete_sequence=[
        '#228b22'], title='3D projection')
    fig.update_layout(showlegend=False, margin=dict(l=0, r=0, b=0))
    fig.update_xaxes(title_text='', autorange='reversed')
    fig.update_yaxes(title_text='')
    fig.update_xaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1,
                     linecolor='#474539', mirror=True)
    col2.plotly_chart(fig)