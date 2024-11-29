document.addEventListener("DOMContentLoaded", function () {
    const titles = document.querySelectorAll(".support-content h3");

    const handleScroll = () => {
        titles.forEach((title) => {
            const rect = title.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom >= 0) {
                title.classList.add("in-view");
            }
        });
    };

    window.addEventListener("scroll", handleScroll);
    handleScroll(); // Ejecutar al cargar
});