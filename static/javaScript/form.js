const inputs = document.querySelectorAll("input")

const checkValidity = (input) => {
    if (!input.classList.contains("skip")) {
        if (input.value === "" || input.value === " ") {
            input.classList.remove("has-text")
        }
        else {
            input.classList.add("has-text")
        };
    };
};

document.addEventListener("DOMContentLoaded", () => {
    inputs.forEach(input => {
        checkValidity(input);
        input.addEventListener("input", () => {
            checkValidity(input);
        });
    });
});
