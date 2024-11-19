import { toggleFavoriteProps } from "./helper.js";

document.addEventListener("DOMContentLoaded", () => {
  document
    .querySelector(".property-list")
    .addEventListener("click", function (e) {
      const btn = e.target.closest(".add-favorite-btn");

      if (btn) {
        const propId = parseInt(btn.getAttribute("data-id"));
        toggleFavoriteProps(propId, btn);
      }
    });

  // Predictive Text Address Search

  const address = [
    "448 BAILEY AVE, San Antonio, TX 78210",
    "5719 Goliad Bluff, San Antonio, TX 78222",
    "4138 Sepulveda Blvd, Sherman Oaks, CA 91403",
    "19211 HABITAT CV, San Antonio, TX 78258",
    "13911 BLUFFOAK, San Antonio, TX 78216",
    "722 N Trumbull Ave, Chicago, IL 60624",
    "6127 LITTLE BRANDYWINE CRK, San Antonio, TX 78233",
  ];

  const addressInput = document.querySelector("#address-input");
  const searchBtn = document.querySelector("#button-addon2");
  const suggestions = document.querySelector(".suggestions ul");

  let results = [];

  addressInput.addEventListener("keyup", searchHandler);
  suggestions.addEventListener("click", useSuggestion);
  // searchBtn.addEventListener("click", searchProperty);

  async function searchHandler(e) {
    const inputVal = e.target.value.trim();

    // Clear the previous suggestions
    results = [];
    suggestions.textContent = "";

    showSuggestion(await search(inputVal), inputVal);
  }

  // Filter the list based on user input
  async function search(str) {
    const resp = await axios.get(`/search_address?q=${str}`);
    const address = resp.data;

    results = [
      ...address.filter((el) => el.toLowerCase().includes(str.toLowerCase())),
    ];

    return results;
  }

  // Display the resutls list as a drop down
  function showSuggestion(results, inputVal) {
    const container = document.querySelector(".suggestions");
    const inputLower = inputVal.toLowerCase();

    for (let el of results) {
      const elLower = el.toLowerCase();
      const li = document.createElement("li");

      const regex = new RegExp(inputLower, "i");
      let address = el.replace(regex, "<strong>$&</strong>");

      li.innerHTML = address;
      suggestions.append(li);

      // Hide suggestions
      if (inputVal === "") {
        suggestions.textContent = "";
        container.classList.add("d-none");
        container.classList.remove("d-block");
      } else {
        container.classList.remove("d-none");
        container.classList.add("d-block");
      }
    }
  }

  // Populate the search bar.
  function useSuggestion(e) {
    addressInput.value = e.target.textContent;
    suggestions.textContent = "";
  }

  // Search property
  // async function searchProperty() {
  //   const inputVal = addressInput.value;
  //   console.log(inputVal);
  //   try {
  //     const resp = await axios.get(`/api/property_detail/${inputVal}`);
  //   } catch (e) {
  //     console.log("Error: ", e);
  //   }
  // }
});

// function displayFlashMessage(category, message) {
//   const container = document.getElementById("flash-messages");
//   container.innerHTML = `
//   <div class="alert alert-${category}" role="alert">
//         ${message}
//       </div>
//   `;
// }
