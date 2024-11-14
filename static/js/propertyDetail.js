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
});

// async function calculatePrincipalAndInterest(loanAmount, years) {
function calculatePrincipalAndInterest(loanAmount, years) {
  // const interestRate = (await getInterestRate()) || 0.06;
  const interestRate = 0.06;
  const monthlyRate = interestRate / 12;
  const numberOfPayments = years * 12;

  const principalAndInterest =
    (loanAmount * monthlyRate) /
    (1 - Math.pow(1 + monthlyRate, -numberOfPayments));

  return principalAndInterest;
}

function calculateMonthlyPayment() {
  const principalInterestInput = document.getElementById("principal-interest");
  console.log(principalInterestInput.innerText);

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
