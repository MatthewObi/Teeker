// Javascript for LEVEL 0 view users

document.addEventListener("DOMContentLoaded", () => {

	// Trigger the choose file input field for profile picture modal
	document.querySelector(".choose-picture-btn").onclick = () => {
		document.querySelector(".choose-picture-input").click();
	}

	// Check the profile picture
    document.querySelector(".choose-picture-input").onchange = () => {
        let image = document.querySelector(".choose-picture-input");
        if (image.files[0].type.match("image.*")) {
            if (image.files && image.files[0]) {

				// Check if the file is a PNG
                if (image.files[0].type == "image/png") {
                    let img = image.files[0].size;
                    let imgsize = img / 1024;
                    if (imgsize <= 2000) {
                        document.querySelector(".choose-picture-btn").innerHTML = "Image: "+image.files[0].name;
                        document.querySelector(".choose-picture-btn").style.backgroundColor = "green";
                        const file = document.querySelector(".choose-picture-input");
                        
                        // Preview image
                        let reader = new FileReader();
                        if (file.files[0].type.match("image.*")) {
                            reader.readAsDataURL(file.files[0]); // convert to base64 string
                        }
                        reader.addEventListener("loadend", () => {
                            document.querySelector(".preview-image-pp").src = reader.result;
                        }, false)
                    } else {
                        document.querySelector(".choose-picture-btn").innerHTML = "Image too large";
                        document.querySelector(".choose-picture-btn").style.backgroundColor = "red";
                        document.querySelector(".choose-picture-input").value = "";
					}
					
				// Check if the file is a JPEG
                } else if (image.files[0].type == "image/jpeg") {
                    let img = image.files[0].size;
                    let imgsize = img / 1024;
                    if (imgsize <= 2000) {
                        document.querySelector(".choose-picture-btn").innerHTML = "Image: "+image.files[0].name;
                        document.querySelector(".choose-picture-btn").style.backgroundColor = "green";
                        const file = document.querySelector(".choose-picture-input");
                        
                        // Preview image
                        let reader = new FileReader();
                        if (file.files[0].type.match("image.*")) {
                            reader.readAsDataURL(file.files[0]); // convert to base64 string
                        }
                        reader.addEventListener("loadend", () => {
                            document.querySelector(".preview-image-pp").src = reader.result;
                        }, false)
                    } else {
                        document.querySelector(".choose-picture-btn").innerHTML = "Image too large";
                        document.querySelector(".choose-picture-btn").style.backgroundColor = "red";
                        document.querySelector(".choose-picture-input").value = "";
                    }
                } else {
                    document.querySelector(".choose-picture-btn").innerHTML = "Image not PNG/JPEG";
                    document.querySelector(".choose-picture-btn").style.backgroundColor = "red";
                    document.querySelector(".choose-picture-input").value = "";
                }
            }
        } else {
            document.querySelector(".choose-picture-btn").innerHTML = "Not Image file.";
            document.querySelector(".choose-picture-btn").style.backgroundColor = "red";
            document.querySelector(".choose-picture-input").value = "";
        }
    }

	// Trigger the choose file input field for banner picture modal
	document.querySelector(".choose-banner-btn").onclick = () => {
		document.querySelector(".choose-banner-input").click();
    }
    
    // Check the banner picture
    document.querySelector(".choose-banner-input").onchange = () => {
        let image = document.querySelector(".choose-banner-input");
        if (image.files[0].type.match("image.*")) {
            if (image.files && image.files[0]) {

				// Check if the file is a PNG
                if (image.files[0].type == "image/png") {
                    let img = image.files[0].size;
                    let imgsize = img / 1024;
                    if (imgsize <= 2000) {
                        document.querySelector(".choose-banner-btn").innerHTML = "Image: "+image.files[0].name;
                        document.querySelector(".choose-banner-btn").style.backgroundColor = "green";
                        const file = document.querySelector(".choose-banner-input");
                        
                        // Preview image
                        let reader = new FileReader();
                        if (file.files[0].type.match("image.*")) {
                            reader.readAsDataURL(file.files[0]); // convert to base64 string
                        }
                        reader.addEventListener("loadend", () => {
                            document.querySelector(".preview-image-bp").src = reader.result;
                        }, false)
                    } else {
                        document.querySelector(".choose-banner-btn").innerHTML = "Image too large";
                        document.querySelector(".choose-banner-btn").style.backgroundColor = "red";
                        document.querySelector(".choose-banner-input").value = "";
					}
					
				// Check if the file is a JPEG
                } else if (image.files[0].type == "image/jpeg") {
                    let img = image.files[0].size;
                    let imgsize = img / 1024;
                    if (imgsize <= 2000) {
                        document.querySelector(".choose-banner-btn").innerHTML = "Image: "+image.files[0].name;
                        document.querySelector(".choose-banner-btn").style.backgroundColor = "green";
                        const file = document.querySelector(".choose-banner-input");
                        
                        // Preview image
                        let reader = new FileReader();
                        if (file.files[0].type.match("image.*")) {
                            reader.readAsDataURL(file.files[0]); // convert to base64 string
                        }
                        reader.addEventListener("loadend", () => {
                            document.querySelector(".preview-image-bp").src = reader.result;
                        }, false)
                    } else {
                        document.querySelector(".choose-banner-btn").innerHTML = "Image too large";
                        document.querySelector(".choose-banner-btn").style.backgroundColor = "red";
                        document.querySelector(".choose-banner-input").value = "";
                    }
                } else {
                    document.querySelector(".choose-banner-btn").innerHTML = "Image not PNG/JPEG";
                    document.querySelector(".choose-banner-btn").style.backgroundColor = "red";
                    document.querySelector(".choose-banner-input").value = "";
                }
            }
        } else {
            document.querySelector(".choose-banner-btn").innerHTML = "Not Image file.";
            document.querySelector(".choose-banner-btn").style.backgroundColor = "red";
            document.querySelector(".choose-banner-input").value = "";
        }
    }
});
