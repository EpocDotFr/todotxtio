PyAIMP documentation
====================

Welcome! This documentation is about PyAIMP, a Python `AIMP <http://www.aimp.ru/>`_ remote API wrapper with some extras.

|pyversion| |pypiv| |pypil|

PyAIMP comes as a simple Python module that covers 100% of the AIMP remote API features with the help of `pywin32 <https://pypi.python.org/pypi/pypiwin32>`_ (the only dependency).

Prerequisites
-------------

  - Python 3.5+
  - AIMP

Installation
------------

The usual way:

.. code-block:: console

    $ pip install pyaimp

The McGyver way, after cloning/downloading this repo:

.. code-block:: console

    $ python setup.py install

Usage
-----

Create a :class:`pyaimp.Client` instance and you are ready to use any of its public methods.

Example displaying the current playback state:

.. code-block:: python

    import pyaimp

    try:
        client = pyaimp.Client()

        state = client.get_playback_state()

        if state == pyaimp.PlayBackState.Stopped:
            print('AIMP actually doesn\'t play anything')
        elif state == pyaimp.PlayBackState.Paused:
            print('AIMP is taking a break')
        elif state == pyaimp.PlayBackState.Playing:
            print('Rock \'n Roll baby')
    except RuntimeError as re: # AIMP instance not found
        print(re)
    except Exception as e:
        print(e)

Continue reading to know about what you can do.

.. note::

   Events are not yet supported.

API docs
--------

.. automodule:: pyaimp
   :members:
   :undoc-members:

.. |pyversion| image:: https://img.shields.io/pypi/pyversions/pyaimp.svg?link=https://pypi.python.org/pypi/pyaimp
.. |pypiv| image:: https://img.shields.io/pypi/v/pyaimp.svg?link=https://pypi.python.org/pypi/pyaimp
.. |pypil| image:: https://img.shields.io/pypi/l/pyaimp.svg?link=https://github.com/EpocDotFr/pyaimp/blob/master/LICENSE.md