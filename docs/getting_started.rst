===============
Quickstart
===============

Requirements
------------
The Bucky model currently supports Linux and OSX and includes GPU support for accelerated modeling and processing. Anaconda environment files are provided for installation of dependencies. 

Installation
------------
Clone the repo using git:

.. code-block:: bash

    git clone https://github.com/mattkinsey/bucky.git


Create Anaconda environment using `environment.yml` or `environment_gpu.yml` if using the GPU.

.. code-block:: bash

    conda env create --file environment[_gpu].yml
    conda activate bucky[_gpu]


*Optional*: Data and output directory default locations are defined in `config.yml`. Edit this file to change these.

Download the required US data using the provided shell script:

.. code-block:: bash

    ./get_US_data.sh


Running the Model
-----------------

In order to illustrate how to run the model, this section contains the commands needed to run a small simulation. First, create the intermediate graph format used by the model. This graph contains county-level data on the nodes and mobility information on the edges. The command below creates a US graph for a simulation that will start on October 1, 2020. 

.. code-block:: bash

    ./bmodel make_input_graph -d 2020-10-01

After creating the graph, run the model with 100 iterations and 20 days:

.. code-block:: bash

    ./bmodel model -n 100 -d 20

This will create a folder in the `raw_output` directory with the unique run ID. The script `postprocess` processes and aggregates the Monte Carlo runs. This script by default postprocesses the most recent data in the `raw_output` directory and aggregates at the national, state, and county level.

.. code-block:: bash

    ./bmodel postprocess


Visualizing Results
-------------------
To create plots:

.. code-block:: bash

    ./bmodel viz.plot


Like postprocessing, this script by default creates plots for the most recently processed data. Plots will be located in `output/<run_id>/plots`. These plots can be customized to show different columns and historical data. See the documentation for more.

Lookup Tables
-------------

During postprocessing, the graph file is used to define geographic relationships between administrative levels (e.g. counties, states). In some cases, a user may want to define custom geographic groupings for visualization and analysis. For example, the National Capital Region includes counties from Maryland and Virginia along with Washington, DC. An example lookup table for this region (also known as the DMV) is included in the repo, *DMV.lookup*. 

To aggregate data with this lookup table, use the flag `--lookup` followed by the path to the lookup file:

.. code-block:: bash

    ./bmodel postprocess --lookup DMV.lookup

This will create a new directory with the prefix *DMV_* in the default output directory (output/DMV_<run_id>/). To plot:

.. code-block:: bash

  ./bmodel model viz.plot --lookup DMV.lookup

