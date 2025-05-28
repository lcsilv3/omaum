document.addEventListener("DOMContentLoaded", function () {
    // Elementos dos filtros
    const cursoSelect = document.getElementById("filtro-curso");
    const turmaSelect = document.getElementById("filtro-turma");

    // Função para atualizar turmas ao selecionar curso
    function atualizarTurmasPorCurso(cursoId, turmaSelectId, endpointUrl) {
        const turmaSelect = document.getElementById(turmaSelectId);
        if (!cursoId) {
            // Se nenhum curso selecionado, limpa as turmas
            turmaSelect.innerHTML = '<option value="">Todas as turmas</option>';
            return;
        }
        fetch(endpointUrl + "?curso_id=" + cursoId, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
            .then((response) => response.json())
            .then((turmas) => {
                turmaSelect.innerHTML = '<option value="">Todas as turmas</option>';
                turmas.forEach(function (turma) {
                    turmaSelect.innerHTML += `<option value="${turma.id}">${turma.nome}</option>`;
                });
            });
    }

    // Detecta contexto (listagem, relatório, dashboard)
    let contexto = "listagem";
    if (document.getElementById("filtro-relatorio-form")) contexto = "relatorio";
    if (document.getElementById("filtro-dashboard-form")) contexto = "dashboard";

    // Define endpoints AJAX conforme contexto
    let endpointTurmas = "/atividades/ajax/turmas-por-curso/";
    let endpointAtividades = "/atividades/ajax/atividades-filtradas/";
    if (contexto === "relatorio") {
        endpointTurmas = "/atividades/ajax/relatorio/turmas-por-curso/";
        endpointAtividades = "/atividades/ajax/relatorio/atividades-filtradas/";
    }
    if (contexto === "dashboard") {
        endpointTurmas = "/atividades/ajax/dashboard/turmas-por-curso/";
        endpointAtividades = "/atividades/ajax/dashboard/conteudo/";
    }

    // Atualiza turmas ao mudar curso
    if (cursoSelect && turmaSelect) {
        cursoSelect.addEventListener("change", function () {
            atualizarTurmasPorCurso(this.value, "filtro-turma", endpointTurmas);
            // Opcional: resetar turma ao trocar curso
            turmaSelect.value = "";
            // Atualiza tabela/conteúdo automaticamente
            atualizarConteudo();
        });
        turmaSelect.addEventListener("change", atualizarConteudo);
    }

    // Atualiza tabela/conteúdo ao buscar
    const formId =
        contexto === "relatorio"
            ? "filtro-relatorio-form"
            : contexto === "dashboard"
            ? "filtro-dashboard-form"
            : "filtro-atividades-form";
    const filtroForm = document.getElementById(formId);
    if (filtroForm) {
        filtroForm.addEventListener("submit", function (e) {
            e.preventDefault();
            atualizarConteudo();
        });
        // Busca instantânea ao digitar (opcional)
        const qInput = filtroForm.querySelector('input[name="q"]');
        if (qInput) {
            qInput.addEventListener("input", function () {
                atualizarConteudo();
            });
        }
    }

    function atualizarConteudo() {
        // Monta query string dos filtros
        const params = new URLSearchParams();
        if (cursoSelect && cursoSelect.value) params.append("curso", cursoSelect.value);
        if (turmaSelect && turmaSelect.value) params.append("turma", turmaSelect.value);
        if (filtroForm) {
            const qInput = filtroForm.querySelector('input[name="q"]');
            if (qInput && qInput.value) params.append("q", qInput.value);
        }
        fetch(endpointAtividades + "?" + params.toString(), {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
            .then((response) => response.text())
            .then((html) => {
                // Atualiza apenas o tbody da tabela
                document.getElementById("atividades-tabela-body").innerHTML = html;
            });
    }
});