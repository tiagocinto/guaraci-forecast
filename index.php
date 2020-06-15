<?php
$xmldata = simplexml_load_file("view.xml") or die("Failed to load view data.");
?>

<!DOCTYPE HTML>
<html>
	<head>
		<title>sw-forecast</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
		<link rel="stylesheet" href="assets/css/main.css" />
		<noscript><link rel="stylesheet" href="assets/css/noscript.css" /></noscript>
	</head>
	<body class="is-preload">
		<!-- Wrapper -->
			<div id="wrapper">
				<!-- Header -->
					<header id="header" class="alt">
						<span class="logo"><img src="images/logo.png" alt="" /></span>
						<h1>sw-forecast <!--</br>Solar Flare Forecasting System--></h1>
						<p>Welcome to sw-forecast, the solar flare forecasting system empowered by <a href="https://highpids.ft.unicamp.br/">High PIDS research group</a> at <a href="ft.unicamp.br">School of Technology (FT), University of Campinas (UNICAMP)</a>.</p>
						</header>

				<!-- Nav -->
					<nav id="nav">
						<ul>
							<li><a href="#intro" class="active">About</a></li>
							<li><a href="#first">Data</a></li>
							<li><a href="#second">Module 1 (C+M+X Flares)</a></li>
							<li><a href="#third">Module 2 (M+X Flares)</a></li>
						</ul>
					</nav>
				<!-- Main -->
					<div id="main">
							<section id="intro" class="main">
								<div class="spotlight">
									<div class="content">
										<header class="major">
											<h2>Get to Know</h2>
										</header>
										<p>Sw-forecast is a forecasting system developed by High PIDS research group at School of Technology, University of Campinas. It aims at forecasting the strongest Sun's phenomena, namely solar flares. Flares are sudden releases of radiation (x-rays) and particles that can affect the Earth's atmosphere in a few hours or days. Disturbances involve damages in several fields, including aviation and aerospace, satellites, oil and gas industries, electrical systems, and astronauts safety, leading to economic and commercial losses.
<br/><br/>
Solar flares are then sudden x-ray releases in the 1-8 Ångström wavelength represented in watts per square meter (W/m2). Depending on their intensities, those phenomena range over a class scale comprehending A (<10e-7), B (<10e-6), C (<10e-5), M (<10e-4), and X (>10e-4) events. Each flare class has a x-ray peak flux ten times higher than its predecessor -- M- and X-class events are the strongest ones. In addition, each class also linearly lies around [1,9], a factor representing the flare intensity. Solar flares are thus represented by the product of its intensity factor with the x-ray peak flux value of its class. 
<br/><br/>
As such, we designed sw-forecast to help to mitigate the impacts of solar flares, that is, by employing efforts in the forecasting of C-, M-, and X-class events.</p>

									</div>
									<!--<span class="image"><img src="images/pic01.jpg" alt="" /></span>-->
								</div>
							</section>
							<section id="first" class="main special">
								<header class="major">
									<h2>Data</h2>
									<p> <?php echo "To provide forecasts, sw-forecast regularly assembles data from the satellites of the Space Weather Prediction Center (SWPC) from the National Oceanic and Atmospheric Administration (NOAA) in the US. The table below comprehends the last 5 days of records available and analyzed."; ?> </p>
									<?php
									$row = 1;
									echo "<table border=1px align=center>\n\n";
									if (($handle = fopen("dataframe.csv", "r")) !== FALSE) {
									    while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
										$num = count($data);
										echo "<tr>\n";
										$row++;
										for ($c=0; $c < $num; $c++) {
										    echo "<td>\n";
										    echo $data[$c] . "<br />\n";
										    echo "</td>\n";
									        }
										echo "</tr>\n";
									    }
									    fclose($handle);
									}
									echo "\n</table>";
									?>
								</header>
							</section>
							<section id="second" class="main special">
								<header class="major">
									<h2>Module 1</h2>
									<p> <?php echo "The forecasting module 1 accounts for two random forest (t+1d and t+2d) and one AdaBoost (t+3d) models designed to forecast >= C-class flares up to 3 days ahead.<br>Module 1 last computed its probabilities at: " . $xmldata->view[0]->mod1_data_processing_time . " UT-3."; ?> </p>
								</header>
								<ul class="statistics">
									<li class="style2">
										<strong>t+1d<sup>a</sup></strong>
										<br/>
										<strong><?php echo $xmldata->view[0]->mod1_t1d_no_proba; ?></strong> Probability of non-flares in t+1d.
										<strong><?php echo $xmldata->view[0]->mod1_t1d_yes_proba; ?></strong> Probability of C+M+X flares in t+1d.
										<br/><br/>
										<strong><?php echo $xmldata->view[0]->mod1_t1d_prediction; ?></strong>
										<?php echo "Will C+M+X flares happen in t+1d from " . $xmldata->view[0]->t_instant . "?"; ?>

									</li>
									<li class="style3">
										<strong>t+2d<sup>b</sup></strong>
										<br/>
										<strong><?php echo $xmldata->view[0]->mod1_t2d_no_proba; ?></strong> Probability of non-flares in t+2d.
										<strong><?php echo $xmldata->view[0]->mod1_t2d_yes_proba; ?></strong> Probability of C+M+X flares in t+2d.
										<br/><br/>
										<strong><?php echo $xmldata->view[0]->mod1_t2d_prediction; ?></strong>
										<?php echo "Will C+M+X flares happen in t+2d from " . $xmldata->view[0]->t_instant . "?"; ?>

									</li>
									<li class="style4">
										<strong>t+3d<sup>c</sup></strong>
										<br/>
										<strong><?php echo $xmldata->view[0]->mod1_t3d_no_proba; ?></strong> Probability of non-flares in t+3d.
										<strong><?php echo $xmldata->view[0]->mod1_t3d_yes_proba; ?></strong> Probability of C+M+X flares in t+3d.
										<br/><br/>
										<strong><?php echo $xmldata->view[0]->mod1_t3d_prediction; ?></strong>
										<?php echo "Will C+M+X flares happen in t+3d from " . $xmldata->view[0]->t_instant . "?"; ?>

									</li>
									<!--<li class="style5">
										<strong>72-96 hours<sup>d</sup></strong>
										<br/>
										<strong><?php echo $xmldata->view[0]->mod1gbm96_no_proba; ?></strong> Probability of ocurrence of flares lower than C-class or no type of flare.
										<strong><?php echo $xmldata->view[0]->mod1gbm96_yes_proba; ?></strong> Probability of ocurrence of flares higher than or equal to C-class.
										<br/><br/>
										<strong><?php echo $xmldata->view[0]->mod1gbm96_prediction; ?></strong>
										<?php echo "Will some X-, M-, or C-class flare happen within 72-96 hours from " . $xmldata->view[0]->t_instant . "?"; ?>
									</li>-->
								</ul><p align=left>
								<sup>a</sup> t+1d § TSS: 0.70 | AUC: 0.93 | POFD: 0.16<br/> 
								<sup>b</sup> t+2d § TSS: 0.70 | AUC: 0.94 | POFD: 0.20<br/>
								<sup>c</sup> t+3d § TSS: 0.69 | AUC: 0.94 | POFD: 0.20<br/></p>

							</section>
							<section id="third" class="main special">
								<header class="major">
									<h2>Module 2</h2>
									<p><?php echo "The forecasting module 2 accounts for three gradient tree boosting models designed to forecast >= M-class flares up to 3 days ahead.<br>Module 2 last computed its probabilities at: " . $xmldata->view[0]->mod2_data_processing_time . " UT-3."; ?> </p>
								</header>
								<ul class="statistics">
									<li class="style5">
										<strong>t+1d<sup>a</sup></strong>
										<br/>
										<strong><?php echo $xmldata->view[0]->mod2_t1d_no_proba; ?></strong> Probability of non-flares in t+1d.
										<strong><?php echo $xmldata->view[0]->mod2_t1d_yes_proba; ?></strong> Probability of M+X flares in t+1d.
										<br/><br/>
										<strong><?php echo $xmldata->view[0]->mod2_t1d_prediction; ?></strong>
										<?php echo "Will M+X flares happen in t+1d from " . $xmldata->view[0]->t_instant . "?"; ?>

									</li>
									<li class="style1">
										<strong>t+2d<sup>b</sup></strong>
										<br/>
										<strong><?php echo $xmldata->view[0]->mod2_t2d_no_proba; ?></strong> Probability of non-flares in t+2d.
										<strong><?php echo $xmldata->view[0]->mod2_t2d_yes_proba; ?></strong> Probability of M+X flares in t+2d.
										<br/><br/>
										<strong><?php echo $xmldata->view[0]->mod2_t2d_prediction; ?></strong>
										<?php echo "Will M+X flares happen in t+2d from " . $xmldata->view[0]->t_instant . "?"; ?>
									</li>
									<li class="style3">
										<strong>t+3d<sup>c</sup></strong>
										<br/>
										<strong><?php echo $xmldata->view[0]->mod2_t3d_no_proba; ?></strong> Probability of non-flares in t+3d.
										<strong><?php echo $xmldata->view[0]->mod2_t3d_yes_proba; ?></strong> Probability of M+X flares in t+3d.
										<br/><br/>
										<strong><?php echo $xmldata->view[0]->mod2_t3d_prediction; ?></strong>
										<?php echo "Will M+X flares happen in t+3d from " . $xmldata->view[0]->t_instant . "?"; ?>
									</li>
									<!--<li class="style5">
										<strong>72-96 hours<sup>d</sup></strong>
										<br/>
										<strong><?php echo $xmldata->view[0]->mod1gbm96_no_proba; ?></strong> Probability of ocurrence of flares lower than C-class or no type of flare.
										<strong><?php echo $xmldata->view[0]->mod1gbm96_yes_proba; ?></strong> Probability of ocurrence of flares higher than or equal to C-class.
										<br/><br/>
										<strong><?php echo $xmldata->view[0]->mod1gbm96_prediction; ?></strong>
										<?php echo "Will some X-, M-, or C-class flare happen within 72-96 hours from " . $xmldata->view[0]->t_instant . "?"; ?>
									</li>-->

								</ul><p align=left>
								<sup>a</sup> t+1d § TSS: 0.53 | AUC: 0.84 | POFD: 0.30<br/> 
								<sup>b</sup> t+2d § TSS: 0.55 | AUC: 0.85 | POFD: 0.30<br/>
								<sup>c</sup> t+3d § TSS: 0.53 | AUC: 0.84 | POFD: 0.27<br/></p>
							</section>

					</div>

				<!-- Footer -->
					<footer id="footer">
						<section>
							<h2>High PIDS</h2>
							<p>The High Performance Intelligent Decision Systems (High PIDS) research group works on design and implementation of decision support systems based on intelligent algorithms to work on high performance computer architectures. The goal of such algorithms is to solve semi-structured data mining and optimization problems. The researchers involved in this project, which are experts in complementary fields, intend to work together to combine their research to advance and contribute to the field of decision support systems. Such systems are extremely important to organizations as they provide valuable information that helps managers take strategic decisions. The HPFS project is developed at High PIDS.</p>
							<ul class="actions">
								<li><a href="https://highpids.ft.unicamp.br/" class="button">Learn More</a></li>
							</ul>
						</section>
						<section>
							<h2>Contact</h2>
							<dl class="alt">
								<dt>Address</dt>
								<dd>Paschoal Marmo st., 1888, Limeira - SP, 13484-332, BR</dd>
								<dt>Email</dt>
								<dd><a href="mailto:tiago.cinto@pos.ft.unicamp.br">tiago.cinto@pos.ft.unicamp.br</a></dd>
							</dl>
							<ul class="icons">
								<li><a href="#" class="icon fa-github alt"><span class="label">GitHub</span></a></li>
							</ul>
						</section>
						<p class="copyright">&copy; 2019</p>
					</footer>

			</div>

		<!-- Scripts -->
			<script src="assets/js/jquery.min.js"></script>
			<script src="assets/js/jquery.scrollex.min.js"></script>
			<script src="assets/js/jquery.scrolly.min.js"></script>
			<script src="assets/js/browser.min.js"></script>
			<script src="assets/js/breakpoints.min.js"></script>
			<script src="assets/js/util.js"></script>
			<script src="assets/js/main.js"></script>

	</body>
</html>
