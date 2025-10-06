/* eslint-disable no-console */
(function () {
    "use strict";

    document.addEventListener("DOMContentLoaded", () => {
        const historicoApiUrl = document.body.dataset.historicoApiUrl || null;
        const addEventoApiUrl = document.body.dataset.addEventoApiUrl || null;
        const tiposCodigosApiUrl = document.body.dataset.tiposCodigosApiUrl || null;
        const codigosPorTipoApiUrl = document.body.dataset.codigosPorTipoApiUrl || null;
        const desativarHistoricoUrlTemplate =
            document.body.dataset.desativarHistoricoUrlTemplate || null;
        const reativarHistoricoUrlTemplate =
            document.body.dataset.reativarHistoricoUrlTemplate || null;
        const alunoId = document.body.dataset.alunoId || null;
        const filtrosStorageKey = alunoId
            ? `timelineFiltros:${alunoId}`
            : null;
        const csrfToken = getCsrfToken();
        const modalDesativarEl = document.getElementById(
            "modal-desativar-historico"
        );
        const motivoDesativacaoInput = document.getElementById(
            "motivo_desativacao"
        );
        const confirmarDesativacaoBtn = document.getElementById(
            "btn-confirmar-desativacao"
        );

        let modalDesativarInstance = null;
        if (
            modalDesativarEl &&
            typeof bootstrap !== "undefined" &&
            bootstrap.Modal
        ) {
            modalDesativarInstance = typeof bootstrap.Modal.getOrCreateInstance ===
            "function"
                ? bootstrap.Modal.getOrCreateInstance(modalDesativarEl)
                : new bootstrap.Modal(modalDesativarEl);
        }

        const modalConfig = modalDesativarInstance
            ? {
                  element: modalDesativarEl,
                  instance: modalDesativarInstance,
                  motivoInput: motivoDesativacaoInput,
                  confirmButton: confirmarDesativacaoBtn,
              }
            : null;

        initializeCollapseToggles();

        if (typeof applyDisplayMasks === "function") {
            applyDisplayMasks();
        }

        if (historicoApiUrl) {
            initializeHistoricoPaginado({
                apiUrl: historicoApiUrl,
                desativarTemplate: desativarHistoricoUrlTemplate,
                reativarTemplate: reativarHistoricoUrlTemplate,
                csrfToken,
                modal: modalConfig,
                storageKey: filtrosStorageKey,
            });
        } else {
            console.warn("URL da API do histórico não definida no dataset do body.");
        }

        initializeAdicionarEventoForm(
            addEventoApiUrl,
            tiposCodigosApiUrl,
            codigosPorTipoApiUrl,
            csrfToken
        );
    });

    function getCsrfToken() {
        const input = document.querySelector("[name=csrfmiddlewaretoken]");
        return input ? input.value : null;
    }

    function initializeCollapseToggles() {
        const toggles = document.querySelectorAll(".collapse-toggle");
        if (!toggles.length) {
            return;
        }

        const obterStoragePrefix = () => {
            if (typeof window === "undefined" || !window.localStorage) {
                return null;
            }

            const alunoIdDataset = document.body?.dataset?.alunoId || "";
            return alunoIdDataset
                ? `alunoDetalhesCollapse:${alunoIdDataset}:`
                : "alunoDetalhesCollapse:global:";
        };

        const storagePrefix = obterStoragePrefix();

        const collapseRegistry = new Map();
        const expandirBtn = document.getElementById("btn-expandir-secoes");
        const recolherBtn = document.getElementById("btn-recolher-secoes");

        const atualizarControlesGlobais = () => {
            if (!collapseRegistry.size) {
                if (expandirBtn) {
                    expandirBtn.disabled = true;
                    expandirBtn.classList.remove("active");
                    expandirBtn.setAttribute("aria-pressed", "false");
                }
                if (recolherBtn) {
                    recolherBtn.disabled = true;
                    recolherBtn.classList.remove("active");
                    recolherBtn.setAttribute("aria-pressed", "false");
                }
                return;
            }

            let total = 0;
            let abertos = 0;
            collapseRegistry.forEach((_, target) => {
                total += 1;
                if (target.classList.contains("show")) {
                    abertos += 1;
                }
            });

            const todosAbertos = total > 0 && abertos === total;
            const todosFechados = total > 0 && abertos === 0;

            if (expandirBtn) {
                expandirBtn.disabled = todosAbertos;
                expandirBtn.classList.toggle("active", todosAbertos);
                expandirBtn.setAttribute(
                    "aria-pressed",
                    todosAbertos ? "true" : "false"
                );
            }

            if (recolherBtn) {
                recolherBtn.disabled = todosFechados;
                recolherBtn.classList.toggle("active", todosFechados);
                recolherBtn.setAttribute(
                    "aria-pressed",
                    todosFechados ? "true" : "false"
                );
            }
        };

        const atualizarChevron = (toggleEl, expandido) => {
            const chevron = toggleEl?.querySelector(".chevron");
            if (!chevron) {
                return;
            }
            chevron.textContent = expandido ? "\u25BC" : "\u25B6";
        };

        const persistirEstado = (storageKey, estado) => {
            if (!storageKey) {
                return;
            }

            try {
                window.localStorage.setItem(storageKey, estado);
            } catch (error) {
                console.warn(
                    "Não foi possível persistir o estado da seção recolhível:",
                    error
                );
            }
        };

        const restaurarEstado = (target, storageKey) => {
            if (!storageKey) {
                return;
            }

            try {
                const estado = window.localStorage.getItem(storageKey);
                if (!estado) {
                    return;
                }

                const possuiBootstrap =
                    typeof bootstrap !== "undefined" && bootstrap.Collapse;

                if (estado === "shown") {
                    if (possuiBootstrap) {
                        const instance =
                            typeof bootstrap.Collapse.getOrCreateInstance === "function"
                                ? bootstrap.Collapse.getOrCreateInstance(target, {
                                      toggle: false,
                                  })
                                : new bootstrap.Collapse(target, { toggle: false });
                        instance.show();
                    } else {
                        target.classList.add("show");
                    }
                } else if (estado === "hidden") {
                    if (possuiBootstrap) {
                        const instance =
                            typeof bootstrap.Collapse.getOrCreateInstance === "function"
                                ? bootstrap.Collapse.getOrCreateInstance(target, {
                                      toggle: false,
                                  })
                                : new bootstrap.Collapse(target, { toggle: false });
                        instance.hide();
                    } else {
                        target.classList.remove("show");
                    }
                }
            } catch (error) {
                console.warn(
                    "Não foi possível restaurar o estado da seção recolhível:",
                    error
                );
            }
        };

        toggles.forEach((toggle) => {
            const targetSelector =
                toggle.getAttribute("href") || toggle.dataset.bsTarget || null;
            if (!targetSelector) {
                return;
            }

            const target = document.querySelector(targetSelector);
            if (!target) {
                return;
            }

            const storageKey =
                storagePrefix && (target.id || targetSelector)
                    ? `${storagePrefix}${target.id || targetSelector}`
                    : null;

            collapseRegistry.set(target, {
                toggle,
                storageKey,
            });

            const atualizarEspecifico = () => {
                const expandido = target.classList.contains("show");
                atualizarChevron(toggle, expandido);
                persistirEstado(storageKey, expandido ? "shown" : "hidden");
            };

            if (typeof bootstrap !== "undefined" && bootstrap.Collapse) {
                target.addEventListener("shown.bs.collapse", () => {
                    atualizarChevron(toggle, true);
                    persistirEstado(storageKey, "shown");
                    atualizarControlesGlobais();
                });
                target.addEventListener("hidden.bs.collapse", () => {
                    atualizarChevron(toggle, false);
                    persistirEstado(storageKey, "hidden");
                    atualizarControlesGlobais();
                });
            }

            toggle.addEventListener("click", () => {
                setTimeout(atualizarEspecifico, 150);
            });

            restaurarEstado(target, storageKey);
            atualizarChevron(toggle, target.classList.contains("show"));
            atualizarControlesGlobais();
        });

        const obterBootstrapCollapse = (element) => {
            if (typeof bootstrap === "undefined" || !bootstrap.Collapse) {
                return null;
            }

            if (typeof bootstrap.Collapse.getOrCreateInstance === "function") {
                return bootstrap.Collapse.getOrCreateInstance(element, {
                    toggle: false,
                });
            }

            return new bootstrap.Collapse(element, { toggle: false });
        };

        const expandirTudo = () => {
            collapseRegistry.forEach(({ toggle, storageKey }, target) => {
                const instancia = obterBootstrapCollapse(target);
                if (instancia) {
                    instancia.show();
                } else {
                    target.classList.add("show");
                }
                atualizarChevron(toggle, true);
                persistirEstado(storageKey, "shown");
            });
            atualizarControlesGlobais();
        };

        const recolherTudo = () => {
            collapseRegistry.forEach(({ toggle, storageKey }, target) => {
                const instancia = obterBootstrapCollapse(target);
                if (instancia) {
                    instancia.hide();
                } else {
                    target.classList.remove("show");
                }
                atualizarChevron(toggle, false);
                persistirEstado(storageKey, "hidden");
            });
            atualizarControlesGlobais();
        };

        if (expandirBtn) {
            expandirBtn.addEventListener("click", expandirTudo);
        }

        if (recolherBtn) {
            recolherBtn.addEventListener("click", recolherTudo);
        }

        atualizarControlesGlobais();
    }

    function initializeHistoricoPaginado({
        apiUrl,
        desativarTemplate = null,
        reativarTemplate = null,
        csrfToken = null,
        modal = null,
        storageKey = null,
    }) {
        if (!apiUrl) {
            return;
        }

        const btnCarregar = document.getElementById("btn-carregar-historico");
        const btnCarregarMais = document.getElementById(
            "btn-carregar-mais-historico"
        );
        const statusEl = document.getElementById("historico-status");
        const timelineContainer = document.getElementById(
            "historico-timeline-container"
        );
        const placeholder = document.getElementById("historico-placeholder");
        const filtroTipoSelect = document.getElementById("timeline-filter-tipo");
        const filtroAnoSelect = document.getElementById("timeline-filter-ano");
        const resetFiltrosBtn = document.getElementById("timeline-reset-filtros");
    const filtroStatusSelect = document.getElementById("timeline-filter-status");

        const podeGerenciarHistorico = Boolean(
            desativarTemplate && reativarTemplate && csrfToken
        );

        const modalConfig = modal || null;
        const filtrosStorageKey =
            typeof storageKey === "string" && storageKey.length > 0
                ? storageKey
                : null;

        const modalState = {
            registroId: null,
            botao: null,
        };

        if (modalConfig?.element) {
            modalConfig.element.addEventListener("hidden.bs.modal", () => {
                modalState.registroId = null;
                modalState.botao = null;
                if (modalConfig.motivoInput) {
                    modalConfig.motivoInput.value = "";
                }
            });
        }

    const processandoIds = new Set();
    let paginaInicialPreferida = 1;

        if (!timelineContainer) {
            console.warn("Elemento da timeline não encontrado.");
            return;
        }

        const state = {
            paginaAtual: 0,
            totalPaginas: 1,
            totalRegistros: 0,
            carregando: false,
            pageSize: 25,
            itens: [],
            filtros: {
                tipo: "",
                ano: "",
                status: "",
            },
            tiposDisponiveis: new Set(),
            anosDisponiveis: new Set(),
            idsCarregados: new Set(),
        };

        timelineContainer.classList.remove("d-none");

    carregarFiltrosPersistidos();

        function persistirFiltros() {
            if (!filtrosStorageKey || typeof window === "undefined") {
                return;
            }

            try {
                const paginaPersistida = Number(state.paginaAtual) || 1;

                window.localStorage.setItem(
                    filtrosStorageKey,
                    JSON.stringify({
                        tipo: state.filtros.tipo || "",
                        ano: state.filtros.ano || "",
                        status: state.filtros.status || "",
                        pagina: paginaPersistida,
                    })
                );
            } catch (error) {
                console.warn(
                    "Não foi possível persistir os filtros da timeline:",
                    error
                );
            }
        }

        function limparFiltrosPersistidos() {
            if (!filtrosStorageKey || typeof window === "undefined") {
                return;
            }

            try {
                window.localStorage.removeItem(filtrosStorageKey);
                paginaInicialPreferida = 1;
            } catch (error) {
                console.warn(
                    "Não foi possível limpar os filtros armazenados da timeline:",
                    error
                );
            }
        }

        function carregarFiltrosPersistidos() {
            if (!filtrosStorageKey || typeof window === "undefined") {
                return;
            }

            try {
                const armazenados = window.localStorage.getItem(
                    filtrosStorageKey
                );
                if (!armazenados) {
                    return;
                }

                const valores = JSON.parse(armazenados);
                if (!valores || typeof valores !== "object") {
                    return;
                }

                if (typeof valores.tipo === "string") {
                    state.filtros.tipo = valores.tipo;
                    if (filtroTipoSelect) {
                        filtroTipoSelect.value = valores.tipo;
                    }
                }

                if (typeof valores.ano === "string") {
                    state.filtros.ano = valores.ano;
                    if (filtroAnoSelect) {
                        filtroAnoSelect.value = valores.ano;
                    }
                }

                if (typeof valores.status === "string") {
                    state.filtros.status = valores.status;
                    if (filtroStatusSelect) {
                        filtroStatusSelect.value = valores.status;
                    }
                }

                const paginaPersistida = parseInt(valores.pagina, 10);
                if (!Number.isNaN(paginaPersistida) && paginaPersistida > 0) {
                    paginaInicialPreferida = paginaPersistida;
                }
            } catch (error) {
                console.warn(
                    "Não foi possível carregar os filtros salvos da timeline:",
                    error
                );
            }
        }

        function resetarState({ clearFilters = false } = {}) {
            state.paginaAtual = 0;
            state.totalPaginas = 1;
            state.totalRegistros = 0;
            state.itens.length = 0;
            state.tiposDisponiveis.clear();
            state.anosDisponiveis.clear();
            state.idsCarregados.clear();
            if (clearFilters) {
                state.filtros.tipo = "";
                state.filtros.ano = "";
                state.filtros.status = "";

                if (filtroTipoSelect) {
                    filtroTipoSelect.value = "";
                }

                if (filtroAnoSelect) {
                    filtroAnoSelect.value = "";
                }

                if (filtroStatusSelect) {
                    filtroStatusSelect.value = "";
                }

                limparFiltrosPersistidos();
            }

            limparTimelineItens();
        }

        function limparTimelineItens() {
            const elementos = timelineContainer.querySelectorAll(
                ".timeline__item, .timeline__year"
            );
            elementos.forEach((el) => el.remove());
        }

        function atualizarBotoes() {
            if (btnCarregar) {
                btnCarregar.disabled = state.carregando;
            }

            if (!btnCarregarMais) {
                return;
            }

            btnCarregarMais.disabled = state.carregando;
            const deveMostrar = state.paginaAtual < state.totalPaginas;
            btnCarregarMais.classList.toggle("d-none", !deveMostrar);
        }

        function atualizarStatus(totalExibidos) {
            if (!statusEl) {
                return;
            }

            if (state.carregando && state.itens.length === 0) {
                statusEl.textContent = "Carregando eventos do histórico...";
                return;
            }

            if (state.itens.length === 0) {
                statusEl.textContent = "Nenhum evento encontrado para este aluno.";
                return;
            }

            const partes = [];
            partes.push(
                `Mostrando ${totalExibidos} de ${state.itens.length} eventos carregados`
            );

            if (state.totalRegistros > state.itens.length) {
                partes[0] += ` (${state.totalRegistros} no total)`;
            }

            partes.push(`Página ${state.paginaAtual} de ${state.totalPaginas}`);

            if (state.filtros.tipo) {
                partes.push(`Tipo: ${state.filtros.tipo}`);
            }

            if (state.filtros.ano) {
                partes.push(`Ano: ${state.filtros.ano}`);
            }

            if (state.filtros.status) {
                const descricaoStatus =
                    state.filtros.status === "ativos"
                        ? "Apenas ativos"
                        : "Apenas inativos";
                partes.push(`Status: ${descricaoStatus}`);
            }

            statusEl.textContent = partes.join(" • ");
        }

        function atualizarPlaceholder(tipo, mensagem) {
            if (!placeholder) {
                return;
            }

            placeholder.classList.remove(
                "d-none",
                "timeline__placeholder--error",
                "timeline__placeholder--empty"
            );
            placeholder.innerHTML = "";

            if (tipo === "loading") {
                placeholder.innerHTML = `
                    <div class="timeline__loading">
                        <div class="spinner-border spinner-border-sm text-primary" role="status" aria-hidden="true"></div>
                        <span>${mensagem}</span>
                    </div>
                `;
                timelineContainer.classList.add("timeline--loading", "timeline--empty");
            } else {
                placeholder.textContent = mensagem;
                timelineContainer.classList.remove("timeline--loading");

                if (tipo === "error") {
                    placeholder.classList.add("timeline__placeholder--error");
                }

                if (tipo === "empty") {
                    placeholder.classList.add("timeline__placeholder--empty");
                }

                timelineContainer.classList.add("timeline--empty");
            }
        }

        function ocultarPlaceholder() {
            if (!placeholder) {
                return;
            }

            placeholder.classList.add("d-none");
            placeholder.classList.remove(
                "timeline__placeholder--error",
                "timeline__placeholder--empty"
            );
            timelineContainer.classList.remove(
                "timeline--loading",
                "timeline--empty"
            );
        }

        function filtrarItens() {
            return state.itens.filter((item) => {
                const correspondeTipo = state.filtros.tipo
                    ? item.tipo === state.filtros.tipo
                    : true;
                const correspondeAno = state.filtros.ano
                    ? item.ano === state.filtros.ano
                    : true;
                let correspondeStatus = true;
                if (state.filtros.status === "ativos") {
                    correspondeStatus = item.ativo !== false;
                } else if (state.filtros.status === "inativos") {
                    correspondeStatus = item.ativo === false;
                }

                return correspondeTipo && correspondeAno && correspondeStatus;
            });
        }

        function renderizarItens() {
            const itensFiltrados = filtrarItens();
            limparTimelineItens();

            if (itensFiltrados.length === 0) {
                const mensagem = state.itens.length
                    ? "Nenhum evento corresponde aos filtros selecionados."
                    : "Nenhum evento encontrado para este aluno.";
                atualizarPlaceholder("empty", mensagem);
                return 0;
            }

            ocultarPlaceholder();

            let anoAtual = null;

            itensFiltrados.forEach((item) => {
                if (item.ano && item.ano !== anoAtual) {
                    anoAtual = item.ano;
                    timelineContainer.appendChild(criarElementoAno(item.ano));
                }

                timelineContainer.appendChild(criarElementoTimeline(item));
            });

            return itensFiltrados.length;
        }

        function criarElementoAno(ano) {
            const heading = document.createElement("div");
            heading.className = "timeline__year";
            heading.textContent = ano;
            return heading;
        }

        function criarElementoTimeline(item) {
            const wrapper = document.createElement("article");
            wrapper.className = "timeline__item";
            wrapper.dataset.tipo = slugify(item.tipo || "");
            wrapper.dataset.ano = item.ano || "";

            if (item.ativo === false) {
                wrapper.classList.add("timeline__item--inativo");
            }

            const header = document.createElement("div");
            header.className = "timeline__header";

            const headerLeft = document.createElement("div");
            headerLeft.className = "timeline__header-left";

            const badge = document.createElement("span");
            badge.className = "timeline__badge";
            if (item.ativo === false) {
                badge.classList.add("timeline__badge--inativo");
            }
            badge.textContent = item.tipo || "Tipo não informado";
            headerLeft.appendChild(badge);

            const titulo = document.createElement("h3");
            titulo.className = "timeline__title";
            titulo.textContent = item.codigo || "Código não informado";
            headerLeft.appendChild(titulo);

            if (item.descricao) {
                const descricao = document.createElement("span");
                descricao.className = "text-muted";
                descricao.textContent = item.descricao;
                headerLeft.appendChild(descricao);
            }

            header.appendChild(headerLeft);

            const headerRight = document.createElement("div");
            headerRight.className = "timeline__header-right";

            if (item.dataOsFormatada) {
                const dataBadge = document.createElement("span");
                dataBadge.innerHTML = `<i class="far fa-calendar-alt"></i> ${item.dataOsFormatada}`;
                headerRight.appendChild(dataBadge);
            }

            if (item.ordemServico) {
                const ordemServico = document.createElement("span");
                ordemServico.innerHTML = `<i class="fas fa-file-signature"></i> ${item.ordemServico}`;
                headerRight.appendChild(ordemServico);
            }

            const statusBadge = document.createElement("span");
            statusBadge.className = "timeline__status";
            if (item.ativo === false) {
                statusBadge.classList.add("timeline__status--inativo");
                statusBadge.innerHTML =
                    '<i class="fas fa-ban"></i> Registro inativo';
            } else {
                statusBadge.classList.add("timeline__status--ativo");
                statusBadge.innerHTML =
                    '<i class="fas fa-check-circle"></i> Registro ativo';
            }
            headerRight.appendChild(statusBadge);

            header.appendChild(headerRight);
            wrapper.appendChild(header);

            if (item.observacoes) {
                const detalhes = document.createElement("details");
                detalhes.className = "timeline__observacoes";

                const summary = document.createElement("summary");
                summary.textContent = "Observações";
                detalhes.appendChild(summary);

                const texto = document.createElement("div");
                texto.className = "timeline__observacoes-texto";
                texto.textContent = item.observacoes;
                detalhes.appendChild(texto);

                wrapper.appendChild(detalhes);
            }

            if (podeGerenciarHistorico) {
                const acoes = criarAcoesTimeline(item);
                if (acoes) {
                    wrapper.appendChild(acoes);
                }
            }

            return wrapper;
        }

        function criarAcoesTimeline(item) {
            const container = document.createElement("div");
            container.className = "timeline__actions";

            const adicionarBotao = ({
                classe,
                icone,
                texto,
                acao,
                handler,
            }) => {
                const botao = document.createElement("button");
                botao.type = "button";
                botao.className = `btn btn-sm ${classe} timeline__action`;
                botao.innerHTML = `<i class="${icone}"></i> ${texto}`;
                botao.setAttribute("data-acao", acao);
                container.appendChild(botao);
                if (typeof handler === "function") {
                    botao.addEventListener("click", (event) => {
                        handler(event, botao);
                    });
                }
                return botao;
            };

            if (item.ativo !== false) {
                const botaoDesativar = adicionarBotao({
                    classe: "btn-outline-danger",
                    icone: "fas fa-ban",
                    texto: "Desativar",
                    acao: "desativar",
                    handler: (_, referenciaBotao) => {
                        abrirModalDesativacao(item, referenciaBotao);
                    },
                });
            } else {
                const botaoReativar = adicionarBotao({
                    classe: "btn-outline-success",
                    icone: "fas fa-undo-alt",
                    texto: "Reativar",
                    acao: "reativar",
                    handler: (_, referenciaBotao) => {
                        executarAcaoHistorico({
                            id: item.id,
                            acao: "reativar",
                            botao: referenciaBotao,
                        });
                    },
                });
            }

            return container.childElementCount ? container : null;
        }

        function abrirModalDesativacao(item, botaoReferencia) {
            if (!podeGerenciarHistorico) {
                return;
            }

            if (modalConfig?.instance) {
                modalState.registroId = item.id;
                modalState.botao = botaoReferencia || null;
                if (modalConfig.motivoInput) {
                    modalConfig.motivoInput.value = "";
                }

                requestAnimationFrame(() => {
                    if (modalConfig?.motivoInput) {
                        modalConfig.motivoInput.focus();
                    }
                });

                modalConfig.instance.show();
                return;
            }

            const motivoPrompt = window.prompt(
                "Deseja registrar um motivo para a desativação?",
                ""
            );

            if (motivoPrompt === null) {
                return;
            }

            executarAcaoHistorico({
                id: item.id,
                acao: "desativar",
                motivo: (motivoPrompt || "").trim(),
                botao: botaoReferencia || null,
            });
        }

        function atualizarFiltrosDisponiveis() {
            let filtrosAlterados = false;
            if (filtroTipoSelect) {
                const valorAtual = state.filtros.tipo;
                filtroTipoSelect.innerHTML = "<option value=\"\">Todos os tipos</option>";

                const tiposOrdenados = Array.from(state.tiposDisponiveis).sort((a, b) =>
                    a.localeCompare(b, "pt-BR")
                );

                tiposOrdenados.forEach((tipo) => {
                    const option = document.createElement("option");
                    option.value = tipo;
                    option.textContent = tipo;
                    if (valorAtual === tipo) {
                        option.selected = true;
                    }
                    filtroTipoSelect.appendChild(option);
                });

                if (valorAtual && !state.tiposDisponiveis.has(valorAtual)) {
                    state.filtros.tipo = "";
                    filtroTipoSelect.value = "";
                    filtrosAlterados = true;
                }
            }

            if (filtroAnoSelect) {
                const valorAtualAno = state.filtros.ano;
                filtroAnoSelect.innerHTML = "<option value=\"\">Todos os anos</option>";

                const anosOrdenados = Array.from(state.anosDisponiveis)
                    .map((ano) => ano)
                    .sort((a, b) => Number(b) - Number(a));

                anosOrdenados.forEach((ano) => {
                    const option = document.createElement("option");
                    option.value = ano;
                    option.textContent = ano;
                    if (valorAtualAno === ano) {
                        option.selected = true;
                    }
                    filtroAnoSelect.appendChild(option);
                });

                if (valorAtualAno && !state.anosDisponiveis.has(valorAtualAno)) {
                    state.filtros.ano = "";
                    filtroAnoSelect.value = "";
                    filtrosAlterados = true;
                }
            }

            if (filtrosAlterados) {
                persistirFiltros();
            }
        }

        function registrarListenersFiltros() {
            if (filtroTipoSelect) {
                filtroTipoSelect.addEventListener("change", () => {
                    state.filtros.tipo = filtroTipoSelect.value;
                    state.paginaAtual = 1;
                    const exibidos = renderizarItens();
                    atualizarStatus(exibidos);
                    persistirFiltros();
                });
            }

            if (filtroAnoSelect) {
                filtroAnoSelect.addEventListener("change", () => {
                    state.filtros.ano = filtroAnoSelect.value;
                    state.paginaAtual = 1;
                    const exibidos = renderizarItens();
                    atualizarStatus(exibidos);
                    persistirFiltros();
                });
            }

            if (filtroStatusSelect) {
                filtroStatusSelect.addEventListener("change", () => {
                    state.filtros.status = filtroStatusSelect.value;
                    state.paginaAtual = 1;
                    const exibidos = renderizarItens();
                    atualizarStatus(exibidos);
                    persistirFiltros();
                });
            }

            if (resetFiltrosBtn) {
                resetFiltrosBtn.addEventListener("click", () => {
                    state.filtros.tipo = "";
                    state.filtros.ano = "";
                    state.filtros.status = "";
                    state.paginaAtual = 0;
                    if (filtroTipoSelect) {
                        filtroTipoSelect.value = "";
                    }
                    if (filtroAnoSelect) {
                        filtroAnoSelect.value = "";
                    }
                    if (filtroStatusSelect) {
                        filtroStatusSelect.value = "";
                    }
                    const exibidos = renderizarItens();
                    atualizarStatus(exibidos);
                    limparFiltrosPersistidos();
                });
            }
        }

        function adicionarItens(resultados) {
            resultados.forEach((resultado) => {
                if (!resultado) {
                    return;
                }

                const ano = extrairAno(resultado.data_os);
                const item = {
                    id: resultado.id,
                    tipo: resultado.tipo_codigo || "Tipo não informado",
                    codigo: resultado.codigo || "Código não informado",
                    descricao: resultado.descricao || "",
                    dataOs: resultado.data_os || null,
                    dataOsFormatada: formatarDataISOParaBR(resultado.data_os),
                    ano,
                    ordemServico: resultado.ordem_servico || "",
                    observacoes: (resultado.observacoes || "").toString(),
                    ativo:
                        resultado.ativo !== undefined
                            ? Boolean(resultado.ativo)
                            : true,
                    createdAt: resultado.created_at || null,
                };

                if (state.idsCarregados.has(item.id)) {
                    return;
                }

                state.idsCarregados.add(item.id);
                state.itens.push(item);

                if (item.tipo) {
                    state.tiposDisponiveis.add(item.tipo);
                }

                if (ano) {
                    state.anosDisponiveis.add(ano);
                }
            });
        }

        function executarAcaoHistorico({ id, acao, motivo = "", botao = null }) {
            if (!podeGerenciarHistorico) {
                return;
            }

            const registroId = Number(id);
            if (Number.isNaN(registroId)) {
                return;
            }

            if (processandoIds.has(registroId)) {
                return;
            }

            const acaoNormalizada = acao === "desativar" ? "desativar" : "reativar";
            const template =
                acaoNormalizada === "desativar"
                    ? desativarTemplate
                    : reativarTemplate;

            if (!template) {
                return;
            }

            const url = template.replace("__ID__", encodeURIComponent(registroId));
            processandoIds.add(registroId);

            let restaurarBotao = null;
            if (botao) {
                const originalHtml = botao.innerHTML;
                const originalTitle = botao.getAttribute("title") || "";
                botao.disabled = true;
                botao.classList.add("timeline__action--loading");
                botao.innerHTML = `
                    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                    <span class="ms-2">Processando...</span>
                `;
                restaurarBotao = () => {
                    botao.disabled = false;
                    botao.classList.remove("timeline__action--loading");
                    botao.innerHTML = originalHtml;
                    if (originalTitle) {
                        botao.setAttribute("title", originalTitle);
                    } else {
                        botao.removeAttribute("title");
                    }
                };
            }

            const payload =
                acaoNormalizada === "desativar"
                    ? { motivo: motivo || null }
                    : {};

            fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Accept: "application/json",
                    "X-CSRFToken": csrfToken,
                },
                credentials: "same-origin",
                body: JSON.stringify(payload),
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error(`Status ${response.status}`);
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data.status !== "success") {
                        const mensagemErro =
                            data.message ||
                            (data.errors
                                ? Object.values(data.errors).flat().join(" ")
                                : "Não foi possível concluir a ação.");
                        throw new Error(mensagemErro);
                    }

                    const registroAtualizado = data.registro || {};
                    const item = state.itens.find(
                        (historico) => Number(historico.id) === registroId
                    );

                    if (item) {
                        if (registroAtualizado.ativo !== undefined) {
                            item.ativo = Boolean(registroAtualizado.ativo);
                        }
                        if (registroAtualizado.observacoes !== undefined) {
                            item.observacoes = (
                                registroAtualizado.observacoes || ""
                            ).toString();
                        }
                    }

                    const exibidos = renderizarItens();
                    atualizarStatus(exibidos);

                    const mensagemSucesso =
                        acaoNormalizada === "desativar"
                            ? "Registro desativado com sucesso."
                            : "Registro reativado com sucesso.";
                    mostrarMensagem(mensagemSucesso, "success");
                })
                .catch((error) => {
                    console.error("Erro ao executar ação no histórico:", error);
                    const mensagemErro =
                        error && error.message && !error.message.startsWith("Status")
                            ? error.message
                            : "Não foi possível completar a ação. Tente novamente.";
                    mostrarMensagem(mensagemErro, "error");
                })
                .finally(() => {
                    processandoIds.delete(registroId);
                    if (restaurarBotao) {
                        restaurarBotao();
                    }
                    if (modalConfig?.instance && modalConfig.element) {
                        modalConfig.element.removeAttribute("data-registro-id");
                    }
                });
        }

        if (modalConfig?.confirmButton) {
            modalConfig.confirmButton.addEventListener("click", () => {
                if (!modalState.registroId) {
                    return;
                }

                const motivoInformado = modalConfig.motivoInput
                    ? modalConfig.motivoInput.value.trim()
                    : "";

                modalConfig.instance.hide();

                executarAcaoHistorico({
                    id: modalState.registroId,
                    acao: "desativar",
                    motivo: motivoInformado,
                    botao: modalState.botao,
                });
            });
        }

        function carregarPagina({
            paginaSolicitada,
            reset = false,
            clearFilters = false,
        } = {}) {
            if (state.carregando) {
                return Promise.resolve(null);
            }

            const pagina = Math.max(paginaSolicitada || state.paginaAtual + 1 || 1, 1);

            if (!reset && state.totalPaginas && pagina > state.totalPaginas) {
                return Promise.resolve(null);
            }

            state.carregando = true;
            atualizarBotoes();

            if (reset) {
                resetarState({ clearFilters });
            }

            if (reset || state.itens.length === 0) {
                atualizarPlaceholder("loading", "Carregando eventos do histórico...");
            }

            const url = `${apiUrl}?page=${pagina}&page_size=${state.pageSize}`;

            return fetch(url, {
                headers: {
                    Accept: "application/json",
                },
                credentials: "same-origin",
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error(`Status ${response.status}`);
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data.status !== "success") {
                        throw new Error(data.message || "Resposta inválida da API.");
                    }

                    adicionarItens(data.results || []);

                    state.paginaAtual = data.page || pagina;
                    state.totalPaginas = data.total_pages || 1;
                    state.totalRegistros = data.count || state.itens.length;

                    atualizarFiltrosDisponiveis();
                    const exibidos = renderizarItens();
                    atualizarStatus(exibidos);

                    persistirFiltros();
                })
                .catch((error) => {
                    console.error("Erro ao carregar histórico do aluno:", error);
                    atualizarPlaceholder(
                        "error",
                        "Não foi possível carregar os eventos do histórico."
                    );
                    if (statusEl) {
                        statusEl.textContent =
                            "Houve um erro ao consultar o histórico. Tente novamente.";
                    }
                })
                .finally(() => {
                    state.carregando = false;
                    atualizarBotoes();
                });
        }

        function registrarBotoes() {
            if (btnCarregar) {
                btnCarregar.addEventListener("click", () => {
                    refreshHistorico({
                        preservePage: false,
                        preserveFilters: true,
                    });
                });
            }

            if (btnCarregarMais) {
                btnCarregarMais.addEventListener("click", () => {
                    carregarPagina({ paginaSolicitada: state.paginaAtual + 1 });
                });
            }
        }

        function refreshHistorico({
            targetPage = null,
            preservePage = false,
            preserveFilters = true,
        } = {}) {
            const paginaDestino = targetPage
                ? Math.max(targetPage, 1)
                : preservePage
                ? Math.max(state.paginaAtual || 1, 1)
                : 1;
            const deveResetar =
                targetPage !== null || !preservePage || state.itens.length === 0;
            const limparFiltros = !preserveFilters;

            if (!deveResetar) {
                return carregarPagina({
                    paginaSolicitada: paginaDestino,
                    reset: false,
                    clearFilters: limparFiltros,
                });
            }

            const paginaFinal = Math.max(paginaDestino, 1);
            let promise = Promise.resolve();

            for (let pagina = 1; pagina <= paginaFinal; pagina += 1) {
                promise = promise.then(() =>
                    carregarPagina({
                        paginaSolicitada: pagina,
                        reset: pagina === 1,
                        clearFilters: pagina === 1 ? limparFiltros : false,
                    })
                );
            }

            return promise;
        }

        registrarListenersFiltros();
        registrarBotoes();

        window.refreshHistoricoTimeline = refreshHistorico;

        refreshHistorico({
            targetPage: paginaInicialPreferida,
            preservePage: paginaInicialPreferida > 1,
            preserveFilters: true,
        });
    }

    function initializeAdicionarEventoForm(
        addEventoApiUrl,
        tiposCodigosApiUrl,
        codigosPorTipoApiUrl,
        csrfToken
    ) {
        const form = document.getElementById("form-adicionar-evento");
        if (!form) {
            console.warn("Formulário de adição de evento não encontrado na página.");
            return;
        }

        const tipoEventoSelect = document.getElementById("tipo_evento");
        const codigoEventoSelect = document.getElementById("codigo_evento");

        if (tiposCodigosApiUrl && tipoEventoSelect) {
            carregarTiposCodigos(tiposCodigosApiUrl).catch((error) => {
                console.error("Erro ao carregar tipos de códigos:", error);
            });
        }

        if (tipoEventoSelect) {
            tipoEventoSelect.addEventListener("change", function () {
                const tipoId = this.value;
                const tooltipCodigo = document.getElementById(
                    "tooltip-codigo-evento"
                );

                if (tipoId && codigosPorTipoApiUrl) {
                    carregarCodigosPorTipo(tipoId, codigosPorTipoApiUrl)
                        .then(() => {
                            if (codigoEventoSelect) {
                                codigoEventoSelect.disabled = false;
                            }
                        })
                        .catch((error) => {
                            console.error("Erro ao carregar códigos pelo tipo:", error);
                        });
                } else if (codigoEventoSelect) {
                    codigoEventoSelect.innerHTML = "<option value=\"\">Selecione</option>";
                    codigoEventoSelect.disabled = true;
                }

                const selectedOption = this.options[this.selectedIndex];
                const descricao = selectedOption
                    ? selectedOption.getAttribute("data-descricao")
                    : "";
                const tooltipTexto = document.getElementById("tooltip-tipo-evento");
                if (tooltipTexto) {
                    tooltipTexto.textContent =
                        descricao || "Descrição não disponível";
                }

                if (tooltipCodigo) {
                    tooltipCodigo.textContent = "Selecione primeiro o tipo de evento";
                }
            });
        }

        if (codigoEventoSelect) {
            codigoEventoSelect.addEventListener("change", function () {
                const selectedOption = this.options[this.selectedIndex];
                const descricao = selectedOption
                    ? selectedOption.getAttribute("data-descricao")
                    : "";
                const tooltip = document.getElementById("tooltip-codigo-evento");
                if (tooltip) {
                    tooltip.textContent = descricao || "Descrição não disponível";
                }
            });
        }

        if (!addEventoApiUrl || !csrfToken) {
            return;
        }

        form.addEventListener("submit", (event) => {
            event.preventDefault();
            adicionarEventoHistorico(addEventoApiUrl, csrfToken);
        });
    }

    function carregarTiposCodigos(tiposCodigosApiUrl) {
        return fetch(tiposCodigosApiUrl, {
            headers: {
                Accept: "application/json",
            },
            credentials: "same-origin",
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`Status ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                if (data.status !== "success") {
                    throw new Error(data.message || "Não foi possível carregar os tipos.");
                }

                const select = document.getElementById("tipo_evento");
                if (!select) {
                    return;
                }

                select.innerHTML = "<option value=\"\">Selecione</option>";

                data.tipos.forEach((tipo) => {
                    const option = document.createElement("option");
                    option.value = tipo.id;
                    option.textContent = tipo.nome;
                    option.setAttribute("data-descricao", tipo.descricao || "");
                    select.appendChild(option);
                });
            });
    }

    function carregarCodigosPorTipo(tipoId, codigosPorTipoApiUrl) {
        const url = `${codigosPorTipoApiUrl}?tipo_id=${encodeURIComponent(tipoId)}`;
        return fetch(url, {
            headers: {
                Accept: "application/json",
            },
            credentials: "same-origin",
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`Status ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                if (data.status !== "success") {
                    throw new Error(
                        data.message || "Não foi possível carregar os códigos deste tipo."
                    );
                }

                const select = document.getElementById("codigo_evento");
                if (!select) {
                    return;
                }

                select.innerHTML = "<option value=\"\">Selecione</option>";

                data.codigos.forEach((codigo) => {
                    const option = document.createElement("option");
                    option.value = codigo.id;
                    option.textContent = codigo.nome;
                    option.setAttribute("data-descricao", codigo.descricao || "");
                    select.appendChild(option);
                });
            });
    }

    function adicionarEventoHistorico(addEventoApiUrl, csrfToken) {
        const form = document.getElementById("form-adicionar-evento");
        if (!form) {
            return;
        }

        const formData = new FormData(form);
        const tipoEventoSelect = document.getElementById("tipo_evento");
        const codigoEventoSelect = document.getElementById("codigo_evento");

            const payload = {
                aluno_id: formData.get("aluno_id"),
                tipo_evento: obterTextoSelecionadoOuNull("tipo_evento"),
                codigo_id: formData.get("codigo_evento"),
                ordem_servico: formData.get("ordem_servico"),
                data_os: formData.get("data_os"),
                data_evento: formData.get("data_evento"),
                observacoes: formData.get("observacoes"),
            };

        fetch(addEventoApiUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
                Accept: "application/json",
            },
            credentials: "same-origin",
            body: JSON.stringify(payload),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.status === "success") {
                    mostrarMensagem("Evento adicionado com sucesso!", "success");
                    form.reset();

                    if (codigoEventoSelect) {
                        codigoEventoSelect.disabled = true;
                    }

                    const tooltipTipo = document.getElementById("tooltip-tipo-evento");
                    const tooltipCodigo = document.getElementById("tooltip-codigo-evento");
                    if (tooltipTipo) {
                        tooltipTipo.textContent =
                            "Selecione o tipo de evento para ver a descrição";
                    }
                    if (tooltipCodigo) {
                        tooltipCodigo.textContent =
                            "Selecione primeiro o tipo de evento";
                    }

                    if (typeof window.refreshHistoricoTimeline === "function") {
                        window.refreshHistoricoTimeline({ preservePage: false });
                    }

                                atualizarEventosRecentesNaTabela(data.registro, {
                        tipoEvento:
                            data.tipo_evento ||
                            (tipoEventoSelect
                                ? tipoEventoSelect.options[tipoEventoSelect.selectedIndex].text
                                : "-"),
                        codigoTexto:
                            data.registro?.codigo_nome ||
                            (codigoEventoSelect
                                ? codigoEventoSelect.options[codigoEventoSelect.selectedIndex]
                                        ?.text
                                : "-"),
                                    dataOs: formData.get("data_os"),
                                    dataEvento: formData.get("data_evento"),
                        observacoes: formData.get("observacoes"),
                    });
                } else {
                    const mensagem =
                        data.message ||
                        (data.errors
                            ? Object.values(data.errors).flat().join(" ")
                            : "Verifique os campos obrigatórios.");
                    mostrarMensagem(`Erro ao adicionar evento: ${mensagem}`, "error");
                }
            })
            .catch((error) => {
                console.error("Erro na submissão do evento:", error);
                mostrarMensagem(
                    "Ocorreu um erro de comunicação com o servidor.",
                    "error"
                );
            });
    }

    function mostrarMensagem(mensagem, tipo) {
        const alertClass = tipo === "success" ? "alert-success" : "alert-danger";
        const flashContainer = document.getElementById("timeline-flash-container");

        if (flashContainer) {
            const toast = document.createElement("div");
            toast.className = `timeline-toast alert ${alertClass} alert-dismissible fade`;
            toast.setAttribute("role", "alert");
            toast.innerHTML = `
                <div class="timeline-toast__content">${mensagem}</div>
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
            `;

            flashContainer.appendChild(toast);

            requestAnimationFrame(() => {
                toast.classList.add("show");
            });

            const maxToasts = 3;
            while (flashContainer.childElementCount > maxToasts) {
                const primeiroToast = flashContainer.firstElementChild;
                if (primeiroToast) {
                    if (typeof bootstrap !== "undefined" && bootstrap.Alert) {
                        const bsPrimeiro = bootstrap.Alert.getOrCreateInstance(
                            primeiroToast
                        );
                        bsPrimeiro.close();
                    } else {
                        primeiroToast.remove();
                    }
                } else {
                    break;
                }
            }

            setTimeout(() => {
                if (!flashContainer.contains(toast)) {
                    return;
                }

                if (typeof bootstrap !== "undefined" && bootstrap.Alert) {
                    const bsAlert = bootstrap.Alert.getOrCreateInstance(toast);
                    bsAlert.close();
                } else {
                    toast.classList.remove("show");
                    setTimeout(() => toast.remove(), 150);
                }
            }, 5000);

            return;
        }

        const form = document.getElementById("form-adicionar-evento");
        if (form) {
            const alertHtml = `
                <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
                    ${mensagem}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Fechar"></button>
                </div>
            `;

            const alertWrapper = document.createElement("div");
            alertWrapper.innerHTML = alertHtml;
            const alertElement = alertWrapper.firstElementChild;

            form.insertAdjacentElement("beforebegin", alertElement);

            setTimeout(() => {
                if (!alertElement || !alertElement.parentElement) {
                    return;
                }

                if (typeof bootstrap !== "undefined" && bootstrap.Alert) {
                    const bsAlert = bootstrap.Alert.getOrCreateInstance(alertElement);
                    bsAlert.close();
                } else {
                    alertElement.classList.remove("show");
                    setTimeout(() => alertElement.remove(), 150);
                }
            }, 5000);

            return;
        }

        if (typeof window !== "undefined" && typeof window.alert === "function") {
            window.alert(mensagem);
        }
    }

    function atualizarEventosRecentesNaTabela(registro, contexto = {}) {
        const tabela = document.getElementById("lista-eventos-recentes");
        if (!tabela) {
            return;
        }

        const placeholder = tabela.querySelector(".timeline-placeholder-row");
        if (placeholder) {
            placeholder.remove();
        }

        const linha = document.createElement("tr");

            const tipo = contexto.tipoEvento || "-";
            const codigoTexto = contexto.codigoTexto || "-";
            const dataOsIso = contexto.dataOs || registro?.data_os || null;
            const dataEventoIso =
                contexto.dataEvento || registro?.data_evento || contexto.dataOs || null;
            const dataOsFormatada = dataOsIso
                ? formatarDataISOParaBR(dataOsIso)
                : "-";
            const dataEventoFormatada = dataEventoIso
                ? formatarDataISOParaBR(dataEventoIso)
                : "-";
            const observacoes = (contexto.observacoes || registro?.observacoes || "-")
                .toString()
                .trim();

        const celulas = [
            { texto: tipo },
            { texto: codigoTexto, titulo: codigoTexto },
                    { texto: dataOsFormatada },
                    { texto: dataEventoFormatada },
            { texto: observacoes || "-", titulo: observacoes || "-" },
        ];

        celulas.forEach((celula) => {
            const td = document.createElement("td");
            td.textContent = celula.texto;
            if (celula.titulo) {
                td.title = celula.titulo;
            }
            linha.appendChild(td);
        });

        tabela.insertBefore(linha, tabela.firstChild);

        const linhas = tabela.querySelectorAll("tr");
        if (linhas.length > 5) {
            tabela.removeChild(linhas[linhas.length - 1]);
        }
    }

    function obterTextoSelecionadoOuNull(selectId) {
        const select = document.getElementById(selectId);
        if (!select) {
            return null;
        }
        const option = select.options[select.selectedIndex];
        return option ? option.text : null;
    }

    function slugify(valor) {
        return (valor || "")
            .toString()
            .normalize("NFD")
            .replace(/[^\p{Letter}\p{Number}]+/gu, "-")
            .replace(/(^-|-$)/g, "")
            .toLowerCase();
    }

    function formatarDataISOParaBR(dataIso) {
        if (!dataIso) {
            return "";
        }

        const data = new Date(dataIso);
        if (Number.isNaN(data.getTime())) {
            return "";
        }

        return data.toLocaleDateString("pt-BR", {
            timeZone: "UTC",
        });
    }

    function extrairAno(dataIso) {
        if (!dataIso) {
            return "";
        }
        const data = new Date(dataIso);
        if (Number.isNaN(data.getTime())) {
            return "";
        }
        return String(data.getUTCFullYear());
    }
})();
