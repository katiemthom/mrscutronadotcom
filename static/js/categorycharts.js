var cwhData = [
	{'title': 'homework 1', score: 4, 'maxScore': 5, date: '2011-01-01'},
	{'title': 'homework 1', score: 3, 'maxScore': 5, date: '2011-01-02'},
	{'title': 'homework 1', score: 2.5, 'maxScore': 5, date: '2011-01-03'},
]

//Width and height
var cwhMargin = {top: 20, right: 20, bottom: 30, left: 40},
    cwhWidth = 500,
    cwhHeight = 300,
    chartWidth = cwhWidth - cwhMargin.left - cwhMargin.right,
    chartHeight = cwhHeight - cwhMargin.top - cwhMargin.bottom,
    parseDate = d3.time.format("%Y-%m-%d").parse;

var x_domain = d3.extent(cwhData, function(d) { return parseDate(d.date); }),
    y_domain = [0, d3.max(cwhData, function(d) { return d.score; })];

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
    .domain(x_domain)
    .range([0, chartWidth]);

// define the y axis
var cwhYAxis = d3.svg.axis()
    .orient("left")
    .ticks(d3.range(y_domain[0], y_domain[1]).length)
    .scale(cwhY);

// define the x axis
var cwhXAxis = d3.svg.axis()
    .orient("bottom")
    .scale(cwhX)
    .ticks(d3.time.days(x_domain[0], x_domain[1]).length)
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
.attr("transform", "translate(" +cwhMargin.left+ "," + (cwhMargin.top + chartHeight) + ")")
.call(cwhXAxis);

vis.selectAll("rect")
   .data(cwhData)
   .enter()
   .append("rect")
   .attr("x", function(d, i) {
   		return i * (chartWidth / cwhData.length);
   })
   .attr("y", function(d) {
   		return chartHeight - (d.score * 4);
   })
   .attr("width", chartWidth / cwhData.length)
   .attr("height", function(d) {
   		return d.score * 4;
   })
   .attr("fill", function(d) {
		return "rgb(0, 0, " + (d.score * 50) + ")";
   });