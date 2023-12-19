document.addEventListener("DOMContentLoaded", function() {
    const dropdown = document.getElementById("yesNoDropdown");
    const textbox = document.getElementById("outputTextbox");

    dropdown.addEventListener("change", function() {
        textbox.value = dropdown.value;
    });
});
