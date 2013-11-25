// ***************** D3 SETUP *****************
// Set variables for width and height of SVG (with margin)
var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

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
    .tickFormat(d3.format(".2s"));

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
          .attr("transform", function(d) { return "translate(" + x(d.Category) + ",0)"; });

      // creates the outline 
      max.selectAll("rect")
          .data(function(d) { return d.cats; })
          .enter().append("rect")
          .attr("width", x.rangeBand())
          .attr("y", function(d) { return y(d.y1); })
          .attr("height", function(d) { return y(d.y0) - y(d.y1); })
          .style("stroke", "white")
          .style("fill", "transparent");



// ***************** ADD STUDENT GRADE DATA (COLORED BANDS) *****************
// csv loader callback function 
d3.csv("/static/data.csv", function(error, data) {
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
        .style("fill", function(d) { return color(d.name); });

      // adds tooltips to elements that are both g and rect elements 
    //   $('g rect').tipsy({ 
    //     gravity: 'w', 
    //     html: true, 
    //     title: function() {
    //       d = this.__data__;
    //       if (d.y2.total) {
    //         return 'Hi there! My d is ' + d.y2.total ;
    //       }
    //   }
    // });
    

      $('.ajax').on('click', function() {
        $.colorbox({href:$(this).attr('href'), open:true});
        return false;
      });

    });


});