# Source Code for Masterthesis: Assessing and Predicting the Optimal Imputation Method Regarding the Predictive Performance of Machine Learning Models

## Target 
An optimization approach for decision making in data science based on benchmarking the impact of different data imputation methods on the predictive performance of machine learning models.

## Disclaimer

This is research project and not intended for production usage.

This Masterthesis is building on the work of Sebastian Jäger, Arndt Allhorn and Felix Bießmann, as described in their paper: "A Benchmark for Data Imputation Methods"
https://www.frontiersin.org/article/10.3389/fdata.2021.693674




## Installation

Steps to set up the required conda environment:

1. create an environment `Data-Imputation-Thesis` with [conda],
   ```bash
   conda env create -f environment.yaml
   ```
2. activate the new environment
   ```bash
   conda activate Data-Imputation-Thesis
   ```
3. install `jenga` 
   ```bash
   cd src/jenga
   python setup.py develop
   ```
4. install `data-imputation-paper`
   ```bash
   cd ../..
   python setup.py develop # or `install`
   ```
It might be necessary to install the required GPU drivers manually (Version might change based on used hardware):
   ```bash
   conda install -c conda-forge cudatoolkit=11.7.0
   pip install nvidia-cudnn-cu11==8.6.0.163
   ```
Activate the packages every time you activate the environment:
   ```bash
   CUDNN_PATH=$(dirname $(python -c "import nvidia.cudnn;print(nvidia.cudnn.__file__)"))
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/:$CUDNN_PATH/lib
   ```
https://www.tensorflow.org/install/pip


## Usage

- Imputation Experiments
  execute `run-experiment.py`with the required settings (explained below). The experiment name must contain `corrupted.

- Baseline Experiments
  execute `run-experiment.py`with the required settings (explained below). The experiment name is not allowed to contain `corrupted.

- Imputation Experiments
  execute `run-experiment-subset.py`with the required settings (explained below). The experiment name must contain `corrupted.

- Baseline Experiments
  execute `run-experiment-subset.py`with the required settings (explained below). The experiment name is not allowed to contain `corrupted.


- Examples to start the experiments
  start requires the ID of the dataset (737), imputation method (mode), experiment name (test_experiment), missing fractions (0.3, 0.5), missing patterns (MAR,MCAR), strategies (single_single), number of repetitions (3), and a path to the storage folder for results (../results).

  ```bash
  python run-experiment.py 737 mode test_experiment --missing-fractions 0.3,0.5 --missing-types MAR,MCAR --strategies single_single --num-repetitions 3 --base-path ../results
  ```




### Note from Sebastian Jäger

This project has been set up using PyScaffold 3.2.2 and the [dsproject extension] 0.4.
For details and usage information on PyScaffold see https://pyscaffold.org/.

[conda]: https://docs.conda.io/
[pre-commit]: https://pre-commit.com/
[Jupyter]: https://jupyter.org/
[nbstripout]: https://github.com/kynan/nbstripout
[Google style]: http://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
[dsproject extension]: https://github.com/pyscaffold/pyscaffoldext-dsproject
