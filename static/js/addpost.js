$('#test').click(function() {
	$('#post-editor').selection('replace', {text: '**'+$('#post-editor').selection()+'**'});
});

$('#preview').click(function() {
	$('#show-preview').html('{% filter markdown %}'+$('#post-editor').val()+'{% endfilter %}');
});

