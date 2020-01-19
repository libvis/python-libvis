
.. image:: https://img.shields.io/pypi/v/webvis.svg
    :target: https://pypi.python.org/pypi/webvis
    :alt: PyPi version


Data visualization made easier
==============================

This is a project for interactive data visualization

It uses a dedicated web app with cards that display python variables.

Check out the notebooks folder for examples

Jump right in: `Quick start <http://docs.webvis.dev/usage/quickstart.html#>`_.


Quick start
-----------

.. code-block:: python

   from webvis import Vis
   import time

   vis = Vis(vis_port=7007)
   vis.start()
   # Opens the browser on 7007 port 
   vis.show()

   # Live plotting
   for i in range(0,100):
      vis.vars.line = [(2**x)%100 for x in range(i)]
      time.sleep(.2)

Add a widget, call it "line", and a live plot appears.

WebVis is a live object visualization tool, best used with jupyter notebook.

A separate thread is created that checks the changes. No network requests performed in main thread.

Values can be matplotlib figures, 1-d and 2-d arrays,
and even bokeh is supported!

Documentation
-------------

http://docs.webvis.dev

