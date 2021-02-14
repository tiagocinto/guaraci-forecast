---
title: 'Guaraci: a solar flare forecasting system'
tags:
  - Python
  - astronomy
  - solar flares 
  - forecasting
  - sunspots
  - active regions
  - magnetic class
  - McIntosh class
authors:
  - name: Tiago Cinto
    orcid: 0000-0003-0724-780X
    affiliation: "1, 2" # (Multiple affiliations must be quoted)
  - name: André L. S. Gradvohl
    orcid: 0000-0002-6520-9740
    affiliation: 1
  - name: Guilherme P. Coelho
    orcid: 0000-0002-4641-0684
    affiliation: 1
  - name: Ana E. A. da Silva
    orcid: 0000-0001-9886-3506
    affiliation: 1
affiliations:
 - name: School of Technology (FT), University of Campinas (UNICAMP), Limeira, SP, Brazil
   index: 1
 - name: Federal Institute of Education, Science and Technology of Rio Grande do Sul (IFRS), Campus Feliz, RS, Brazil
   index: 2
date: 13 December 2019
bibliography: paper.bib

# Optional fields if submitting to a AAS journal too, see this blog post:
# https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
aas-doi: 10.3847/xxxxx
---

# Summary
In astronomy and astrophysics, the consequences of solar flares lead researchers to investigate approaches to forecast them accurately. The field of "space weather" is now well-established, comprehending the study of any conditions or events in the Sun, the near-Earth space, and the Earth's atmosphere. Disturbances in space weather can damage several fields, including aviation and aerospace, satellites, oil and gas industries, and electrical systems, leading to economic and commercial losses [@NRC:2009]. Aside from the plethora of satellite’s data daily collected from the Sun's bevahiours, efficient forecasting tools must be researched to help mitigating the effects of solar flares. Here we propose Guaraci, a python-based solar flare forecasting system to deploy learning models from the automated design methods described in @Cinto:2020a and @Cinto:2020b.

# Statement of Need

The solar events and structures often influencing the space weather comprehend sunspots [@Moldwin:2008], active regions (AR) [@Canfield:2001], and solar flares [@Messerotti:2009]. A sunspot is often observed in the Sun's photosphere, which relates to the existence of complex magnetic fields in the Sun's surface. In turn, ARs comprehend groups of sunspots and magnetic arcs interconnecting them. Those phenomena usually create conditions for releasing sudden bursts of radiation, namely the solar flares [@Canfield:2001]. 

Solar flares comprehend releases of X-rays in the 1-8 Ångström wavelength. We represent their intensities in watts per square meter ($\mathrm{W/m}^{2}$) [@Canfield:2001]. Solar physicists classify them through a labeled scale ranging between A- (the smallest events), B- (as tiny as A, usually called subflares), C- (cause few noticeable consequences on Earth), M- (medium-sized events often accompanying coronal mass ejections -- CME), and X-class (the largest events, causing major radio blackouts and long-lasting radiation storms in the Earth's atmosphere). Taking the strongest flare type (X-class) as an example, composed of X-rays releases $>10^{-4}\:\mathrm{W/m}^{2}$, each class has its X-ray peak flux ten times higher than its predecessor.

Because of the several known solar flare effects, it is imperative to employ efforts to forecast them. Forecasting -- accurately -- solar flare events allows several mitigation actions, including powering off power plants, rotating  satellite’s radiation shields toward the Sun, and warning astronauts in deep space that they are likely to be hit by radiation. On the other hand, the consequences of mispredicting solar flares can be severe, depending on the associated event class [@Raboonik:2016]. 

Although several Space Weather Prediction Centers (SWPC) employ human-based flare predictions [@Crown:2012; @Devos:2014; @Murray:2017; @Kubo:2017], many researchers have also been researching forecast efforts relying on machine learning. To name some, we can cite the use of random forests [@Domijan:2019], linear discriminant analysis [@Leka:2018], k-nearest neighbors (k-NN) [@Nishizuka:2017], support-vector machines (SVM)[@Yang:2013; @Muranushi:2015; @Bobra:2015], relevance-vector machines [@Al-Ghraibah:2015a], multiple linear regression [@Shin:2016], and neural networks [@Ahmed:2013; @Nishizuka:2018; @Huang:2018]. 

In the past decade, a plethora of machine learning methods has emerged along with their corresponding applications. However, a notable barrier for new users comprehends the performance of those methods as they are very sensitive to design decisions. Efficient decision-making is paramount in such domain, where engineers urge to design correct algorithms' architectures, training procedures, input features, and hyperparameters to leverage their expected forecast performance [@Hutter:2019].

Within this context, the domain of automated machine learning has emerged to support those decisions through an automated, data-driven, and objective way. As such, users can simply provide their input data, and the automated machine learning process fully determines the best performing forecast approach for that particular case. Besides, automated machine learning provides state-of-the-art learning methods to researchers interested in applying concepts rather than knowing the technologies in their details [@Hutter:2019]. Specifically in space weather research, automating machine learning can be rather valuable as not all solar physicists are experts in the artificial intelligence domain.

Aware of the benefits of automating machine learning for space weather, we proposed automated design pipelines for the solar flare classifiers in @Cinto:2020a and @Cinto:2020b. However, besides assessing the performance of such optimized classifiers in simulated forecast scenarios, as done in those papers, it also worth assessing their performance in real-time forecast environments that is the aim of Guaraci\footnote{In the Guaraní mythology, Guaraci is the god of the Sun.}, the solar flare forecasting system presented in this article.


# Features and functionalities

By default, Guaraci is set up to provide forecasts once a day for up to three days ahead. To do so, Guaraci regularly assembles input data\footnote{Such data assembling involves the calculation of features as stated in [@Cinto:2020b]} from some repositories of NOAA/SWPC, namely the Daily Solar Data (DSD) and Sunspot Region Summary (SRS) data products. NOAA/SWPC regularly issues data for DSD at 02:30 AM, 08:30 AM, 02:30 PM, and 08:30 PM UT [@Noaa:2011], as well as the SRS is daily updated always at 00:30 AM UT -- which refers to the previous day daily aggregated data [@Noaa:2008]. 

Accordingly, by definition, Guaraci runs daily at 01:00 AM UT. However, choosing either the system's run cadence or the execution time schedule solely depends on the user's requirements, as Guaraci offers ways to customize those parameters during installation. At each run, Guaraci then gathers records from the SRS at 00:30 AM UT and from the DSD, that is, the records referring to 08:30 PM UT. To link DSD and SRS data, Guaraci uses the compilation dates of records (month, day, and year).

We designed the Guaraci system under the layered architecture shown in Figure 1. Overall, Guaraci\footnote{An installed version of Guaraci system is currently available at: \url{https://highpids.ft.unicamp.br/guaraci}.} comprehends an Ubuntu-based Linux instance running a Python virtual machine prepared for machine learning, namely with the Scikit-learn\footnote{The Scikit-learn toolkit is available at: \url{https://scikit-learn.org/}.}, NumPy\footnote{The NumPy toolkit is available at: \url{https://numpy.org/}.}, Pandas\footnote{The Pandas toolkit is available at: \url{https://pandas.pydata.org/}.}, and imbalanced-learn\footnote{The imbalanced-learn toolkit is available at: \url{https://imbalanced-learn.readthedocs.io/en/stable/}.} toolkits -- the Artificial Intelligence (AI) layer. 

The components of the AI layer process NOAA/SWPC data and feed the model layer prepared under an Apache Web Server -- containing the data for system's forecasts, history, and graphics (i.e., XML and CSV data files). The system then renders such data in the view layer (i.e., HTML and CSS) supported by its PHP-based controller module.

![Guaraci's Architecture.](imgs/guaraci-architecture.png)

By using six indepent tree-based machine learning ensembles [@Han:2006], Guaraci daily provides $\geq$ C- and $\geq$ M-class flare forecasts within the next 24, 48, and 72 h. To support the visualization of such forecasts, the system has a detailed user interface holding the calculated probabilities for each horizon, as well as the suggested binary forecasts, drawn by custom prediction thresholds adjusted during the learning algorithms' designs\footnote{For further information on how to design custom forecast models for Guaraci, refer to @Cinto:2020b and @Cinto:2020a}. Figure 2 shows this interface for flares higher than or equal to M-class.

![Guaraci's daily M+X forecasts.](imgs/guaraci-daily-mx-forecasts.png)

Besides presenting detailed forecast reports daily, Guaraci also holds a feature for displaying the graphical probabilities of events in the last two weeks. However, in this graph, such probabilities are only displayed for the next 24 h along with a horizontal red line: the flare threshold. Accordingly, Figure 3 shows this graph for flares higher than or equal to C-class. The tool also extends this feature to $\geq$ M-class events.

![Guaraci's two-week C+M+X flare forecasts.](imgs/guaraci-two-week-mx-forecasts.png)

The last feature comprehending Guaraci is the full report of forecasts within 24 h. This component refers to the table shown in Figure 4. This table holds "True" and "Forecast" columns representing whether flares happened (NOAA/SWPC confirmations), and the probabilities of flares by Guaraci, respectively. Each new entry in this table always keeps the "True" column as "Not available" until the next 24 h period closes, when the system confirms with NOAA/SWPC whether some event occurred.

![Guaraci's forecast history.](imgs/guaraci-forecast-history.png)


# Acknowledgements

This study was partly funded by the Coordenação de Aperfeiçoamento de Pessoal de Nível Superior (CAPES), Brazil -- Finance Code 001. Besides, we thank the Federal Institute of Education, Science and Technology of Rio Grande do Sul (IFRS) -- Campus Feliz, for the cooperation with this research.

# References
