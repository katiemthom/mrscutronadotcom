$('#bold').click(function() {
	$('#post_content').selection('replace', {text: '**'+$('#post_content').selection()+'**'});
});

$('#italic').click(function() {
	$('#post_content').selection('replace', {text: '*'+$('#post_content').selection()+'*'});
});

$('#header').click(function() {
	$('#post_content').selection('replace', {text: '###'+$('#post_content').selection()});
});

// $('#link').click(function() {
// 	$('#post_content').selection('replace', {text: '[replace]('+$('#post_content').selection()+')'});
// });

setInterval(function() {
	$.ajax({
		type: 'POST',
		url: '/addpostajax',
		data: {'hello': $('#post_content').val(), 'title': $('#post_title').val()},
		}).done(function(result) {
			$('#preview').html(result);
		});}
, 3000);

