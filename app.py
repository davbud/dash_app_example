
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

# In[1]:


#Install the relevant packages

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv('data.csv')

df.head(5)


# In[2]:


#renaming column headers for dashboard
df = df.rename(index=str, columns={"TIME":"year","GEO":"geo","UNIT":"unit","NA_ITEM":"indicator","Value":"value"})

#df.rename(index=str, columns={"A": "a", "C": "c"})


# In[ ]:


#show current form of dataframe
df.head(10)


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

