
# coding: utf-8

# # Final Project
# Create a Dashboard taking data from Eurostat, GDP and main components (output, expenditure and income). 
# The dashboard will have two graphs:
# 1. The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data. 
# #we already have this. we just need to adapt it to the new data.
# 2. The other graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators. (hint use Scatter object using mode = 'lines' (more here)
# Step 3. put it in the cloud. he wants to receive two links. one: where the application is running two: the link to github where our code is. we will learn about deployment in the next session
# 
# we download the data from eurostat. then we set up everything in local. in next class, we will learn how to do everything in github.

# In[ ]:


#Install the relevant packages

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv('data.csv', sep= '\t')

df.head(5)


# In[ ]:


# Dividing the 'unit,na_item,geo\time'-column into three separate columns

df['unit'] = df.iloc[:,0].str.split(',').apply(lambda x: x[0])
df['indicator'] = df.iloc[:,0].str.split(',').apply(lambda x: x[1])
df['geo'] = df.iloc[:,0].str.split(',').apply(lambda x: x[2])

#Removing the first column
df = df.drop(df.columns[0], axis=1)


# In[ ]:


# Changing variable names and cleaning column names

df = df.replace({'indicator' : {'B1GQ' : 'Gross domestic product at market prices',
                         'B1G' : 'Value added, gross',
                         'P3' : 'Final consumption expenditure',
                         'P3_S13': 'Final consumption expenditure of general government',
                         'P31_S13': 'Individual consumption expenditure of general government',
                         'P32_S13': 'Collective consumption expenditure of general government',
                         'P31_S14_S15': 'Household and NPISH final consumption expenditure',
                         'P31_S14': 'Final consumption expenditure of households',
                         'P31_S15': 'Final consumption expenditure of NPISH',
                         'P41': 'Actual individual consumption',
                         'P5G': 'Gross capital formation',
                         'P51G': 'Gross fixed capital formation',
                         'P52_P53': 'Changes in inventories and acquisitions less disposals of valuables',
                         'P52': 'Changes in inventories',
                         'P53': 'Acquisitions less disposals of valuables',
                         'P6': 'Exports of goods and services',
                         'P61': 'Exports of goods',
                         'P62': 'Exports of services',
                         'P7': 'Imports of goods and services',
                         'P71': 'Imports of goods',
                         'P72': 'Imports of services',
                         'B11': 'External balance of goods and services',
                         'B111': 'External balance - Goods',
                         'B112': 'External balance - Services',
                         'D1': 'Compensation of employees',
                         'D11': 'Wages and salaries',
                         'D12': "Employers' social contributions",
                         'B2A3G': 'Operating surplus and mixed income, gross',
                         'D2X3': 'Taxes on production and imports less subsidies',
                         'D2': 'Taxes on production and imports',
                         'D3': 'Subsidies',
                         'D21X31': 'Taxes less subsidies on products',
                         'D21': 'Taxes on products',
                         'D31': 'Subsidies on products',
                         'YA1': 'Statistical discrepancy (production approach)',
                         'YA0': 'Statistical discrepancy (expenditure approach)',
                         'YA2': 'Statistical discrepancy (income approach)',
                         'P3_P5': 'Final consumption expenditure and gross capital formation',
                         'P3_P6':'Final consumption expenditure, gross capital formation and exports of goods and services',
                        }})

df = df.replace({'unit' : {'CLV_I10': 'Chain linked volumes, index 2010=100',
                      'CLV_I05': 'Chain linked volumes, index 2005=100',
                      'PC_GDP': 'Percentage of gross domestic product (GDP)',
                      'PC_EU28_MEUR_CP': 'Percentage of EU28 total (based on million euro), current prices',
                      'PC_EU28_MPPS_CP': 'Percentage of EU28 total (based on million PPS), current prices',
                      'CP_MEUR': 'Current prices, million euro',
                      'CP_MNAC': 'Current prices, million units of national currency',
                      'CP_MPPS': 'Current prices, million purchasing power standards',
                      'CLV05_MEUR': 'Chain linked volumes (2005), million euro',
                      'CLV05_MNAC': 'Chain linked volumes (2005), million units of national currency',
                      'CLV10_MEUR': 'Chain linked volumes (2010), million euro',
                      'CLV10_MNAC': 'Chain linked volumes (2010), million units of national currency',
                      'CLV_PCH_PRE': 'Chain linked volumes, percentage change on previous period',
                      'PYP_MNAC': 'Previous year prices, million units of national currency',
                      'PYP_MEUR': 'Previous year prices, million euro',
                      'CON_PPCH_PRE': 'Contribution to GDP growth, percentage point change on previous period',
                      'PD10_NAC': 'Price index (implicit deflator), 2010=100, national currency',
                      'PD05_NAC': 'Price index (implicit deflator), 2005=100, national currency',
                      'PD10_EUR': 'Price index (implicit deflator), 2010=100, euro',
                      'PD05_EUR': 'Price index (implicit deflator), 2005=100, euro',
                      'PD_PCH_PRE_NAC': 'Price index (implicit deflator), percentage change on previous period, national currency',
                      'PD_PCH_PRE_EUR': 'Price index (implicit deflator), percentage change on previous period, euro',
                        }})

df = df.rename(columns=lambda x: x.strip())


# In[ ]:


# Transforming the dataframe into a more analysis-friendly form

df = pd.melt(frame=df, id_vars=['unit', 'indicator', 'geo'], value_vars=[str(i) for i in range(1975,2017)], var_name = 'year', value_name = 'value')


# In[ ]:


#show current form of dataframe
df.head(10)


# In[ ]:


# Changing the year-column into int type, which necessary in order to make the slicer work correctly

df['year'] = df['year'].astype('int64')


# In[ ]:


# Build dashboard
# I added an interactive hover element

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

available_indicators = df['indicator'].unique()
available_units = df['unit'].unique()
available_geos = df['geo'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            html.H2(children='Select Measurement Unit'),
            dcc.Dropdown(
                id='unit',
                options=[{'label': i, 'value': i} for i in available_units],
                value='Current prices, million euro'
            )]),

        html.Div([
            html.H2(children='Select First Indicator'),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Exports of goods and services'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            html.H2(children='Select Second Indicator'),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Imports of goods and services'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thick black solid',
        'backgroundColor': 'rgb(255, 175, 181)',
        'padding': '5px 3px'
    }),

    html.Div([
        dcc.Graph(
            id='indicator-scatter',
            hoverData={'points': [{'customdata': 'Spain'}]}
        )
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 20'}),    
    
    html.Div(dcc.Slider(
        id='year--slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].max(),
        step=None,
        marks={str(year): str(year) for year in df['year'].unique()}

    ), style={'width': '100%', 'padding': '10px 20px 20px 20px'}),
    
    html.Div([
        dcc.Graph(id='x-time-series')
    ], style={'display': 'inline-block', 'width': '99%'}),
    
   

])


@app.callback(
    dash.dependencies.Output('indicator-scatter', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('year--slider', 'value'),
     dash.dependencies.Input('unit', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value, unit_value):
    dff = df[df['year'] == year_value]
    dff = dff[dff['unit'] == unit_value]

    return {
        'data': [go.Scatter(
            x=dff[dff['indicator'] == xaxis_column_name]['value'],
            y=dff[dff['indicator'] == yaxis_column_name]['value'],
            text=dff[dff['indicator'] == yaxis_column_name]['geo'],
            customdata=dff[dff['indicator'] == yaxis_column_name]['geo'],
            mode='markers',
            marker={
                'size': 50,
                'opacity': 0.7,
                'color' : 'rgba(152, 0, 0, .8)',
                'line': {'width': 1.0, 'color': 'black'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }


def create_time_series(dff, axis_type, title):
    return {
        'data': [go.Scatter(
            x=dff['year'],
            y=dff['value'],
            mode='lines+markers',
            marker={
            'size': 10,
            'color': 'rgba(152, 0, 0, .8)',
            'line': {'width': 3.0, 'color': 'black'}
            }
        )],
        'layout': {
            'height': 250,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 175, 181, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': True}
        }
    }


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('indicator-scatter', 'hoverData'),
     dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('unit', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name, axis_type, unit_value):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['geo'] == country_name]
    dff = dff[dff['unit'] == unit_value]
    dff = dff[dff['indicator'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)



if __name__ == '__main__':
    app.run_server()

