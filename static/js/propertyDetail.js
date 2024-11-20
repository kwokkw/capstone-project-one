import { toggleFavoriteProps } from "./helper.js";

document.addEventListener("DOMContentLoaded", () => {
  const loanAmount =
    parseFloat(document.getElementById("prop-price").textContent) * 0.8;
  const years = 30;
  const monthlyPrincipalInterest = calculatePrincipalAndInterest(
    loanAmount,
    years
  );

  const principalInterest = document.getElementById("principal-interest");
  const hoa = parseFloat(document.getElementById("monthly-hoa-fee").innerText);
  const monthlyTax =
    parseFloat(document.getElementById("tax-annual-amount").innerText) / 12;
  const monthlyInsurance =
    parseFloat(
      document.getElementById("annual-homeowners-insurance").innerText
    ) / 12;

  principalInterest.innerText = monthlyPrincipalInterest.toFixed(2);
  document.getElementById("monthly-hoa-fee").innerText = hoa.toFixed(2);
  document.getElementById("tax-annual-amount").innerText =
    monthlyTax.toFixed(2);
  document.getElementById("annual-homeowners-insurance").innerText =
    monthlyInsurance.toFixed(2);

  calculateMonthlyPayment();

  const btn = document.querySelector(".add-favorite-btn");
  if (btn) {
    btn.addEventListener("click", function (evt) {
      const propId = evt.currentTarget.getAttribute("data-id");

      toggleFavoriteProps(propId, btn);
    });
  }

  // Calculate monthly payment based on user input
  document
    .querySelector("#calculate-payment-btn")
    .addEventListener("click", function () {
      const homePrice = parseFloat(document.querySelector("#home-price").value);
      const downpayment = parseFloat(
        document.querySelector("#downpayment").value
      );
      const interestRate =
        parseFloat(document.querySelector("#interest-rate").value) / 100;
      const selectedTerm = parseFloat(
        document.querySelector('input[name="terms"]:checked').value
      );

      const principal = homePrice - downpayment;

      principalInterest.textContent = calculatePrincipalAndInterest(
        principal,
        selectedTerm,
        interestRate
      ).toFixed(2);

      calculateMonthlyPayment();
    });
});

// async function calculatePrincipalAndInterest(loanAmount, years) {
function calculatePrincipalAndInterest(loanAmount, years, interestRate = 0.06) {
  // const interestRate = (await getInterestRate());
  const monthlyRate = interestRate / 12;
  const numberOfPayments = years * 12;

  const principalAndInterest =
    (loanAmount * monthlyRate) /
    (1 - Math.pow(1 + monthlyRate, -numberOfPayments));

  return principalAndInterest;
}

function calculateMonthlyPayment() {
  const principalInterestInput = document.getElementById("principal-interest");
  const taxesInput = document.getElementById("tax-annual-amount");
  const insuranceInput = document.getElementById("annual-homeowners-insurance");
  const hoaInput = document.getElementById("monthly-hoa-fee");
  const totalMonthlyPayment = document.getElementById("total-monthly-payment");

  const principalInterest = parseFloat(principalInterestInput.innerText) || 0;
  const taxes = parseFloat(taxesInput.innerText) || 0;
  const insurance = parseFloat(insuranceInput.innerText) || 0;
  const hoa = parseFloat(hoaInput.innerText) || 0;

  const total = principalInterest + taxes + insurance + hoa;
  totalMonthlyPayment.textContent = total.toFixed(2);
}
