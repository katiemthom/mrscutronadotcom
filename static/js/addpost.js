 $('#test').click(function() {
	$('#post-editor').selection('replace', {text: '[b]'+$('#post-editor').selection()+'[/b]'});
});

$('#preview').click(function() {
	$('#show-preview').text($('#post-editor').val())
	var unparsed_html = $('#show-preview').html()
	parsed_html = unparsed_html.replace('[b]', '<b>');
	parsed_html = parsed_html.replace('[/b]', '</b>')
	$('#show-preview').html(parsed_html);
});

