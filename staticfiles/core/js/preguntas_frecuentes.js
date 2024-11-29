function toggleFaq(questionElement) {
    const answer = questionElement.nextElementSibling;
    if (answer.style.display === "block") {
        answer.style.display = "none"; // Ocultar respuesta
    } else {
        answer.style.display = "block"; // Mostrar respuesta
    }
}