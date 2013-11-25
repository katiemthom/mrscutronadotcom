var cwhData = [
	{'title': 'homework 1', score: 4, 'maxScore': 5, date: '2011-01-01'},
	{'title': 'homework 1', score: 3, 'maxScore': 5, date: '2011-01-02'},
	{'title': 'homework 1', score: 2.5, 'maxScore': 5, date: '2011-01-03'},
  {'title': 'homework 1', score: 1, 'maxScore': 5, date: '2011-01-04'},
  {'title': 'homework 1', score: 5, 'maxScore': 5, date: '2011-01-05'},
  {'title': 'homework 1', score: 0, 'maxScore': 5, date: '2011-01-06'},
  {'title': 'homework 1', score: .33, 'maxScore': 5, date: '2011-01-07'},
  {'title': 'homework 1', score: 4.33, 'maxScore': 5, date: '2011-01-08'},
  {'title': 'homework 1', score: 2.67, 'maxScore': 5, date: '2011-01-09'},
]

//Width and height
var cwhMargin = {top: 20, right: 20, bottom: 30, left: 40},
    cwhWidth = 700,
    cwhHeight = 300,
    chartWidth = cwhWidth - cwhMargin.left - cwhMargin.right,
    chartHeight = cwhHeight - cwhMargin.top - cwhMargin.bottom,
    barPadding = 41, 
    parseDate = d3.time.format("%Y-%m-%d").parse;


var x_domain = d3.extent(cwhData, function(d) { return parseDate(d.date); }),
    y_domain = [0, 5];

var  date_format = d3.time.format("%d %b");

//Create SVG element
var vis = d3.select(".cwh-graph")
			.append("svg:svg")
			.attr("class","vis")
			.attr("width", cwhWidth)
			.attr("height", cwhHeight);

var cwhY = d3.scale.linear()
    .domain(y_domain)   
    .range([chartHeight, 0]);
    
var cwhX = d3.time.scale()
    .range([0, chartWidth])
    .domain(x_domain);

// define the y axis
var cwhYAxis = d3.svg.axis()
    .orient("left")
    .ticks(d3.range(y_domain[0], y_domain[1]).length)
    .scale(cwhY);

// define the x axis
var cwhXAxis = d3.svg.axis()
    .orient("bottom")
    .scale(cwhX)
    .ticks(d3.time.days(x_domain[0], x_domain[1]).length/3)
    .tickFormat(date_format);

vis.append("g")
.attr("class", "axis")
.attr("transform", "translate("+cwhMargin.left+"," + cwhMargin.top + ")")
.call(cwhYAxis)
.selectAll('text')
  .style('color','#99D500')
  .style('text-anchor','middle');

vis.append("g")
.attr("class", "xaxis axis")  
.attr("transform", "translate(" + cwhMargin.left + "," + (cwhMargin.top + chartHeight) + ")")
.call(cwhXAxis);

vis.selectAll("rect")
   .data(cwhData)
   .enter()
   .append("rect")
   .attr("x", function(d, i) {
   		return i * (chartWidth / cwhData.length) + barPadding;
   })
   .attr("y", function(d) {
   		return cwhY(d.score) + cwhMargin.top;
   })
   .attr("width", chartWidth / cwhData.length - barPadding)

   .attr("height", function(d) {
   		return cwhHeight - cwhMargin.bottom - cwhMargin.top - cwhY(d.score) - 1;
   })
   .attr("fill", function(d) {
		return "rgb(0, 0, " + (d.score * 50) + ")";
   });