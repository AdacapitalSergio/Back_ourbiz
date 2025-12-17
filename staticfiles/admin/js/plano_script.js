let formData = {
  tipo: "",
  localizacao: "",
  nome_empresa: "",
  diferencial: ""
};

function esconderFormulario() {
  document.getElementById("formulario").style.display = "none";
}

function mostrarLoading() {
  document.getElementById("tela-loading").style.display = "block";
}

function nextStep(atual) {
  if (atual === 1) {
    formData.tipo = document.getElementById('tipo').value.trim();
    if (!formData.tipo) return alert("Informe o tipo de negócio!");
  }

  if (atual === 2) {
    formData.localizacao = document.getElementById('localizacao').value.trim();
    if (!formData.localizacao) return alert("Informe a localização!");
    carregarSugestoesNome();
  }

  if (atual === 3) {
    formData.nome_empresa = document.getElementById('nome_empresa').value.trim();
    if (!formData.nome_empresa) return alert("Informe o nome da empresa!");
    carregarSugestoesDiferencial();
  }

  document.getElementById('step' + atual).classList.remove('active');
  document.getElementById('step' + (atual + 1)).classList.add('active');
}

async function carregarSugestoesNome() {
  const box = document.getElementById('sugestoes_nome');
  box.innerHTML = "<p>Carregando sugestões...</p>";
  box.style.display = "block";

  const res = await fetch("/api/plano_negocio/sugerir_respostas", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      dados: `${formData.tipo}, ${formData.localizacao}`,
      pergunta: "Qual é o nome da sua empresa?",
      limite: 25
    })
  });

  const json = await res.json();
  box.innerHTML = "<p>Sugestões:</p>" + json.resultado
    .map(s => `<div class="suggestion-item" onclick="selectSugestao('nome_empresa', '${s}')">${s}</div>`)
    .join("");
}

async function carregarSugestoesDiferencial() {
  const box = document.getElementById('sugestoes_diferencial');
  box.innerHTML = "<p>Carregando sugestões...</p>";
  box.style.display = "block";

  const res = await fetch("/api/plano_negocio/sugerir_respostas", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      dados: `${formData.tipo}, ${formData.localizacao}`,
      pergunta: "O que torna o teu negócio único?",
      limite: 50
    })
  });

  const json = await res.json();
  box.innerHTML = "<p>Sugestões:</p>" + json.resultado
    .map(s => `<div class="suggestion-item" onclick="selectSugestao('diferencial', '${s}')">${s}</div>`)
    .join("");
}

function selectSugestao(campo, valor) {
  document.getElementById(campo).value = valor;
}

async function enviarPlano() {
  formData.diferencial = document.getElementById('diferencial').value.trim();
  if (!formData.diferencial) return alert("Escreva o diferencial!");

  esconderFormulario();
  mostrarLoading();

  const res = await fetch("/api/plano_negocio/gerar_plano_negocio/", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      tipo_de_negocio: formData.tipo,
      localizacao: formData.localizacao,
      nome_empresa: formData.nome_empresa,
      diferencial: formData.diferencial
    })
  });

  const json = await res.json();
  const taskId = json.task_id;

  const interval = setInterval(async () => {
    const statusRes = await fetch(`/api/plano_negocio/gerar_plano_status/${taskId}`);
    
    // Se a task retornar JSON com status, é ainda processamento
    const contentType = statusRes.headers.get("content-type");
    
    if (contentType && contentType.includes("application/json")) {
      const statusJson = await statusRes.json();
      if (statusJson.status === "erro") {
        clearInterval(interval);
        alert("Erro ao gerar plano: " + statusJson.detalhes);
        location.reload();
      }
      return; // ainda processando
    }

    // Se não for JSON, significa que o backend retornou render do template (SUCCESS)
    clearInterval(interval);
    window.location.href = `/api/plano_negocio/gerar_plano_status/${taskId}`;
  }, 3000);
}
