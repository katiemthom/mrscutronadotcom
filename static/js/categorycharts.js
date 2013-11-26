function show_cwh() {
    var cwhData = [
      {aTitle: 'homework 1', score: 4, 'maxScore': 5, date: '2011-01-01', pk: 1},
      {aTitle: 'homework 1', score: 3, 'maxScore': 5, date: '2011-01-02', pk: 2},
      {aTitle: 'homework 1', score: 2.5, 'maxScore': 5, date: '2011-01-03', pk: 3},
      {aTitle: 'homework 1', score: 1, 'maxScore': 5, date: '2011-01-04', pk: 4},
      {aTitle: 'homework 1', score: 5, 'maxScore': 5, date: '2011-01-05', pk: 5},
      {aTitle: 'homework 1', score: 0, 'maxScore': 5, date: '2011-01-06', pk: 6},
      {aTitle: 'homework 1', score: .33, 'maxScore': 5, date: '2011-01-07', pk: 7},
      {aTitle: 'homework 1', score: 4.33, 'maxScore': 5, date: '2011-01-08', pk: 8},
      {aTitle: 'homework 1', score: 2.67, 'maxScore': 5, date: '2011-01-09', pk: 9},
      {aTitle: 'homework 2', score: 0, 'maxScore': 5, date: '2011-01-10', pk: 10},
      {aTitle: 'homework 3', score: .33, 'maxScore': 5, date: '2011-01-11', pk: 11},
      {aTitle: 'homework 4', score: 4.33, 'maxScore': 5, date: '2011-01-12', pk: 12},
    ]

    //Width and height
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
            $('#assignment_title').append(d.aTitle);
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


$(document).ready(function() {
    $("#testclear").click(function() {
        $(".cwh-graph").html("");
    });

    $("#testshowcwh").click(function() {
        show_cwh();
    });

});


function show_details() {
    $(".testdiv").append('<h1>Assignment Details</h1><br><br><p class="larger">Assignment Title: <span id="assignment_title"></span></p><p class="larger">Score: <span id="assignment_score"></span></p><p class="larger">Due Date: <span id="assignment_due_on"></span></p>');
}


