# What is *tmap*?

For large scale and integrative microbiome research, it is expected to apply advanced data mining techniques in microbiome data analysis.

Topological data analysis (TDA) provides a promising technique for analyzing large scale complex data. The most popular *Mapper* algorithm is effective in distilling data-shape from high dimensional data, and provides a compressive network representation for pattern discovery and statistical analysis.

***tmap*** is a topological data analysis framework implementing the TDA *Mapper* algorithm for population-scale microbiome data analysis. We developed ***tmap*** to enable easy adoption of TDA in microbiome data analysis pipeline, providing network-based statistical methods for enterotype analysis, driver species identification, and microbiome-wide association analysis of host meta-data.

# How to Install?

To install tmap, run:
```bash
    # (recommend)
    git clone https://github.com/GPZ-Bioinfo/tmap.git
    cd tmap
    python setup.py install
    # For some dependency problems. please install following packages.
    pip install scikit-bio
    R -e "install.packages('vegan',repo='http://cran.rstudio.com/')"
```

or you could also use pip now:
```bash
pip install tmap
```

Now, we also provide a better way to install tmap package. Using [docker](https://docs.docker.com/) and [dockerfile](https://github.com/GPZ-Bioinfo/tmap/blob/master/dockerfile) to build a images to solve all dependency problems.

After clone the repositories, you could use `cd tmap; docker build -t tmap .`

If you encounter any error like `Import error: tkinter`, you need to run `sudo apt install python-tk` or `sudo apt install python3-tk`.

# Documentation

* [Basic Usage of tmap](https://tmap.readthedocs.io/en/latest/basic.html)
* [How to Choose Parameters in tmap](https://tmap.readthedocs.io/en/latest/param.html)
* [Visualizing and Exploring TDA Network](https://tmap.readthedocs.io/en/latest/vis.html)
* [Network Statistical Analysis in tmap](https://tmap.readthedocs.io/en/latest/statistical.html)
* [How tmap work](https://tmap.readthedocs.io/en/latest/how2work.html)
* [Microbiome Examples](https://tmap.readthedocs.io/en/latest/example.html)
* [Tutorial of executable scripts](https://tmap.readthedocs.io/en/latest/scripts.html)
* [API](https://tmap.readthedocs.io/en/latest/api.html)
* [Reference](https://tmap.readthedocs.io/en/latest/reference.html)
* [FAQ](https://tmap.readthedocs.io/en/latest/FAQ.html)

# Quick Guides

You can read the [Basic Usage of tmap](https://tmap.readthedocs.io/en/latest/basic.html) for general use of tmap.
Or follow the [Microbiome examples](https://tmap.readthedocs.io/en/latest/example.html) for using tmap in microbiome analysis.

For more convenient usage, we implement some executable scripts which will automatically build upon `$PATH`. For more information about these scripts, you could see.
[Tutorial of executable scripts](https://tmap.readthedocs.io/en/latest/scripts.html)

# Publication
Liao, T., Wei, Y., Luo, M. *et al*. *tmap*: an integrative framework based on topological data analysis for population-scale microbiome stratification and association studies. Genome Biol 20, 293 (2019) [doi:10.1186/s13059-019-1871-4](https://doi.org/10.1186/s13059-019-1871-4)

# Contact Us
If you have any questions or suggestions, you are welcome to contact us via email: haokui.zhou@gmail.com.
