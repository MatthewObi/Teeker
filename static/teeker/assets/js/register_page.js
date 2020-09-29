// Javascript for Register page

document.addEventListener("DOMContentLoaded", () => {
	// Get the CSRF token from the cookie
	let cookieValue = null
	if (document.cookie && document.cookie != '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, 10) == ('csrftoken' + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
	}

	// Check username
	document.querySelector("#username").onchange = () => {
		const request = new XMLHttpRequest()
		request.open("POST", "/register/check")
		const data = new FormData()
		data.append("csrfmiddlewaretoken", cookieValue)
		data.append("register_check", true)
		data.append("username", document.querySelector("#username").value)
		request.send(data)
		request.onreadystatechange = () => {
			if (request.readyState === 4 && request.status === 200) {
				if (JSON.parse(request.response)["STATUS"]) {

					if (JSON.parse(request.response)["USERNAME"] === "usable_true") {
						// If the username is usable notify the user
						document.querySelector("#label_username").innerHTML = JSON.parse(request.response)["MESSAGE"]
						document.querySelector("#label_username").style.display = "inline"
						document.querySelector("#label_username").style.color = "green"
						document.querySelector("#label_username").classList.toggle("text-danger", false)
						document.querySelector("#username").style.borderColor = "green"

					} else if (JSON.parse(request.response)["USERNAME"] === "usable_false") {
						// If the username is usable notify the user
						document.querySelector("#label_username").innerHTML = JSON.parse(request.response)["MESSAGE"]
						document.querySelector("#label_username").style.display = "inline"
						document.querySelector("#label_username").classList.toggle("text-danger", true)
						document.querySelector("#username").style.borderColor = "red"

					} else if (JSON.parse(request.response)["USERNAME"]) {
						// If the server sends back any error messages
						document.querySelector("#label_username").innerHTML = JSON.parse(request.response)["MESSAGE"]
						document.querySelector("#label_username").style.display = "inline"
						document.querySelector("#label_username").classList.toggle("text-danger", true)
						document.querySelector("#username").style.borderColor = "red"

					}
				}
			}
		}
	}

	// Check email address
	document.querySelector("#email").onchange = () => {
		const request = new XMLHttpRequest()
		request.open("POST", "/register/check")
		const data = new FormData()
		data.append("csrfmiddlewaretoken", cookieValue)
		data.append("register_check", true)
		data.append("email", document.querySelector("#email").value)
		request.send(data)
		request.onreadystatechange = () => {
			if (request.readyState === 4 && request.status === 200) {
				if (JSON.parse(request.response)["STATUS"]) {
					
					if (JSON.parse(request.response)["EMAIL"] === "usable_true") {
						// If the email is usable notify the user
						document.querySelector("#label_email").innerHTML = JSON.parse(request.response)["MESSAGE"]
						document.querySelector("#label_email").style.display = "inline"
						document.querySelector("#label_email").style.color = "green"
						document.querySelector("#label_email").classList.toggle("text-danger", false)
						document.querySelector("#email").style.borderColor = "green"

					} else if (JSON.parse(request.response)["EMAIL"] === "usable_false") {
						// If the email is usable notify the user
						document.querySelector("#label_email").innerHTML = JSON.parse(request.response)["MESSAGE"]
						document.querySelector("#label_email").style.display = "inline"
						document.querySelector("#label_email").classList.toggle("text-danger", true)
						document.querySelector("#email").style.borderColor = "red"

					} else if (JSON.parse(request.response)["EMAIL"]) {
						// If the server sends back any error messages
						document.querySelector("#label_email").innerHTML = JSON.parse(request.response)["MESSAGE"]
						document.querySelector("#label_email").style.display = "inline"
						document.querySelector("#label_email").classList.toggle("text-danger", true)
						document.querySelector("#email").style.borderColor = "red"

					}
				}
			}
		}
	}


	// Check the password
	document.querySelector("#pwd").onchange = () => {
		let _pwd = document.querySelector("#pwd")
		if (_pwd.value.length >= 8 && _pwd.value.length <= 128) {
			document.querySelector("#label_pwd").innerHTML = "Password is good!"
			document.querySelector("#label_pwd").style.display = "inline"
			document.querySelector("#label_pwd").style.color = "green"
			document.querySelector("#label_pwd").classList.toggle("text-danger", false)
			document.querySelector("#pwd").style.borderColor = "green"
		} else {
			if (_pwd.value.length < 8) {
				document.querySelector("#label_pwd").innerHTML = "Password is too short..."
			} else if (_pwd.value.length > 128) {
				document.querySelector("#label_pwd").innerHTML = "Password is too long..."
			}
			document.querySelector("#label_pwd").style.display = "inline"
			document.querySelector("#label_pwd").classList.toggle("text-danger", true)
			document.querySelector("#pwd").style.borderColor = "red"
		}

		// Reset confirm password
		if (document.querySelector("#cpwd")) {
			document.querySelector("#label_cpwd").style.display = "none"
			document.querySelector("#cpwd").value = ""
		}
	}

	// Check confirm password with the password
	document.querySelector("#cpwd").onchange = () => {
		let _pwd = document.querySelector("#pwd")
		let _cpwd = document.querySelector("#cpwd")
		if (_pwd.value === _cpwd.value) {
			document.querySelector("#label_cpwd").innerHTML = "Passwords match!"
			document.querySelector("#label_cpwd").style.display = "inline"
			document.querySelector("#label_cpwd").style.color = "green"
			document.querySelector("#label_cpwd").classList.toggle("text-danger", false)
			document.querySelector("#cpwd").style.borderColor = "green"
		} else {
			document.querySelector("#label_cpwd").innerHTML = "Passwords don't match!"
			document.querySelector("#label_cpwd").style.display = "inline"
			document.querySelector("#label_cpwd").classList.toggle("text-danger", true)
			document.querySelector("#cpwd").style.borderColor = "red"
		}
	}
})

grecaptcha.ready(function() {
	$('#registerform').submit(function(e){
		var form = this;
		e.preventDefault()
		grecaptcha.execute(document.querySelector("#recaptcha_site_key").value, {action: 'registerform'}).then(function(token) {
			$('#recaptcha').val(token)
			form.submit()
		});
	})
});
