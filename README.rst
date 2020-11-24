
.. raw:: html

    <div align="center">
        <a href="http://libvis.dev>
        <img width="312px" alt="libvis logo" src="assets/libvis.png"/>
        </a>
    </div>
    

.. image:: https://libvis.dev/libvis-sm.png


.. image:: https://img.shields.io/pypi/v/libvis.svg
    :target: https://pypi.python.org/pypi/libvis
    :alt: PyPi version
    

`libvis.dev <https://libvis.dev>`_

Live data visualization
=======================


This project allow live and interactive visualization of python variables
in a web dashboard application.
Data is sent both ways: you can visualize and update the
variables while running another code.


`Machine learning visualization <#machine-learning-visualization>`_:

.. image:: assets/torch_adv_demo.gif


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

   vis = Vis()
   vis.show() # Opens the browser on 7000 port 

   # Live plotting
   for i in range(0,100):
      vis.vars.line = [(2**x)%100 for x in range(i)]
      time.sleep(.2)

You should see a live plot of the `vis.vars.line` object.

Libvis is a live object visualization tool, best used with jupyter notebook.

Natively supported variables:

- 1-d array -> line plot
- tuple of 2 1-d arrays -> line plot with custom x-values
- 2-d array -> image
- matplotlib and seaborn figures
- bokeh figures

See `notebooks/test <notebooks/test.ipynb>`_
for more detailed usage.


Use cases
---------

.. _ml-vis:

Machine learning visualization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using as a live visualization of machine learning training.


Features:

- Live loss plot
- Learning rate adjustments while training
- Live histograms of gradients/weights
- Real-time confusion matrix for each training batch

Demo notebooks:

- `Basic usage <notebooks/libvis_with_pytorch.ipynb>`_: loss plot + learning rate
- `Advanced usage <notebooks/torch_advanced.ipynb>`_: histograms and confusion matrix

.. image:: assets/torch_adv_demo.gif



How this works?
---------------

A separate thread is created that checks the changes. No network requests performed in main thread.

The overhead is negligible, most of the time libvis spends waiting for updates.
There are two ways to send updates to front:

Watch a variable
~~~~~~~~~~~~~~~~

This approach is useful for rapidly-updating or large data.
It periodically sends updates about a mutable variable.

.. code-block:: python

    mylist = []
    vis.watch(mylist, 'mylist')

    mylist.append(2) # will be sent every 0.2 seconds by default

Update by setting an attribute
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This approach is good when you want faster update speeds
and don't have updates very frequently.
Each time a live object is assigned an attribute,
the updates are scheduled to sending.


.. code-block:: python

    image = libvis.modules.insatlled.Image()
    vis.vars.image = image
    image.data = test_data # sends data (almost) immediately

Documentation
-------------

http://docs.libvis.dev

