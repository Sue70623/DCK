const hamburger = document.getElementById("hamburger");
const navVertical = document.getElementById("nav-vertical");

hamburger.addEventListener("click", () => {
  navVertical.classList.toggle("show"); // Affiche ou cache le menu vertical
});

// Afficher/Masquer le bouton en fonction du défilement
window.addEventListener("scroll", () => {
  const scrollTopButton = document.getElementById("scroll-top");
  if (window.scrollY > 200) {
    scrollTopButton.classList.add("show");
  } else {
    scrollTopButton.classList.remove("show");
  }
});

// Fonction pour remonter en haut
function scrollToTop() {
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// Récupérer les paramètres de l'URL
const urlParams = new URLSearchParams(window.location.search);
const courseType = urlParams.get("type");
// Références aux éléments HTML
const dateInput = document.getElementById("date");
const serviceDropdown = document.getElementById("service");
const timeDropdown = document.getElementById("time");
const privateTimeDropdown = document.getElementById("private-time");

console.log("Reservation URL:", reservationUrl);

//Réservation des cours//
document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".cta-button");

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const type = button.getAttribute("data-type");
      console.log("Type détecté:", type);
      if (type) {
        const url = `${reservationUrl}?type=${type}#reservation`;
        console.log("URL générée:", url);
        location.href = url;
      }
    });
  });
});

//pré-selection des services via la bouton//
document.addEventListener("DOMContentLoaded", () => {
  // Récupérer le paramètre "type" de l'URL
  const params = new URLSearchParams(window.location.search);
  const courseType = params.get("type");

  if (courseType) {
    // Trouver le champ "service" et sélectionner la bonne option
    const serviceSelect = document.getElementById("service");
    const optionToSelect = [...serviceSelect.options].find(
      (option) => option.value === courseType
    );

    if (optionToSelect) {
      optionToSelect.selected = true;
    }
  }
});

// Horaires pour les cours collectifs
const groupSchedules = {
  monday: ["10h-11h", "15h-16h"],
  tuesday: ["9h-10h", "14h-15h"],
  wednesday: ["11h-12h", "16h-17h"],
  thursday: ["10h-11h", "18h-19h"],
  friday: ["9h-10h", "15h-16h"],
};

// Horaires pour les cours privés
const privateSchedules = {
  monday: ["9h-10h", "16h-17h"],
  tuesday: ["14h-15h"],
  wednesday: ["11h-12h", "16h-17h"],
  thursday: ["10h-11h"],
  friday: ["16h-17h"],
};

// Créneaux réservés pour les cours privés
const reservedSlots = {
  "private-danse-classique": ["Mardi 14h-15h"],
  "private-fitness-pilates": ["Lundi 9h-10h"],
};

// Fonction pour gérer les horaires des cours collectifs
function handleGroupSchedules(dayOfWeek) {
  if (groupSchedules[dayOfWeek]) {
    timeDropdown.style.display = "block";
    timeDropdown.innerHTML = ""; // Réinitialiser les options
    groupSchedules[dayOfWeek].forEach((schedule) => {
      const option = document.createElement("option");
      option.value = schedule;
      option.textContent = schedule;
      timeDropdown.appendChild(option);
    });
  } else {
    timeDropdown.innerHTML =
      "<option value=''>Aucun horaire disponible</option>";
  }
}

// Fonction pour gérer les horaires des cours privés
function handlePrivateSchedules(dayOfWeek) {
  if (privateSchedules[dayOfWeek]) {
    privateTimeDropdown.style.display = "block";
    privateTimeDropdown.innerHTML = ""; // Réinitialiser les options
    privateSchedules[dayOfWeek]
      .filter((slot) => !reservedSlots[serviceDropdown.value]?.includes(slot)) // Exclure les créneaux réservés
      .forEach((schedule) => {
        const option = document.createElement("option");
        option.value = schedule;
        option.textContent = schedule;
        privateTimeDropdown.appendChild(option);
      });
  } else {
    privateTimeDropdown.innerHTML =
      "<option value=''>Aucune disponibilité</option>";
  }
}

// Écouteur sur le champ de date
dateInput.addEventListener("change", () => {
  const selectedDate = new Date(dateInput.value);
  const dayOfWeek = selectedDate
    .toLocaleString("en-us", { weekday: "long" })
    .toLowerCase();
  const selectedService = serviceDropdown.value;

  // Vérification du type de cours
  if (selectedService.startsWith("group")) {
    handleGroupSchedules(dayOfWeek);
  } else if (selectedService.startsWith("private")) {
    handlePrivateSchedules(dayOfWeek);
  }
});

// Écouteur sur le menu déroulant "Service"
serviceDropdown.addEventListener("change", () => {
  const selectedService = serviceDropdown.value;

  if (selectedService.startsWith("group")) {
    timeDropdown.style.display = "block";
    privateTimeDropdown.style.display = "none";
  } else if (selectedService.startsWith("private")) {
    privateTimeDropdown.style.display = "block";
    timeDropdown.style.display = "none";
  } else {
    timeDropdown.style.display = "none";
    privateTimeDropdown.style.display = "none";
  }
});
