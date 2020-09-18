// Javascript for the Account page

// Show the Home content
document.querySelector("#account_home_row").className += " d-none";

// Hide the Recommended content
document.querySelector("#account_recommended_row").className += " d-none";

// Hide the About me content
document.querySelector("#account_aboutme_row").className += " d-none";

document.addEventListener("DOMContentLoaded", () => {

	// Show the home content
	document.querySelector("#account_home_row").classList.toggle("d-none", false);
	document.querySelector("#account_home_row").classList.toggle("d-flex", true);

	// Hide the rest of the row content
	document.querySelector("#account_recommended_row").classList.toggle("d-none", true);
	document.querySelector("#account_recommended_row").classList.toggle("d-flex", false);
	document.querySelector("#account-recommended-btn").classList.toggle("active", false);
	document.querySelector("#account-aboutme-btn").classList.toggle("active", false);

	// Function to see which contents to display
	display_content = (show_section) => {

		// Show the Home content
		if (show_section === 0) {
			document.querySelector("#account_home_row").classList.toggle("d-none", false);
			document.querySelector("#account_home_row").classList.toggle("d-flex", true);
			document.querySelector("#account-home-btn").classList.toggle("active", true);
		} else {
			document.querySelector("#account_home_row").classList.toggle("d-none", true);
			document.querySelector("#account_home_row").classList.toggle("d-flex", false);
			document.querySelector("#account-home-btn").classList.toggle("active", false);
		}
			
		// Hide the Recommended content
		if (show_section === 2) {
			document.querySelector("#account_recommended_row").classList.toggle("d-none", false);
			document.querySelector("#account_recommended_row").classList.toggle("d-flex", true);
			document.querySelector("#account-recommended-btn").classList.toggle("active", true);
		} else {
			document.querySelector("#account_recommended_row").classList.toggle("d-none", true);
			document.querySelector("#account_recommended_row").classList.toggle("d-flex", false);
			document.querySelector("#account-recommended-btn").classList.toggle("active", false);
		}

		// Hide the About me content
		if (show_section === 3) {
			document.querySelector("#account_aboutme_row").classList.toggle("d-none", false);
			document.querySelector("#account-aboutme-btn").classList.toggle("active", true);
		} else {
			document.querySelector("#account_aboutme_row").classList.toggle("d-none", true);
			document.querySelector("#account-aboutme-btn").classList.toggle("active", false);
		}
	}
	
	// When the Home button is pressed hide all other content and display only the home content
	document.querySelector("#account-home-btn").onclick = () => {
		display_content(0);
	}

	// When the recommended button is pressed hide all other content and display only the recommended content
	document.querySelector("#account-recommended-btn").onclick = () => {
		display_content(2);
	}

	// When the about me button is pressed hide all other content and display only the about me content
	document.querySelector("#account-aboutme-btn").onclick = () => {
		display_content(3);
	}

	// Attempt to chase the user
	if (document.querySelector(".chase-btn")) {
		document.querySelector(".chase-btn").onclick = () => {
			const request = new XMLHttpRequest();
			request.open("POST", "/TK/view="+document.querySelector(".chase-btn").dataset.user_id);
			const data = new FormData();
			data.append("csrfmiddlewaretoken", document.querySelector("input[name='csrfmiddlewaretoken']").value);
			data.append("user_id", document.querySelector(".chase-btn").dataset.user_id);
			data.append("chase", true);
			request.send(data);
			request.onreadystatechange = () => {
				if (request.readyState === 4 && request.status === 200) {
					if (JSON.parse(request.response)["STATUS"]) {
						if (!JSON.parse(request.response)["CHASING"]) {
							document.querySelector(".chase-btn").classList.toggle("chasing-active", false);
							document.querySelector(".chase-btn").classList.toggle("chasing-deactive", true);
							document.querySelector(".chase-btn").innerHTML = "CHASE";
						} else if (JSON.parse(request.response)["CHASING"]) {
							document.querySelector(".chase-btn").classList.toggle("chasing-active", true);
							document.querySelector(".chase-btn").classList.toggle("chasing-deactive", false);
							document.querySelector(".chase-btn").innerHTML = "CHASING";
						}
					}
				}
			}
		}
	}

	// For the Report Modal
	document.querySelectorAll(".report-check-box").forEach( check_btn => {
		check_btn.onclick = () => {

			// For blocking the user
			if (parseInt(check_btn.dataset.reportcheck) === 1 && check_btn.checked) {
				document.querySelector("#form_g_block_user").classList.toggle("d-none", false);
			} else {
				document.querySelector("#formCheck-1").checked = false;
				document.querySelector("#form_g_block_user").classList.toggle("d-none", true);
			}

			// For reporting the user's banner
			if (parseInt(check_btn.dataset.reportcheck) === 2 && check_btn.checked) {
				document.querySelector("#form_g_report_banner").classList.toggle("d-none", false);
			} else {
				document.querySelector("#formCheck-2").checked = false;
				document.querySelector("#form_g_report_banner").classList.toggle("d-none", true);
			}

			// For reporting the user's profile picture
			if (parseInt(check_btn.dataset.reportcheck) === 3 && check_btn.checked) {
				document.querySelector("#form_g_report_pp").classList.toggle("d-none", false);
			} else {
				document.querySelector("#formCheck-3").checked = false;
				document.querySelector("#form_g_report_pp").classList.toggle("d-none", true);
			}

			// For reporting the user
			if (parseInt(check_btn.dataset.reportcheck) === 4 && check_btn.checked) {
				document.querySelector("#form_g_report_user").classList.toggle("d-none", false);
			} else {
				document.querySelector("#formCheck-4").checked = false;
				document.querySelector("#form_g_report_user").classList.toggle("d-none", true);
			}
		}
	})

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
	}
	// Trigger a control update
	update_content_controls();
	
	// Get more content when scroll to the bottom
	let flag = true;
	window.onscroll = () => {
		if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 5) {

			// Try preventing duplicate requests
			if (flag) {
				
				// Determine what content section to get
				if (!document.querySelector("#account_home_row").classList.contains("d-none") && document.querySelector("#account_recommended_row").classList.contains("d-none")) {
					
					// Set the flag to false till request is fully completed
					flag = false;

					// Activate the loading gif
					document.querySelector("#loading_gif").classList.toggle("d-none", false);

					// Get the last content id on the feed
					let last_content = 0;
					document.querySelectorAll("#content-box-images").forEach(item => {
						last_content = item.dataset.content_id;
					});

					const request = new XMLHttpRequest();
					request.open("GET", "/TK/viewposts?user="+document.querySelector(".username").dataset.user_id+"&lastid="+last_content+"&section=home");
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

										content_HTML_build = `<div class="row content-owner-details" id="content-owner-info">
																	<div class="col-10 col-sm-9 col-md-9 col-lg-9 col-xl-9 d-flex flex-row justify-content-start align-items-center"><a class="d-flex flex-row justify-content-start align-items-center content-box-links" href="/TK/view=`+JSON.parse(request.response)["content_data"][i]["owner"]+`"><img class="rounded-circle" src="`+JSON.parse(request.response)["content_data"][i]["profile_picture"]+`" width="50px" height="50px" alt="profile_picture"><p class="text-white username-content-box">&nbsp;`+JSON.parse(request.response)["content_data"][i]["username"]+`&nbsp;</p></a></div>
																	<div class="col-2 col-sm-3 col-md-3 col-lg-3 col-xl-3 d-flex justify-content-end">
																		<div class="dropleft"><button class="btn btn-sm dropdown-toggle little-dropdown-dots" data-toggle="dropdown" aria-expanded="false" type="button">...</button>
																			<div class="dropdown-menu" role="menu"><a class="dropdown-item dropdown-menu-options copy-link-btn" role="presentation" data-content="`+JSON.parse(request.response)["content_data"][i]["pk"]+`">Copy Link</a><a class="dropdown-item dropdown-menu-options recommend-btn" role="presentation" data-content="`+JSON.parse(request.response)["content_data"][i]["pk"]+`">Recommend</a></div>
																		</div>
																</div>
															</div>
															<div class="row d-flex flex-column justify-content-center" id="content-preview">
																`+shared_link+`
															</div>
															<div class="row" id="content-details">
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
																			<div class="btn-group" role="group">
																				<button class="btn content-vote-btn up-vote-btn" type="button" data-content_id="`+JSON.parse(request.response)["content_data"][i]["pk"]+`">
																					<i class="fa fa-chevron-up"></i>
																				</button>
																				<button class="btn btn-lg content-vote-btn down-vote-btn" type="button" data-content_id="`+JSON.parse(request.response)["content_data"][i]["pk"]+`">
																					<i class="fas fa-angle-down"></i>
																				</button>
																			</div>
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
															</div>
														</div>`;

										if (content_HTML_build) {
											const html_o = document.createElement("div");
											html_o.className = "col-11 col-sm-5 col-md-5 col-lg-4 col-xl-3 col-content-box";
											//html_o.setAttribute("data-aos", "fade-up"); // Breaks the phone size screen content (Makes them invisible)
											html_o.setAttribute("data-aos-once", "true");
											html_o.setAttribute("data-content_id", JSON.parse(request.response)["content_data"][i]["pk"]);
											html_o.setAttribute("id", "content-box-images");
											html_o.innerHTML = content_HTML_build;
											document.querySelector("#account_home_row").append(html_o);
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

				} else if (!document.querySelector("#account_recommended_row").classList.contains("d-none") && document.querySelector("#account_home_row").classList.contains("d-none")) {
					
					// Set the flag to false till request is fully completed
					flag = false;

					// Activate the loading gif
					document.querySelector("#loading_gif").classList.toggle("d-none", false);
					
					// Get the last content id on the feed
					let last_content = 0;
					document.querySelectorAll("#content-box-images-1").forEach(item => {
						last_content = item.dataset.content_id;
					});

					// Get all the id's of all the content already in the feed
					let posted_content = [];
					document.querySelectorAll("#content-box-images-1").forEach(item => {
						posted_content.push(item.dataset.content_id);
					})

					const request = new XMLHttpRequest();
					request.open("GET", "/TK/viewposts?user="+document.querySelector(".username").dataset.user_id+"&lastid="+last_content+"&section=recommended&list="+JSON.stringify(posted_content));
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

										content_HTML_build = `<div class="row content-owner-details" id="content-owner-info">
																	<div class="col-10 col-sm-9 col-md-9 col-lg-9 col-xl-9 d-flex flex-row justify-content-start align-items-center"><a class="d-flex flex-row justify-content-start align-items-center content-box-links" href="/TK/view=`+JSON.parse(request.response)["content_data"][i]["owner"]+`"><img class="rounded-circle" src="`+JSON.parse(request.response)["content_data"][i]["profile_picture"]+`" width="50px" height="50px" alt="profile_picture"><p class="text-white username-content-box">&nbsp;`+JSON.parse(request.response)["content_data"][i]["username"]+`&nbsp;</p></a></div>
																	<div class="col-2 col-sm-3 col-md-3 col-lg-3 col-xl-3 d-flex justify-content-end">
																		<div class="dropleft"><button class="btn btn-sm dropdown-toggle little-dropdown-dots" data-toggle="dropdown" aria-expanded="false" type="button">...</button>
																			<div class="dropdown-menu" role="menu"><a class="dropdown-item dropdown-menu-options copy-link-btn" role="presentation" data-content="`+JSON.parse(request.response)["content_data"][i]["pk"]+`">Copy Link</a><a class="dropdown-item dropdown-menu-options recommend-btn" role="presentation" data-content="`+JSON.parse(request.response)["content_data"][i]["pk"]+`">Recommend</a></div>
																		</div>
																</div>
															</div>
															<div class="row d-flex flex-column justify-content-center" id="content-preview">
																`+shared_link+`
															</div>
															<div class="row" id="content-details">
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
																			<div class="btn-group" role="group">
																				<button class="btn content-vote-btn up-vote-btn" type="button" data-content_id="`+JSON.parse(request.response)["content_data"][i]["pk"]+`">
																					<i class="fa fa-chevron-up"></i>
																				</button>
																				<button class="btn btn-lg content-vote-btn down-vote-btn" type="button" data-content_id="`+JSON.parse(request.response)["content_data"][i]["pk"]+`">
																					<i class="fas fa-angle-down"></i>
																				</button>
																			</div>
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
															</div>
														</div>`;

										if (content_HTML_build) {
											const html_o = document.createElement("div");
											html_o.className = "col-11 col-sm-5 col-md-5 col-lg-4 col-xl-3 col-content-box";
											//html_o.setAttribute("data-aos", "fade-up"); // Breaks the phone size screen content (Makes them invisible)
											html_o.setAttribute("data-aos-once", "true");
											html_o.setAttribute("data-content_id", JSON.parse(request.response)["content_data"][i]["pk"]);
											html_o.setAttribute("id", "content-box-images-1");
											html_o.innerHTML = content_HTML_build;
											document.querySelector("#account_recommended_row").append(html_o);
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
	}
});