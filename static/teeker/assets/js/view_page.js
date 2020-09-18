// Javascript for View page

document.addEventListener("DOMContentLoaded", () => {
	
	// Trigger for when the up vote button is pressed
	document.querySelector("#vote-up-btn").onclick = () => {
		const request = new XMLHttpRequest();
		request.open("POST", "/votesystem");
		const data = new FormData();
		data.append("csrfmiddlewaretoken", document.querySelector("input[name='csrfmiddlewaretoken']").value);
		data.append("content_id", document.querySelector("#vote-up-btn").dataset.content_id);
		data.append("votestatus", 1);
		request.send(data);
		request.onreadystatechange = () => {
			if (request.readyState === 4 && request.status === 200) {
				if (JSON.parse(request.response)["STATUS"]) {
					document.querySelector("#fire-rating").innerHTML = JSON.parse(request.response)["FIRE"];
					document.querySelector("#fire-rating").setAttribute("title", "UP: "+JSON.parse(request.response)["UP"]+" DOWN: "+JSON.parse(request.response)["DOWN"]);
				} else {
					document.querySelector("#fire-rating").innerHTML = "N/A";
					document.querySelector("#fire-rating").setAttribute("title", "UP: N/A DOWN: N/A");
				}
			}
		}
	}

	// Trigger for when the down vote button is pressed
	document.querySelector("#vote-down-btn").onclick = () => {
		const request = new XMLHttpRequest();
		request.open("POST", "/votesystem");
		const data = new FormData();
		data.append("csrfmiddlewaretoken", document.querySelector("input[name='csrfmiddlewaretoken']").value);
		data.append("content_id", document.querySelector("#vote-down-btn").dataset.content_id);
		data.append("votestatus", 0);
		request.send(data);
		request.onreadystatechange = () => {
			if (request.readyState === 4 && request.status === 200) {
				if (JSON.parse(request.response)["STATUS"]) {
					document.querySelector("#fire-rating").innerHTML = JSON.parse(request.response)["FIRE"];
					document.querySelector("#fire-rating").setAttribute("title", "UP: "+JSON.parse(request.response)["UP"]+" DOWN: "+JSON.parse(request.response)["DOWN"]);
				} else {
					document.querySelector("#fire-rating").innerHTML = "N/A";
					document.querySelector("#fire-rating").setAttribute("title", "UP: N/A DOWN: N/A");
				}
			}
		}
	}

	// Trigger for Copy link button from dropdown Menu to the clipboard
	document.querySelectorAll(".copy-link-btn").forEach(button => {
		button.onclick = () => {
			const el = document.createElement("textarea");
			el.value = location.hostname+"/view="+button.dataset.content_id;
			el.setAttribute("readonly", "");
			el.style.position = "absolute";
			el.style.left = "-9999px";
			document.body.appendChild(el);
			el.select();
			document.execCommand("copy");
			document.body.removeChild(el);
		}
	});

	// Shorten the description paragraph of the content
	const des_p = document.querySelector("#description-p").innerHTML;
	if (document.querySelector("#description-p").innerHTML.length > 50) {
		document.querySelector("#description-p").innerHTML = des_p.slice(0, 50) + "...";
	}
	
	// Show the rest of the content description and hide the 'more' button
	if (document.querySelector("#description-more")) {
		document.querySelector("#description-more").onclick = () => {
			document.querySelector("#description-p").innerHTML = des_p;
			document.querySelector("#description-more").style.display = "none";
		}
	}

	// Place content in the recommended list of the user
	document.querySelector(".recommend-btn").onclick = () => {
		
		const request = new XMLHttpRequest();
		request.open("POST", "recommend_sys");
		const data = new FormData();
		data.append("csrfmiddlewaretoken", document.querySelector("input[name='csrfmiddlewaretoken']").value);
		data.append("option", "recommend");
		data.append("content", document.querySelector(".recommend-btn").dataset.content_id);
		request.send(data);
		request.onreadystatechange = () => {
			if (request.status === 200 && request.readyState === 4) {
				if (JSON.parse(request.response)["STATUS"]) {
					if (JSON.parse(request.response)["recommended"]) {
						document.querySelector(".recommend-btn").innerHTML = '<i class="icon ion-android-remove-circle"></i>  Unrecommend';
					} else if (!JSON.parse(request.response)["recommended"]) {
						document.querySelector(".recommend-btn").innerHTML = '<i class="icon ion-ios-checkmark-outline"></i>  Recommend';
					}
				} else {
					document.querySelector(".recommend-btn").innerHTML = '<i class="icon ion-ios-checkmark-outline"></i>  E-JS. Try again...';
				}
			}
		}
	}

	// Used to shorten comment details
	let comment_des_storage = [];
	document.querySelectorAll(".comment-details").forEach( des => {
		if (des.innerHTML.length > 5) {
			comment_des = {
				"id": des.dataset.comment_id,
				"comment": des.innerHTML
			};
			comment_des_storage.push(comment_des);
			des.innerHTML = des.innerHTML.slice(0, 20) + "...";
		}
	});

	// Used to show the full comment
	document.querySelectorAll(".comment-option").forEach( des => {
		des.onclick = () => {

			// Check if the comment ID is available
			if (des.dataset.comment_id) {
				
				// Loop the list of shorten comment details
				for (var i = 0; i < comment_des_storage.length; i++) {
					
					// Find the correct comment to show the full comment datail
					if (parseInt(comment_des_storage[i]["id"]) === parseInt(des.dataset.comment_id)) {

						// Loop and find the corrent comment box
						document.querySelectorAll(".comment-details").forEach( new_des => {
							if (new_des.dataset.comment_id === des.dataset.comment_id) {
								new_des.innerHTML = comment_des_storage[i]["comment"];
							}
						});

						des.style.display = "none";
					}
				}
			}
		}
	});

	// Used to remove comments
	document.querySelectorAll("#del_btn").forEach( button => {
		button.onclick = () => {

			const request = new XMLHttpRequest();
			request.open("POST", "/comment");
			const data = new FormData();
			data.append("csrfmiddlewaretoken", document.querySelector("input[name='csrfmiddlewaretoken']").value);
			data.append("content_id", button.dataset.content_id);
			data.append("comment_id", button.dataset.comment_id);
			data.append("user_id", button.dataset.user_id);
			data.append("delete", true);
			request.send(data);
			request.onreadystatechange = () => {
				if (request.readyState === 4 && request.status === 200) {
					if (JSON.parse(request.response)["STATUS"]) {
						document.querySelector("#comment-"+button.dataset.comment_id).style.display = "none";
					} else {
						button.style.color = "red";
					}
				}
			}
		}
	});
	
});
