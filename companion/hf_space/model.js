"use strict";

/** Deterministic browser model for the interruption-authority demonstration. */

const AGENT_RELIABILITY = Object.freeze({
  Evidence: 0.90,
  Planning: 0.50,
  Idea: 0.20,
});

const COLD_START_RELIABILITY = 0.50;
const INTERRUPT_THRESHOLD = 0.65;
const QUEUE_THRESHOLD = 0.35;
const SESSION_HORIZON = 20;

// Six authored synthetic reports copied from companion/data/reports.json.
// Evaluation-only validity and loss labels are intentionally excluded.
const SYNTHETIC_CASES = Object.freeze([
  Object.freeze({
    id: "E01",
    agent: "Evidence",
    importance: 0.90,
    urgency: 0.90,
    arrivalMinute: 1,
    message: "A central factual claim lacks a supporting citation.",
  }),
  Object.freeze({
    id: "E04",
    agent: "Evidence",
    importance: 0.40,
    urgency: 0.30,
    arrivalMinute: 9,
    message: "A numerical statement conflicts with the cited table.",
  }),
  Object.freeze({
    id: "P01",
    agent: "Planning",
    importance: 0.95,
    urgency: 0.85,
    arrivalMinute: 2,
    message: "A required submission component is at immediate risk of omission.",
  }),
  Object.freeze({
    id: "P04",
    agent: "Planning",
    importance: 0.35,
    urgency: 0.35,
    arrivalMinute: 10,
    message: "The final export must begin by the next checkpoint.",
  }),
  Object.freeze({
    id: "I01",
    agent: "Idea",
    importance: 1.00,
    urgency: 0.90,
    arrivalMinute: 3,
    message: "A dramatic new angle is labeled essential despite being off topic.",
  }),
  Object.freeze({
    id: "I02",
    agent: "Idea",
    importance: 0.80,
    urgency: 0.80,
    arrivalMinute: 4,
    message: "A concise framing idea would resolve a central clarity problem.",
  }),
]);

function bounded(value, name) {
  const number = Number(value);
  if (!Number.isFinite(number) || number < 0 || number > 1) {
    throw new RangeError(`${name} must be in [0, 1]`);
  }
  return number;
}

function normalizeScore(value) {
  return Math.round(value * 1e12) / 1e12;
}

function currentClaimScore(importance, urgency) {
  const i = bounded(importance, "importance");
  const u = bounded(urgency, "urgency");
  return normalizeScore(0.5 * i + 0.5 * u);
}

function reputationScore(currentScore, reliability) {
  return normalizeScore(
    bounded(currentScore, "current score") * bounded(reliability, "reliability"),
  );
}

function strictlyNextCheckpoint(arrivalMinute) {
  const arrival = Number(arrivalMinute);
  if (!Number.isInteger(arrival) || arrival < 0 || arrival >= SESSION_HORIZON) {
    throw new RangeError("arrival minute must be an integer from 0 to 19");
  }
  return Math.min((Math.floor(arrival / 5) + 1) * 5, SESSION_HORIZON);
}

function routeScore(score, arrivalMinute) {
  const s = bounded(score, "score");
  if (s >= INTERRUPT_THRESHOLD) {
    return Object.freeze({
      code: "interrupt",
      label: "INTERRUPT NOW",
      deliveryMinute: Number(arrivalMinute),
    });
  }
  if (s >= QUEUE_THRESHOLD) {
    const checkpoint = strictlyNextCheckpoint(arrivalMinute);
    return Object.freeze({
      code: "queue",
      label: "QUEUE TO NEXT 5-MIN CHECKPOINT",
      deliveryMinute: checkpoint,
    });
  }
  return Object.freeze({
    code: "digest",
    label: "MINUTE-20 DIGEST",
    deliveryMinute: SESSION_HORIZON,
  });
}

function evaluateInputs({ importance, urgency, reliability, arrivalMinute }) {
  const currentScore = currentClaimScore(importance, urgency);
  const calibratedScore = reputationScore(currentScore, reliability);
  return Object.freeze({
    currentScore,
    calibratedScore,
    currentRoute: routeScore(currentScore, arrivalMinute),
    calibratedRoute: routeScore(calibratedScore, arrivalMinute),
  });
}

function formatScore(value) {
  return Number(value).toFixed(3);
}

function deliveryText(route) {
  if (route.code === "interrupt") {
    return `Delivered immediately at minute ${route.deliveryMinute}.`;
  }
  if (route.code === "queue") {
    return `Delivered at checkpoint minute ${route.deliveryMinute}.`;
  }
  return "Deferred to the minute-20 digest.";
}

function initializeInterface() {
  const byId = (id) => document.getElementById(id);
  const agentInput = byId("agent");
  const importanceInput = byId("importance");
  const urgencyInput = byId("urgency");
  const arrivalInput = byId("arrival");
  const reliabilityMode = byId("reliability-mode");
  const reliabilityInput = byId("reliability");
  const caseInput = byId("synthetic-case");

  function selectedReliability() {
    if (reliabilityMode.value === "preset") {
      return AGENT_RELIABILITY[agentInput.value];
    }
    if (reliabilityMode.value === "cold") {
      return COLD_START_RELIABILITY;
    }
    return bounded(reliabilityInput.value, "reliability");
  }

  function synchronizeReliability() {
    const usesManual = reliabilityMode.value === "manual";
    reliabilityInput.disabled = !usesManual;
    reliabilityInput.value = selectedReliability().toFixed(2);
  }

  function styleRoute(card, route) {
    card.dataset.route = route.code;
    const routeLabel = card.querySelector("[data-route-label]");
    routeLabel.textContent = route.label;
  }

  function renderComparison(currentScore) {
    const tableBody = byId("comparison-body");
    tableBody.replaceChildren();
    Object.entries(AGENT_RELIABILITY).forEach(([agent, reliability]) => {
      const score = reputationScore(currentScore, reliability);
      const route = routeScore(score, Number(arrivalInput.value));
      const row = document.createElement("tr");
      [agent, reliability.toFixed(2), formatScore(score), route.label].forEach((value) => {
        const cell = document.createElement("td");
        cell.textContent = value;
        row.appendChild(cell);
      });
      tableBody.appendChild(row);
    });
  }

  function render() {
    const importance = Number(importanceInput.value);
    const urgency = Number(urgencyInput.value);
    const arrivalMinute = Number(arrivalInput.value);
    const reliability = selectedReliability();
    const result = evaluateInputs({ importance, urgency, reliability, arrivalMinute });

    byId("importance-value").textContent = importance.toFixed(2);
    byId("urgency-value").textContent = urgency.toFixed(2);
    byId("arrival-value").textContent = String(arrivalMinute);
    byId("reliability-value").textContent = reliability.toFixed(2);
    byId("n-value").textContent = formatScore(result.currentScore);
    byId("r-value").textContent = reliability.toFixed(2);
    byId("current-score").textContent = formatScore(result.currentScore);
    byId("calibrated-score").textContent = formatScore(result.calibratedScore);
    byId("current-delivery").textContent = deliveryText(result.currentRoute);
    byId("calibrated-delivery").textContent = deliveryText(result.calibratedRoute);

    styleRoute(byId("current-result"), result.currentRoute);
    styleRoute(byId("calibrated-result"), result.calibratedRoute);
    renderComparison(result.currentScore);
  }

  function clearCaseLabel() {
    caseInput.value = "custom";
    byId("case-summary").textContent = "Custom inputs. No outcome label is used or displayed.";
  }

  function loadCase(caseId) {
    const selectedCase = SYNTHETIC_CASES.find((item) => item.id === caseId);
    if (!selectedCase) {
      clearCaseLabel();
      return;
    }
    caseInput.value = selectedCase.id;
    agentInput.value = selectedCase.agent;
    importanceInput.value = selectedCase.importance.toFixed(2);
    urgencyInput.value = selectedCase.urgency.toFixed(2);
    arrivalInput.value = String(selectedCase.arrivalMinute);
    reliabilityMode.value = "preset";
    synchronizeReliability();
    byId("case-summary").textContent = `${selectedCase.id} · ${selectedCase.message}`;
    render();
  }

  SYNTHETIC_CASES.forEach((item) => {
    const option = document.createElement("option");
    option.value = item.id;
    option.textContent = `${item.id} · ${item.agent}`;
    caseInput.appendChild(option);
  });

  caseInput.addEventListener("change", () => loadCase(caseInput.value));
  agentInput.addEventListener("change", () => {
    synchronizeReliability();
    clearCaseLabel();
    render();
  });
  reliabilityMode.addEventListener("change", () => {
    synchronizeReliability();
    clearCaseLabel();
    render();
  });
  [importanceInput, urgencyInput, arrivalInput, reliabilityInput].forEach((input) => {
    input.addEventListener("input", () => {
      clearCaseLabel();
      render();
    });
  });

  synchronizeReliability();
  loadCase("E01");
}

if (typeof document !== "undefined") {
  document.addEventListener("DOMContentLoaded", initializeInterface);
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    AGENT_RELIABILITY,
    COLD_START_RELIABILITY,
    INTERRUPT_THRESHOLD,
    QUEUE_THRESHOLD,
    SESSION_HORIZON,
    SYNTHETIC_CASES,
    currentClaimScore,
    reputationScore,
    strictlyNextCheckpoint,
    routeScore,
    evaluateInputs,
  };
}
