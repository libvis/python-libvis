Simple use story
================
    
Let's say you want to run a simple python program that counts sheep that jump over a fence.
And some sheep are not able to make it.

.. code-block:: python

    for s in generate_sheep(100):
        jump_result = random.choice([True, False])
        if jump_result is False:
            print('Oops, failed to jump!')

And you are really interested in how many sheep couldn't jump.
In fact, you are so interested that you don't want to wait until the loop ends.
You want to monitor them `live`.

One way of doing it is to use plain old ``print`` function.
just output total number of fails every time one occurs.
This will leave you with a mess in your console output.

Another option is to use `libvis`.

.. code-block:: python

    from libvis import Vis
    vis = Vis(vis_port=7000)

    for s in generate_sheep(100):
        jump_result = random.choice([True, False])
        if jump_result is False:
            print('Oops, failed to jump!')
            vis.vars.fails += 1

Now, you have a live dashboard running at http://localhost:7000
with up-to-date number of your poor sheep.

