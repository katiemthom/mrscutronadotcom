// ***************** DOCUMENT.READY *****************
$(document).ready(function() { 
	new AWS.S3().listObjects({Bucket: 'myBucket'}, function(error, data) {
  		if (error) {
    		console.log(error); // an error occurred
  		} else {
    		console.log(data); // request succeeded
  		}
	});
})