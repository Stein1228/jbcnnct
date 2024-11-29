document.addEventListener('DOMContentLoaded', function () {
    const cifras = document.querySelectorAll('.cifra');  // Seleccionar todas las cifras (usuarios registrados y trabajos postulados)

    cifras.forEach(function (cifra) {
        const count = cifra.getAttribute('data-count');  // Obtener el valor de "data-count" (usuarios o trabajos)
        let currentCount = 0;
        const targetCount = parseInt(count);  // Convertir a número el valor del "data-count"

        const interval = setInterval(function () {
            if (currentCount < targetCount) {
                currentCount += Math.ceil(targetCount / 100);  // Incrementar suavemente
                cifra.textContent = currentCount.toLocaleString();  // Actualizar el texto con el número formateado
            } else {
                cifra.textContent = targetCount.toLocaleString();  // Asegurarse de que se muestre el número final
                clearInterval(interval);  // Detener la animación cuando se alcanza el número
            }
        }, 10);  // Intervalo de tiempo para la animación
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const track = document.querySelector('.carousel-track');
    const slides = Array.from(track.children);
    const carouselContainer = document.querySelector('.carousel');
    
    // Colores de fondo ajustados para cada imagen
    const backgroundColors = ["#000000", "#004aad", "#5ce1e6"];
    
    // Clonar el primer y último slide para lograr un efecto "infinito"
    const firstClone = slides[0].cloneNode(true);
    const lastClone = slides[slides.length - 1].cloneNode(true);
    track.appendChild(firstClone);
    track.insertBefore(lastClone, slides[0]);
    
    // Actualizar la lista de slides después de clonar
    const updatedSlides = Array.from(track.children);
    let currentIndex = 1; // Empezamos en el primer slide "real"

    // Configurar el ancho del track para contener todos los slides duplicados
    track.style.width = `${updatedSlides.length * 100}%`;
    updatedSlides.forEach(slide => (slide.style.width = `${100 / updatedSlides.length}%`));
    
    // Posicionar el track para mostrar el primer slide "real"
    track.style.transform = `translateX(-${currentIndex * 100}%)`;

    // Función para mover al siguiente slide
    const moveToNextSlide = () => {
        currentIndex++;
        track.style.transition = "transform 0.5s ease";
        track.style.transform = `translateX(-${currentIndex * 100}%)`;

        // Cambiar el color de fondo según el índice
        const realIndex = (currentIndex - 1 + slides.length) % slides.length;
        carouselContainer.style.backgroundColor = backgroundColors[realIndex];

        // Si estamos en el último slide clonado, saltamos al primero real
        if (currentIndex === updatedSlides.length - 1) {
            setTimeout(() => {
                track.style.transition = "none";
                currentIndex = 1;
                track.style.transform = `translateX(-${currentIndex * 100}%)`;
            }, 500);
        }
    };

    // Función para mover al slide anterior
    const moveToPreviousSlide = () => {
        currentIndex--;
        track.style.transition = "transform 0.5s ease";
        track.style.transform = `translateX(-${currentIndex * 100}%)`;

        // Cambiar el color de fondo según el índice
        const realIndex = (currentIndex - 1 + slides.length) % slides.length;
        carouselContainer.style.backgroundColor = backgroundColors[realIndex];

        // Si estamos en el primer slide clonado, saltamos al último real
        if (currentIndex === 0) {
            setTimeout(() => {
                track.style.transition = "none";
                currentIndex = slides.length;
                track.style.transform = `translateX(-${currentIndex * 100}%)`;
            }, 500);
        }
    };

    // Cambia de imagen cada 10 segundos
    setInterval(moveToNextSlide, 10000);

    // Añadir eventos a los botones
    const leftButton = document.querySelector('.left-btn');
    const rightButton = document.querySelector('.right-btn');

    leftButton.addEventListener('click', moveToPreviousSlide);
    rightButton.addEventListener('click', moveToNextSlide);
});

// Esperamos que el DOM se haya cargado completamente
document.addEventListener('DOMContentLoaded', function () {
    const paragraphs = document.querySelectorAll('.welcome-section p'); // Seleccionamos los párrafos de bienvenida

    paragraphs.forEach(function (paragraph) {
        const text = paragraph.textContent;  // Guardamos el texto original
        paragraph.textContent = '';  // Limpiamos el contenido del párrafo

        let i = 0;
        const interval = setInterval(function () {
            paragraph.textContent += text[i];  // Añadimos una letra cada vez
            i++;
            if (i === text.length) {
                clearInterval(interval);  // Detenemos la animación una vez que se ha mostrado todo el texto
            }
        }, 5);  // Reducimos el tiempo entre letras a 10ms
    });
});