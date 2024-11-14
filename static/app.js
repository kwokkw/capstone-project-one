document.addEventListener("DOMContentLoaded", () => {
  const loanAmount =
    parseFloat(document.getElementById("prop-price").textContent) * 0.8;
  const years = 30;
  const principalAndInterestInput =
    document.getElementById("principal-interest");

  principalAndInterestInput.value = calculatePrincipalAndInterest(
    loanAmount,
    years
  );

  calculateMonthlyPayment();

  function calculateMonthlyPayment() {
    const principalInterestInput =
      document.getElementById("principal-interest");
    const taxesInput = document.getElementById("tax-annual-amount");
    const insuranceInput = document.getElementById(
      "annual-homeowners-insurance"
    );
    const hoaInput = document.getElementById("monthly-hoa-fee");
    const totalMonthlyPayment = document.getElementById(
      "total-monthly-payment"
    );

    const principalInterest = parseFloat(principalInterestInput.value) || 0;
    const taxes = parseFloat(taxesInput.value) || 0;
    const insurance = parseFloat(insuranceInput.value) || 0;
    const hoa = parseFloat(hoaInput.value) || 0;

    const total = principalInterest + taxes + insurance + hoa;
    totalMonthlyPayment.textContent = total.toFixed(2);
  }

  async function getInterestRate() {
    try {
      const resp = await axios.get("/api/get-interest-rate");
      return resp.data;
    } catch (e) {
      console.error("error: ", e);
    }
  }

  // async function calculatePrincipalAndInterest(loanAmount, years) {
  function calculatePrincipalAndInterest(loanAmount, years) {
    // const interestRate = (await getInterestRate()) || 0.06;
    const interestRate = 0.06;
    const monthlyRate = interestRate / 12;
    const numberOfPayments = years * 12;

    const principalAndInterest =
      (loanAmount * monthlyRate) /
      (1 - Math.pow(1 + monthlyRate, -numberOfPayments));

    console.log(principalAndInterest.toFixed(2));
    return principalAndInterest.toFixed(2);
  }
});

/* 

project-root/
├── static/
│   ├── css/
│   ├── js/
|   ├── templates/
│   │   ├── properteis/
|   |   |   ├──details.html
|   |   ├── users/
|   |   |   ├── changes_password.html
|   |   |   ├── detail.html
|   |   |   ├── edit.html
|   |   |   ├── favorites.html
|   |   |   ├── login.html
|   |   |   ├── signup.html
│   │   ├── _macros.html
│   │   ├── 404.html
|   |   ├── home.html
│   │   └── base.html 

*/
