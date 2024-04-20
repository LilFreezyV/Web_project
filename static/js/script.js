function quit() {
    window.location.href = 'http://127.0.0.1:5000/';
}

function get_content() {
    var node = document.getElementById('btn');
    htmlContent = node.innerHTML;
    const textContent = node.textContent;
    alert(textContent)

}
