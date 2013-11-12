function addComment(authorId,postId,startId,destId) {
	$.ajax({
		type: "POST",
  		url: "/post/" + postId, 
  		data: { user_id: authorId, post_pk: postId, comment: $(startId).val() }
		}).done(function( msg ) {
			$('#comment_input').val(""); 
			$('#added_comments').append('<div class="page-header"><h4>'
				+msg['comment_author']
				+':</h4><div id="'
				+msg['comment_pk']
				+'-mom"></div><div id="'
				+msg['comment_pk']
				+'">'
				+msg['comment_content']
				+'<br><br><small>'
				+msg['comment_timestamp']
				+'<a href="javascript:editComment(\'#'
				+msg['comment_pk']
				+'\','
				+msg['comment_pk']
				+');"> edit</a><a href="/deletecomment/'
				+msg['comment_pk']
				+'"> delete</a></small></div></div>');
  		});	
}





$(document).ready(function() {
	$('#comment_input').keyup(function(event) {
		if(event.keyCode == 13) {
			$('#comment_submit').click();
		}
	});
});
function editComment(destId,commentPk) {
	$.ajax({
		type: "GET",
		url: "/edit_comment/" + commentPk
	}).done(function(msg) {
		var first = '<textarea class="form-control" id="edited_comment">'+msg['comment_content']+'</textarea><br><a href="javascript:submitEdit(\'' + destId + '\',' + commentPk + ');"><button class="btn btn-default" id="edit_submit">Submit</button></a><br>';
		$(destId).append('<br><br>');
		$(destId).append(first);
	});
}
function submitEdit(startId,commentPk) {
	$.ajax({
		type: "POST",
  		url: "/edit_comment/" + commentPk,
  		data: { edited_comment: $('#edited_comment').val() }
		}).done(function( msg ) {
			$(startId).hide();
			$(startId+"-mom").append(msg['comment_content']);
			$(startId+"-mom").append('<br><br><small>');
			$(startId+"-mom").append(msg['comment_timestamp']);
			$(startId+"-mom").append('<a href="javascript:editComment(#');
			$(startId+"-mom").append(msg['comment_pk']);
			$(startId+"-mom").append(',');
			$(startId+"-mom").append(msg['comment_pk']);
			$(startId+"-mom").append(');">edit</a></small></div>');
  		});	
}
