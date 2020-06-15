<?php
$xmldata = simplexml_load_file("view.xml") or die("Failed to load view data.");
?>

<!DOCTYPE HTML>
<html>
	<head>
		<title>Guaraci</title>
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
						<h1>Guaraci<!--</br>Solar Flare Forecasting System--></h1>
						<p>Welcome to Guaraci, the solar flare forecasting system empowered by <a href="https://highpids.ft.unicamp.br/">High PIDS research group</a> at <a href="https://www.ft.unicamp.br/">School of Technology (FT), University of Campinas (UNICAMP)</a>.</p>
						</header>

				<!-- Nav -->
					<nav id="nav">
						<ul>
							<li><a href="#intro" class="active">Get to Know</a></li>
							<li><a href="#first">Data</a></li>
							<li><a href="#second">Two-Week C+M+X Flare Forecasts</a></li>
							<li><a href="#third">Two-Week M+X Flare Forecasts</a></li><br>
							<li><a href="#fourth">Complete Forecasts History</a></li>
							<li><a href="#fifth">Daily C+M+X Flare Forecast</a></li>
							<li><a href="#sixth">Daily M+X Flare Forecast</a></li>
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
										<p>Guaraci is a forecasting system developed by High PIDS research group at School of Technology, University of Campinas. It aims at forecasting the strongest Sun's phenomena, namely solar flares. Flares are sudden releases of radiation (X-rays) and particles that can affect the Earth's atmosphere in a few hours or days. Disturbances involve damages in several fields, including aviation and aerospace, satellites, oil and gas industries, electrical systems, and astronauts safety, leading to economic and commercial losses.
<br/><br/>
Solar flares are then sudden X-ray releases in the 1-8 Ångström wavelength represented in watts per square meter (W/m<sup>2</sup>). Depending on their intensities, those phenomena range over a class scale comprehending A (<10e<sup>-7</sup>), B (<10e<sup>-6</sup>), C (<10e<sup>-5</sup>), M (<10e<sup>-4</sup>), and X (>10e<sup>-4</sup>) events. Each flare class has a X-ray peak flux ten times higher than its predecessor -- M- and X-class events are the strongest ones. In addition, each class also linearly lies around [1,9], that is, a factor representing the flare intensity. Solar flares are thus represented by the product of their intensity factors with the X-ray peak flux values of their classes. 
<br/><br/>
As such, we designed Guaraci to help to mitigate the effects of solar flares, that is, by employing efforts in the forecasting of C+M+X and M+X events in the next 24, 48, and 72 h.</p>

									</div>
									<!--<span class="image"><img src="images/pic01.jpg" alt="" /></span>-->
								</div>
							</section>
							<section id="first" class="main special">
								<header class="major">
									<h2>Data</h2>
									<p> <?php echo "To provide forecasts, Guaraci regularly assembles data from the Geostationary Operational Environmental Satellite (GOES) of the Space Weather Prediction Center (SWPC) from the National Oceanic and Atmospheric Administration (NOAA) in the US. The table below comprehends the last 5 days of records available and analyzed."; ?> </p>
									<?php
									$row = 1;
									echo "<table border=1px align=center>\n\n";
									if (($handle = fopen("dataframe.csv", "r")) !== FALSE) {
									    while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
										$num = count($data);
										echo "<tr>";
										$row++;
										for ($c=0; $c < $num; $c++) {
										    echo "<td>";
										    echo $data[$c] . "<br/>";
										    echo "</td>";
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
									<h2>Two-Week C+M+X Flare Forecasts</h2>
								</header>
								<canvas id="c-m-x-bar-chart" ></canvas>
							</section>
							<section id="third" class="main special">
								<header class="major">
									<h2>Two-Week M+X Flare Forecasts</h2>
								</header>
								<canvas id="m-x-bar-chart" ></canvas>
							</section>
							<section id="fourth" class="main special">
								<header class="major">
									<h2>Complete Forecasts History</h2>
									<p> Coming soon... </p>
								</header>
								<ul class="statistics">
								</ul>
							</section>
							<section id="fifth" class="main special">
								<header class="major">
									<h2>Daily C+M+X Flare Forecast</h2>
									<p> <?php echo "Guaraci last computed the C+M+X flare probabilities at: " . $xmldata->view[0]->mod1_data_processing_time . " UT-3."; ?> </p>
								</header>
								<ul class="statistics">
									<li class="style2">
										<strong>next 24 h</strong>
										<br/>
										<strong><?php echo $xmldata->view[0]->mod1_t1d_no_proba; ?></strong> Non-flare events probability for the next 24 h.
										<strong><?php echo $xmldata->view[0]->mod1_t1d_yes_proba; ?></strong> C+M+X flare events probability for the next 24 h.
										<br/><br/>
										<strong><?php echo $xmldata->view[0]->mod1_t1d_prediction; ?></strong>
										<?php echo "Will C+M+X flares happen in the next 24 h ahead " . $xmldata->view[0]->t_instant . "?"; ?>

									</li>
									<li class="style3">
										<strong>next 48 h</strong>
										<br/>
										<strong><?php echo $xmldata->view[0]->mod1_t2d_no_proba; ?></strong> Non-flare events probability for the next 48 h.
										<strong><?php echo $xmldata->view[0]->mod1_t2d_yes_proba; ?></strong> C+M+X flare events probability for the next 48 h.
										<br/><br/>
										<strong><?php echo $xmldata->view[0]->mod1_t2d_prediction; ?></strong>
										<?php echo "Will C+M+X flares happen in the next 48 h ahead " . $xmldata->view[0]->t_instant . "?"; ?>

									</li>
									<li class="style4">
										<strong>next 72 h</strong>
										<br/>
										<strong><?php echo $xmldata->view[0]->mod1_t3d_no_proba; ?></strong> Non-flare events probability for the next 72 h.
										<strong><?php echo $xmldata->view[0]->mod1_t3d_yes_proba; ?></strong> C+M+X flare events probability for the next 72 h.
										<br/><br/>
										<strong><?php echo $xmldata->view[0]->mod1_t3d_prediction; ?></strong>
										<?php echo "Will C+M+X flares happen in the next 72 h ahead " . $xmldata->view[0]->t_instant . "?"; ?>

									</li>
								</ul>
							</section>
							<section id="sixth" class="main special">
								<header class="major">
									<h2>Daily M+X Flare Forecast</h2>
									<p><?php echo "Guaraci last computed the M+X flare probabilities at: " . $xmldata->view[0]->mod2_data_processing_time . " UT-3."; ?> </p>
								</header>
								<ul class="statistics">
									<li class="style5">
										<strong>next 24 h</strong>
										<br/>
										<strong><?php echo $xmldata->view[0]->mod2_t1d_no_proba; ?></strong> Non-flare events probability for the next 24 h. 
										<strong><?php echo $xmldata->view[0]->mod2_t1d_yes_proba; ?></strong> M+X flare events probability for the next 24 h.
										<br/><br/>
										<strong><?php echo $xmldata->view[0]->mod2_t1d_prediction; ?></strong>
										<?php echo "Will M+X flares happen in the next 24 h ahead " . $xmldata->view[0]->t_instant . "?"; ?>

									</li>
									<li class="style1">
										<strong>next 48 h</strong>
										<br/>
										<strong><?php echo $xmldata->view[0]->mod2_t2d_no_proba; ?></strong> Non-flare events probability for the next 48 h.
										<strong><?php echo $xmldata->view[0]->mod2_t2d_yes_proba; ?></strong> M+X flare events probability for the next 48 h.
										<br/><br/>
										<strong><?php echo $xmldata->view[0]->mod2_t2d_prediction; ?></strong>
										<?php echo "Will M+X flares happen in the next 48 h ahead " . $xmldata->view[0]->t_instant . "?"; ?>
									</li>
									<li class="style3">
										<strong>next 72 h</strong>
										<br/>
										<strong><?php echo $xmldata->view[0]->mod2_t3d_no_proba; ?></strong> Non-flare events probability for the next 72 h.
										<strong><?php echo $xmldata->view[0]->mod2_t3d_yes_proba; ?></strong> M+X flare events probability for the next 72 h.
										<br/><br/>
										<strong><?php echo $xmldata->view[0]->mod2_t3d_prediction; ?></strong>
										<?php echo "Will M+X flares happen in the next 72 h ahead " . $xmldata->view[0]->t_instant . "?"; ?>
									</li>

								</ul>
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
		<script src="assets/js/Chart.min.js"></script>
		<!--<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.min.js"></script>-->


	<script>

	Chart.pluginService.register({
	    afterDraw: function(chart) {
		if (typeof chart.config.options.lineAt != 'undefined') {
		    var lineAt = chart.config.options.lineAt;
		    var ctxPlugin = chart.chart.ctx;
		    var xAxe = chart.scales[chart.config.options.scales.xAxes[0].id];
		    var yAxe = chart.scales[chart.config.options.scales.yAxes[0].id];
		    ctxPlugin.strokeStyle = "red";
		    ctxPlugin.beginPath();
		    lineAt = yAxe.getPixelForValue(lineAt);
		    ctxPlugin.moveTo(xAxe.left, lineAt);
		    ctxPlugin.lineTo(xAxe.right, lineAt);
		    ctxPlugin.stroke();
		}
	    }
	});
	
	var ctxCMXBarChar = document.getElementById("c-m-x-bar-chart");
	var CMXChart = new Chart(ctxCMXBarChar, {
	  type: 'bar',
	  data: {
		<?php
		echo "labels:[";
		if (($handle = fopen("c-m-x-flare-forecasts-graphical-input.csv", "r")) !== FALSE) {
		    $i=0;
	            $linecount = count(file("c-m-x-flare-forecasts-graphical-input.csv"));
		    while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
			if ($i >= ($linecount - 14)) {
			    echo "\"". $data[0] . "\",";
			}
			$i++;
		    }
		    fclose($handle);
		}
		echo "],\n"
		?>
	  datasets: [{
	      label: 'C+M+X flare probability in the next 24 h',
		
		<?php
		echo "data:[";
		if (($handle = fopen("c-m-x-flare-forecasts-graphical-input.csv", "r")) !== FALSE) {
		    $i=0;
	            $linecount = count(file("c-m-x-flare-forecasts-graphical-input.csv"));
		    while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
			if ($i >= ($linecount - 14)) {
			    echo "\"". $data[1] . "\",";
			}
			$i++;
		    }
		    fclose($handle);
		}
		echo "],\n"
		?>
	      backgroundColor: 'rgba(153, 102, 255, 0.2)',
	      borderColor: 'rgba(153, 102, 255, 1)',
	      borderWidth: 1
	    }]
	  },
	  options: {
	    responsive: true,
	    lineAt: 0.45,
	    scales: {
	      xAxes: [{
		ticks: {
		  maxRotation: 90,
		  minRotation: 80
		}
	      }],
	      yAxes: [{
		ticks: {
		  beginAtZero: true,
                  stepSize: 0.05,
                  max: 1
		}
	      }]
	    },


	  },
	});
	
	
        
	var ctxMXBarChar = document.getElementById("m-x-bar-chart");
	var MXChart = new Chart(ctxMXBarChar, {
	  type: 'bar',
	  data: {
		<?php
		echo "labels:[";
		if (($handle = fopen("m-x-flare-forecasts-graphical-input.csv", "r")) !== FALSE) {
		    $i=0;
	            $linecount = count(file("m-x-flare-forecasts-graphical-input.csv"));
		    while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
			if ($i >= ($linecount - 14)) {
			    echo "\"". $data[0] . "\",";
			}
			$i++;
		    }
		    fclose($handle);
		}
		echo "],\n"
		?>
	  datasets: [{
	      label: 'M+X flare probability in the next 24 h',
		
		<?php
		echo "data:[";
		if (($handle = fopen("m-x-flare-forecasts-graphical-input.csv", "r")) !== FALSE) {
		    $i=0;
	            $linecount = count(file("m-x-flare-forecasts-graphical-input.csv"));
		    while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
			if ($i >= ($linecount - 14)) {
			    echo "\"". $data[1] . "\",";
			}
			$i++;
		    }
		    fclose($handle);
		}
		echo "],\n"
		?>
	      backgroundColor: 'rgba(75, 192, 192, 0.2)',
	      borderColor: 'rgba(75, 192, 192, 1)',
	      borderWidth: 1
	    }]
	  },
	  options: {
	    responsive: true,
	    lineAt: 0.43,
	    scales: {
	      xAxes: [{
		ticks: {
		  maxRotation: 90,
		  minRotation: 80
		}
	      }],
	      yAxes: [{
		ticks: {
		  beginAtZero: true,
		  stepSize: 0.05,
                  max: 1
		}
	      }]
	    }
	  }
	});
        </script>
	</body>
</html>
