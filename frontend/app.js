const bmiForm = document.querySelector("#bmi-form");
const emailForm = document.querySelector("#email-form");
const weightInput = document.querySelector("#weight");
const heightInput = document.querySelector("#height");
const emailButton = document.querySelector("#email-button");
const resultSection = document.querySelector("#result");
const statusSection = document.querySelector("#status");

let currentResult = null;
let currentWeight = null;
let currentHeight = null;

function invalidateResult() {
  currentResult = null;
  currentWeight = null;
  currentHeight = null;
  emailButton.disabled = true;
  statusSection.textContent = "";
}

weightInput.addEventListener("input", invalidateResult);
heightInput.addEventListener("input", invalidateResult);

bmiForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  statusSection.textContent = "";

  const weight = Number(weightInput.value);
  const height = Number(heightInput.value);

  try {
    const response = await fetch("/api/v1/bmi/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ weight, height }),
    });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail?.[0]?.msg || "No se pudo calcular el IMC.");
    }

    currentResult = data;
    currentWeight = weight;
    currentHeight = height;
    resultSection.textContent =
      `IMC: ${data.bmi} — ${data.category}`;
    emailButton.disabled = false;
  } catch (error) {
    invalidateResult();
    resultSection.textContent = error.message;
  }
});

emailForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  if (!currentResult || !weightInput.value || !heightInput.value) {
    emailButton.disabled = true;
    return;
  }

  const weight = Number(weightInput.value);
  const height = Number(heightInput.value);
  if (weight !== currentWeight || height !== currentHeight) {
    invalidateResult();
    return;
  }

  emailButton.disabled = true;
  statusSection.textContent = "Enviando...";

  try {
    const response = await fetch("/api/v1/bmi/send-email", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: document.querySelector("#email").value,
        weight,
        height,
      }),
    });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        typeof data.detail === "string"
          ? data.detail
          : "No fue posible enviar el correo.",
      );
    }

    statusSection.textContent = data.message;
  } catch (error) {
    statusSection.textContent = error.message;
  } finally {
    emailButton.disabled =
      !currentResult ||
      Number(weightInput.value) !== currentWeight ||
      Number(heightInput.value) !== currentHeight;
  }
});
