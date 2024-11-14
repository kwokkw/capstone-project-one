import { toggleFavoriteProps } from "./helper.js";

document.addEventListener("DOMContentLoaded", () => {
  document
    .querySelector(".property-list")
    .addEventListener("click", function (evt) {
      const btn = evt.target.closest(".add-favorite-btn");
      // console.log(evt.target);

      if (btn) {
        const propId = parseInt(btn.getAttribute("data-id"));
        toggleFavoriteProps(propId, btn);
      }
    });

  // document
  //   .getElementById("signup-btn")
  //   .addEventListener("click", async function (evt) {
  //     evt.preventDefault();
  //     const form = document.getElementById("signup-form");
  //     const formData = new FormData(form);

  //     const resp = await axios.post("/signup", formData);
  //     const data = resp.data;
  //     console.log(resp);

  //     if (data.success) {
  //       window.location.href = "/";
  //     } else {
  //       const messages = data.messages;
  //       displayFlashMessage(messages.category, messages.message);
  //     }
  //   });
});

function displayFlashMessage(category, message) {
  const container = document.getElementById("flash-messages");
  container.innerHTML = `
  <div class="alert alert-${category}" role="alert">
        ${message}
      </div>
  `;
}
