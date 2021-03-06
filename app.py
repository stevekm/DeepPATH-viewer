#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Dash app to view DeepPATH analysis output

https://github.com/plotly/dash/issues/71
https://github.com/plotly/dash-core-components/pull/73
https://community.plot.ly/t/data-from-file-in-dash-upload-component/4922
https://plot.ly/python/heatmaps/
https://plot.ly/python/reference/#heatmap
https://plot.ly/python/reference/#layout-images
https://community.plot.ly/t/using-local-image-as-background-image/4381

https://plot.ly/dash/dash-core-components/upload
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import plotly.plotly as py
import plotly.graph_objs as go
import base64
import os
import glob
import io


# ~~~~ FUNCTIONS ~~~~~ #
def get_images(image_directory, exts = ['.jpg']):
    """
    Get the images in a dir
    """
    paths = []
    for ext in exts:
        ext_pattern = '*{0}'.format(ext)
        search_pattern = os.path.join(image_directory, ext_pattern)
        for image in glob.glob(search_pattern):
            paths.append(image)
    return(paths)

def _heatmap():
    """
    Demo Plotly heatmap
    """
    heatmap = go.Heatmap(
    z=[[1, 20, 30], [20, 1, 60], [30, 60, 1]],
    opacity = 0
    )
    return(heatmap)

def _layout():
    """
    Demo heatmap layout
    """
    layout = go.Layout(
    title='User Uploaded Image',
    xaxis = dict(visible = False),
    yaxis = dict(visible = False),
    images= [dict(
                  source= "https://images.plot.ly/language-icons/api-home/python-logo.png",
                  xref= "x",
                  yref= "y",
                  x= 0,
                  y= 0,
                  sizex= 2,
                  sizey= 2,
                  sizing= "stretch",
                  opacity= 0.5,
                  layer= "below",
                  xanchor= "middle",
                  yanchor= "middle")]
    )
    return(layout)

def parse_contents(contents, filename, date):
    """
    Parses the file uploaded by the user
    """
    content_type, content_string = contents.split(',')

    default_message = 'heres your file:\n\n{0}\n\n{1}\n\n{2}\n\n{3}'.format(filename, date, content_type, content_string)

    decoded = base64.b64decode(content_string)
    # decoded_io = io.StringIO(decoded.decode('utf-8'))

    try:
        encoded_image = base64.b64encode(open(filename, 'rb').read())

        return(html.Div([
                html.Img(id='image1', style = {"max-width": "100%", "max-height": "100%"}, src='data:image/png;base64,{}'.format(encoded_image)),
                default_message
            ]))
    except:
        return(html.Div([
                "The image parsing broke !!",
                default_message
            ]))

# ~~~~~ SETUP ~~~~~ #
image_directory = 'input'
image_filename = os.path.join(image_directory, 'cat.jpg')
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
static_image_route = '/static/'
list_of_images = get_images(image_directory)


# ~~~~~ APP LAYOUT ~~~~~ #
app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='DeepPATH Viewer'),

    html.Div(id = 'row1', className = 'row', children=[
    html.Div(id = 'row1-col1', className = 'row', children=[
    html.Div(id = 'image1-dropdown-div', children=[
    html.H2(children='Select first image:'),
    dcc.Dropdown(
        id='image1-dropdown',
        options=[{'label': i, 'value': i} for i in list_of_images]
    ),
    html.Div(id = 'image1-div')
    ])
    ], style = {'float': 'left', 'width': "48%"}),


    html.Div(id = 'row1-col2', className = 'row', children=[
    html.Div(id = 'image2-dropdown-div', children=[
    html.H2(children='Select second image:'),
    dcc.Dropdown(
        id='image2-dropdown',
        options=[{'label': i, 'value': i} for i in list_of_images]
    ),
    html.Div(id = 'image2-div')
    ])
    ], style = {'float': 'left', 'width': "48%"})


    # html.Div(children=[
    # dcc.Graph( id = "heatmap", figure = go.Figure(  data = [ _heatmap() ],
    #                                                 layout = _layout() ) )
    # ])

    ]),


    html.Div(id = 'row2', className = 'row', children=[
    html.Div(id = 'row2-col1', className = 'row', children=[
    html.Div(id = 'image-upload-div', children=[
    html.H2(children='Upload an image:'),
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-image-upload'),

    ])
    ], style = {'float': 'left', 'width': "48%"})
    ])

])



# ~~~~~ APP SERVER ~~~~~ #
@app.callback(
    Output(component_id = 'image1-div', component_property = 'children'),
    [Input(component_id = 'image1-dropdown', component_property = 'value')]
)
def update_image1(input_value):
    """
    """
    if not input_value:
        return("No image selected")
    if input_value not in list_of_images:
        return("Invalid selection")
    else:
        encoded_image = base64.b64encode(open(input_value, 'rb').read())
        return(html.Img(id='image1', style = {"max-width": "100%", "max-height": "100%"}, src='data:image/png;base64,{}'.format(encoded_image)))

@app.callback(
    Output(component_id = 'image2-div', component_property = 'children'),
    [Input(component_id = 'image2-dropdown', component_property = 'value')]
)
def update_image2(input_value):
    """
    """
    if not input_value:
        return("No image selected")
    if input_value not in list_of_images:
        return("Invalid selection")
    else:
        encoded_image = base64.b64encode(open(input_value, 'rb').read())
        return(html.Img(id='image2', style = {"max-width": "100%", "max-height": "100%"}, src='data:image/png;base64,{}'.format(encoded_image)))

@app.callback(Output('output-image-upload', 'children'),
              [Input('upload-image', 'contents'),
               Input('upload-image', 'filename'),
               Input('upload-image', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return(children)


if __name__ == '__main__':
    app.run_server(debug=True)
