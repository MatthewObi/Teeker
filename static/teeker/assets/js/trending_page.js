// Javascript for Trending page

let flag = true
document.addEventListener("DOMContentLoaded", () => {

	// Control for the VOTE btn, Copy link and recommend
	update_content_controls = () => {
		// Trigger for when the up vote button is pressed
		document.querySelectorAll(".up-vote-btn").forEach(button => {
			button.onclick = () => {
				const request = new XMLHttpRequest();
				request.open("POST", "/votesystem");
				const data = new FormData();
				data.append("csrfmiddlewaretoken", document.querySelector("input[name='csrfmiddlewaretoken']").value);
				data.append("content_id", button.dataset.content_id);
				data.append("votestatus", 1);
				request.send(data);
				request.onreadystatechange = () => {
					if (request.readyState === 4 && request.status === 200) {
						if (JSON.parse(request.response)["STATUS"]) {
							document.querySelectorAll(".fire-avg-number-696969").forEach(fire_element => {
								if (fire_element.dataset.content_id === button.dataset.content_id) {
									fire_element.innerHTML = JSON.parse(request.response)["FIRE"];
									fire_element.setAttribute("title", "UP: "+JSON.parse(request.response)["UP"]+" DOWN: "+JSON.parse(request.response)["DOWN"]);
								}
							});
						} else {
							document.querySelectorAll(".fire-avg-number-696969").forEach(fire_element => {
								if (fire_element.dataset.content_id === button.dataset.content_id) {
									fire_element.innerHTML = "N/A";
									fire_element.setAttribute("title", "UP: N/A DOWN: N/A");
								}
							});
						}
					}
				}
			}
		});

		// Trigger for when the down vote button is pressed
		document.querySelectorAll(".down-vote-btn").forEach(button => {
			button.onclick = () => {
				const request = new XMLHttpRequest();
				request.open("POST", "/votesystem");
				const data = new FormData();
				data.append("csrfmiddlewaretoken", document.querySelector("input[name='csrfmiddlewaretoken']").value);
				data.append("content_id", button.dataset.content_id);
				data.append("votestatus", 0);
				request.send(data);
				request.onreadystatechange = () => {
					if (request.readyState === 4 && request.status === 200) {
						if (JSON.parse(request.response)["STATUS"]) {
							document.querySelectorAll(".fire-avg-number-696969").forEach(fire_element => {
								if (parseInt(fire_element.dataset.content_id) === parseInt(button.dataset.content_id)) {
									fire_element.innerHTML = JSON.parse(request.response)["FIRE"];
									fire_element.setAttribute("title", "UP: "+JSON.parse(request.response)["UP"]+" DOWN: "+JSON.parse(request.response)["DOWN"]);
								}
							});
						} else {
							document.querySelectorAll(".fire-avg-number-696969").forEach(fire_element => {
								if (parseInt(fire_element.dataset.content_id) === parseInt(button.dataset.content_id)) {
									fire_element.innerHTML = "N/A";
									fire_element.setAttribute("title", "UP: N/A DOWN: N/A");
								}
							});
						}
					}
				}
			}
		});

		// Trigger for Copy link button from dropdown Menu to the clipboard
		document.querySelectorAll(".copy-link-btn").forEach(button => {
			button.onclick = () => {
				const el = document.createElement("textarea");
				el.value = location.hostname+"/view="+button.dataset.content;
				el.setAttribute("readonly", "");
				el.style.position = "absolute";
				el.style.left = "-9999px";
				document.body.appendChild(el);
				el.select();
				document.execCommand("copy");
				document.body.removeChild(el);
			}
		});

		// Place content in the recommended list of the user
		document.querySelectorAll(".recommend-btn").forEach(button => {
			button.onclick = () => {
				const request = new XMLHttpRequest();
				request.open("POST", "recommend_sys");
				const data = new FormData();
				data.append("csrfmiddlewaretoken", document.querySelector("input[name='csrfmiddlewaretoken']").value);
				data.append("option", "recommend");
				data.append("content", button.dataset.content);
				request.send(data);
				request.onreadystatechange = () => {
					if (request.status === 200 && request.readyState === 4) {
						if (JSON.parse(request.response)["STATUS"]) {
							if (JSON.parse(request.response)["recommended"]) {
								button.innerHTML = '<i class="fas fa-minus"></i>  Unrecommend';
							} else if (!JSON.parse(request.response)["recommended"]) {
								button.innerHTML = '<i class="fas fa-plus"></i>  Recommend';
							}
						} else {
							button.innerHTML = '<i class="icon ion-ios-checkmark-outline"></i>  E-JS. Try again...';
						}
					}
				}
			}
		});
	}
	// Trigger a control update
	update_content_controls();

	// Get more content when scroll to the bottom
	window.onscroll = () => {
		if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 5) {

			// Try preventing duplicate requests
			if (flag) {

				// Set the flag to false till request is fully completed
				flag = false;

				// Get the last content id on the feed
				let last_content = 0;
				document.querySelectorAll("#content-box-images").forEach(item => {
					last_content = item.dataset.content_id;
				});

				// Activate the loading gif
				document.querySelector("#loading_gif").classList.toggle("d-none", false);

				const request = new XMLHttpRequest();
				request.open("GET", "/homefeed?last_id="+last_content, true);
				request.send(null);
				request.onreadystatechange = () => {
					if (request.status === 200 && request.readyState === 4) {
						if (JSON.parse(request.response)["content_data"]) {
							
							for (let i = 0; i <= JSON.parse(request.response)["content_data"].length; i++) {
								
								if (JSON.parse(request.response)["content_data"][i]) {
									
									if (JSON.parse(request.response)["content_data"][i]["content_type"] === "instagram") {
										shared_link = `<div class="col" id="preview-instagram"><iframe src="`+JSON.parse(request.response)["content_data"][i]["shared_link"]+`" allowtransparency="true" frameborder="0" scrolling="no" width="100%" height="400"></iframe></div>`;
									} else if (JSON.parse(request.response)["content_data"][i]["content_type"] === "youtube") {
										shared_link = `<div class="col" id="preview-youtube"><iframe allowfullscreen="" frameborder="0" src="`+JSON.parse(request.response)["content_data"][i]["shared_link"]+`" width="100%" height="215"></iframe></div>`;
									} else if (JSON.parse(request.response)["content_data"][i]["content_type"] === "vimeo") {
										shared_link = `<div class="col" id="preview-vimeo"><iframe allowfullscreen="" frameborder="0" src="`+JSON.parse(request.response)["content_data"][i]["shared_link"]+`" width="100%" height="215"></iframe></div>`;
									} else if (JSON.parse(request.response)["content_data"][i]["content_type"] === "soundcloud") {
										shared_link = `<div class="col" id="preview-soundcloud"><div id="soundcloud_content">`+JSON.parse(request.response)["content_data"][i]["shared_link"]+`</div></div>`;
									} else if (JSON.parse(request.response)["content_data"][i]["content_type"] === "spotify") {
										shared_link = `<div class="col" id="preview-spotify"><div id="spotify_content">`+JSON.parse(request.response)["content_data"][i]["shared_link"]+`</div></div>`;
									}

									if (JSON.parse(request.response)["content_data"][i]["recommended_status"]) {
										recommended_status = `<i class="fas fa-minus"></i> Unrecommend`
									} else {
										recommended_status = `<i class="fas fa-plus"></i> Recommend`
									}

									content_HTML_build = `<div class="row content-owner-details" id="content-owner-info-5">
																	<div class="col-10 col-sm-9 col-md-9 col-lg-9 col-xl-9 d-flex flex-row justify-content-start align-items-center"><a class="d-flex flex-row justify-content-start align-items-center content-box-links" href="/TK/view=`+JSON.parse(request.response)["content_data"][i]["owner"]+`"><img class="rounded-circle" src="`+JSON.parse(request.response)["content_data"][i]["profile_picture"]+`" width="50px" height="50px" alt="profile_picture"><p class="text-white username-content-box">&nbsp;`+JSON.parse(request.response)["content_data"][i]["username"]+`&nbsp;</p></a></div>
																	<div
																		class="col-2 col-sm-3 col-md-3 col-lg-3 col-xl-3 d-flex justify-content-end">
																		<div class="dropleft"><button class="btn btn-sm dropdown-toggle little-dropdown-dots" data-toggle="dropdown" aria-expanded="false" type="button">...</button>
																			<div class="dropdown-menu" role="menu"><a class="dropdown-item dropdown-menu-options copy-link-btn" role="presentation" data-content="`+JSON.parse(request.response)["content_data"][i]["pk"]+`"><i class="fas fa-link" ></i> Copy Link</a><a class="dropdown-item dropdown-menu-options recommend-btn" role="presentation" data-content="`+JSON.parse(request.response)["content_data"][i]["pk"]+`">`+recommended_status+`</a></div>
																		</div>
																</div>
															</div>
															<div class="row d-flex flex-column justify-content-center" id="content-preview-5">
																`+shared_link+`
															</div>
															<div class="row" id="content-details-5">
																<div class="col">
																	<div class="row">
																		<div class="col">
																			<a class="content-box-links" href="/view=`+JSON.parse(request.response)["content_data"][i]["pk"]+`">
																				<h5 class="text-white">`+JSON.parse(request.response)["content_data"][i]["title"]+`</h5>
																			</a>
																		</div>
																	</div>
																	<div class="row">
																		<div class="col-xl-4">
																			<div class="btn-group" role="group"><button class="btn content-vote-btn up-vote-btn" type="button" data-content_id="`+JSON.parse(request.response)["content_data"][i]["pk"]+`"><i class="fa fa-chevron-up"></i></button><button class="btn btn-lg content-vote-btn down-vote-btn" type="button" data-content_id="`+JSON.parse(request.response)["content_data"][i]["pk"]+`"><i class="fas fa-angle-down"></i></button></div>
																		</div>
																		<div class="col d-flex flex-row justify-content-start align-items-center justify-content-xl-end"><i class="fas fa-fire content-fire-icon"></i>
																			<h5 class="text-break text-white fire-avg-number-696969" data-content_id="`+JSON.parse(request.response)["content_data"][i]["pk"]+`" style="margin-left: 5px;">`+JSON.parse(request.response)["content_data"][i]["fire"]+`</h5>
																		</div>
																	</div>
																	<div class="row">
																		<div class="col">
																			<p class="text-muted content-date">Date: `+JSON.parse(request.response)["content_data"][i]["date"]+`</p>
																		</div>
																	</div>
																</div>
															</div>`;

									if (content_HTML_build) {
										const html_o = document.createElement("div");
										html_o.setAttribute("class", "col-11 col-sm-5 col-md-5 col-lg-4 col-xl-3 col-content-box");
										//html_o.setAttribute("data-aos", "fade-up"); // Breaks the phone size screen content (Makes them invisible)
										html_o.setAttribute("data-aos-once", "true");
										html_o.setAttribute("data-content_id", JSON.parse(request.response)["content_data"][i]["pk"]);
										html_o.setAttribute("id", "content-box-images");
										html_o.innerHTML = content_HTML_build;
										document.querySelector("#content-row-holder").append(html_o);
									}
								}
							}
							// Set flag to true to allow another loading
							flag = true;

							// Trigger a control update
							update_content_controls();

							// De-activate the loading gif
							if (!document.querySelector("#loading_gif").classList.toggle("d-none")) {
								document.querySelector("#loading_gif").classList.toggle("d-none", true);
							}

						}
					} else {

						// Set a timer to set the flag to true
						setTimeout(() => {
							flag = true;
						}, 1000);

						// De-activate the loading gif
						if (!document.querySelector("#loading_gif").classList.toggle("d-none")) {
							document.querySelector("#loading_gif").classList.toggle("d-none", true);
						}
					}
				}
			}
		}
	}
});