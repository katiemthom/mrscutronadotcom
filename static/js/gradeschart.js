// ***************** GLOBAL VARIABLES *****************
var csvFile; 
var gradesDict;
var AKGrade; 
var MKGrade;
var TOTALGrade;
var CWHGrade;
var CWHGrades = new Array;
var AKGrades = new Array;
var MKGrades = new Array;
var TOTALGrades = new Array;

// ***************** DOCUMENT.READY *****************
$(document).ready(function() {
	// ***************** AJAX CALL FOR DATA *****************
	$.ajax({
		type: "GET",
		url: "/gradeinfo"
	}).done(function( msg ) {
		csvFile = msg['grades_file'];
		gradesDict = eval(msg['grades_dict']);
		load_main_chart();
		show_main_details();
		TOTALGrade = msg['total_grade'];
		MKGrade = msg['mk_grade'];
		AKGrade = msg['ak_grade'];
		CWHGrade = msg['cwh_grade'];
		$("#cat_details").append("<p class=larger>Total Grade: " + msg['total_grade'] + "%</p>");
		$("#gradesfor").append("Current Grade: " + msg['total_grade'] + "%");
		create_data();
	}); 
	// ***************** LOADS MAIN GRADE CHART ****************
});

// ***************** FUNCTIONS *****************
function create_data() {
	for (var i = gradesDict.length - 1; i >= 0; i--) {
		if ( gradesDict[i].category == "CWH" ) {
			CWHGrades.push(gradesDict[i]);
		} else if ( gradesDict[i].category == "MK" ) {
			MKGrades.push(gradesDict[i]);
		} else if ( gradesDict[i].category == "AK" ) {
			AKGrades.push(gradesDict[i]);
		}
		TOTALGrades.push(gradesDict[i]);
	};

}

// ***************** LOADS MAIN GRADE CHART *****************
function load_main_chart () {
	// ***************** D3 MAIN GRADES CHART *****************
	// ***************** VARIABLES *****************
	var margin = {top: 20, right: 20, bottom: 30, left: 40},
		width = 400 - margin.left - margin.right,
		height = 190 - margin.top - margin.bottom;

	// ***************** SCALING FUNCTIONS *****************
	var x = d3.scale.ordinal()
		.rangeRoundBands([0, width], .1);
	var y = d3.scale.linear()
		.rangeRound([height, 0]);
	var color = d3.scale.ordinal()
		.range(["#707070", "#ADADAD", "#FFFFFF"]);

	// ***************** SVG *****************
	var svg = d3.select(".chart").append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
		.append("g")
		.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	// ***************** LOAD MAX GRADE DATA (OUTLINES) *****************
	d3.csv("/static/data2.csv", function(error, data) {
		color.domain(d3.keys(data[0]).filter(function(key) { return key !== "Category"; }));
		data.forEach(function(d) {
			var y0 = 0;
			d.cats = color.domain().map(function(name) { return {name: name, y0: y0, y1: y0 += +d[name]}; });
			d.total = d.cats[d.cats.length - 1].y1;
		});

		x.domain(data.map(function(d) { return d.Category; }));
		y.domain([0, d3.max(data, function(d) { return d.total; })]);

		var max = svg.selectAll(".max")
				.data(data)
				.enter().append("g")
				.attr("class", "g")
				.attr("transform", function(d) { return "translate(" + x(d.Category) + ",0)";})

		max.selectAll("rect")
				.data(function(d) { return d.cats; })
				.enter().append("rect")
				.attr("width", x.rangeBand())
				.attr("y", function(d) { return y(d.y1); })
				.attr("height", function(d) { return y(d.y0) - y(d.y1); })
				.style("stroke", "white")
				.on("mouseover", function(){d3.select(this).style("cursor", "pointer");})
				.style("fill", "transparent");


		// ***************** ADD STUDENT GRADE DATA (COLORED BANDS) *****************
		d3.csv(csvFile, function(error, data) {
			color.domain(d3.keys(data[0]).filter(function(key) { return key !== "Category"; }));
			data.forEach(function(d) {
				var y0 = 0;
				d.cats = color.domain().map(function(name) { return {name: name, y0: y0, y1: y0 += +d[name], y2: d}; });
				d.total = d.cats[d.cats.length - 1].y1;
			});

			var Category = svg.selectAll(".Category")
				.data(data)
				.enter().append("g")
				.on("mouseover", function(d){
					d3.select(this).style("cursor", "pointer");
					$('#category_title').html("");
					$('#max_possible').html("");
					$('#category_score').html("");
					if (d.Category == "CWH") {
						$('#category_title').append("College Work Habits");
						$('#max_possible').append("15%");
						$('#category_score').append(CWHGrade+"%");
					} else if (d.Category == "MK") {
						$('#category_title').append("Mastery of Knowledge");
						$('#max_possible').append("40%");
						$('#category_score').append(MKGrade+"%");
					} else if (d.Category == "AK") {
						$('#category_title').append("Application of Knowledge");
						$('#max_possible').append("45%");
						$('#category_score').append(AKGrade+"%");
					} else if (d.Category == "TOTAL") {
						$('#category_title').append("Total");
						$('#max_possible').append("100%");
						$('#category_score').append(TOTALGrade+"%");
					}
				})
				.on("click",function(d){
					$(".cwh-graph").html("");
					$(".testdiv").html("");
					if (d.Category == "CWH") {
						show_cwh(CWHGrades);
					} else if (d.Category == "AK") {
						show_cwh(AKGrades);
					} else if (d.Category == "MK") {
						show_cwh(MKGrades);
					} else if (d.Category == "TOTAL") {
						show_cwh(TOTALGrades);
					}
					show_details();
				})
				.attr("transform", function(d) { return "translate(" + x(d.Category) + ",0)"; });

			Category.selectAll("rect")
				.data(function(d) { return d.cats; })
				.enter().append("g:rect")
				.attr("class","ajax")
				.attr("href", "/static/content/ajax.html")
				.attr("width", x.rangeBand())
				.attr("y", function(d) { return y(d.y1); })
				.attr("height", function(d) { return y(d.y0) - y(d.y1); })
				.style("fill", function(d) { return color(d.name); })
				// .on("mouseover", function(d){
				// 	$('#category_title').html("");
		  //           $('#category_score').html("");
		  //           $('#max_possible').html("");
				// 	if (d.name == "CWH") {
				// 		$('#category_title').append("College Work Habits");
				// 		$('#max_possible').append("15%");
				// 	} else if (d.name == "MK") {
				// 		$('#category_title').append("Mastery of Knowledge");
				// 		$('#max_possible').append("40%");
				// 	} else if (d.name == "AK") {
				// 		$('#category_title').append("Application of Knowledge");
				// 		$('#max_possible').append("45%");
				// 	}  
    //     		})

			// ***************** AXES *****************
			var xAxis = d3.svg.axis()
					.scale(x)
					.orient("bottom");
			var yAxis = d3.svg.axis()
					.scale(y)
					.orient("left")
					.tickFormat(d3.format(".2s"))
					.ticks(2);
			svg.append("g")
					.attr("class", "x axis")
					.attr("transform", "translate(0," + height + ")")
					.call(xAxis);
			svg.append("g")
					.attr("class", "y axis")
					.call(yAxis)
				.append("text")
					.attr("transform", "rotate(-90)")
					.attr("y", 6)
					.attr("dy", ".71em")
					.style("text-anchor", "end")
					.text("Percent");

			// ***************** END SECOND CALLBACK *****************
			});
		
			// ***************** CLEAR COVERS *****************
		    var cover = svg.selectAll(".cover")
				.data(data)
				.enter().append("g")
				.attr("class", "cover")
				.attr("transform", function(d) { return "translate(" + x(d.Category) + ",0)";})
				.on("click",function(d){
					$(".cwh-graph").html("");
					$(".testdiv").html("");
					if (d.Category == "CWH") {
						show_cwh(CWHGrades);
					} else if (d.Category == "AK") {
						show_cwh(AKGrades);
					} else if (d.Category == "MK") {
						show_cwh(MKGrades);
					} else if (d.Category == "TOTAL") {
						show_cwh(TOTALGrades);
					}
					show_details();
				});

			cover.selectAll("rect")
				.data(function(d) { return d.cats; })
				.enter().append("rect")
				.attr("width", x.rangeBand())
				.attr("y", function(d) { return y(d.y1); })
				.attr("height", function(d) { return y(d.y0) - y(d.y1); })
				.on("mouseover", function(){d3.select(this).style("cursor", "pointer");})
				.style("fill", "transparent");
		// ***************** END FIRST CALLBACK *****************
		});
}

// ***************** LOADS CATEGORY GRADE CHART *****************
function show_cwh(cwhData) {
	// ***************** VARIABLES *****************
    var cwhMargin = {top: 20, right: 20, bottom: 30, left: 40},
        cwhWidth = 700,
        cwhHeight = 300,
        chartWidth = cwhWidth - cwhMargin.left - cwhMargin.right,
        chartHeight = cwhHeight - cwhMargin.top - cwhMargin.bottom,
        barPadding = 10, 
        parseDate = d3.time.format("%Y-%m-%d").parse;
    var x_domain = d3.extent(cwhData, function(d) { return parseDate(d.date); }),
        y_domain = [0, 5];
    var  date_format = d3.time.format("%d %b");

    // ***************** SCALING FUNCTIONS *****************
    var cwhY = d3.scale.linear()
        .domain(y_domain)   
        .range([chartHeight, 0]);  
    var cwhX = d3.time.scale()
        .range([0, chartWidth])
        .domain(x_domain);

    // ***************** SVG *****************
    var vis = d3.select(".cwh-graph")
      	.append("svg:svg")
      	.attr("class","vis")
      	.attr("width", cwhWidth)
      	.attr("height", cwhHeight);

	// ***************** AXES *****************
    var cwhYAxis = d3.svg.axis()
        .orient("left")
        .ticks(d3.range(y_domain[0], y_domain[1]).length)
        .scale(cwhY);
    var cwhXAxis = d3.svg.axis()
        .orient("bottom")
        .scale(cwhX)
        .ticks(d3.time.days(x_domain[0], x_domain[1]).length/5)
        .tickFormat(date_format);
    vis.append("g")
	    .attr("class", "axis")
	    .attr("transform", "translate("+cwhMargin.left+"," + cwhMargin.top + ")")
	    .call(cwhYAxis)
	    .append("text")
			.attr("transform", "rotate(-90)")
			.attr("y", 6)
			.attr("dy", ".71em")
			.style("text-anchor", "end")
			.text("Score");
    vis.append("g")
	    .attr("class", "xaxis axis")  
	    .attr("transform", "translate(" + cwhMargin.left + "," + (cwhMargin.top + chartHeight) + ")")
	    .call(cwhXAxis)
	   	.append("text")
			.attr("y", 6)
			.attr("x", chartWidth - 10)
			.attr("dy", ".71em")
			.style("text-anchor", "end")
			.text("Time");

	// ***************** LOAD AND DISPLAY DATA *****************
    vis.selectAll("rect")
        .data(cwhData)
        .enter()
        .append("rect")
        .attr("id",function(d) { return String("grade" + d.pk); })
        .attr("x", function(d, i) {
        	return i * (chartWidth / cwhData.length) + 41;
        })
        .attr("y", function(d) {
            if (d.score == 0) {
                return cwhY(0.08) + cwhMargin.top
            } else {
                return cwhY(d.score) + cwhMargin.top;
            }
        })
        .attr("width", chartWidth / cwhData.length - barPadding)

        .attr("height", function(d) {
            if (d.score == 0) {
                return cwhHeight - cwhMargin.bottom - cwhMargin.top - cwhY(0.08) - 1
            } else {
                return cwhHeight - cwhMargin.bottom - cwhMargin.top - cwhY(d.score) - 1;
            }
        })
        .attr("fill", "#707070")
        .on("mouseover", function(d){
            d3.select(this).style("fill", "#ADADAD");
            $('#assignment_title').append(d.atitle);
            $('#assignment_score').append(d.score);
            $('#assignment_due_on').append(d.date);
        })
       .on("mouseout", function(){
            d3.select(this).style("fill", "#707070");
            $('#assignment_title').html("");
            $('#assignment_score').html("");
            $('#assignment_due_on').html("");
        });
}

// ***************** SHOW ASSIGNMENT/GRADE DETAILS *****************
function show_details() {
    $(".cwh-graph").append('<div class="container" id="assignment_details"><h1>Assignment Details</h1><br><br><p class="larger">Assignment Title: <span id="assignment_title"></span></p><p class="larger">Score: <span id="assignment_score"></span></p><p class="larger">Due Date: <span id="assignment_due_on"></span></p></div>');
}

function show_main_details() {
    $(".chart").append('<div class="container" id="cat_details"><br><h1>Category Details</h1><br><br><p class="larger">Category Title: <span id="category_title"></span></p><p class="larger">Grade: <span id="category_score"></span></p><p class="larger">Max Possible: <span id="max_possible"></span></p></div>');
}