# Abstract

`Guaraci` is a solar flare forecasting system to deploy classifiers optimized in this [automated toolkit](https://github.com/tiagocinto/guaraci-toolkit). For further information on such a toolkit, refer to:

* CINTO, T. et al. A Framework for Designing and Evaluating Solar Flare Forecasting Systems. Monthly Notices of the Royal Astronomical Society, Oxford University Press, v. 495, p. 3332–3349, 2020.

* CINTO, T. et al. Solar Flare Forecasting Using Time Series and Extreme Gradient Boosting Ensembles. Solar Physics, Springer Nature B.V., v. 295, n. 93, p. 30pp, 2020.

`Guaraci` is based on the Python's [Scikit-learn](https://scikit-learn.org/stable/) machine learning library for supervised and unsupervised learning. 

`Guaraci` daily provides ≥ C- and ≥ M-class flare forecasts within the next 24, 48, and 72 h. 

# Forecast algorithms

`Guaraci` comes with some pre-packed decision tree-based ensembles to make forecasts. Ensembles are meta-algorithms that merge the output of several base learners to boost their overall predictive performance. The base-learners of `Guaraci's` ensembles are classification decision trees. For further information on `Guaraci's` meta-algorithms, refer to the references below. If you want to configure your own custom forecast models, check the `How to set up custom forecast models` section.

### Random forest (≥ C-class flare forecasts in the next 24, and 48 h)

* JAMES, G. et al. An Introduction to Statistical Learning. 1st. ed. New York, NY, USA: Springer, 2013.

### AdaBoost (≥ C-class flare forecasts in the next 72 h)

* ZAKI, M. J.; MEIRA JR., W. Data Mining and Analysis: Fundamental Concepts and Algorithms. New York: Cambridge University Press, 2013.

### Gradient tree boosting (≥ M-class flare forecasts in the next 24, 48, and 72 h)

* HASTIE, T.; TIBSHIRANI, R.; FRIEDMAN, J. The Elements of Statistical Learning - Data Mining, Inference, and Prediction. 2nd. ed. New York, NY, USA: Springer, 2009.

# Archictecture

We designed the `Guaraci` under the layered architecture shown below. Overall, it comprehends a Linux-based machine running a Python virtual machine prepared for machine learning, namely with the Scikit-learn, NumPy, Pandas, and imbalanced-learn toolkits -- the artificial intelligence (AI) layer.

![alt text](https://github.com/tiagocinto/guaraci-forecast/blob/master/images/guaraci-architecture.png?raw=true)

The components of the AI layer process [NOAA/SWPC](https://www.swpc.noaa.gov/)'s dataᵃ and feed the model layer -- holding info on system's forecasts, history, and graphics (i.e., XML and CSV data files). `Guaraci` then renders such a data in the view layer (i.e., HTML and CSS) supported by its PHP-based controller module.

ᵃ By default, `Guaraci` comes with data from NOAA/SWPC to feed its forecast models. However, it does not restrict to such a nature of features. To set up your own set of features, provide your dataset designed under the CSV format in the `data` directory and configure the features' names in the `guaraci-forecast.py` file. In addition, adjust the `assemble_dataset()` function to fit your on-demand pre-processing needs.

# Installation and configuration

As `Guaraci` runs under Linux-based operating systems, we will use Ubuntu as a reference for this guide.

At first, type `sudo apt-get update` and `sudo apt-get upgrade` to update and upgrade your operating system if needed.

You shall need a text editor to configure some `Guaraci's` params. We suggest nano for usability purposes. To install nano, open a terminal and type `sudo apt-get install nano`.

You can then install the apache webserver `sudo apt-get install apache2`.

After installing apache, you will need to install some modules to allow such a server to cope with php, xml and sqlite. Type `sudo apt-get install php7.2-xml php libapache2-mod-php php-sqlite3` in the terminal. We strongly suggest you to adhere to those versions as we used them to develop `Guaraci`. 

You can then restart the apache: `sudo systemctl restart apache2.service`.

The next step is to prepare the Python's runtime environment. Install Python 2.7 and pip 2: `sudo apt-get install python python-pip`. We designed Guaraci under Python 2.7, so we encourage you to adhere to this version, otherwise the `Guaraci's` source code may experience several syntax or compatibility issues.

You must then install our Python's dependencies: `sudo -H pip install numpy==1.16.6 schedule==0.6.0 pandas==0.24.2 scipy==1.2.3 scikit-learn==0.19.2 pillow==6.2.2 h5py==2.10.0 imbalanced-learn==0.4.1`. Once more, stuck into those versions to guarantee that the `Guaraci` will run correctly.

Clone the [Guaraci's repository](https://github.com/tiagocinto/guaraci-forecast) into your apache's html directory.

To install the `Guaraci` as a Linux service, configure it in the operating system's `rc.local` file. That shall allow the `Guaraci` to run along with the operating system. Open the `rc.local` file for editing: `sudo nano /etc/rc.local` and input the following line right before `exit 0`: `/usr/bin/python /path/to/guaraci-forecast.py >/tmp/guaraci-forecast.out 2>/tmp/guaraci-forecast.error`.

Finally, you should guarantee that both `rc.local` and `guaraci-forecast.py` files are runnable:

`sudo chmod +x /etc/rc.local`

`sudo chmod +x /path/to/guaraci-forecast.py`

Once installed, you must configure some `Guaraci's` params as described next.

Guaraci uses an SMTP server to notify users in case of crashes. As such, configure the following params in the `guaraci.smtp` file: `smtp_key`,`from_address`,`to_address`, and `smtp_server`:

* `smtp_key`: SMTP password;
* `from_address`: sender's e-mail; 
* `to_address`: recipient's e-mail;
* `smtp_server`: SMTP server plus the port used: `server:port`.

To set up the `Guaraci's` routine of execution, refer to the `SCHEDULED_EXECUTION` and `EXECUTION_HOUR` params in the `guaraci-forecast.py` file. Adjust the former as `True/False` whether the `Guaraci` should run daily. Provided that you set the `Guaraci` to run once per day, configure the latter with the hour that it is expected to run (`HH:mm`).

Besides, one must also provide the work path of `Guaraci`, that is, the place where it was installed. In the `WORK_PATH` param, input the apache's directory where the `Guaraci` was stored: `//var//www//html//guaraci-forecast`.


### Requirements

* apache 2;
* php-sqlite 3;
* libapache2-mod-php;
* php 7.2;
* php-xml 7.2;
* python 2.7;
* pip 2;
* numpy 1.16.6;
* schedule 0.6.0;
* pandas 0.24.2;
* scipy 1.2.3;
* scikit-learn 0.19.2;
* pillow 6.2.2;
* h5py 2.10.0;
* imbalanced-learn 0.4.1.

# License

Distributed under the GNU General Public License v3.0 License. See `LICENSE` for more information.

# How to test Guaraci 

To carry out a stand-alone run of Guaraci, open a terminal and type `sudo python /var/www/html/guaraci-forecast/guaraci-forecast.py`. It is worth saying that whether the `SCHEDULED_EXECUTION` param was set up to `True`, Guaraci will then follow its scheduled time from now on. Another option to run Guaraci is to reboot the operating system -- provided that you set up the `rc.local` file as suggested -- by only inputting `sudo reboot` in the terminal.

To check whether the stand-alone run succeded, go to your apache's loopback URL in the browser and seek the `Guaraci's` directory: `http://127.0.0.1/guaraci-forecast`. The system must render updated forecast probabilities at this point.

# How to set up custom forecast models

`Guaraci` comes with some pre-packed decision tree-based ensembles to make its forecasts. We design them in the `guaraci-forecast.py` file as defined by Scikit-learn: 

* RandomForest for ≥ C-class flare forecasts in the next 24 h: `RandomForestClassifier(n_estimators=300, min_samples_split=100, min_samples_leaf=40, max_depth=15, max_features=4, min_impurity_split=0.001, class_weight={'0':1,'1':0.78}, random_state=10)`;

* RandomForest for ≥ C-class flare forecasts in the next 48 h: `RandomForestClassifier(n_estimators=300, min_samples_split=50, min_samples_leaf=90, max_depth=8, max_features=4, min_impurity_split=1e-07, class_weight={'0':1,'1':0.55}, random_state=100)`;

* AdaBoost for ≥ C-class flare forecasts in the next 72 h: `AdaBoostClassifier(DecisionTreeClassifier(min_samples_split=800, min_samples_leaf=75, max_depth=13, max_features=2, class_weight={'0':1,'1':0.45}, random_state=10), n_estimators=350, learning_rate=0.01, random_state=10)`.

* GradientTreeBoosting for ≥ M-class flare forecasts in the next 24 h: `GradientBoostingClassifier(n_estimators=250, learning_rate=0.01, min_samples_split=200, min_samples_leaf=40, max_depth=9, max_features=8, subsample=0.8, random_state=10)`

* GradientTreeBoosting for ≥ M-class flare forecasts in the next 48 h: `GradientBoostingClassifier(n_estimators=200, learning_rate=0.05, min_samples_split=350, min_samples_leaf=5, max_depth=13, max_features=9, subsample=0.85, random_state=10)`

* GradientTreeBoosting for ≥ M-class flare forecasts in the next 72 h: `GradientBoostingClassifier(n_estimators=500, learning_rate=0.01, min_samples_split=350, min_samples_leaf=25,  max_depth=11, max_features=10, subsample=0.85, random_state=10)`

However, provided that you want to set up your own custom forecast models, you can do so by providing the learning algorithms (params: `MOD1` and `MOD2`), input features (params: `MOD1_FEATURES` and `MOD2_FEATURES`), and training data files (params: `MOD1_TRAINING_DATA_FILES` and `MOD2_TRAINING_DATA_FILES`) in the `guaraci-forecast.py` file. All Scikit-learn algorithms can be used in `Guaraci`.

The `MOD1` param is a dict with the forecast models for ≥ C-class flare forecasting over all horizons (i.e., the next 24, 48, and 72 h). Within `MOD1`, you must provide the learning algorithm of each horizon (i.e., the keys named `t1d_model`, `t2d_model`, and `t3d_model`), the prediction thresholds (i.e., the keys named `t1d_model_t`, `t2d_model_t`, and `t3d_model_t`), and the resampling methods (i.e., the keys named `t1d_model_resampling_method`, `t2d_model_resampling_method`, and `t3d_model_resampling_method`). Analogously, the `MOD2` dict represents the ≥ M-class forecast scenario. 

You must then provide your models' input features through CSV data files inside the `data` folder. In addition, configure the features' names in the `MOD1_FEATURES` dict, that is, provide the features' names in the `t1d_features_set`, `t2d_features_set`, and `t3d_features_set` keys. Do not forget to provide the target features in the `t1d_target_feature`, `t2d_target_feature`, and `t3d_target_feature` keys. Once more, the `MOD2_FEATURES` dict represents the ≥ M-class forecast scenario. Noteworthily, whether you chose to provide your own custom datasets, you must also adjust the `assemble_dataset()` function in the `guaraci-forecast.py` file for tayloring the on-demand pre-processing to your needs.

Finally, set up the name of your dataset files in the `MOD1_TRAINING_DATA_FILES` and `MOD2_TRAINING_DATA_FILES` params.

# Sample dataset

By default, `Guaraci` comes with sample data from NOAA/SWPC to feed its forecast models. The list of sample features include: 

* `Radio flux`;
* `Sunspot number`;
* `Sunspot area`;
* `X-ray background flux`;
* `Z component WMFR`;
* `p component WMFR`;
* `c component WMFR`;
* `Magnetic type WMFR`.

Refer to the reference below for further information on the features used:

* CINTO, T. et al. Solar Flare Forecasting Using Time Series and Extreme Gradient Boosting Ensembles. Solar Physics, Springer Nature B.V., v. 295, n. 93, p. 30pp, 2020.

We designed this list of features through a sliding time window with 5-days of evolutionary data.

Besides, for each record of our sample datasets, we have binary features to represent whether at least one flare (≥ C or ≥ M) shall happen within the next 24, 48, and 72 h (i.e., our target features).

# Documentation

For futher information on `Guaraci's` documentation, please refer to the docs section.

# Contact

If you wish to contribute to the software, report issues or problems or seek suport, feel free to use the issue report of this repository or to contact us.

* Tiago Cinto - tiago.cinto@pos.ft.unicamp.br

* André Leon S. Gradvohl - gradvohl@ft.unicamp.br

