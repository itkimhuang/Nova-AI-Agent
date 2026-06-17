const state = {
  sending: false,
};

const els = {
  composer: document.querySelector("#composer"),
  input: document.querySelector("#message"),
  send: document.querySelector("#send"),
  status: document.querySelector("#status"),
  conversation: document.querySelector("#conversation"),
  goal: document.querySelector("#memory-goal"),
  time: document.querySelector("#memory-time"),
  task: document.querySelector("#memory-task"),
  progress: document.querySelector("#memory-progress"),
};

function text(value, fallback = "Not set") {
  if (value === null || value === undefined || value === "") {
    return fallback;
  }
  return String(value);
}

function renderMemory(memory) {
  els.goal.textContent = text(memory.current_goal);
  els.time.textContent = memory.available_time_today_minutes
    ? `${memory.available_time_today_minutes} minutes`
    : "Not set";
  els.task.textContent = text(memory.last_suggested_task);
  const recent = Array.isArray(memory.recent_progress)
    ? memory.recent_progress
    : [];
  els.progress.textContent = recent.length
    ? recent.slice(-3).join(" | ")
    : "No recent progress";
}

function addMessage(kind, content) {
  const node = document.createElement("article");
  node.className = `message ${kind}`;
  if (typeof content === "string") {
    node.textContent = content;
  } else {
    node.append(content);
  }
  els.conversation.append(node);
  els.conversation.scrollTop = els.conversation.scrollHeight;
}

function renderNovaResponse(response) {
  const fragment = document.createDocumentFragment();
  const lines = [
    ["Main task", response.main_task],
    ["Optional", response.optional_task],
    ["Tip", response.tip],
    ["Progress", response.progress],
    ["Encouragement", response.encouragement],
  ].filter(([, value]) => value);

  for (const [label, value] of lines) {
    const p = document.createElement("p");
    p.className = "line";
    p.innerHTML = `<b>${label}:</b> `;
    p.append(document.createTextNode(value));
    fragment.append(p);
  }

  addMessage("nova", fragment);
}

async function loadMemory() {
  const res = await fetch("/api/memory");
  if (!res.ok) {
    throw new Error("Could not load memory.");
  }
  const data = await res.json();
  renderMemory(data.memory);
}

async function sendMessage(message) {
  const res = await fetch("/api/message", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message }),
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.error || "Nova could not answer.");
  }
  renderNovaResponse(data.response);
  renderMemory(data.memory);
}

els.composer.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = els.input.value.trim();
  if (!message || state.sending) {
    return;
  }

  state.sending = true;
  els.send.disabled = true;
  els.status.textContent = "Thinking";
  addMessage("user", message);
  els.input.value = "";

  try {
    await sendMessage(message);
    els.status.textContent = "Local";
  } catch (error) {
    addMessage("error", error.message);
    els.status.textContent = "Error";
  } finally {
    state.sending = false;
    els.send.disabled = false;
    els.input.focus();
  }
});

loadMemory().catch((error) => {
  addMessage("error", error.message);
  els.status.textContent = "Error";
});
