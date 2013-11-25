function show_cwh() {
    var cwhData = [
      {'title': 'homework 1', score: 4, 'maxScore': 5, date: '2011-01-01', pk: 1},
      {'title': 'homework 1', score: 3, 'maxScore': 5, date: '2011-01-02', pk: 2},
      {'title': 'homework 1', score: 2.5, 'maxScore': 5, date: '2011-01-03', pk: 3},
      {'title': 'homework 1', score: 1, 'maxScore': 5, date: '2011-01-04', pk: 4},
      {'title': 'homework 1', score: 5, 'maxScore': 5, date: '2011-01-05', pk: 5},
      {'title': 'homework 1', score: 0, 'maxScore': 5, date: '2011-01-06', pk: 6},
      {'title': 'homework 1', score: .33, 'maxScore': 5, date: '2011-01-07', pk: 7},
      {'title': 'homework 1', score: 4.33, 'maxScore': 5, date: '2011-01-08', pk: 8},
      {'title': 'homework 1', score: 2.67, 'maxScore': 5, date: '2011-01-09', pk: 9},
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
        .ticks(d3.time.days(x_domain[0], x_domain[1]).length/5)
        .tickFormat(date_format);

    vis.append("g")
    .attr("class", "axis")
    .attr("transform", "translate("+cwhMargin.left+"," + cwhMargin.top + ")")
    .call(cwhYAxis)
    .selectAll('text')
      .style("color","#99D500")
      .style("text-anchor", "end")

    vis.append("g")
    .attr("class", "xaxis axis")  
    .attr("transform", "translate(" + cwhMargin.left + "," + (cwhMargin.top + chartHeight) + ")")
    .call(cwhXAxis);

    vis.selectAll("rect")
       .data(cwhData)
       .enter()
       .append("rect")
       .attr("id",function(d) { return String("grade" + d.pk); })
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
       .attr("fill", "#707070")
       .on("mouseover", function(){d3.select(this).style("fill", "#ADADAD");})
       .on("mouseout", function(){d3.select(this).style("fill", "#707070");});
}





var csvFile; 

// ***************** AJAX CALL FOR DATA *****************
$(document).ready(function() {
    $.ajax({
    type: "GET",
        url: "/gradeinfo"
    }).done(function( msg ) {
        csvFile = msg['grades_file'];
        }); 


    // ***************** D3 SETUP *****************
// Set variables for width and height of SVG (with margin)
var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 400 - margin.left - margin.right,
    height = 150 - margin.top - margin.bottom;

// x and y scaling functions 
var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1);

var y = d3.scale.linear()
    .rangeRound([height, 0]);

// color scaling function
var color = d3.scale.ordinal()
    .range(["#707070", "#ADADAD", "#FFFFFF"]);

// define x and y axes 
var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .tickFormat(d3.format(".2s"))
    .ticks(2);

// create svg 'canvas'
var svg = d3.select(".chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");



    // ***************** ADD MAX GRADE DATA (OUTLINES) *****************
    // loads category max values
    // csv loader callback function  
    d3.csv("/static/data2.csv", function(error, data) {
      color.domain(d3.keys(data[0]).filter(function(key) { return key !== "Category"; }));

      // creates an object for each row in the data set 
      data.forEach(function(d) {
        var y0 = 0;
        d.cats = color.domain().map(function(name) { return {name: name, y0: y0, y1: y0 += +d[name]}; });
        d.total = d.cats[d.cats.length - 1].y1;
      });


    // creates domains for x and y scaling functions 
    x.domain(data.map(function(d) { return d.Category; }));
    y.domain([0, d3.max(data, function(d) { return d.total; })]);

      // creates a g element to add the outline bar
      var max = svg.selectAll(".max")
          .data(data)
          .enter().append("g")
          .attr("class", "g")
          .attr("transform", function(d) { return "translate(" + x(d.Category) + ",0)";});

      // creates the outline 
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
// csv loader callback function 
// d3.csv("/static/data.csv", function(error, data) {
    d3.csv(csvFile, function(error, data) {
    color.domain(d3.keys(data[0]).filter(function(key) { return key !== "Category"; }));

    // name = category 
    // cats = categories 
    data.forEach(function(d) {
      var y0 = 0;
      d.cats = color.domain().map(function(name) { return {name: name, y0: y0, y1: y0 += +d[name], y2: d}; });
      d.total = d.cats[d.cats.length - 1].y1;
    });


    // adds x and y axes
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

    // creates g element for each bar 
    var Category = svg.selectAll(".Category")
        .data(data)
      .enter().append("g")
        .on("mouseover", function(){d3.select(this).style("cursor", "pointer");})
        .on("click",function(){
          $(".cwh-graph").html("");
          show_cwh();
        })
        .attr("transform", function(d) { return "translate(" + x(d.Category) + ",0)"; });

    // creates colored rect for each bar 
    Category.selectAll("rect")
        .data(function(d) { return d.cats; })
      .enter().append("g:rect")
        .attr("class","ajax")
        .attr("href", "/static/content/ajax.html")
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d.y1); })
        .attr("height", function(d) { return y(d.y0) - y(d.y1); })
        .style("fill", function(d) { return color(d.name); })
    });
});
});




