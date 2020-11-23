

.. raw:: html

    <div align="center">
        <a href="http://libvis.dev>
        <img width="312px" alt="libvis logo" src="assets/libvis.png"/>
        </a>
    </div>
    
.. image:: https://img.shields.io/pypi/v/libvis.svg
    :target: https://pypi.python.org/pypi/libvis
    :alt: PyPi version
    

`libvis.dev <https://libvis.dev>`_

Data visualization made easier
==============================

This is a project for interactive data visualization

It uses a dedicated web app with widgets that show live state of python variables.

Example `notebooks <notebooks>`_ are:

- `basics <notebooks/test.ipynb>`_.
- `using for ML  <notebooks/libvis_with_pytorch.ipynb>`_.
- `writing custom modules <notebooks/modules.ipynb>`_.

`Quick start <http://docs.libvis.dev/usage/quickstart.html#>`_.


Quick start
-----------

.. code-block:: python

   from libvis import Vis
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

Libvis is a live object visualization tool, best used with jupyter notebook.

A separate thread is created that checks the changes. No network requests performed in main thread.

Values can be matplotlib figures, 1-d and 2-d arrays,
and even bokeh is supported!

Documentation
-------------

http://docs.libvis.dev

