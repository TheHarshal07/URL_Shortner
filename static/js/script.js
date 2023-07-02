document.querySelectorAll(".copy-link").forEach(copyLinkContainer =>{
    const inputField = copyLinkContainer.querySelector(".copy-link-input");
    const copyButton = copyLinkContainer.querySelector(".copy-link-button");
    const text = inputField.value;
    inputField.addEventListener("focus", () => inputField.select())
    copyButton.addEventListener("click", () => {
        inputField.select()
        navigator.clipboard.writeText(text);
        } )
});