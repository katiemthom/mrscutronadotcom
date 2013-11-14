$('#bold').click(function() {
	$('#post_content').selection('replace', {text: '**'+$('#post_content').selection()+'**'});
});

$('#italic').click(function() {
	$('#post_content').selection('replace', {text: '*'+$('#post_content').selection()+'*'});
});


setInterval(function() {
	$.ajax({
		type: 'POST',
		url: '/testajax',
		data: {'hello': $('#post_content').val()},
		}).done(function(result) {
			$('#preview').html(result);
		});}
, 3000);

