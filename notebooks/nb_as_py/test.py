# ---
# jupyter:
#   jupytext:
#     formats: ipynb,nb_as_py//py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# + [markdown] toc=true
# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Libvis-basic-usage" data-toc-modified-id="Libvis-basic-usage-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Libvis basic usage</a></span><ul class="toc-item"><li><span><a href="#Start-the-server" data-toc-modified-id="Start-the-server-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Start the server</a></span></li><li><span><a href="#Visualisation-of-different-objects" data-toc-modified-id="Visualisation-of-different-objects-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>Visualisation of different objects</a></span><ul class="toc-item"><li><span><a href="#Number-->-Number" data-toc-modified-id="Number-->-Number-1.2.1"><span class="toc-item-num">1.2.1&nbsp;&nbsp;</span>Number -&gt; Number</a></span></li><li><span><a href="#List-of-numbers-->-Line-graph" data-toc-modified-id="List-of-numbers-->-Line-graph-1.2.2"><span class="toc-item-num">1.2.2&nbsp;&nbsp;</span>List of numbers -&gt; Line graph</a></span></li><li><span><a href="#2d-Array-->-Image" data-toc-modified-id="2d-Array-->-Image-1.2.3"><span class="toc-item-num">1.2.3&nbsp;&nbsp;</span>2d Array -&gt; Image</a></span></li></ul></li><li><span><a href="#Restart-the-server" data-toc-modified-id="Restart-the-server-1.3"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>Restart the server</a></span></li><li><span><a href="#Live-data-stream" data-toc-modified-id="Live-data-stream-1.4"><span class="toc-item-num">1.4&nbsp;&nbsp;</span>Live data stream</a></span></li><li><span><a href="#Matplotlib-figures" data-toc-modified-id="Matplotlib-figures-1.5"><span class="toc-item-num">1.5&nbsp;&nbsp;</span>Matplotlib figures</a></span></li><li><span><a href="#Bokeh-figures" data-toc-modified-id="Bokeh-figures-1.6"><span class="toc-item-num">1.6&nbsp;&nbsp;</span>Bokeh figures</a></span></li><li><span><a href="#Camera-live-stream" data-toc-modified-id="Camera-live-stream-1.7"><span class="toc-item-num">1.7&nbsp;&nbsp;</span>Camera live stream</a></span></li></ul></li></ul></div>

# +
import numpy as np
import matplotlib.pyplot as plt
from tqdm.auto import tqdm
import time

from libvis import Vis
import libvis.modules

# %load_ext autoreload
# %autoreload 2
# -

# ## Libvis basic usage
#

# ### Start the server
#

vis = Vis(ws_port=7700, vis_port=7000)


vis.start()

# ### Visualisation of different objects
# #### Number -> Number
#

vis.vars.number = 1

# #### List of numbers -> Line graph
#
# The idea behind libvis is that any object has a visual representation.
# The default representation for a `list` is a line graph.
#
# The 1-d numpy array also will be represented as a line graph
#

# +
vis.vars.graph = [2, 1, 7, 1, 8, 2, 8]

x = np.linspace(0, 10, 50)
vis.vars.graph_np = np.sin(x)
# -

# #### 2d Array -> Image
#

im = np.random.randn(120,101)*145
vis.vars.image = im


# ### Restart the server



vis.stop()

vis.start()

# ### Live data stream

vis.vars.bii = [1]
for i in range(60):
    vis.vars.bii+=[np.random.randint(100)]
    time.sleep(.01)

# +
# %%time

for i in tqdm(range(100)):
    vis.vars.test=np.sin(
        [
         np.linspace(0 +i/10,10+i/10, 40)
        ,np.linspace(10+i/5, 10+i/10, 40)
        ,np.linspace(10+i/5, 5 +i/10, 40)
        ]
    ).tolist()
    time.sleep(0.1)
#jkjkvis.vars['test']
# -

# ### Matplotlib figures

# generate df
N = np.random.randn(1000)
fig, ax = plt.subplots(figsize=(10,5))
ax.hist(N,bins=100)
vis.vars.image = fig


# ### Bokeh figures

# +
from bokeh.plotting import figure
from bokeh.transform import linear_cmap
from bokeh.util.hex import hexbin
from bokeh.embed import file_html
import bokeh

n = 50000
x = np.random.standard_normal(n)
y = np.random.standard_normal(n)

bins = hexbin(x, y, 0.1)

p = figure(title="Manual hex bin for 50000 points", tools="wheel_zoom,pan,reset",
           match_aspect=True,
           sizing_mode='stretch_both',
           plot_width=300, plot_height=300,
           background_fill_color='#440154')
p.grid.visible = False

p.hex_tile(q="q", r="r", size=0.1, line_color=None, source=bins,
           fill_color=linear_cmap('counts', 'Viridis256', 0, max(bins.counts)))
type(p)

vis.vars.bokeh = p
print(isinstance(p,bokeh.model.Model))
print(isinstance(p,bokeh.document.document.Document))

#output_file("hex_tile.html")

# +
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="whitegrid")

# Load the example iris dataset
diamonds = sns.load_dataset("diamonds")

# Draw a scatter plot while assigning point colors and sizes to different
# variables in the dataset
f, ax = plt.subplots(figsize=(6.5, 6.5))
sns.despine(f, left=True, bottom=True)
clarity_ranking = ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"]
sns.scatterplot(x="carat", y="price",
                hue="clarity", size="depth",
                palette="ch:r=-.2,d=.3_r",
                hue_order=clarity_ranking,
                sizes=(1, 8), linewidth=0,
                data=diamonds, ax=ax)

vis.vars.sns = f
# -

# ### Camera live stream

import cv2


# +
cap = cv2.VideoCapture(1)
camera_opened = cap.isOpened()
print('Camera opened:', camera_opened)

if camera_opened:
    ret, frame = cap.read()
    if ret:
        print('Camera frame shape:', frame.shape)
# -


for i in range(10):
    
    ret, frame = cap.read()
    if ret:
        vis.vars.image = frame[:320, :480, :]
    
    time.sleep(0.9)


# close the camera 
cap.release()


# Stop the server
vis.stop()

