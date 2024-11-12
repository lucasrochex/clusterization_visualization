import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from dash import Dash, dcc, html, Input, Output, no_update
from PIL import Image
import random

def generate_random_hex_color():
    """Generates a random hex color code."""
    return "#" + ''.join(random.choices('0123456789ABCDEF', k=6))

# Directory where the original images are located
image_dir = '/tf/birds/'

# Opening the .csv with the 3 "main" pca's and the image cluster
images_df = pd.read_csv('birds.csv', sep='|')
images_df = images_df.sort_values('images_cluster_s')
# Cluster number column is converted to string so that plotly can interpret it as categorical
images_df['images_cluster_s'] = images_df['images_cluster_s'].apply(lambda x: str(x))

print('Amount of images before filter:', len(images_df))
# This filter allows us to get the images closest to cluster centroid, hence, the best representatives of the cluster.
# The smaller this value the closest to centroid
filter_std = (images_df['std_units']<0)
images_df = images_df[filter_std]

print('Amount of images after filter:', len(images_df))

# Generating the dashboard
num_clusters = len(images_df['images_cluster_s'].unique())
discrete_colors = [generate_random_hex_color() for a in range(num_clusters)]

fig = px.scatter_3d(images_df,
                    x='pca_1',
                    y='pca_2',
                    z='pca_3',
                    hover_data='image_name',
                    color = 'images_cluster_s',
                    height = 1000,
                    width=1000,
                    color_discrete_sequence=discrete_colors
                )

fig.update_layout(
    autosize=False,
    title="PCA and clustering - Birds",
    width=1000,
    height=1000,
    margin=dict(l=50, r=50, b=100, t=100, pad=10),
    scene=dict(
        xaxis=dict(title="x"),
        yaxis=dict(title="y"),
        zaxis=dict(title="z"),
    ),
)


app = Dash(__name__)

app.layout = html.Div(
    style={'display': 'flex'},
    children = [
        html.Div(
            dcc.Graph(id="graph-basic-2", figure=fig)
        ),
        html.Div(
            style={'width': '50%', 'height': '100%', 'verticalAlign': 'center', 'marginLeft': '10px', 'marginRight': '5px'},
            children=[
                dcc.Graph(id='image_holder', figure={}, style = {'marginLeft': '10px', 'marginRight': '10px', 'marginTop': '10px'})
            ],
            id='carousel'
        )
    ]
    
)

@app.callback(
    #Output("carousel", "children"),
    Output("image_holder", 'figure'),
    Input("graph-basic-2", "hoverData"),
)
def display_hover(hoverData):
    print(hoverData)
    #if hoverData is not None:
    #    image_name = (hoverData['points'][0]['customdata'][0])
    #else:
    #    return

    image_name = (hoverData['points'][0]['customdata'][0])
    #foto_path = f'{image_dir}/{image_name}'
    foto_path = image_name.replace('data/', '/tf/birds/data/')
    #print(foto_path)
    print(image_name)
    img = np.array(Image.open(image_name))
    fig = px.imshow(img, color_continuous_scale="gray")
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    return fig 

if __name__ == "__main__":
    print('Oi')
    app.run_server(debug=True, host='0.0.0.0', port=8851)