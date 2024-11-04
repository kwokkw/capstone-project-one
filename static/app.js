document.addEventListener("DOMContentLoaded", () => {
  const favoritesContainer = document.querySelector(".property-list");

  favoritesContainer.addEventListener("click", function (e) {
    btn = e.target.closest(".add-favorite-btn");
    if (btn) {
      propId = parseInt(btn.getAttribute("data-id"));
      toggleFavoriteProps(propId, btn);
    }
  });

  async function toggleFavoriteProps(propId, btn) {
    try {
      const resp = await axios.post(`/favorites/${propId}`);

      // Update button appearance based on the response
      if (resp.data.favorite) {
        btn.innerHTML = '<i class="fa-solid fa-heart"></i>';
      } else {
        btn.innerHTML = '<i class="fa-regular fa-heart"></i>';
      }
    } catch (e) {
      console.error(e);
    }
  }
});
