document.addEventListener('DOMContentLoaded', function () {
    const sections = document.querySelectorAll('.section-container, .about-us h2');

    function revealOnScroll() {
        const viewportHeight = window.innerHeight;
        
        sections.forEach(section => {
            const sectionTop = section.getBoundingClientRect().top;

            if (sectionTop < viewportHeight - 100) {
                section.classList.add('visible');  // Añade la clase visible para iniciar la animación
            }
        });
    }

    window.addEventListener('scroll', revealOnScroll);
    revealOnScroll();  // Llamada inicial para elementos visibles al cargar
});