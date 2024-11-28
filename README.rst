|PyPI| |Build Status| |codecov.io|

===
xo1
===

Python framework for creating terminal applications.

Requirements
============

* >=python-3.10
* >=eaf-0.2

Installation
============

.. code-block:: console

	$ pip install xo1


Development
===========

Installation
------------

.. code-block:: console

   $ uv sync --extras dev

Testing
-------

.. code-block:: console

   $ uv run poe ci  # Run all the checks.

   # Or run them separately.
   $ uv run poe test
   $ uv run poe format
   $ # run type checking
   $ uv run poe typecheck
   $ # run code linting
   $ uv run poe lint

Documentation
-------------

* **To be added**

.. |PyPI| image:: https://badge.fury.io/py/xo1.svg
   :target: https://badge.fury.io/py/xo1
.. |Build Status| image:: https://github.com/pkulev/xo1/workflows/CI/badge.svg
.. |codecov.io| image:: http://codecov.io/github/pkulev/xo1/coverage.svg?branch=master
   :target: http://codecov.io/github/pkulev/xo1?branch=master
