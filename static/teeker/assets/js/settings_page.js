// Javascript for Settings Page

document.addEventListener("DOMContentLoaded", () => {

    // Toggle the Edit account details form
    document.querySelector("#edit_acc_details").onclick = () => {
        if (document.querySelector(".form-update-account-details").style.display === "none") {
            document.querySelector(".form-update-account-details").style.display = "inline";
        } else {
            document.querySelector(".form-update-account-details").style.display = "none";
        }
    }

    // Delete the Social Media link
    document.querySelectorAll("#delete_social_media").forEach( button => {
        button.onclick = () => {
            const request = new XMLHttpRequest();
            request.open("POST", "/settings=removesocial");
            const data = new FormData();
            data.append("csrfmiddlewaretoken", document.querySelector("input[name='csrfmiddlewaretoken']").value);
            data.append("social_media_id", button.dataset.social_media_id);
            request.send(data);
            document.querySelector("#del_"+button.dataset.social_media_id).innerHTML = "";
            document.querySelector("#del_"+button.dataset.social_media_id).style.display = "none";
        }
    });

    // Toggle the change password form
    document.querySelector("#change_pwd").onclick = () => {
        if (document.querySelector(".form-change-pwd").style.display === "none") {
            document.querySelector(".form-change-pwd").style.display = "inline";
        } else {
            document.querySelector(".form-change-pwd").style.display = "none";
        }
    }

    // Toggle the change email form
    document.querySelector("#change_email").onclick = () => {
        if (document.querySelector(".form-change-email").style.display === "none") {
            document.querySelector(".form-change-email").style.display = "inline";
        } else {
            document.querySelector(".form-change-email").style.display = "none";
        }
    }

    // Trigger the choose a file input for the profile picture
    document.querySelector("#upload_new_pp").onclick = () => {
        document.querySelector(".file-input-profile-picture").click();
    }

    // Check the profile picture
    document.querySelector(".file-input-profile-picture").onchange = () => {
        var image = document.querySelector(".file-input-profile-picture");
        if (image.files[0].type.match("image.*")) {
            if (image.files && image.files[0]) {
                if (image.files[0].type == "image/png") {
                    var img = image.files[0].size;
                    var imgsize = img / 1024;
                    if (imgsize <= 2000) {
                        document.querySelector("#upload_new_pp").innerHTML = "Image: "+image.files[0].name;
                        document.querySelector("#upload_new_pp").style.backgroundColor = "green";
                        const file = document.querySelector(".file-input-profile-picture");
                        // Preview image
                        var reader = new FileReader();
                        if (file.files[0].type.match("image.*")) {
                            reader.readAsDataURL(file.files[0]); // convert to base64 string
                        }
                        reader.addEventListener("loadend", () => {
                            document.querySelector("#preview_pp").src = reader.result;
                        }, false)
                    } else {
                        document.querySelector("#upload_new_pp").innerHTML = "Image too large";
                        document.querySelector("#upload_new_pp").style.backgroundColor = "red";
                        document.querySelector(".file-input-profile-picture").value = "";
                    }
                } else if (image.files[0].type == "image/jpeg") {
                    var img = image.files[0].size;
                    var imgsize = img / 1024;
                    if (imgsize <= 2000) {
                        document.querySelector("#upload_new_pp").innerHTML = "Image: "+image.files[0].name;
                        document.querySelector("#upload_new_pp").style.backgroundColor = "green";
                        const file = document.querySelector(".file-input-profile-picture");
                        // Preview image
                        var reader = new FileReader();
                        if (file.files[0].type.match("image.*")) {
                            reader.readAsDataURL(file.files[0]); // convert to base64 string
                        }
                        reader.addEventListener("loadend", () => {
                            document.querySelector("#preview_pp").src = reader.result;
                        }, false)
                    } else {
                        document.querySelector("#upload_new_pp").innerHTML = "Image too large";
                        document.querySelector("#upload_new_pp").style.backgroundColor = "red";
                        document.querySelector(".file-input-profile-picture").value = "";
                    }
                } else {
                    document.querySelector("#upload_new_pp").innerHTML = "Image not PNG/JPEG";
                    document.querySelector("#upload_new_pp").style.backgroundColor = "red";
                    document.querySelector(".file-input-profile-picture").value = "";
                }
            }
        } else {
            document.querySelector("#upload_new_pp").innerHTML = "Not Image file.";
            document.querySelector("#upload_new_pp").style.backgroundColor = "red";
            document.querySelector(".file-input-profile-picture").value = "";
        }
    }

    // Trigger the choose a file input for the banner picture
    document.querySelector("#upload_new_bp").onclick = () => {
        document.querySelector(".file-input-banner-picture").click();
    }

    // Check the banner picture
    document.querySelector(".file-input-banner-picture").onchange = () => {
        var image = document.querySelector(".file-input-banner-picture");
        if (image.files[0].type.match("image.*")) {
            if (image.files && image.files[0]) {
                if (image.files[0].type == "image/png") {
                    var img = image.files[0].size;
                    var imgsize = img / 1024;
                    if (imgsize <= 2000) {
                        document.querySelector("#upload_new_bp").innerHTML = "Image: "+image.files[0].name;
                        document.querySelector("#upload_new_bp").style.backgroundColor = "green";
                        const file = document.querySelector(".file-input-banner-picture");
                        // Preview image
                        var reader = new FileReader();
                        if (file.files[0].type.match("image.*")) {
                            reader.readAsDataURL(file.files[0]); // convert to base64 string
                        }
                        reader.addEventListener("loadend", () => {
                            document.querySelector("#preview_bp").src = reader.result;
                        }, false)
                    } else {
                        document.querySelector("#upload_new_bp").innerHTML = "Image too large";
                        document.querySelector("#upload_new_bp").style.backgroundColor = "red";
                        document.querySelector(".file-input-banner-picture").value = "";
                    }
                } else if (image.files[0].type == "image/jpeg") {
                    var img = image.files[0].size;
                    var imgsize = img / 1024;
                    if (imgsize <= 2000) {
                        document.querySelector("#upload_new_bp").innerHTML = "Image: "+image.files[0].name;
                        document.querySelector("#upload_new_bp").style.backgroundColor = "green";
                        const file = document.querySelector(".file-input-banner-picture");
                        // Preview image
                        var reader = new FileReader();
                        if (file.files[0].type.match("image.*")) {
                            reader.readAsDataURL(file.files[0]); // convert to base64 string
                        }
                        reader.addEventListener("loadend", () => {
                            document.querySelector("#preview_bp").src = reader.result;
                        }, false)
                    } else {
                        document.querySelector("#upload_new_bp").innerHTML = "Image too large";
                        document.querySelector("#upload_new_bp").style.backgroundColor = "red";
                        document.querySelector(".file-input-banner-picture").value = "";
                    }
                } else {
                    document.querySelector("#upload_new_bp").innerHTML = "Image not PNG/JPEG";
                    document.querySelector("#upload_new_bp").style.backgroundColor = "red";
                    document.querySelector(".file-input-banner-picture").value = "";
                }
            }
        } else {
            document.querySelector("#upload_new_bp").innerHTML = "Not Image file.";
            document.querySelector("#upload_new_bp").style.backgroundColor = "red";
            document.querySelector(".file-input-banner-picture").value = "";
        }
    }

    // Update the switches (Privacy and Notifications)
    if (document.querySelector("#formCheck-2").dataset.current_state === "True") {
        document.querySelector("#formCheck-2").checked = true;
    } else if (document.querySelector("#formCheck-2").dataset.current_state === "False") {
        document.querySelector("#formCheck-2").checked = false;
    } else {
        document.querySelector("#formCheck-2").disabled = true;
    }
    if (document.querySelector("#formCheck-3").dataset.current_state === "True") {
        document.querySelector("#formCheck-3").checked = true;
    } else if (document.querySelector("#formCheck-3").dataset.current_state === "False") {
        document.querySelector("#formCheck-3").checked = false;
    } else {
        document.querySelector("#formCheck-3").disabled = true;
    }
    
    // Toogles for switches (Privacy and Notifications)
    document.querySelector("#formCheck-2").onchange = () => {
        const request = new XMLHttpRequest();
        request.open("POST", "/settings=toggle");
        const data = new FormData();
        data.append("csrfmiddlewaretoken", document.querySelector("input[name='csrfmiddlewaretoken']").value);
        data.append("toggle_switch", "formCheck-2");
        data.append("switch", document.querySelector("#formCheck-2").checked);
        request.send(data);
    }
    document.querySelector("#formCheck-3").onchange = () => {
        const request = new XMLHttpRequest();
        request.open("POST", "/settings=toggle");
        const data = new FormData();
        data.append("csrfmiddlewaretoken", document.querySelector("input[name='csrfmiddlewaretoken']").value);
        data.append("toggle_switch", "formCheck-3");
        data.append("switch", document.querySelector("#formCheck-3").checked);
        request.send(data);
    }
});
