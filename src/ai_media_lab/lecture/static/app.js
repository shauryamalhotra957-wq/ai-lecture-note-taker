const health = document.querySelector("#health");
const form = document.querySelector("#uploadForm");
const fileInput = document.querySelector("#file");
const fileLabel = document.querySelector("#fileLabel");
const submitBtn = document.querySelector("#submitBtn");
const canvas = document.querySelector("#waveform");
const ctx = canvas.getContext("2d");

function drawWave(seed = 4) {
  const width = canvas.width;
  const height = canvas.height;
  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, width, height);
  ctx.strokeStyle = "#d9e2ec";
  ctx.beginPath();
  ctx.moveTo(0, height / 2);
  ctx.lineTo(width, height / 2);
  ctx.stroke();

  const bars = 92;
  const step = width / bars;
  for (let index = 0; index < bars; index += 1) {
    const energy = Math.abs(Math.sin((index + seed) * 0.37)) * 0.7 + Math.abs(Math.cos(index * 0.11)) * 0.3;
    const barHeight = Math.max(10, energy * (height - 20));
    ctx.fillStyle = index % 5 === 0 ? "#0f766e" : "#2563eb";
    ctx.fillRect(index * step + 2, (height - barHeight) / 2, Math.max(3, step - 4), barHeight);
  }
}

function setLoading(isLoading) {
  submitBtn.disabled = isLoading;
  submitBtn.textContent = isLoading ? "Generating" : "Generate Notes";
}

function renderList(target, values) {
  target.innerHTML = "";
  values.forEach((value) => {
    const li = document.createElement("li");
    li.textContent = value;
    target.appendChild(li);
  });
}

function renderConcepts(concepts) {
  const root = document.querySelector("#concepts");
  root.innerHTML = "";
  concepts.forEach((concept) => {
    const item = document.createElement("div");
    item.className = "item";
    item.innerHTML = `<h4></h4><p></p><p></p>`;
    item.querySelector("h4").textContent = concept.concept;
    item.querySelectorAll("p")[0].textContent = concept.why_it_matters;
    item.querySelectorAll("p")[1].textContent = concept.evidence;
    root.appendChild(item);
  });
}

function renderQuiz(questions) {
  const root = document.querySelector("#quiz");
  root.innerHTML = "";
  questions.forEach((question) => {
    const item = document.createElement("div");
    item.className = "item quiz";
    const options = question.options.map((option) => `<li>${option}</li>`).join("");
    item.innerHTML = `<h4></h4><ul>${options}</ul><p></p>`;
    item.querySelector("h4").textContent = question.question;
    item.querySelector("p").textContent = `Answer: ${question.answer}`;
    root.appendChild(item);
  });
}

function renderGuide(guide) {
  const root = document.querySelector("#guide");
  const groups = [
    ["Focus", guide.focus_areas],
    ["Plan", guide.review_plan],
    ["Exam", guide.exam_tips],
  ];
  root.innerHTML = "";
  groups.forEach(([label, values]) => {
    const block = document.createElement("div");
    block.className = "guide-block";
    block.innerHTML = `<h4>${label}</h4><ul></ul>`;
    values.forEach((value) => {
      const li = document.createElement("li");
      li.textContent = value;
      block.querySelector("ul").appendChild(li);
    });
    root.appendChild(block);
  });
}

async function checkHealth() {
  try {
    const response = await fetch("/api/health");
    const data = await response.json();
    health.textContent = data.status === "ok" ? "Ready" : "Offline";
  } catch {
    health.textContent = "Offline";
  }
}

fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  fileLabel.textContent = file ? file.name : "Choose lecture recording";
  drawWave(file ? file.size % 31 : 4);
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!fileInput.files.length) return;
  setLoading(true);
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  formData.append("topic", document.querySelector("#topic").value);
  formData.append("demo_mode", document.querySelector("#demoMode").checked ? "true" : "false");

  try {
    const response = await fetch("/api/analyze", { method: "POST", body: formData });
    if (!response.ok) throw new Error(await response.text());
    const result = await response.json();
    const analysis = result.analysis;
    document.querySelector("#title").textContent = analysis.title;
    document.querySelector("#markdownLink").href = result.markdown_url;
    document.querySelector("#jsonLink").href = result.json_url;
    renderList(document.querySelector("#summary"), analysis.summary);
    renderConcepts(analysis.key_concepts);
    renderQuiz(analysis.quiz_questions);
    renderGuide(analysis.study_guide);
    document.querySelector("#result").classList.remove("hidden");
  } catch (error) {
    alert(`Unable to generate notes: ${error.message}`);
  } finally {
    setLoading(false);
  }
});

drawWave();
checkHealth();

