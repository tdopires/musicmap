(function() {

	var sparqlCache = {};
	var performSparqlQuery = function(url, callback) {
		callback = callback || function() {};
		if (!url){
			throw 'URL is required';
		}

		if (sparqlCache[url]) {
			callback(sparqlCache[url]);
		}

		var req = jQuery.get(url);
		var respObj = {};
		req.done(function(response) {

			var results = $(response).find('result').each(function(i, result) {
				var obj = {}
				$(result).find('binding').each(function(idx, binding) {
					binding = $(binding);
					obj[binding.attr('name')] = binding.find('literal').text();
				});
				if (obj['countryCode']) {
					respObj[ obj['countryCode'] ] = obj['alllist'];	
				}
			});

			sparqlCache[url] = respObj;
			if (callback) {
				callback(respObj);
			}
		});
	}

	var totalListeners = [];
	performSparqlQuery('http://localhost:8080/sparql?query=PREFIX+rdfs%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0D%0APREFIX+mbo%3A+%3Chttp%3A%2F%2Fwww.semanticweb.org%2Ftdopires%2Fontologies%2F2014%2F9%2Funtitled-ontology-12%23%3E%0D%0APREFIX+mo%3A+%3Chttp%3A%2F%2Fpurl.org%2Fontology%2Fmo%2F%3E%0D%0APREFIX+geo%3A+%3Chttp%3A%2F%2Fwww.geonames.org%2Fontology%23%3E%0D%0ASELECT+%3FcountryCode+%28sum%28%3Flist%29+as+%3Falllist%29%0D%0AWHERE+{+%0D%0A++%3Flocation+a+%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2Fcountry%3E+.%0D%0A++%3Flocation+geo%3AcountryCode+%3FcountryCode+.%0D%0A++%3Frelation+a+mbo%3ARelation_Artist_Location+.%0D%0A++%3Frelation+%3Fy+%3Flocation+.%0D%0A++%3Frelation+mbo%3Ahas_listeners+%3Flist+.%0D%0A++%0D%0A}+group+by+%3FcountryCode&accept=xml',
			function(respObj) {
				totalListeners = respObj;
			});

	var sparqlQueryURL = function(genreName) {
		return 'http://localhost:8080/sparql?query=PREFIX+rdfs%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0D%0APREFIX+mbo%3A+%3Chttp%3A%2F%2Fwww.semanticweb.org%2Ftdopires%2Fontologies%2F2014%2F9%2Funtitled-ontology-12%23%3E%0D%0APREFIX+mo%3A+%3Chttp%3A%2F%2Fpurl.org%2Fontology%2Fmo%2F%3E%0D%0APREFIX+geo%3A+%3Chttp%3A%2F%2Fwww.geonames.org%2Fontology%23%3E%0D%0ASELECT+%3FcountryCode+%28sum%28%3Flist%29+as+%3Falllist%29%0D%0AWHERE+%7B+%0D%0A++%3Flocation+a+%3Chttp%3A%2F%2Fdbpedia.org%2Fontology%2Fcountry%3E+.%0D%0A++%3Flocation+geo%3AcountryCode+%3FcountryCode+.%0D%0A++%3Frelation+a+mbo%3ARelation_Artist_Location+.%0D%0A++%3Frelation+%3Fy+%3Flocation+.%0D%0A++%3Frelation+mbo%3Ahas_listeners+%3Flist+.%0D%0A++%3Fartist+%3Fx+%3Frelation+.%0D%0A++%3Fgenre+a+mo%3AGenre+.%0D%0A++%3Fartist+%3Fp+%3Fgenre+.%0D%0A++%3Fgenre+rdfs%3Alabel+%3Fgenrename+.%0D%0Afilter+%28%3Fgenrename+%3D+%22' + encodeURIComponent(genreName) + '%22%29%0D%0A%7D+group+by+%3FcountryCode&accept=xml';
	}

	var loadGenreGeoChart = function(genreName, colorHex) {
		$('#loading').show();
		$('.genre-selected-title').hide();
		performSparqlQuery(sparqlQueryURL(genreName),
			function(respObj) {
				var respArrayGeoChart = [], genreListeners = respObj;
				for (var countryCode in genreListeners) {
					var listeners_to_map = (parseInt(genreListeners[countryCode]) / parseInt(totalListeners[countryCode])) * 100;

					respArrayGeoChart.push([ countryCode, listeners_to_map ]);
				}

				if (respArrayGeoChart.length == 0)
					throw 'No data for ' + genreName;

				respArrayGeoChart.unshift(['Country', 'Genre popularity (%)']);

				var data = google.visualization.arrayToDataTable(respArrayGeoChart);

				var chart = new google.visualization.GeoChart(document.getElementById('regions_div'));

				chart.draw(data, {
					legend: 'none', 
					region: '150',
					colorAxis: {minValue: 0,  colors: ['#FFFFFF', colorHex]},
				});

				$('#loading').hide();
				$('.genre-selected-title h1').text(genreName);
				$('.genre-selected-title').show();
			});
	}
	
	var carouselActive = true;
	$(document).ready(function() {
		$('.genre').click(function() {
			$('.genre').removeClass('active');
			$(this).addClass('active');

			var bg = $(this).find('.label').css('background-color');
			var components = bg.substring(bg.indexOf('(') + 1, bg.indexOf(')')).split(',');
			var r = parseInt(components[0].trim());
			var g = parseInt(components[1].trim());
			var b = parseInt(components[2].trim());

			loadGenreGeoChart($(this).text(), rgbToHex(r, g, b));
		});
		$('.genre').eq(0).click();

		setTimeout(scheduleCarousel, 15000);

		$('.carousel-active').click(function() {
			if (carouselActive) {
				carouselActive = false;
			} else {
				carouselActive = true;
			}
		})
	});

	var componentToHex = function(c) {
		var hex = c.toString(16);
		return hex.length == 1 ? "0" + hex : hex;
	}

	var rgbToHex = function(r, g, b) {
		return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
	}

	var mapIdx = 1;
	var scheduleCarousel = function() {
		performSparqlQuery(sparqlQueryURL($('.genre').eq(1).text().trim()));

		setInterval(function() {
			if (!carouselActive) {
				return;
			}

			$('.genre').eq(mapIdx++).click();

			var genreName = $('.genre').eq(mapIdx).text().trim();
			performSparqlQuery(sparqlQueryURL(genreName));
		}, 30000);
	}

})();

