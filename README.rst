|PyPI| |Build Status| |codecov.io|

===
xo1
===

Python framework for creating terminal applications.

Requirements
============

* >=python-3.7
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

   $ poetry install

Testing
-------

.. code-block:: console

   $ poetry run pytest -s -v tests/  # run all tests
   $ poetry run pytest --cov=xo1 -s -v tests/  # run all tests with coverage
   $ poetry run black xo1/ tests/  # autoformat code
   $ # run type checking
   $ poetry run pytest --mypy --mypy-ignore-missing-imports -s -v xo1/ tests/
   $ # run code linting
   $ poetry run pytest --pylint -s -v xo1/ tests/

Documentation
-------------

* **To be added**

.. |PyPI| image:: https://badge.fury.io/py/xo1.svg
   :target: https://badge.fury.io/py/xo1
.. |Build Status| image:: https://github.com/pkulev/xo1/workflows/CI/badge.svg
.. |codecov.io| image:: http://codecov.io/github/pkulev/xo1/coverage.svg?branch=master
   :target: http://codecov.io/github/pkulev/xo1?branch=master
