$(document).ready(function() {
	$('*[id*=date]:visible').each(function() {
		var date = new Date($(this).html());
		date = date.toLocaleString();
		$(this).html(date);
	});
});