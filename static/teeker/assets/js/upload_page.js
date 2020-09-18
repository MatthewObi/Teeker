// Javascript for Upload Page

document.addEventListener("DOMContentLoaded", () => {

	// Get the selected post type
	document.querySelector("#post_type_selector").onchange = () => {
		if (document.querySelector("#post_type_selector").value === "12") {
			document.querySelectorAll(".col-box-instagram").forEach(postbox => {
				postbox.style.display = "inline";
			});
			document.querySelectorAll(".col-box-youtube").forEach(postbox => {
				postbox.style.display = "none";
			});
			document.querySelectorAll(".col-box-vimeo").forEach(postbox => {
				postbox.style.display = "none";
			});
			document.querySelectorAll(".col-box-soundcloud").forEach(postbox => {
				postbox.style.display = "none";
			});
			document.querySelectorAll(".col-box-spotify").forEach(postbox => {
				postbox.style.display = "none";
			});

		} else if (document.querySelector("#post_type_selector").value === "13") {
			document.querySelectorAll(".col-box-instagram").forEach(postbox => {
				postbox.style.display = "none";
			});
			document.querySelectorAll(".col-box-youtube").forEach(postbox => {
				postbox.style.display = "inline";
			});
			document.querySelectorAll(".col-box-vimeo").forEach(postbox => {
				postbox.style.display = "none";
			});
			document.querySelectorAll(".col-box-soundcloud").forEach(postbox => {
				postbox.style.display = "none";
			});
			document.querySelectorAll(".col-box-spotify").forEach(postbox => {
				postbox.style.display = "none";
			});

		} else if (document.querySelector("#post_type_selector").value === "14") {
			document.querySelectorAll(".col-box-instagram").forEach(postbox => {
				postbox.style.display = "none";
			});
			document.querySelectorAll(".col-box-youtube").forEach(postbox => {
				postbox.style.display = "none";
			});
			document.querySelectorAll(".col-box-vimeo").forEach(postbox => {
				postbox.style.display = "inline";
			});
			document.querySelectorAll(".col-box-soundcloud").forEach(postbox => {
				postbox.style.display = "none";
			});
			document.querySelectorAll(".col-box-spotify").forEach(postbox => {
				postbox.style.display = "none";
			});

		} else if (document.querySelector("#post_type_selector").value === "15") {
			document.querySelectorAll(".col-box-instagram").forEach(postbox => {
				postbox.style.display = "none";
			});
			document.querySelectorAll(".col-box-youtube").forEach(postbox => {
				postbox.style.display = "none";
			});
			document.querySelectorAll(".col-box-vimeo").forEach(postbox => {
				postbox.style.display = "none";
			});
			document.querySelectorAll(".col-box-soundcloud").forEach(postbox => {
				postbox.style.display = "inline";
			});
			document.querySelectorAll(".col-box-spotify").forEach(postbox => {
				postbox.style.display = "none";
			});

		} else if (document.querySelector("#post_type_selector").value === "16") {
			document.querySelectorAll(".col-box-instagram").forEach(postbox => {
				postbox.style.display = "none";
			});
			document.querySelectorAll(".col-box-youtube").forEach(postbox => {
				postbox.style.display = "none";
			});
			document.querySelectorAll(".col-box-vimeo").forEach(postbox => {
				postbox.style.display = "none";
			});
			document.querySelectorAll(".col-box-soundcloud").forEach(postbox => {
				postbox.style.display = "none";
			});
			document.querySelectorAll(".col-box-spotify").forEach(postbox => {
				postbox.style.display = "inline";
			});
		}
	}

	// INSTAGRAM EMBED
	// Used to extract the part of the URL to make the embed
	buildInstagramEmbedLink = (media_id) => {
		var link = "";
		for (var i = 0; media_id.length > i; i++) {
			if (media_id[i] === "?") {
				break;
			}
			link += media_id[i];
		}
		return link + "embed";
	}
	document.querySelector("#instagram_input").onchange = () => {
		document.querySelector("#instagram_embed").src = buildInstagramEmbedLink(document.querySelector("#instagram_input").value);
	}

	// YOUTUBE EMBED
	// Used to extract the part of the URL to make the embed
	buildYoutubeEmbedLink = (media_id) => {
		var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\??v?=?))([^#\&\?]*).*/;
		var match = media_id.match(regExp);
		return (match&&match[7].length==11)? match[7] : false;
	}
	document.querySelector("#youtube_input").onchange = () => {
		document.querySelector("#youtube_embed").src = "https://www.youtube.com/embed/"+buildYoutubeEmbedLink(document.querySelector("#youtube_input").value);
	}

	// VIMEO EMBED
	// Used to extract the part of the URL to make the embed
	buildVimeoEmbedLink = (media_id) => {
		var regExp = /https?:\/\/(?:www\.|player\.)?vimeo.com\/(?:channels\/(?:\w+\/)?|groups\/([^\/]*)\/videos\/|album\/(\d+)\/video\/|video\/|)(\d+)(?:$|\/|\?)/;
		var match = media_id.match(regExp);
		return match[3];
	}
	document.querySelector("#vimeo_input").onchange = () => {
		document.querySelector("#vimeo_embed").src = "https://player.vimeo.com/video/"+buildVimeoEmbedLink(document.querySelector("#vimeo_input").value);
	}

	// SOUNDCLOUD EMBED
	// Used to extract the part of the URL to make the embed
	document.querySelector("#soundcloud_input").onchange = () => {
		document.querySelector("#preview_soundcloud").innerHTML = document.querySelector("#soundcloud_input").value;
	}

	// SPOTIFY EMBED
	// Used to extract the part of the URL to make the embed
	document.querySelector("#spotify_input").onchange = () => {
		document.querySelector("#preview_spotify").innerHTML = document.querySelector("#spotify_input").value;
	}
});
