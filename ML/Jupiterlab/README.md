* Reference link: https://nathan.vertile.com/blog/2017/12/07/run-jupyter-notebook-behind-a-nginx-reverse-proxy-subpath/

* Install Anaconda 5.3:
  * wget https://repo.anaconda.com/archive/Anaconda3-5.3.0-Linux-x86_64.sh
  * bash Anaconda3-5.3.0-Linux-x86_64.sh
  * It will prompt for setting, fill in as needed

* __For first time setup__: conda create -n py35 python=3.5 anaconda - This installs and setup python 3.5 environment.

* Install jupiterlab:
  * conda install -c conda-forge jupyterlab
* Install ipython:
  conda install ipython

* Configure jupiterlab to work with Ngnix:
  * jupyter notebook --generate-config
  * vim /home/sdn-nfv/.jupyter/jupyter_notebook_config.py
  * Write below config at the end of file
    ```
    c.NotebookApp.allow_origin = '*'
    c.NotebookApp.base_url = '/jupiterlab'
    c.NotebookApp.port = 8888
    ```
