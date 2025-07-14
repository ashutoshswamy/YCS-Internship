const imageUpload = document.getElementById("imageUpload");
const profileImage = document.getElementById("profileImage");
const uploadButton = document.getElementById("uploadButton");

// Add event listener to the hidden file input.
// This function will execute when a file is selected.
imageUpload.addEventListener("change", function (event) {
  // Get the first file from the selected files (users can only select one here)
  const file = event.target.files[0];

  // Check if a file was actually selected
  if (file) {
    // Create a FileReader object to read the contents of the file
    const reader = new FileReader();

    // Set up the onload event handler for the FileReader.
    // This function will execute once the file has been successfully read.
    reader.onload = function (e) {
      // Set the 'src' attribute of the profileImage to the result of the FileReader.
      // The result is a Data URL (base64 encoded string) representing the image.
      profileImage.src = e.target.result;
    };

    // Read the file as a Data URL. This triggers the 'onload' event when complete.
    reader.readAsDataURL(file);
  } else {
    // If no file is selected (e.g., user cancels the file dialog),
    // revert to a placeholder image or display a message.
    profileImage.src =
      "https://placehold.co/128x128/e0e0e0/ffffff?text=Add%20Photo";
  }
});

// Add event listener to the "Choose Photo" button.
// When clicked, it programmatically clicks the hidden file input.
uploadButton.addEventListener("click", function () {
  imageUpload.click();
});

// Add event listener to the profile image itself.
// When clicked, it also programmatically clicks the hidden file input.
profileImage.addEventListener("click", function () {
  imageUpload.click();
});
