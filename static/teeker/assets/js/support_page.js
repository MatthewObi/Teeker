// Javascript for Support Page

grecaptcha.ready(function() {
	$('#supportform').submit(function(e){
		var form = this;
		e.preventDefault()
		grecaptcha.execute(document.querySelector("#recaptcha_site_key").value, {action: 'supportform'}).then(function(token) {
			$('#recaptcha').val(token)
			form.submit()
		});
	})
});
