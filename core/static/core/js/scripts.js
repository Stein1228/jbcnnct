function showSidebar(){
    const sidebar = document.querySelector('.sidebar')
    sidebar.style.display = 'flex'
}

function hideSidebar(){
    const sidebar = document.querySelector('.sidebar')
    sidebar.style.display = 'none'
}

// Mostrar el botón cuando el usuario hace scroll hacia abajo 20px desde la parte superior
window.onscroll = function() {
    scrollFunction();
};

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        document.getElementById("scrollTopBtn").style.display = "block";
    } else {
        document.getElementById("scrollTopBtn").style.display = "none";
    }
}

// Cuando el usuario hace clic en el botón, vuelve al inicio
function scrollToTop() {
    document.body.scrollTop = 0; // Para Safari
    document.documentElement.scrollTop = 0; // Para Chrome, Firefox, IE y Opera
}

document.addEventListener('DOMContentLoaded', function () {
    var profileImages = document.querySelectorAll('.profile-image');
    var defaultImage = '/static/images/foto_perfil_defecto.svg';

    profileImages.forEach(function (img) {
        var link = img.closest('.profile-link');
        
        img.onerror = function() {
            this.setAttribute('src', defaultImage);
            this.setAttribute('alt', "Imagen de perfil no disponible");
            if (link) {
                link.setAttribute('href', defaultImage);
            }
        };
    });
});