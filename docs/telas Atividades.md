<main id="main-content" class="py-4">

`    `<div class="container mt-4">

`        `<!-- Cabeçalho com título e botões na mesma linha -->

`        `<div class="d-flex justify-content-between align-items-center mb-3">

`            `<h1>Lista de Atividades Acadêmicas</h1>

`            `<div class="btn-group">

`                `<a href="/" class="btn btn-secondary me-2">Página Inicial</a>



`                `<!-- Botão para criar nova atividade acadêmica com URL de retorno -->

`                `<a href="/atividades/academicas/criar/?return\_url=/atividades/academicas/" class="btn btn-primary me-2">

`                    `<i class="fas fa-plus"></i> Nova Atividade

`                `</a>



`                `<!-- Botões para as novas funcionalidades -->

`                `<a href="/atividades/calendario/" class="btn btn-info me-2">

`                    `<i class="fas fa-calendar-alt"></i> Calendário

`                `</a>



`                `<a href="/atividades/dashboard/" class="btn btn-success me-2">

`                    `<i class="fas fa-chart-bar"></i> Dashboard

`                `</a>



`                `<a href="/atividades/relatorio/" class="btn btn-warning">

`                    `<i class="fas fa-file-alt"></i> Relatórios

`                `</a>

`            `</div>

`        `</div>



`        `<!-- Barra de busca e filtros -->

`        `<div class="card mb-4">

`            `<div class="card-header">

`                `<form method="get" class="row g-3">

`                    `<div class="col-md-6">

`                        `<input type="text" name="q" class="form-control" placeholder="Buscar por título, descrição ou responsável..." value="">

`                    `</div>

`                    `<div class="col-md-2">

`                        `<button type="submit" class="btn btn-primary w-100">Filtrar</button>

`                    `</div>

`                `</form>

`            `</div>

`            `<div class="card-body">

`                `<div class="table-responsive">

`                    `<table class="table table-striped">

`                        `<thead>

`                            `<tr>

`                                `<th>Título</th>

`                                `<th>Responsável</th>

`                                `<th>Data de Início</th>

`                                `<th>Status</th>

`                                `<th>Turmas</th>

`                                `<th>Ações</th>

`                            `</tr>

`                        `</thead>

`                        `<tbody>

`                            `<tr>

`                                `<td>Plenilúnio</td>

`                                `<td>Não informado</td>

`                                `<td>26/10/2026</td>

`                                `<td>

`                                    `<span class="badge bg-warning">

`                                        `Agendada

`                                    `</span>

`                                `</td>

`                                `<td>

`                                    `Turma A

`                                `</td>

`                                `<td>

`                                    `<a href="/atividades/academicas/detalhar/2/" class="btn btn-sm btn-info" title="Ver detalhes completos da atividade">Detalhes</a>

`                                    `<a href="/atividades/academicas/editar/2/" class="btn btn-sm btn-warning" title="Editar informações da atividade">Editar</a>

`                                    `<a href="/atividades/academicas/excluir/2/" class="btn btn-sm btn-danger" title="Excluir esta atividade">Excluir</a>

`                                    `<a href="/atividades/academicas/2/copiar/" class="btn btn-sm btn-secondary" title="Criar uma cópia desta atividade">Copiar</a>

`                                `</td>

`                            `</tr>

`                            `<tr>

`                                `<td>Aula</td>

`                                `<td>Não informado</td>

`                                `<td>26/10/2024</td>

`                                `<td>

`                                    `<span class="badge bg-warning">

`                                        `Agendada

`                                    `</span>

`                                `</td>

`                                `<td>

`                                    `Turma A

`                                `</td>

`                                `<td>

`                                    `<a href="/atividades/academicas/detalhar/1/" class="btn btn-sm btn-info" title="Ver detalhes completos da atividade">Detalhes</a>

`                                    `<a href="/atividades/academicas/editar/1/" class="btn btn-sm btn-warning" title="Editar informações da atividade">Editar</a>

`                                    `<a href="/atividades/academicas/excluir/1/" class="btn btn-sm btn-danger" title="Excluir esta atividade">Excluir</a>

`                                    `<a href="/atividades/academicas/1/copiar/" class="btn btn-sm btn-secondary" title="Criar uma cópia desta atividade">Copiar</a>

`                                `</td>

`                            `</tr>

`                        `</tbody>

`                    `</table>

`                `</div>

`            `</div>

`            `<div class="card-footer">

`                `<p class="text-muted mb-0">Total: 2 atividade(s)</p>

`            `</div>

`        `</div>

`    `</div>

</main>

<body>

`    `<!-- Cabeçalho/Barra de Navegação -->

`    `<header>

`        `<nav class="navbar navbar-expand-lg navbar-dark bg-primary">

`            `<div class="container">

`                `<a class="navbar-brand" href="/">

`                    `<img src="/static/img/logo.png" alt="OMAUM Logo" height="40">

`                `</a>

`                `<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">

`                    `<span class="navbar-toggler-icon"></span>

`                `</button>



`                `<div class="collapse navbar-collapse" id="navbarNav">

`                    `<ul class="navbar-nav me-auto">

`                        `<li class="nav-item">

`                            `<a class="nav-link " href="/">

`                                `<i class="fas fa-home"></i> Início

`                            `</a>

`                        `</li>





`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/alunos/">

`                                    `<i class="fas fa-user-graduate"></i> Alunos

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/cursos/">

`                                    `<i class="fas fa-book"></i> Cursos

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/turmas/">

`                                    `<i class="fas fa-users"></i> Turmas

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/matriculas/">

`                                    `<i class="fas fa-clipboard-list"></i> Matrículas

`                                `</a>

`                            `</li>

`                            `<li class="nav-item dropdown">

`                                `<a class="nav-link dropdown-toggle" href="#" id="navbarDropdownAtividades" role="button" data-bs-toggle="dropdown" aria-expanded="false">

`                                   `<i class="fas fa-calendar-alt"></i> Atividades

`                                `</a>

`                                `<ul class="dropdown-menu" aria-labelledby="navbarDropdownAtividades">

`                                    `<li>

`                                        `<a class="dropdown-item" href="/atividades/academicas/">

`                                            `<i class="fas fa-school"></i> Acadêmicas

`                                        `</a>

`                                    `</li>

`                                    `<li>

`                                        `<a class="dropdown-item" href="/atividades/ritualisticas/">

`                                            `<i class="fas fa-pray"></i> Ritualísticas

`                                        `</a>

`                                    `</li>

`                                `</ul>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/frequencias/">

`                                    `<i class="fas fa-check-square"></i> Frequências

`                                `</a>

`                            `</li>



`                    `</ul>



`                    `<ul class="navbar-nav">





`                                `<li class="nav-item">

`                                    `<a class="nav-link" href="/painel-controle/">

`                                        `<i class="fas fa-cog"></i> Painel de Controle

`                                    `</a>

`                                `</li>



`                            `<li class="nav-item dropdown">

`                                `<a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">

`                                   `<i class="fas fa-user-circle"></i> lcsilv3

`                                `</a>

`                                `<ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">

`                                    `<li><a class="dropdown-item" href="#">Meu Perfil</a></li>

`                                    `<li><hr class="dropdown-divider"></li>

`                                    `<li>

`                                        `<form method="post" action="/sair/" class="d-inline">

`                                            `<input type="hidden" name="csrfmiddlewaretoken" value="6JIjlqgcbMPEz3xuixdQhr6ybdN0P9h3vJv6XYgzvaOzWHL4j5IvQpiEhocB4gIK">

`                                            `<button type="submit" class="dropdown-item">

`                                                `<i class="fas fa-sign-out-alt"></i> Sair

`                                            `</button>

`                                        `</form>

`                                    `</li>

`                                `</ul>

`                            `</li>



`                    `</ul>

`                `</div>

`            `</div>

`        `</nav>

`    `</header>



`    `<!-- Mensagens do sistema (flash messages) -->

`    `<div class="message-container">



`    `</div>



`    `<!-- Conteúdo principal -->

`    `<main id="main-content" class="py-4">



<div class="container mt-4">

`    `<div class="d-flex justify-content-between align-items-center mb-4">

`        `<h1>Nova Atividade Acadêmica</h1>

`        `<a href="/atividades/academicas/" class="btn btn-secondary me-2">Voltar</a>

`    `</div>







`    `<form method="post">

`        `<input type="hidden" name="csrfmiddlewaretoken" value="6JIjlqgcbMPEz3xuixdQhr6ybdN0P9h3vJv6XYgzvaOzWHL4j5IvQpiEhocB4gIK">





`        `<div class="card mb-4">

`            `<div class="card-header">

`                `<h5>Informações Básicas</h5>

`            `</div>

`            `<div class="card-body">

`                `<div class="row">

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_nome" class="form-label">Nome</label>

`    `<input type="text" name="nome" class="form-control" maxlength="100" required="" id="id\_nome">





</div>

`                    `</div>

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_responsavel" class="form-label">Responsável</label>

`    `<input type="text" name="responsavel" class="form-control" maxlength="100" id="id\_responsavel">





</div>

`                    `</div>

`                `</div>

`                `<div class="row">

`                    `<div class="col-md-12">

`                        `<div class="mb-3">

`    `<label for="id\_descricao" class="form-label">Descrição</label>

`    `<textarea name="descricao" cols="40" rows="3" class="form-control" id="id\_descricao"></textarea>





</div>

`                    `</div>

`                `</div>

`            `</div>

`        `</div>



`        `<div class="card mb-4">

`            `<div class="card-header">

`                `<h5>Data e Local</h5>

`            `</div>

`            `<div class="card-body">

`                `<div class="row">

`                    `<div class="col-md-3">

`                        `<div class="mb-3">

`    `<label for="id\_data\_inicio" class="form-label">Data de Início</label>

`    `<input type="date" name="data\_inicio" value="06/05/2025" class="form-control" required="" id="id\_data\_inicio"><input type="hidden" name="initial-data\_inicio" value="2025-05-06 12:23:08" id="initial-id\_data\_inicio">





</div>

`                    `</div>

`                    `<div class="col-md-3">

`                        `<div class="mb-3">

`    `<label for="id\_data\_fim" class="form-label">Data de Término</label>

`    `<input type="date" name="data\_fim" class="form-control" id="id\_data\_fim">





</div>

`                    `</div>

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_local" class="form-label">Local</label>

`    `<input type="text" name="local" class="form-control" maxlength="100" id="id\_local">





</div>

`                    `</div>

`                `</div>

`            `</div>

`        `</div>



`        `<!-- Nova seção para Turmas -->

`        `<div class="card mb-4">

`            `<div class="card-header">

`                `<h5>Turmas</h5>

`            `</div>

`            `<div class="card-body">

`                `<div class="row">

`                    `<div class="col-md-12">

`                        `<div class="mb-3">

`    `<label for="id\_turmas" class="form-label">Turmas</label>

`    `<select name="turmas" class="form-control select2-hidden-accessible" id="id\_turmas" multiple="" tabindex="-1" aria-hidden="true" data-select2-id="select2-data-id\_turmas">

`  `<option value="6">D - Introdução à Meditação</option>

`  `<option value="2">A - Introdução à Meditação</option>

`  `<option value="4">B - Introdução à Meditação</option>

`  `<option value="5">C - Introdução à Meditação</option>

</select><span class="select2 select2-container select2-container--bootstrap4" dir="ltr" data-select2-id="select2-data-8-0qng" style="width: 100%;"><span class="selection"><span class="select2-selection select2-selection--multiple" role="combobox" aria-haspopup="true" aria-expanded="false" tabindex="-1" aria-disabled="false"><ul class="select2-selection\_\_rendered" id="select2-id\_turmas-container"></ul><span class="select2-search select2-search--inline"><textarea class="select2-search\_\_field" type="search" tabindex="0" autocorrect="off" autocapitalize="none" spellcheck="false" role="searchbox" aria-autocomplete="list" autocomplete="off" aria-label="Search" aria-describedby="select2-id\_turmas-container" placeholder="Selecione as opções" style="width: 100%;"></textarea></span></span></span><span class="dropdown-wrapper" aria-hidden="true"></span></span><span class="select2 select2-container select2-container--bootstrap4 select2-hidden-accessible" dir="ltr" data-select2-id="select2-data-2-r7jm" style="width: 100%;" tabindex="-1" aria-hidden="true"><span class="selection"><span class="select2-selection select2-selection--single" role="combobox" aria-haspopup="true" aria-expanded="false" tabindex="0" aria-disabled="false" aria-labelledby="select2-oxpr-container" aria-controls="select2-oxpr-container"><span class="select2-selection\_\_rendered" id="select2-oxpr-container" role="textbox" aria-readonly="true"></span><span class="select2-selection\_\_arrow" role="presentation"><b role="presentation"></b></span></span></span><span class="dropdown-wrapper" aria-hidden="true"></span></span><span class="select2 select2-container select2-container--bootstrap4" dir="ltr" data-select2-id="select2-data-3-up2v" style="width: 100%;"><span class="selection"><span class="select2-selection select2-selection--single" role="combobox" aria-haspopup="true" aria-expanded="false" tabindex="0" aria-disabled="false" aria-labelledby="select2-cpo5-container" aria-controls="select2-cpo5-container"><span class="select2-selection\_\_rendered" id="select2-cpo5-container" role="textbox" aria-readonly="true"></span><span class="select2-selection\_\_arrow" role="presentation"><b role="presentation"></b></span></span></span><span class="dropdown-wrapper" aria-hidden="true"></span></span>





</div>

`                    `</div>

`                `</div>

`                `<div class="row mt-2">

`                    `<div class="col-md-12">

`                        `<div class="form-check">

`                            `<input type="checkbox" name="todas\_turmas" id="id\_todas\_turmas">

`                            `<label class="form-check-label" for="id\_todas\_turmas">

`                                `Aplicar a todas as turmas ativas

`                            `</label>

`                            `<small class="form-text text-muted">

`                                `Marque esta opção para aplicar esta atividade a todas as turmas ativas automaticamente.

`                            `</small>

`                        `</div>

`                    `</div>

`                `</div>

`            `</div>

`        `</div>



`        `<div class="card mb-4">

`            `<div class="card-header">

`                `<h5>Classificação</h5>

`            `</div>

`            `<div class="card-body">

`                `<div class="row">

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_tipo\_atividade" class="form-label">Tipo de Atividade</label>

`    `<select name="tipo\_atividade" class="form-control" id="id\_tipo\_atividade">

`  `<option value="aula" selected="">Aula</option>

`  `<option value="palestra">Palestra</option>

`  `<option value="workshop">Workshop</option>

`  `<option value="seminario">Seminário</option>

`  `<option value="outro">Outro</option>

</select>





</div>

`                    `</div>

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_status" class="form-label">Status</label>

`    `<select name="status" class="form-control" id="id\_status">

`  `<option value="agendada" selected="">Agendada</option>

`  `<option value="em\_andamento">Em Andamento</option>

`  `<option value="concluida">Concluída</option>

`  `<option value="cancelada">Cancelada</option>

</select>





</div>

`                    `</div>

`                `</div>

`            `</div>

`        `</div>



`        `<div class="d-flex justify-content-between mb-5">

`            `<!-- Use a URL de retorno fornecida pela view -->

`            `<a href="/atividades/academicas/" class="btn btn-secondary">Cancelar</a>

`            `<button type="submit" class="btn btn-primary">

`                `Criar Atividade

`            `</button>

`        `</div>

`    `</form>

</div>

`    `</main>



`    `<!-- Rodapé -->

`    `<footer class="footer mt-auto py-3 bg-light">

`        `<div class="container text-center">

`            `<span class="text-muted">© 2025 OMAUM - Sistema de Gestão de Iniciados</span>

`        `</div>

`    `</footer>



`    `<!-- Scripts de componentes globais -->

`    `<script src="/static/js/modules/dias-semana.js"></script>



`    `<!-- Scripts específicos da página -->



<script>

`    `document.addEventListener('DOMContentLoaded', function() {

`        `const todasTurmasCheckbox = document.getElementById('id\_todas\_turmas');

`        `const turmasSelect = document.getElementById('id\_turmas');



`        `function toggleTurmasField() {

`            `if (todasTurmasCheckbox.checked) {

`                `turmasSelect.disabled = true;

`                `// Adicionar uma mensagem informativa

`                `if (!document.getElementById('turmas-info')) {

`                    `const infoDiv = document.createElement('div');

`                    `infoDiv.id = 'turmas-info';

`                    `infoDiv.className = 'alert alert-info mt-2';

`                    `infoDiv.textContent = 'Todas as turmas ativas serão incluídas automaticamente.';

`                    `turmasSelect.parentNode.appendChild(infoDiv);

`                `}

`            `} else {

`                `turmasSelect.disabled = false;

`                `// Remover a mensagem informativa se existir

`                `const infoDiv = document.getElementById('turmas-info');

`                `if (infoDiv) {

`                    `infoDiv.remove();

`                `}

`            `}

`        `}



`        `// Inicializar

`        `toggleTurmasField();



`        `// Adicionar listener para mudanças

`        `todasTurmasCheckbox.addEventListener('change', toggleTurmasField);



`        `// Inicializar Select2 para o campo de turmas

`        `if (typeof $.fn.select2 === 'function') {

`            `$(turmasSelect).select2({

`                `theme: 'bootstrap4',

`                `placeholder: 'Selecione as turmas',

`                `allowClear: true,

`                `width: '100%'

`            `});

`        `}

`    `});

</script>



`    `<!-- Script global do sistema -->

`    `<script>

`        `// Inicialização global do site

`        `document.addEventListener('DOMContentLoaded', function() {

`            `// Inicializar tooltips do Bootstrap

`            `var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));

`            `var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {

`                `return new bootstrap.Tooltip(tooltipTriggerEl);

`            `});



`            `// Inicializar popovers do Bootstrap

`            `var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));

`            `var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {

`                `return new bootstrap.Popover(popoverTriggerEl);

`            `});



`            `// Verificação CSRF para AJAX

`            `function getCookie(name) {

`                `let cookieValue = null;

`                `if (document.cookie && document.cookie !== '') {

`                    `const cookies = document.cookie.split(';');

`                    `for (let i = 0; i < cookies.length; i++) {

`                        `const cookie = cookies[i].trim();

`                        `if (cookie.substring(0, name.length + 1) === (name + '=')) {

`                            `cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

`                            `break;

`                        `}

`                    `}

`                `}

`                `return cookieValue;

`            `}



`            `// Configuração global do AJAX para incluir o token CSRF

`            `$.ajaxSetup({

`                `beforeSend: function(xhr, settings) {

`                    `if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {

`                        `xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));

`                    `}

`                `}

`            `});



`            `// Verificação periódica do token CSRF para sessões longas

`            `setInterval(function() {

`                `$.get("/csrf\_check/");

`            `}, 3600000); // A cada hora



`            `// Aplicar máscaras globais

`            `if (typeof $.fn.mask === 'function') {

`                `$('.cpf-mask').mask('000.000.000-00');

`                `$('.cep-mask').mask('00000-000');

`                `$('.phone-mask').mask('(00) 0000-00009');

`                `$('.phone-mask').blur(function(event) {

`                    `if($(this).val().length == 15){

`                        `$('.phone-mask').mask('(00) 00000-0009');

`                    `} else {

`                        `$('.phone-mask').mask('(00) 0000-00009');

`                    `}

`                `});

`                `$('.date-mask').mask('00/00/0000');

`                `$('.time-mask').mask('00:00 às 00:00');

`            `}



`            `// Inicialização global do Select2

`            `if (typeof $.fn.select2 === 'function') {

`                `$('.select2').select2({

`                    `theme: 'bootstrap4',

`                    `width: '100%'

`                `});

`            `}

`        `});

`    `</script>

`    `<script src="/static/js/inicializar\_select2.js"></script>


<link rel="stylesheet" href="/static/debug\_toolbar/css/print.css" media="print">

<link rel="stylesheet" href="/static/debug\_toolbar/css/toolbar.css">


<script type="module" src="/static/debug\_toolbar/js/toolbar.js" async=""></script>

<div id="djDebug" class="" dir="ltr" data-store-id="14313be0115c494c916908db53b1c5fe" data-render-panel-url="/\_\_debug\_\_/render\_panel/" data-sidebar-url="/\_\_debug\_\_/history\_sidebar/" data-default-show="true" data-update-on-fetch="False" data-theme="auto">

`  `<div class="djdt-hidden" id="djDebugToolbar">

`    `<ul id="djDebugPanelList">

`      `<li><a id="djHideToolBarButton" href="#" title="Ocultar barra de ferramentas">Esconder »</a></li>

`      `<li>

`        `<a id="djToggleThemeButton" href="#" title="Toggle Theme">

`          `Toggle Theme <svg aria-hidden="true" class="djdt-hidden theme-auto" fill="currentColor" viewBox="0 0 32 32" version="1.1" xmlns="http://www.w3.org/2000/svg">

`  `<path d="M0 16q0 3.264 1.28 6.24t3.392 5.088 5.12 3.424 6.208 1.248q3.264 0 6.24-1.248t5.088-3.424 3.392-5.088 1.28-6.24-1.28-6.208-3.392-5.12-5.088-3.392-6.24-1.28q-3.264 0-6.208 1.28t-5.12 3.392-3.392 5.12-1.28 6.208zM4 16q0-3.264 1.6-6.016t4.384-4.352 6.016-1.632 6.016 1.632 4.384 4.352 1.6 6.016-1.6 6.048-4.384 4.352-6.016 1.6-6.016-1.6-4.384-4.352-1.6-6.048zM16 26.016q2.72 0 5.024-1.344t3.648-3.648 1.344-5.024-1.344-4.992-3.648-3.648-5.024-1.344v20z"></path>

</svg>

<svg aria-hidden="true" class="djdt-hidden theme-light" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">

`  `<path fill-rule="evenodd" clip-rule="evenodd" d="M12 1.25C12.4142 1.25 12.75 1.58579 12.75 2V4C12.75 4.41421 12.4142 4.75 12 4.75C11.5858 4.75 11.25 4.41421 11.25 4V2C11.25 1.58579 11.5858 1.25 12 1.25ZM3.66865 3.71609C3.94815 3.41039 4.42255 3.38915 4.72825 3.66865L6.95026 5.70024C7.25596 5.97974 7.2772 6.45413 6.9977 6.75983C6.7182 7.06553 6.2438 7.08677 5.9381 6.80727L3.71609 4.77569C3.41039 4.49619 3.38915 4.02179 3.66865 3.71609ZM20.3314 3.71609C20.6109 4.02179 20.5896 4.49619 20.2839 4.77569L18.0619 6.80727C17.7562 7.08677 17.2818 7.06553 17.0023 6.75983C16.7228 6.45413 16.744 5.97974 17.0497 5.70024L19.2718 3.66865C19.5775 3.38915 20.0518 3.41039 20.3314 3.71609ZM12 7.75C9.65279 7.75 7.75 9.65279 7.75 12C7.75 14.3472 9.65279 16.25 12 16.25C14.3472 16.25 16.25 14.3472 16.25 12C16.25 9.65279 14.3472 7.75 12 7.75ZM6.25 12C6.25 8.82436 8.82436 6.25 12 6.25C15.1756 6.25 17.75 8.82436 17.75 12C17.75 15.1756 15.1756 17.75 12 17.75C8.82436 17.75 6.25 15.1756 6.25 12ZM1.25 12C1.25 11.5858 1.58579 11.25 2 11.25H4C4.41421 11.25 4.75 11.5858 4.75 12C4.75 12.4142 4.41421 12.75 4 12.75H2C1.58579 12.75 1.25 12.4142 1.25 12ZM19.25 12C19.25 11.5858 19.5858 11.25 20 11.25H22C22.4142 11.25 22.75 11.5858 22.75 12C22.75 12.4142 22.4142 12.75 22 12.75H20C19.5858 12.75 19.25 12.4142 19.25 12ZM17.0255 17.0252C17.3184 16.7323 17.7933 16.7323 18.0862 17.0252L20.3082 19.2475C20.6011 19.5404 20.601 20.0153 20.3081 20.3082C20.0152 20.6011 19.5403 20.601 19.2475 20.3081L17.0255 18.0858C16.7326 17.7929 16.7326 17.3181 17.0255 17.0252ZM6.97467 17.0253C7.26756 17.3182 7.26756 17.7931 6.97467 18.086L4.75244 20.3082C4.45955 20.6011 3.98468 20.6011 3.69178 20.3082C3.39889 20.0153 3.39889 19.5404 3.69178 19.2476L5.91401 17.0253C6.2069 16.7324 6.68177 16.7324 6.97467 17.0253ZM12 19.25C12.4142 19.25 12.75 19.5858 12.75 20V22C12.75 22.4142 12.4142 22.75 12 22.75C11.5858 22.75 11.25 22.4142 11.25 22V20C11.25 19.5858 11.5858 19.25 12 19.25Z" fill="currentColor"></path>

</svg>

<svg aria-hidden="true" class="djdt-hidden theme-dark" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">

`  `<path d="M3.32031 11.6835C3.32031 16.6541 7.34975 20.6835 12.3203 20.6835C16.1075 20.6835 19.3483 18.3443 20.6768 15.032C19.6402 15.4486 18.5059 15.6834 17.3203 15.6834C12.3497 15.6834 8.32031 11.654 8.32031 6.68342C8.32031 5.50338 8.55165 4.36259 8.96453 3.32996C5.65605 4.66028 3.32031 7.89912 3.32031 11.6835Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>

</svg>

`        `</a>

`      `</li>





<li id="djdt-HistoryPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtHistoryPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Histórico" class="HistoryPanel">



`  `Histórico





`      `<br><small>/atividades/academicas/criar/?return\_url=/atividades/academicas/</small>







`    `</a>



</li>





<li id="djdt-VersionsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtVersionsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Versões" class="VersionsPanel">



`  `Versões





`      `<br><small>Django 5.1.7</small>







`    `</a>



</li>





<li id="djdt-TimerPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtTimerPanel" checked="" title="Desativar para próximas requisições">



`    `<div class="djdt-contentless">



`  `Tempo





`      `<br><small>Total: 198.58ms</small>







`    `</div>



</li>





<li id="djdt-SettingsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSettingsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Settings from omaum.settings" class="SettingsPanel">



`  `Configurações













`    `</a>



</li>





<li id="djdt-HeadersPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtHeadersPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Cabeçalhos" class="HeadersPanel">



`  `Cabeçalhos













`    `</a>



</li>





<li id="djdt-RequestPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtRequestPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Requisição" class="RequestPanel">



`  `Requisição





`      `<br><small>criar\_atividade\_academica</small>







`    `</a>



</li>





<li id="djdt-SQLPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSQLPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="SQL queries from 1 connection" class="SQLPanel">



`  `SQL





`      `<br><small>7 queries in 7.56ms</small>







`    `</a>



</li>





<li id="djdt-StaticFilesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtStaticFilesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Arquivos estáticos (154 encontrados, 6 sendo utilizados)" class="StaticFilesPanel">



`  `Arquivos estáticos





`      `<br><small>6 arquivos utilizados</small>







`    `</a>



</li>





<li id="djdt-TemplatesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtTemplatesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Templates (12 renderizados)" class="TemplatesPanel">



`  `Templates





`      `<br><small>atividades/formulario\_atividade\_academica.html</small>







`    `</a>



</li>





<li id="djdt-AlertsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtAlertsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Alerts" class="AlertsPanel">



`  `Alerts













`    `</a>



</li>





<li id="djdt-CachePanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtCachePanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Chamadas ao cache de 1 backend" class="CachePanel">



`  `Cache





`      `<br><small>0 chamada em 0.00ms</small>







`    `</a>



</li>





<li id="djdt-SignalsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSignalsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Sinais" class="SignalsPanel">



`  `Sinais





`      `<br><small>35 receptores de 15 sinais</small>







`    `</a>



</li>





<li id="djdt-RedirectsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtRedirectsPanel" title="Habilitar para próximas requisições">



`    `<div class="djdt-contentless djdt-disabled">



`  `Interceptar redirecionamentos





`    `</div>



</li>





<li id="djdt-ProfilingPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtProfilingPanel" title="Habilitar para próximas requisições">



`    `<div class="djdt-contentless djdt-disabled">



`  `Profiling





`    `</div>



</li>



`    `</ul>

`  `</div>

`  `<div class="" id="djDebugToolbarHandle" style="top: 265px;">

`    `<div title="Mostrar barra de ferramentas" id="djShowToolBarButton">

`      `<span id="djShowToolBarD">D</span><span id="djShowToolBarJ">J</span>DT

`    `</div>

`  `</div>






`  `<div id="HistoryPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Histórico</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="VersionsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Versões</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>













`  `<div id="SettingsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Settings from omaum.settings</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="HeadersPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Cabeçalhos</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="RequestPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Requisição</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="SQLPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>SQL queries from 1 connection</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="StaticFilesPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Arquivos estáticos (154 encontrados, 6 sendo utilizados)</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="TemplatesPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Templates (12 renderizados)</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="AlertsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Alerts</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="CachePanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Chamadas ao cache de 1 backend</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="SignalsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Sinais</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>
















`  `<div id="djDebugWindow" class="djdt-panelContent djdt-hidden"></div>

</div>


</body>

<body>

`    `<!-- Cabeçalho/Barra de Navegação -->

`    `<header>

`        `<nav class="navbar navbar-expand-lg navbar-dark bg-primary">

`            `<div class="container">

`                `<a class="navbar-brand" href="/">

`                    `<img src="/static/img/logo.png" alt="OMAUM Logo" height="40">

`                `</a>

`                `<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">

`                    `<span class="navbar-toggler-icon"></span>

`                `</button>



`                `<div class="collapse navbar-collapse" id="navbarNav">

`                    `<ul class="navbar-nav me-auto">

`                        `<li class="nav-item">

`                            `<a class="nav-link " href="/">

`                                `<i class="fas fa-home"></i> Início

`                            `</a>

`                        `</li>





`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/alunos/">

`                                    `<i class="fas fa-user-graduate"></i> Alunos

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/cursos/">

`                                    `<i class="fas fa-book"></i> Cursos

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/turmas/">

`                                    `<i class="fas fa-users"></i> Turmas

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/matriculas/">

`                                    `<i class="fas fa-clipboard-list"></i> Matrículas

`                                `</a>

`                            `</li>

`                            `<li class="nav-item dropdown">

`                                `<a class="nav-link dropdown-toggle" href="#" id="navbarDropdownAtividades" role="button" data-bs-toggle="dropdown" aria-expanded="false">

`                                   `<i class="fas fa-calendar-alt"></i> Atividades

`                                `</a>

`                                `<ul class="dropdown-menu" aria-labelledby="navbarDropdownAtividades">

`                                    `<li>

`                                        `<a class="dropdown-item" href="/atividades/academicas/">

`                                            `<i class="fas fa-school"></i> Acadêmicas

`                                        `</a>

`                                    `</li>

`                                    `<li>

`                                        `<a class="dropdown-item" href="/atividades/ritualisticas/">

`                                            `<i class="fas fa-pray"></i> Ritualísticas

`                                        `</a>

`                                    `</li>

`                                `</ul>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/frequencias/">

`                                    `<i class="fas fa-check-square"></i> Frequências

`                                `</a>

`                            `</li>



`                    `</ul>



`                    `<ul class="navbar-nav">





`                                `<li class="nav-item">

`                                    `<a class="nav-link" href="/painel-controle/">

`                                        `<i class="fas fa-cog"></i> Painel de Controle

`                                    `</a>

`                                `</li>



`                            `<li class="nav-item dropdown">

`                                `<a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">

`                                   `<i class="fas fa-user-circle"></i> lcsilv3

`                                `</a>

`                                `<ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">

`                                    `<li><a class="dropdown-item" href="#">Meu Perfil</a></li>

`                                    `<li><hr class="dropdown-divider"></li>

`                                    `<li>

`                                        `<form method="post" action="/sair/" class="d-inline">

`                                            `<input type="hidden" name="csrfmiddlewaretoken" value="7Ia08xTzkHIWkonGVajeA1YVtq7NzS2NwIXNK5TWE5HRH2BgWIOT9Za1zBwoOZtu">

`                                            `<button type="submit" class="dropdown-item">

`                                                `<i class="fas fa-sign-out-alt"></i> Sair

`                                            `</button>

`                                        `</form>

`                                    `</li>

`                                `</ul>

`                            `</li>



`                    `</ul>

`                `</div>

`            `</div>

`        `</nav>

`    `</header>



`    `<!-- Mensagens do sistema (flash messages) -->

`    `<div class="message-container">



`    `</div>



`    `<!-- Conteúdo principal -->

`    `<main id="main-content" class="py-4">



<div class="container mt-4">

`    `<h1>Detalhes da Atividade Acadêmica</h1>



`    `<div class="card">

`        `<div class="card-header">

`            `<h5 class="mb-0">Plenilúnio</h5>

`        `</div>

`        `<div class="card-body">

`            `<div class="row">

`                `<div class="col-md-6">

`                    `<p><strong>Descrição:</strong> Atividade acadêmica de plenilúnio</p>

`                    `<p><strong>Data de Início:</strong> 26/10/2026 00:00</p>

`                    `<p><strong>Data de Término:</strong> Não definida</p>

`                    `<p><strong>Responsável:</strong> Não informado</p>

`                    `<p><strong>Local:</strong> Não informado</p>

`                `</div>

`                `<div class="col-md-6">

`                    `<p><strong>Tipo:</strong> Aula</p>

`                    `<p><strong>Status:</strong> Agendada</p>



`                    `<!-- Mostrar todas as turmas associadas -->

`                    `<p><strong>Turmas:</strong></p>

`                    `<ul class="list-group">



`                            `<li class="list-group-item">

`                                `<a href="/turmas/2/">A</a>



`                                    `- Introdução à Meditação



`                            `</li>



`                    `</ul>

`                `</div>

`            `</div>



`            `<div class="mt-3">

`                `<a href="/atividades/academicas/editar/2/?return\_url=/atividades/academicas/detalhar/2/" class="btn btn-primary">Editar</a>

`                `<a href="/atividades/academicas/confirmar-exclusao/2/?return\_url=/atividades/academicas/detalhar/2/" class="btn btn-danger">Excluir</a>

`                `<!-- Novo botão para copiar atividade -->

`                `<a href="/atividades/academicas/2/copiar/" class="btn btn-secondary">Copiar</a>

`                `<a href="/atividades/academicas/" class="btn btn-secondary">Voltar para Lista</a>

`            `</div>

`        `</div>

`    `</div>

</div>

`    `</main>



`    `<!-- Rodapé -->

`    `<footer class="footer mt-auto py-3 bg-light">

`        `<div class="container text-center">

`            `<span class="text-muted">© 2025 OMAUM - Sistema de Gestão de Iniciados</span>

`        `</div>

`    `</footer>



`    `<!-- Scripts de componentes globais -->

`    `<script src="/static/js/modules/dias-semana.js"></script>



`    `<!-- Scripts específicos da página -->





`    `<!-- Script global do sistema -->

`    `<script>

`        `// Inicialização global do site

`        `document.addEventListener('DOMContentLoaded', function() {

`            `// Inicializar tooltips do Bootstrap

`            `var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));

`            `var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {

`                `return new bootstrap.Tooltip(tooltipTriggerEl);

`            `});



`            `// Inicializar popovers do Bootstrap

`            `var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));

`            `var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {

`                `return new bootstrap.Popover(popoverTriggerEl);

`            `});



`            `// Verificação CSRF para AJAX

`            `function getCookie(name) {

`                `let cookieValue = null;

`                `if (document.cookie && document.cookie !== '') {

`                    `const cookies = document.cookie.split(';');

`                    `for (let i = 0; i < cookies.length; i++) {

`                        `const cookie = cookies[i].trim();

`                        `if (cookie.substring(0, name.length + 1) === (name + '=')) {

`                            `cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

`                            `break;

`                        `}

`                    `}

`                `}

`                `return cookieValue;

`            `}



`            `// Configuração global do AJAX para incluir o token CSRF

`            `$.ajaxSetup({

`                `beforeSend: function(xhr, settings) {

`                    `if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {

`                        `xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));

`                    `}

`                `}

`            `});



`            `// Verificação periódica do token CSRF para sessões longas

`            `setInterval(function() {

`                `$.get("/csrf\_check/");

`            `}, 3600000); // A cada hora



`            `// Aplicar máscaras globais

`            `if (typeof $.fn.mask === 'function') {

`                `$('.cpf-mask').mask('000.000.000-00');

`                `$('.cep-mask').mask('00000-000');

`                `$('.phone-mask').mask('(00) 0000-00009');

`                `$('.phone-mask').blur(function(event) {

`                    `if($(this).val().length == 15){

`                        `$('.phone-mask').mask('(00) 00000-0009');

`                    `} else {

`                        `$('.phone-mask').mask('(00) 0000-00009');

`                    `}

`                `});

`                `$('.date-mask').mask('00/00/0000');

`                `$('.time-mask').mask('00:00 às 00:00');

`            `}



`            `// Inicialização global do Select2

`            `if (typeof $.fn.select2 === 'function') {

`                `$('.select2').select2({

`                    `theme: 'bootstrap4',

`                    `width: '100%'

`                `});

`            `}

`        `});

`    `</script>

`    `<script src="/static/js/inicializar\_select2.js"></script>


<link rel="stylesheet" href="/static/debug\_toolbar/css/print.css" media="print">

<link rel="stylesheet" href="/static/debug\_toolbar/css/toolbar.css">


<script type="module" src="/static/debug\_toolbar/js/toolbar.js" async=""></script>

<div id="djDebug" class="" dir="ltr" data-store-id="b8a9fdd73a824709931fe09174167133" data-render-panel-url="/\_\_debug\_\_/render\_panel/" data-sidebar-url="/\_\_debug\_\_/history\_sidebar/" data-default-show="true" data-update-on-fetch="False" data-theme="auto">

`  `<div class="djdt-hidden" id="djDebugToolbar">

`    `<ul id="djDebugPanelList">

`      `<li><a id="djHideToolBarButton" href="#" title="Ocultar barra de ferramentas">Esconder »</a></li>

`      `<li>

`        `<a id="djToggleThemeButton" href="#" title="Toggle Theme">

`          `Toggle Theme <svg aria-hidden="true" class="djdt-hidden theme-auto" fill="currentColor" viewBox="0 0 32 32" version="1.1" xmlns="http://www.w3.org/2000/svg">

`  `<path d="M0 16q0 3.264 1.28 6.24t3.392 5.088 5.12 3.424 6.208 1.248q3.264 0 6.24-1.248t5.088-3.424 3.392-5.088 1.28-6.24-1.28-6.208-3.392-5.12-5.088-3.392-6.24-1.28q-3.264 0-6.208 1.28t-5.12 3.392-3.392 5.12-1.28 6.208zM4 16q0-3.264 1.6-6.016t4.384-4.352 6.016-1.632 6.016 1.632 4.384 4.352 1.6 6.016-1.6 6.048-4.384 4.352-6.016 1.6-6.016-1.6-4.384-4.352-1.6-6.048zM16 26.016q2.72 0 5.024-1.344t3.648-3.648 1.344-5.024-1.344-4.992-3.648-3.648-5.024-1.344v20z"></path>

</svg>

<svg aria-hidden="true" class="djdt-hidden theme-light" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">

`  `<path fill-rule="evenodd" clip-rule="evenodd" d="M12 1.25C12.4142 1.25 12.75 1.58579 12.75 2V4C12.75 4.41421 12.4142 4.75 12 4.75C11.5858 4.75 11.25 4.41421 11.25 4V2C11.25 1.58579 11.5858 1.25 12 1.25ZM3.66865 3.71609C3.94815 3.41039 4.42255 3.38915 4.72825 3.66865L6.95026 5.70024C7.25596 5.97974 7.2772 6.45413 6.9977 6.75983C6.7182 7.06553 6.2438 7.08677 5.9381 6.80727L3.71609 4.77569C3.41039 4.49619 3.38915 4.02179 3.66865 3.71609ZM20.3314 3.71609C20.6109 4.02179 20.5896 4.49619 20.2839 4.77569L18.0619 6.80727C17.7562 7.08677 17.2818 7.06553 17.0023 6.75983C16.7228 6.45413 16.744 5.97974 17.0497 5.70024L19.2718 3.66865C19.5775 3.38915 20.0518 3.41039 20.3314 3.71609ZM12 7.75C9.65279 7.75 7.75 9.65279 7.75 12C7.75 14.3472 9.65279 16.25 12 16.25C14.3472 16.25 16.25 14.3472 16.25 12C16.25 9.65279 14.3472 7.75 12 7.75ZM6.25 12C6.25 8.82436 8.82436 6.25 12 6.25C15.1756 6.25 17.75 8.82436 17.75 12C17.75 15.1756 15.1756 17.75 12 17.75C8.82436 17.75 6.25 15.1756 6.25 12ZM1.25 12C1.25 11.5858 1.58579 11.25 2 11.25H4C4.41421 11.25 4.75 11.5858 4.75 12C4.75 12.4142 4.41421 12.75 4 12.75H2C1.58579 12.75 1.25 12.4142 1.25 12ZM19.25 12C19.25 11.5858 19.5858 11.25 20 11.25H22C22.4142 11.25 22.75 11.5858 22.75 12C22.75 12.4142 22.4142 12.75 22 12.75H20C19.5858 12.75 19.25 12.4142 19.25 12ZM17.0255 17.0252C17.3184 16.7323 17.7933 16.7323 18.0862 17.0252L20.3082 19.2475C20.6011 19.5404 20.601 20.0153 20.3081 20.3082C20.0152 20.6011 19.5403 20.601 19.2475 20.3081L17.0255 18.0858C16.7326 17.7929 16.7326 17.3181 17.0255 17.0252ZM6.97467 17.0253C7.26756 17.3182 7.26756 17.7931 6.97467 18.086L4.75244 20.3082C4.45955 20.6011 3.98468 20.6011 3.69178 20.3082C3.39889 20.0153 3.39889 19.5404 3.69178 19.2476L5.91401 17.0253C6.2069 16.7324 6.68177 16.7324 6.97467 17.0253ZM12 19.25C12.4142 19.25 12.75 19.5858 12.75 20V22C12.75 22.4142 12.4142 22.75 12 22.75C11.5858 22.75 11.25 22.4142 11.25 22V20C11.25 19.5858 11.5858 19.25 12 19.25Z" fill="currentColor"></path>

</svg>

<svg aria-hidden="true" class="djdt-hidden theme-dark" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">

`  `<path d="M3.32031 11.6835C3.32031 16.6541 7.34975 20.6835 12.3203 20.6835C16.1075 20.6835 19.3483 18.3443 20.6768 15.032C19.6402 15.4486 18.5059 15.6834 17.3203 15.6834C12.3497 15.6834 8.32031 11.654 8.32031 6.68342C8.32031 5.50338 8.55165 4.36259 8.96453 3.32996C5.65605 4.66028 3.32031 7.89912 3.32031 11.6835Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>

</svg>

`        `</a>

`      `</li>





<li id="djdt-HistoryPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtHistoryPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Histórico" class="HistoryPanel">



`  `Histórico





`      `<br><small>/atividades/academicas/detalhar/2/</small>







`    `</a>



</li>





<li id="djdt-VersionsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtVersionsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Versões" class="VersionsPanel">



`  `Versões





`      `<br><small>Django 5.1.7</small>







`    `</a>



</li>





<li id="djdt-TimerPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtTimerPanel" checked="" title="Desativar para próximas requisições">



`    `<div class="djdt-contentless">



`  `Tempo





`      `<br><small>Total: 202.13ms</small>







`    `</div>



</li>





<li id="djdt-SettingsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSettingsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Settings from omaum.settings" class="SettingsPanel">



`  `Configurações













`    `</a>



</li>





<li id="djdt-HeadersPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtHeadersPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Cabeçalhos" class="HeadersPanel">



`  `Cabeçalhos













`    `</a>



</li>





<li id="djdt-RequestPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtRequestPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Requisição" class="RequestPanel">



`  `Requisição





`      `<br><small>detalhar\_atividade\_academica</small>







`    `</a>



</li>





<li id="djdt-SQLPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSQLPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="SQL queries from 1 connection" class="SQLPanel">



`  `SQL





`      `<br><small>8 queries in 7.97ms</small>







`    `</a>



</li>





<li id="djdt-StaticFilesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtStaticFilesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Arquivos estáticos (154 encontrados, 6 sendo utilizados)" class="StaticFilesPanel">



`  `Arquivos estáticos





`      `<br><small>6 arquivos utilizados</small>







`    `</a>



</li>





<li id="djdt-TemplatesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtTemplatesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Templates (2 renderizados)" class="TemplatesPanel">



`  `Templates





`      `<br><small>atividades/detalhar\_atividade\_academica.html</small>







`    `</a>



</li>





<li id="djdt-AlertsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtAlertsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Alerts" class="AlertsPanel">



`  `Alerts













`    `</a>



</li>





<li id="djdt-CachePanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtCachePanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Chamadas ao cache de 1 backend" class="CachePanel">



`  `Cache





`      `<br><small>0 chamada em 0.00ms</small>







`    `</a>



</li>





<li id="djdt-SignalsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSignalsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Sinais" class="SignalsPanel">



`  `Sinais





`      `<br><small>35 receptores de 15 sinais</small>







`    `</a>



</li>





<li id="djdt-RedirectsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtRedirectsPanel" title="Habilitar para próximas requisições">



`    `<div class="djdt-contentless djdt-disabled">



`  `Interceptar redirecionamentos





`    `</div>



</li>





<li id="djdt-ProfilingPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtProfilingPanel" title="Habilitar para próximas requisições">



`    `<div class="djdt-contentless djdt-disabled">



`  `Profiling





`    `</div>



</li>



`    `</ul>

`  `</div>

`  `<div class="" id="djDebugToolbarHandle" style="top: 265px;">

`    `<div title="Mostrar barra de ferramentas" id="djShowToolBarButton">

`      `<span id="djShowToolBarD">D</span><span id="djShowToolBarJ">J</span>DT

`    `</div>

`  `</div>






`  `<div id="HistoryPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Histórico</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="VersionsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Versões</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>













`  `<div id="SettingsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Settings from omaum.settings</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="HeadersPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Cabeçalhos</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="RequestPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Requisição</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="SQLPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>SQL queries from 1 connection</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="StaticFilesPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Arquivos estáticos (154 encontrados, 6 sendo utilizados)</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="TemplatesPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Templates (2 renderizados)</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="AlertsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Alerts</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="CachePanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Chamadas ao cache de 1 backend</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="SignalsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Sinais</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>
















`  `<div id="djDebugWindow" class="djdt-panelContent djdt-hidden"></div>

</div>


</body>
<body>

`    `<!-- Cabeçalho/Barra de Navegação -->

`    `<header>

`        `<nav class="navbar navbar-expand-lg navbar-dark bg-primary">

`            `<div class="container">

`                `<a class="navbar-brand" href="/">

`                    `<img src="/static/img/logo.png" alt="OMAUM Logo" height="40">

`                `</a>

`                `<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">

`                    `<span class="navbar-toggler-icon"></span>

`                `</button>



`                `<div class="collapse navbar-collapse" id="navbarNav">

`                    `<ul class="navbar-nav me-auto">

`                        `<li class="nav-item">

`                            `<a class="nav-link " href="/">

`                                `<i class="fas fa-home"></i> Início

`                            `</a>

`                        `</li>





`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/alunos/">

`                                    `<i class="fas fa-user-graduate"></i> Alunos

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/cursos/">

`                                    `<i class="fas fa-book"></i> Cursos

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/turmas/">

`                                    `<i class="fas fa-users"></i> Turmas

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/matriculas/">

`                                    `<i class="fas fa-clipboard-list"></i> Matrículas

`                                `</a>

`                            `</li>

`                            `<li class="nav-item dropdown">

`                                `<a class="nav-link dropdown-toggle" href="#" id="navbarDropdownAtividades" role="button" data-bs-toggle="dropdown" aria-expanded="false">

`                                   `<i class="fas fa-calendar-alt"></i> Atividades

`                                `</a>

`                                `<ul class="dropdown-menu" aria-labelledby="navbarDropdownAtividades">

`                                    `<li>

`                                        `<a class="dropdown-item" href="/atividades/academicas/">

`                                            `<i class="fas fa-school"></i> Acadêmicas

`                                        `</a>

`                                    `</li>

`                                    `<li>

`                                        `<a class="dropdown-item" href="/atividades/ritualisticas/">

`                                            `<i class="fas fa-pray"></i> Ritualísticas

`                                        `</a>

`                                    `</li>

`                                `</ul>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/frequencias/">

`                                    `<i class="fas fa-check-square"></i> Frequências

`                                `</a>

`                            `</li>



`                    `</ul>



`                    `<ul class="navbar-nav">





`                                `<li class="nav-item">

`                                    `<a class="nav-link" href="/painel-controle/">

`                                        `<i class="fas fa-cog"></i> Painel de Controle

`                                    `</a>

`                                `</li>



`                            `<li class="nav-item dropdown">

`                                `<a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">

`                                   `<i class="fas fa-user-circle"></i> lcsilv3

`                                `</a>

`                                `<ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">

`                                    `<li><a class="dropdown-item" href="#">Meu Perfil</a></li>

`                                    `<li><hr class="dropdown-divider"></li>

`                                    `<li>

`                                        `<form method="post" action="/sair/" class="d-inline">

`                                            `<input type="hidden" name="csrfmiddlewaretoken" value="ppjYtzRfBQiDNzDvJRESijgcRfrYf68POp6L57RCVehyadR5Kp9xRhsiXqQzudzw">

`                                            `<button type="submit" class="dropdown-item">

`                                                `<i class="fas fa-sign-out-alt"></i> Sair

`                                            `</button>

`                                        `</form>

`                                    `</li>

`                                `</ul>

`                            `</li>



`                    `</ul>

`                `</div>

`            `</div>

`        `</nav>

`    `</header>



`    `<!-- Mensagens do sistema (flash messages) -->

`    `<div class="message-container">



`    `</div>



`    `<!-- Conteúdo principal -->

`    `<main id="main-content" class="py-4">



<div class="container mt-4">

`    `<div class="d-flex justify-content-between align-items-center mb-4">

`        `<h1>Editar Atividade Acadêmica</h1>

`        `<a href="/atividades/academicas/detalhar/2/" class="btn btn-secondary me-2">Voltar</a>

`    `</div>







`    `<form method="post">

`        `<input type="hidden" name="csrfmiddlewaretoken" value="ppjYtzRfBQiDNzDvJRESijgcRfrYf68POp6L57RCVehyadR5Kp9xRhsiXqQzudzw">





`        `<div class="card mb-4">

`            `<div class="card-header">

`                `<h5>Informações Básicas</h5>

`            `</div>

`            `<div class="card-body">

`                `<div class="row">

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_nome" class="form-label">Nome</label>

`    `<input type="text" name="nome" value="Plenilúnio" class="form-control" maxlength="100" required="" id="id\_nome">





</div>

`                    `</div>

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_responsavel" class="form-label">Responsável</label>

`    `<input type="text" name="responsavel" class="form-control" maxlength="100" id="id\_responsavel">





</div>

`                    `</div>

`                `</div>

`                `<div class="row">

`                    `<div class="col-md-12">

`                        `<div class="mb-3">

`    `<label for="id\_descricao" class="form-label">Descrição</label>

`    `<textarea name="descricao" cols="40" rows="3" class="form-control" id="id\_descricao">Atividade acadêmica de plenilúnio</textarea>





</div>

`                    `</div>

`                `</div>

`            `</div>

`        `</div>



`        `<div class="card mb-4">

`            `<div class="card-header">

`                `<h5>Data e Local</h5>

`            `</div>

`            `<div class="card-body">

`                `<div class="row">

`                    `<div class="col-md-3">

`                        `<div class="mb-3">

`    `<label for="id\_data\_inicio" class="form-label">Data de Início</label>

`    `<input type="date" name="data\_inicio" value="2026-10-26" class="form-control" required="" id="id\_data\_inicio"><input type="hidden" name="initial-data\_inicio" value="2026-10-26" id="initial-id\_data\_inicio">





</div>

`                    `</div>

`                    `<div class="col-md-3">

`                        `<div class="mb-3">

`    `<label for="id\_data\_fim" class="form-label">Data de Término</label>

`    `<input type="date" name="data\_fim" class="form-control" id="id\_data\_fim">





</div>

`                    `</div>

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_local" class="form-label">Local</label>

`    `<input type="text" name="local" class="form-control" maxlength="100" id="id\_local">





</div>

`                    `</div>

`                `</div>

`            `</div>

`        `</div>



`        `<!-- Nova seção para Turmas -->

`        `<div class="card mb-4">

`            `<div class="card-header">

`                `<h5>Turmas</h5>

`            `</div>

`            `<div class="card-body">

`                `<div class="row">

`                    `<div class="col-md-12">

`                        `<div class="mb-3">

`    `<label for="id\_turmas" class="form-label">Turmas</label>

`    `<select name="turmas" class="form-control select2-hidden-accessible" id="id\_turmas" multiple="" tabindex="-1" aria-hidden="true" data-select2-id="select2-data-id\_turmas">

`  `<option value="6">D - Introdução à Meditação</option>

`  `<option value="2" selected="" data-select2-id="select2-data-11-22yn">A - Introdução à Meditação</option>

`  `<option value="4">B - Introdução à Meditação</option>

`  `<option value="5">C - Introdução à Meditação</option>

</select><span class="select2 select2-container select2-container--bootstrap4" dir="ltr" data-select2-id="select2-data-10-99lx" style="width: 100%;"><span class="selection"><span class="select2-selection select2-selection--multiple select2-selection--clearable" role="combobox" aria-haspopup="true" aria-expanded="false" tabindex="-1" aria-disabled="false"><button type="button" class="select2-selection\_\_clear" tabindex="-1" title="Remove all items" aria-label="Remove all items" aria-describedby="select2-id\_turmas-container" data-select2-id="select2-data-15-3udj"><span aria-hidden="true">×</span></button><ul class="select2-selection\_\_rendered" id="select2-id\_turmas-container"><li class="select2-selection\_\_choice" title="A - Introdução à Meditação" data-select2-id="select2-data-14-481s"><button type="button" class="select2-selection\_\_choice\_\_remove" tabindex="-1" title="Remove item" aria-label="Remove item" aria-describedby="select2-id\_turmas-container-choice-mhjm-2"><span aria-hidden="true">×</span></button><span class="select2-selection\_\_choice\_\_display" id="select2-id\_turmas-container-choice-mhjm-2">A - Introdução à Meditação</span></li></ul><span class="select2-search select2-search--inline"><textarea class="select2-search\_\_field" type="search" tabindex="0" autocorrect="off" autocapitalize="none" spellcheck="false" role="searchbox" aria-autocomplete="list" autocomplete="off" aria-label="Search" aria-describedby="select2-id\_turmas-container" placeholder="" style="width: 0.75em;"></textarea></span></span></span><span class="dropdown-wrapper" aria-hidden="true"></span></span><span class="select2 select2-container select2-container--bootstrap4 select2-hidden-accessible" dir="ltr" data-select2-id="select2-data-5-gf3o" style="width: 100%;" tabindex="-1" aria-hidden="true"><span class="selection"><span class="select2-selection select2-selection--single" role="combobox" aria-haspopup="true" aria-expanded="false" tabindex="0" aria-disabled="false" aria-labelledby="select2-nehy-container" aria-controls="select2-nehy-container"><span class="select2-selection\_\_rendered" id="select2-nehy-container" role="textbox" aria-readonly="true"></span><span class="select2-selection\_\_arrow" role="presentation"><b role="presentation"></b></span></span></span><span class="dropdown-wrapper" aria-hidden="true"></span></span><span class="select2 select2-container select2-container--bootstrap4" dir="ltr" data-select2-id="select2-data-6-0zwc" style="width: 100%;"><span class="selection"><span class="select2-selection select2-selection--single" role="combobox" aria-haspopup="true" aria-expanded="false" tabindex="0" aria-disabled="false" aria-labelledby="select2-bnp6-container" aria-controls="select2-bnp6-container"><span class="select2-selection\_\_rendered" id="select2-bnp6-container" role="textbox" aria-readonly="true"></span><span class="select2-selection\_\_arrow" role="presentation"><b role="presentation"></b></span></span></span><span class="dropdown-wrapper" aria-hidden="true"></span></span>





</div>

`                    `</div>

`                `</div>

`                `<div class="row mt-2">

`                    `<div class="col-md-12">

`                        `<div class="form-check">

`                            `<input type="checkbox" name="todas\_turmas" id="id\_todas\_turmas">

`                            `<label class="form-check-label" for="id\_todas\_turmas">

`                                `Aplicar a todas as turmas ativas

`                            `</label>

`                            `<small class="form-text text-muted">

`                                `Marque esta opção para aplicar esta atividade a todas as turmas ativas automaticamente.

`                            `</small>

`                        `</div>

`                    `</div>

`                `</div>

`            `</div>

`        `</div>



`        `<div class="card mb-4">

`            `<div class="card-header">

`                `<h5>Classificação</h5>

`            `</div>

`            `<div class="card-body">

`                `<div class="row">

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_tipo\_atividade" class="form-label">Tipo de Atividade</label>

`    `<select name="tipo\_atividade" class="form-control" id="id\_tipo\_atividade">

`  `<option value="aula" selected="">Aula</option>

`  `<option value="palestra">Palestra</option>

`  `<option value="workshop">Workshop</option>

`  `<option value="seminario">Seminário</option>

`  `<option value="outro">Outro</option>

</select>





</div>

`                    `</div>

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_status" class="form-label">Status</label>

`    `<select name="status" class="form-control" id="id\_status">

`  `<option value="agendada" selected="">Agendada</option>

`  `<option value="em\_andamento">Em Andamento</option>

`  `<option value="concluida">Concluída</option>

`  `<option value="cancelada">Cancelada</option>

</select>





</div>

`                    `</div>

`                `</div>

`            `</div>

`        `</div>



`        `<div class="d-flex justify-content-between mb-5">

`            `<!-- Use a URL de retorno fornecida pela view -->

`            `<a href="/atividades/academicas/detalhar/2/" class="btn btn-secondary">Cancelar</a>

`            `<button type="submit" class="btn btn-primary">

`                `Atualizar Atividade

`            `</button>

`        `</div>

`    `</form>

</div>

`    `</main>



`    `<!-- Rodapé -->

`    `<footer class="footer mt-auto py-3 bg-light">

`        `<div class="container text-center">

`            `<span class="text-muted">© 2025 OMAUM - Sistema de Gestão de Iniciados</span>

`        `</div>

`    `</footer>



`    `<!-- Scripts de componentes globais -->

`    `<script src="/static/js/modules/dias-semana.js"></script>



`    `<!-- Scripts específicos da página -->



<script>

`    `document.addEventListener('DOMContentLoaded', function() {

`        `const todasTurmasCheckbox = document.getElementById('id\_todas\_turmas');

`        `const turmasSelect = document.getElementById('id\_turmas');



`        `function toggleTurmasField() {

`            `if (todasTurmasCheckbox.checked) {

`                `turmasSelect.disabled = true;

`                `// Adicionar uma mensagem informativa

`                `if (!document.getElementById('turmas-info')) {

`                    `const infoDiv = document.createElement('div');

`                    `infoDiv.id = 'turmas-info';

`                    `infoDiv.className = 'alert alert-info mt-2';

`                    `infoDiv.textContent = 'Todas as turmas ativas serão incluídas automaticamente.';

`                    `turmasSelect.parentNode.appendChild(infoDiv);

`                `}

`            `} else {

`                `turmasSelect.disabled = false;

`                `// Remover a mensagem informativa se existir

`                `const infoDiv = document.getElementById('turmas-info');

`                `if (infoDiv) {

`                    `infoDiv.remove();

`                `}

`            `}

`        `}



`        `// Inicializar

`        `toggleTurmasField();



`        `// Adicionar listener para mudanças

`        `todasTurmasCheckbox.addEventListener('change', toggleTurmasField);



`        `// Inicializar Select2 para o campo de turmas

`        `if (typeof $.fn.select2 === 'function') {

`            `$(turmasSelect).select2({

`                `theme: 'bootstrap4',

`                `placeholder: 'Selecione as turmas',

`                `allowClear: true,

`                `width: '100%'

`            `});

`        `}

`    `});

</script>



`    `<!-- Script global do sistema -->

`    `<script>

`        `// Inicialização global do site

`        `document.addEventListener('DOMContentLoaded', function() {

`            `// Inicializar tooltips do Bootstrap

`            `var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));

`            `var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {

`                `return new bootstrap.Tooltip(tooltipTriggerEl);

`            `});



`            `// Inicializar popovers do Bootstrap

`            `var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));

`            `var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {

`                `return new bootstrap.Popover(popoverTriggerEl);

`            `});



`            `// Verificação CSRF para AJAX

`            `function getCookie(name) {

`                `let cookieValue = null;

`                `if (document.cookie && document.cookie !== '') {

`                    `const cookies = document.cookie.split(';');

`                    `for (let i = 0; i < cookies.length; i++) {

`                        `const cookie = cookies[i].trim();

`                        `if (cookie.substring(0, name.length + 1) === (name + '=')) {

`                            `cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

`                            `break;

`                        `}

`                    `}

`                `}

`                `return cookieValue;

`            `}



`            `// Configuração global do AJAX para incluir o token CSRF

`            `$.ajaxSetup({

`                `beforeSend: function(xhr, settings) {

`                    `if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {

`                        `xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));

`                    `}

`                `}

`            `});



`            `// Verificação periódica do token CSRF para sessões longas

`            `setInterval(function() {

`                `$.get("/csrf\_check/");

`            `}, 3600000); // A cada hora



`            `// Aplicar máscaras globais

`            `if (typeof $.fn.mask === 'function') {

`                `$('.cpf-mask').mask('000.000.000-00');

`                `$('.cep-mask').mask('00000-000');

`                `$('.phone-mask').mask('(00) 0000-00009');

`                `$('.phone-mask').blur(function(event) {

`                    `if($(this).val().length == 15){

`                        `$('.phone-mask').mask('(00) 00000-0009');

`                    `} else {

`                        `$('.phone-mask').mask('(00) 0000-00009');

`                    `}

`                `});

`                `$('.date-mask').mask('00/00/0000');

`                `$('.time-mask').mask('00:00 às 00:00');

`            `}



`            `// Inicialização global do Select2

`            `if (typeof $.fn.select2 === 'function') {

`                `$('.select2').select2({

`                    `theme: 'bootstrap4',

`                    `width: '100%'

`                `});

`            `}

`        `});

`    `</script>

`    `<script src="/static/js/inicializar\_select2.js"></script>


<link rel="stylesheet" href="/static/debug\_toolbar/css/print.css" media="print">

<link rel="stylesheet" href="/static/debug\_toolbar/css/toolbar.css">


<script type="module" src="/static/debug\_toolbar/js/toolbar.js" async=""></script>

<div id="djDebug" class="" dir="ltr" data-store-id="8ae58eb3ab6c4d318ea5b9685fc42ccb" data-render-panel-url="/\_\_debug\_\_/render\_panel/" data-sidebar-url="/\_\_debug\_\_/history\_sidebar/" data-default-show="true" data-update-on-fetch="False" data-theme="auto">

`  `<div class="djdt-hidden" id="djDebugToolbar">

`    `<ul id="djDebugPanelList">

`      `<li><a id="djHideToolBarButton" href="#" title="Ocultar barra de ferramentas">Esconder »</a></li>

`      `<li>

`        `<a id="djToggleThemeButton" href="#" title="Toggle Theme">

`          `Toggle Theme <svg aria-hidden="true" class="djdt-hidden theme-auto" fill="currentColor" viewBox="0 0 32 32" version="1.1" xmlns="http://www.w3.org/2000/svg">

`  `<path d="M0 16q0 3.264 1.28 6.24t3.392 5.088 5.12 3.424 6.208 1.248q3.264 0 6.24-1.248t5.088-3.424 3.392-5.088 1.28-6.24-1.28-6.208-3.392-5.12-5.088-3.392-6.24-1.28q-3.264 0-6.208 1.28t-5.12 3.392-3.392 5.12-1.28 6.208zM4 16q0-3.264 1.6-6.016t4.384-4.352 6.016-1.632 6.016 1.632 4.384 4.352 1.6 6.016-1.6 6.048-4.384 4.352-6.016 1.6-6.016-1.6-4.384-4.352-1.6-6.048zM16 26.016q2.72 0 5.024-1.344t3.648-3.648 1.344-5.024-1.344-4.992-3.648-3.648-5.024-1.344v20z"></path>

</svg>

<svg aria-hidden="true" class="djdt-hidden theme-light" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">

`  `<path fill-rule="evenodd" clip-rule="evenodd" d="M12 1.25C12.4142 1.25 12.75 1.58579 12.75 2V4C12.75 4.41421 12.4142 4.75 12 4.75C11.5858 4.75 11.25 4.41421 11.25 4V2C11.25 1.58579 11.5858 1.25 12 1.25ZM3.66865 3.71609C3.94815 3.41039 4.42255 3.38915 4.72825 3.66865L6.95026 5.70024C7.25596 5.97974 7.2772 6.45413 6.9977 6.75983C6.7182 7.06553 6.2438 7.08677 5.9381 6.80727L3.71609 4.77569C3.41039 4.49619 3.38915 4.02179 3.66865 3.71609ZM20.3314 3.71609C20.6109 4.02179 20.5896 4.49619 20.2839 4.77569L18.0619 6.80727C17.7562 7.08677 17.2818 7.06553 17.0023 6.75983C16.7228 6.45413 16.744 5.97974 17.0497 5.70024L19.2718 3.66865C19.5775 3.38915 20.0518 3.41039 20.3314 3.71609ZM12 7.75C9.65279 7.75 7.75 9.65279 7.75 12C7.75 14.3472 9.65279 16.25 12 16.25C14.3472 16.25 16.25 14.3472 16.25 12C16.25 9.65279 14.3472 7.75 12 7.75ZM6.25 12C6.25 8.82436 8.82436 6.25 12 6.25C15.1756 6.25 17.75 8.82436 17.75 12C17.75 15.1756 15.1756 17.75 12 17.75C8.82436 17.75 6.25 15.1756 6.25 12ZM1.25 12C1.25 11.5858 1.58579 11.25 2 11.25H4C4.41421 11.25 4.75 11.5858 4.75 12C4.75 12.4142 4.41421 12.75 4 12.75H2C1.58579 12.75 1.25 12.4142 1.25 12ZM19.25 12C19.25 11.5858 19.5858 11.25 20 11.25H22C22.4142 11.25 22.75 11.5858 22.75 12C22.75 12.4142 22.4142 12.75 22 12.75H20C19.5858 12.75 19.25 12.4142 19.25 12ZM17.0255 17.0252C17.3184 16.7323 17.7933 16.7323 18.0862 17.0252L20.3082 19.2475C20.6011 19.5404 20.601 20.0153 20.3081 20.3082C20.0152 20.6011 19.5403 20.601 19.2475 20.3081L17.0255 18.0858C16.7326 17.7929 16.7326 17.3181 17.0255 17.0252ZM6.97467 17.0253C7.26756 17.3182 7.26756 17.7931 6.97467 18.086L4.75244 20.3082C4.45955 20.6011 3.98468 20.6011 3.69178 20.3082C3.39889 20.0153 3.39889 19.5404 3.69178 19.2476L5.91401 17.0253C6.2069 16.7324 6.68177 16.7324 6.97467 17.0253ZM12 19.25C12.4142 19.25 12.75 19.5858 12.75 20V22C12.75 22.4142 12.4142 22.75 12 22.75C11.5858 22.75 11.25 22.4142 11.25 22V20C11.25 19.5858 11.5858 19.25 12 19.25Z" fill="currentColor"></path>

</svg>

<svg aria-hidden="true" class="djdt-hidden theme-dark" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">

`  `<path d="M3.32031 11.6835C3.32031 16.6541 7.34975 20.6835 12.3203 20.6835C16.1075 20.6835 19.3483 18.3443 20.6768 15.032C19.6402 15.4486 18.5059 15.6834 17.3203 15.6834C12.3497 15.6834 8.32031 11.654 8.32031 6.68342C8.32031 5.50338 8.55165 4.36259 8.96453 3.32996C5.65605 4.66028 3.32031 7.89912 3.32031 11.6835Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>

</svg>

`        `</a>

`      `</li>





<li id="djdt-HistoryPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtHistoryPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Histórico" class="HistoryPanel">



`  `Histórico





`      `<br><small>/atividades/academicas/editar/2/?return\_url=/atividades/academicas/detalhar/2/</small>







`    `</a>



</li>





<li id="djdt-VersionsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtVersionsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Versões" class="VersionsPanel">



`  `Versões





`      `<br><small>Django 5.1.7</small>







`    `</a>



</li>





<li id="djdt-TimerPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtTimerPanel" checked="" title="Desativar para próximas requisições">



`    `<div class="djdt-contentless">



`  `Tempo





`      `<br><small>Total: 140.08ms</small>







`    `</div>



</li>





<li id="djdt-SettingsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSettingsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Settings from omaum.settings" class="SettingsPanel">



`  `Configurações













`    `</a>



</li>





<li id="djdt-HeadersPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtHeadersPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Cabeçalhos" class="HeadersPanel">



`  `Cabeçalhos













`    `</a>



</li>





<li id="djdt-RequestPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtRequestPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Requisição" class="RequestPanel">



`  `Requisição





`      `<br><small>editar\_atividade\_academica</small>







`    `</a>



</li>





<li id="djdt-SQLPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSQLPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="SQL queries from 1 connection" class="SQLPanel">



`  `SQL





`      `<br><small>11 queries in 9.31ms</small>







`    `</a>



</li>





<li id="djdt-StaticFilesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtStaticFilesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Arquivos estáticos (154 encontrados, 6 sendo utilizados)" class="StaticFilesPanel">



`  `Arquivos estáticos





`      `<br><small>6 arquivos utilizados</small>







`    `</a>



</li>





<li id="djdt-TemplatesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtTemplatesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Templates (12 renderizados)" class="TemplatesPanel">



`  `Templates





`      `<br><small>atividades/formulario\_atividade\_academica.html</small>







`    `</a>



</li>





<li id="djdt-AlertsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtAlertsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Alerts" class="AlertsPanel">



`  `Alerts













`    `</a>



</li>





<li id="djdt-CachePanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtCachePanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Chamadas ao cache de 1 backend" class="CachePanel">



`  `Cache





`      `<br><small>0 chamada em 0.00ms</small>







`    `</a>



</li>





<li id="djdt-SignalsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSignalsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Sinais" class="SignalsPanel">



`  `Sinais





`      `<br><small>35 receptores de 15 sinais</small>







`    `</a>



</li>





<li id="djdt-RedirectsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtRedirectsPanel" title="Habilitar para próximas requisições">



`    `<div class="djdt-contentless djdt-disabled">



`  `Interceptar redirecionamentos





`    `</div>



</li>





<li id="djdt-ProfilingPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtProfilingPanel" title="Habilitar para próximas requisições">



`    `<div class="djdt-contentless djdt-disabled">



`  `Profiling





`    `</div>



</li>



`    `</ul>

`  `</div>

`  `<div class="" id="djDebugToolbarHandle" style="top: 265px;">

`    `<div title="Mostrar barra de ferramentas" id="djShowToolBarButton">

`      `<span id="djShowToolBarD">D</span><span id="djShowToolBarJ">J</span>DT

`    `</div>

`  `</div>






`  `<div id="HistoryPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Histórico</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="VersionsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Versões</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>













`  `<div id="SettingsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Settings from omaum.settings</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="HeadersPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Cabeçalhos</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="RequestPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Requisição</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="SQLPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>SQL queries from 1 connection</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="StaticFilesPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Arquivos estáticos (154 encontrados, 6 sendo utilizados)</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="TemplatesPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Templates (12 renderizados)</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="AlertsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Alerts</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="CachePanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Chamadas ao cache de 1 backend</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="SignalsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Sinais</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>
















`  `<div id="djDebugWindow" class="djdt-panelContent djdt-hidden"></div>

</div>


</body>

<body>

`    `<!-- Cabeçalho/Barra de Navegação -->

`    `<header>

`        `<nav class="navbar navbar-expand-lg navbar-dark bg-primary">

`            `<div class="container">

`                `<a class="navbar-brand" href="/">

`                    `<img src="/static/img/logo.png" alt="OMAUM Logo" height="40">

`                `</a>

`                `<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">

`                    `<span class="navbar-toggler-icon"></span>

`                `</button>



`                `<div class="collapse navbar-collapse" id="navbarNav">

`                    `<ul class="navbar-nav me-auto">

`                        `<li class="nav-item">

`                            `<a class="nav-link " href="/">

`                                `<i class="fas fa-home"></i> Início

`                            `</a>

`                        `</li>





`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/alunos/">

`                                    `<i class="fas fa-user-graduate"></i> Alunos

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/cursos/">

`                                    `<i class="fas fa-book"></i> Cursos

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/turmas/">

`                                    `<i class="fas fa-users"></i> Turmas

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/matriculas/">

`                                    `<i class="fas fa-clipboard-list"></i> Matrículas

`                                `</a>

`                            `</li>

`                            `<li class="nav-item dropdown">

`                                `<a class="nav-link dropdown-toggle" href="#" id="navbarDropdownAtividades" role="button" data-bs-toggle="dropdown" aria-expanded="false">

`                                   `<i class="fas fa-calendar-alt"></i> Atividades

`                                `</a>

`                                `<ul class="dropdown-menu" aria-labelledby="navbarDropdownAtividades">

`                                    `<li>

`                                        `<a class="dropdown-item" href="/atividades/academicas/">

`                                            `<i class="fas fa-school"></i> Acadêmicas

`                                        `</a>

`                                    `</li>

`                                    `<li>

`                                        `<a class="dropdown-item" href="/atividades/ritualisticas/">

`                                            `<i class="fas fa-pray"></i> Ritualísticas

`                                        `</a>

`                                    `</li>

`                                `</ul>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/frequencias/">

`                                    `<i class="fas fa-check-square"></i> Frequências

`                                `</a>

`                            `</li>



`                    `</ul>



`                    `<ul class="navbar-nav">





`                                `<li class="nav-item">

`                                    `<a class="nav-link" href="/painel-controle/">

`                                        `<i class="fas fa-cog"></i> Painel de Controle

`                                    `</a>

`                                `</li>



`                            `<li class="nav-item dropdown">

`                                `<a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">

`                                   `<i class="fas fa-user-circle"></i> lcsilv3

`                                `</a>

`                                `<ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">

`                                    `<li><a class="dropdown-item" href="#">Meu Perfil</a></li>

`                                    `<li><hr class="dropdown-divider"></li>

`                                    `<li>

`                                        `<form method="post" action="/sair/" class="d-inline">

`                                            `<input type="hidden" name="csrfmiddlewaretoken" value="eCB62uRK9tIk1KwnfO2Dghn2j1TkLCzWDCoTE2R7tRHfooKXgmxiPfz8pciV0J0D">

`                                            `<button type="submit" class="dropdown-item">

`                                                `<i class="fas fa-sign-out-alt"></i> Sair

`                                            `</button>

`                                        `</form>

`                                    `</li>

`                                `</ul>

`                            `</li>



`                    `</ul>

`                `</div>

`            `</div>

`        `</nav>

`    `</header>



`    `<!-- Mensagens do sistema (flash messages) -->

`    `<div class="message-container">



`    `</div>



`    `<!-- Conteúdo principal -->

`    `<main id="main-content" class="py-4">



<div class="container mt-4">

`    `<div class="d-flex justify-content-between align-items-center mb-4">

`        `<h1>Copiar Atividade Acadêmica</h1>

`        `<a href="javascript:history.back()" class="btn btn-secondary">Voltar</a>

`    `</div>







`    `<div class="card mb-4">

`        `<div class="card-header">

`            `<h5>Atividade Original</h5>

`        `</div>

`        `<div class="card-body">

`            `<div class="row">

`                `<div class="col-md-6">

`                    `<p><strong>Nome:</strong> Plenilúnio</p>

`                    `<p><strong>Tipo:</strong> Aula</p>

`                    `<p><strong>Responsável:</strong> Não informado</p>

`                `</div>

`                `<div class="col-md-6">

`                    `<p><strong>Data de Início:</strong> 26/10/2026</p>

`                    `<p><strong>Data de Término:</strong> Não definida</p>

`                    `<p><strong>Turma:</strong> </p>

`                `</div>

`            `</div>

`            `<div class="row">

`                `<div class="col-md-12">

`                    `<p><strong>Descrição:</strong></p>

`                    `<p></p><p>Atividade acadêmica de plenilúnio</p><p></p>

`                `</div>

`            `</div>

`        `</div>

`    `</div>



`    `<form method="post">

`        `<input type="hidden" name="csrfmiddlewaretoken" value="eCB62uRK9tIk1KwnfO2Dghn2j1TkLCzWDCoTE2R7tRHfooKXgmxiPfz8pciV0J0D">





`        `<div class="card mb-4">

`            `<div class="card-header">

`                `<h5>Informações da Nova Atividade</h5>

`            `</div>

`            `<div class="card-body">

`                `<div class="row">

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_nome" class="form-label">Nome</label>

`    `<input type="text" name="nome" value="Cópia de Plenilúnio" class="form-control" maxlength="100" required="" id="id\_nome">





</div>

`                    `</div>

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="" class="form-label"></label>







</div>

`                    `</div>

`                `</div>

`                `<div class="row">

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_data\_inicio" class="form-label">Data de Início</label>

`    `<input type="date" name="data\_inicio" value="06/05/2025" class="form-control" required="" id="id\_data\_inicio"><input type="hidden" name="initial-data\_inicio" value="2025-05-06 12:39:47" id="initial-id\_data\_inicio">





</div>

`                    `</div>

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_data\_fim" class="form-label">Data de Término</label>

`    `<input type="date" name="data\_fim" class="form-control" id="id\_data\_fim">





</div>

`                    `</div>

`                `</div>

`                `<div class="row">

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_responsavel" class="form-label">Responsável</label>

`    `<input type="text" name="responsavel" class="form-control" maxlength="100" id="id\_responsavel">





</div>

`                    `</div>

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_local" class="form-label">Local</label>

`    `<input type="text" name="local" class="form-control" maxlength="100" id="id\_local">





</div>

`                    `</div>

`                `</div>

`                `<div class="row">

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_tipo\_atividade" class="form-label">Tipo de Atividade</label>

`    `<select name="tipo\_atividade" class="form-control" id="id\_tipo\_atividade">

`  `<option value="aula" selected="">Aula</option>

`  `<option value="palestra">Palestra</option>

`  `<option value="workshop">Workshop</option>

`  `<option value="seminario">Seminário</option>

`  `<option value="outro">Outro</option>

</select>





</div>

`                    `</div>

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_status" class="form-label">Status</label>

`    `<select name="status" class="form-control" id="id\_status">

`  `<option value="agendada" selected="">Agendada</option>

`  `<option value="em\_andamento">Em Andamento</option>

`  `<option value="concluida">Concluída</option>

`  `<option value="cancelada">Cancelada</option>

</select>





</div>

`                    `</div>

`                `</div>

`                `<div class="row">

`                    `<div class="col-md-12">

`                        `<div class="mb-3">

`    `<label for="id\_descricao" class="form-label">Descrição</label>

`    `<textarea name="descricao" cols="40" rows="3" class="form-control" id="id\_descricao">Atividade acadêmica de plenilúnio</textarea>





</div>

`                    `</div>

`                `</div>

`                `<div class="form-check mt-3">

`                    `<input class="form-check-input" type="checkbox" id="copiar\_frequencias" name="copiar\_frequencias">

`                    `<label class="form-check-label" for="copiar\_frequencias">

`                        `Copiar registros de frequência (se aplicável)

`                    `</label>

`                `</div>

`            `</div>

`        `</div>



`        `<div class="d-flex justify-content-between mb-5">

`            `<a href="javascript:history.back()" class="btn btn-secondary">Cancelar</a>

`            `<button type="submit" class="btn btn-primary">Criar Cópia</button>

`        `</div>

`    `</form>

</div>

`    `</main>



`    `<!-- Rodapé -->

`    `<footer class="footer mt-auto py-3 bg-light">

`        `<div class="container text-center">

`            `<span class="text-muted">© 2025 OMAUM - Sistema de Gestão de Iniciados</span>

`        `</div>

`    `</footer>



`    `<!-- Scripts de componentes globais -->

`    `<script src="/static/js/modules/dias-semana.js"></script>



`    `<!-- Scripts específicos da página -->





`    `<!-- Script global do sistema -->

`    `<script>

`        `// Inicialização global do site

`        `document.addEventListener('DOMContentLoaded', function() {

`            `// Inicializar tooltips do Bootstrap

`            `var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));

`            `var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {

`                `return new bootstrap.Tooltip(tooltipTriggerEl);

`            `});



`            `// Inicializar popovers do Bootstrap

`            `var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));

`            `var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {

`                `return new bootstrap.Popover(popoverTriggerEl);

`            `});



`            `// Verificação CSRF para AJAX

`            `function getCookie(name) {

`                `let cookieValue = null;

`                `if (document.cookie && document.cookie !== '') {

`                    `const cookies = document.cookie.split(';');

`                    `for (let i = 0; i < cookies.length; i++) {

`                        `const cookie = cookies[i].trim();

`                        `if (cookie.substring(0, name.length + 1) === (name + '=')) {

`                            `cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

`                            `break;

`                        `}

`                    `}

`                `}

`                `return cookieValue;

`            `}



`            `// Configuração global do AJAX para incluir o token CSRF

`            `$.ajaxSetup({

`                `beforeSend: function(xhr, settings) {

`                    `if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {

`                        `xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));

`                    `}

`                `}

`            `});



`            `// Verificação periódica do token CSRF para sessões longas

`            `setInterval(function() {

`                `$.get("/csrf\_check/");

`            `}, 3600000); // A cada hora



`            `// Aplicar máscaras globais

`            `if (typeof $.fn.mask === 'function') {

`                `$('.cpf-mask').mask('000.000.000-00');

`                `$('.cep-mask').mask('00000-000');

`                `$('.phone-mask').mask('(00) 0000-00009');

`                `$('.phone-mask').blur(function(event) {

`                    `if($(this).val().length == 15){

`                        `$('.phone-mask').mask('(00) 00000-0009');

`                    `} else {

`                        `$('.phone-mask').mask('(00) 0000-00009');

`                    `}

`                `});

`                `$('.date-mask').mask('00/00/0000');

`                `$('.time-mask').mask('00:00 às 00:00');

`            `}



`            `// Inicialização global do Select2

`            `if (typeof $.fn.select2 === 'function') {

`                `$('.select2').select2({

`                    `theme: 'bootstrap4',

`                    `width: '100%'

`                `});

`            `}

`        `});

`    `</script>

`    `<script src="/static/js/inicializar\_select2.js"></script>


<link rel="stylesheet" href="/static/debug\_toolbar/css/print.css" media="print">

<link rel="stylesheet" href="/static/debug\_toolbar/css/toolbar.css">


<script type="module" src="/static/debug\_toolbar/js/toolbar.js" async=""></script>

<div id="djDebug" class="" dir="ltr" data-store-id="d892138ffb284ae8b6ff10d80d571cfd" data-render-panel-url="/\_\_debug\_\_/render\_panel/" data-sidebar-url="/\_\_debug\_\_/history\_sidebar/" data-default-show="true" data-update-on-fetch="False" data-theme="auto">

`  `<div class="djdt-hidden" id="djDebugToolbar">

`    `<ul id="djDebugPanelList">

`      `<li><a id="djHideToolBarButton" href="#" title="Ocultar barra de ferramentas">Esconder »</a></li>

`      `<li>

`        `<a id="djToggleThemeButton" href="#" title="Toggle Theme">

`          `Toggle Theme <svg aria-hidden="true" class="djdt-hidden theme-auto" fill="currentColor" viewBox="0 0 32 32" version="1.1" xmlns="http://www.w3.org/2000/svg">

`  `<path d="M0 16q0 3.264 1.28 6.24t3.392 5.088 5.12 3.424 6.208 1.248q3.264 0 6.24-1.248t5.088-3.424 3.392-5.088 1.28-6.24-1.28-6.208-3.392-5.12-5.088-3.392-6.24-1.28q-3.264 0-6.208 1.28t-5.12 3.392-3.392 5.12-1.28 6.208zM4 16q0-3.264 1.6-6.016t4.384-4.352 6.016-1.632 6.016 1.632 4.384 4.352 1.6 6.016-1.6 6.048-4.384 4.352-6.016 1.6-6.016-1.6-4.384-4.352-1.6-6.048zM16 26.016q2.72 0 5.024-1.344t3.648-3.648 1.344-5.024-1.344-4.992-3.648-3.648-5.024-1.344v20z"></path>

</svg>

<svg aria-hidden="true" class="djdt-hidden theme-light" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">

`  `<path fill-rule="evenodd" clip-rule="evenodd" d="M12 1.25C12.4142 1.25 12.75 1.58579 12.75 2V4C12.75 4.41421 12.4142 4.75 12 4.75C11.5858 4.75 11.25 4.41421 11.25 4V2C11.25 1.58579 11.5858 1.25 12 1.25ZM3.66865 3.71609C3.94815 3.41039 4.42255 3.38915 4.72825 3.66865L6.95026 5.70024C7.25596 5.97974 7.2772 6.45413 6.9977 6.75983C6.7182 7.06553 6.2438 7.08677 5.9381 6.80727L3.71609 4.77569C3.41039 4.49619 3.38915 4.02179 3.66865 3.71609ZM20.3314 3.71609C20.6109 4.02179 20.5896 4.49619 20.2839 4.77569L18.0619 6.80727C17.7562 7.08677 17.2818 7.06553 17.0023 6.75983C16.7228 6.45413 16.744 5.97974 17.0497 5.70024L19.2718 3.66865C19.5775 3.38915 20.0518 3.41039 20.3314 3.71609ZM12 7.75C9.65279 7.75 7.75 9.65279 7.75 12C7.75 14.3472 9.65279 16.25 12 16.25C14.3472 16.25 16.25 14.3472 16.25 12C16.25 9.65279 14.3472 7.75 12 7.75ZM6.25 12C6.25 8.82436 8.82436 6.25 12 6.25C15.1756 6.25 17.75 8.82436 17.75 12C17.75 15.1756 15.1756 17.75 12 17.75C8.82436 17.75 6.25 15.1756 6.25 12ZM1.25 12C1.25 11.5858 1.58579 11.25 2 11.25H4C4.41421 11.25 4.75 11.5858 4.75 12C4.75 12.4142 4.41421 12.75 4 12.75H2C1.58579 12.75 1.25 12.4142 1.25 12ZM19.25 12C19.25 11.5858 19.5858 11.25 20 11.25H22C22.4142 11.25 22.75 11.5858 22.75 12C22.75 12.4142 22.4142 12.75 22 12.75H20C19.5858 12.75 19.25 12.4142 19.25 12ZM17.0255 17.0252C17.3184 16.7323 17.7933 16.7323 18.0862 17.0252L20.3082 19.2475C20.6011 19.5404 20.601 20.0153 20.3081 20.3082C20.0152 20.6011 19.5403 20.601 19.2475 20.3081L17.0255 18.0858C16.7326 17.7929 16.7326 17.3181 17.0255 17.0252ZM6.97467 17.0253C7.26756 17.3182 7.26756 17.7931 6.97467 18.086L4.75244 20.3082C4.45955 20.6011 3.98468 20.6011 3.69178 20.3082C3.39889 20.0153 3.39889 19.5404 3.69178 19.2476L5.91401 17.0253C6.2069 16.7324 6.68177 16.7324 6.97467 17.0253ZM12 19.25C12.4142 19.25 12.75 19.5858 12.75 20V22C12.75 22.4142 12.4142 22.75 12 22.75C11.5858 22.75 11.25 22.4142 11.25 22V20C11.25 19.5858 11.5858 19.25 12 19.25Z" fill="currentColor"></path>

</svg>

<svg aria-hidden="true" class="djdt-hidden theme-dark" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">

`  `<path d="M3.32031 11.6835C3.32031 16.6541 7.34975 20.6835 12.3203 20.6835C16.1075 20.6835 19.3483 18.3443 20.6768 15.032C19.6402 15.4486 18.5059 15.6834 17.3203 15.6834C12.3497 15.6834 8.32031 11.654 8.32031 6.68342C8.32031 5.50338 8.55165 4.36259 8.96453 3.32996C5.65605 4.66028 3.32031 7.89912 3.32031 11.6835Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>

</svg>

`        `</a>

`      `</li>





<li id="djdt-HistoryPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtHistoryPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Histórico" class="HistoryPanel">



`  `Histórico





`      `<br><small>/atividades/academicas/2/copiar/</small>







`    `</a>



</li>





<li id="djdt-VersionsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtVersionsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Versões" class="VersionsPanel">



`  `Versões





`      `<br><small>Django 5.1.7</small>







`    `</a>



</li>





<li id="djdt-TimerPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtTimerPanel" checked="" title="Desativar para próximas requisições">



`    `<div class="djdt-contentless">



`  `Tempo





`      `<br><small>Total: 53.93ms</small>







`    `</div>



</li>





<li id="djdt-SettingsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSettingsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Settings from omaum.settings" class="SettingsPanel">



`  `Configurações













`    `</a>



</li>





<li id="djdt-HeadersPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtHeadersPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Cabeçalhos" class="HeadersPanel">



`  `Cabeçalhos













`    `</a>



</li>





<li id="djdt-RequestPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtRequestPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Requisição" class="RequestPanel">



`  `Requisição





`      `<br><small>copiar\_atividade\_academica</small>







`    `</a>



</li>





<li id="djdt-SQLPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSQLPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="SQL queries from 1 connection" class="SQLPanel">



`  `SQL





`      `<br><small>3 queries in 2.77ms</small>







`    `</a>



</li>





<li id="djdt-StaticFilesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtStaticFilesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Arquivos estáticos (154 encontrados, 6 sendo utilizados)" class="StaticFilesPanel">



`  `Arquivos estáticos





`      `<br><small>6 arquivos utilizados</small>







`    `</a>



</li>





<li id="djdt-TemplatesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtTemplatesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Templates (12 renderizados)" class="TemplatesPanel">



`  `Templates





`      `<br><small>atividades/copiar\_atividade\_academica.html</small>







`    `</a>



</li>





<li id="djdt-AlertsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtAlertsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Alerts" class="AlertsPanel">



`  `Alerts













`    `</a>



</li>





<li id="djdt-CachePanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtCachePanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Chamadas ao cache de 1 backend" class="CachePanel">



`  `Cache





`      `<br><small>0 chamada em 0.00ms</small>







`    `</a>



</li>





<li id="djdt-SignalsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSignalsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Sinais" class="SignalsPanel">



`  `Sinais





`      `<br><small>35 receptores de 15 sinais</small>







`    `</a>



</li>





<li id="djdt-RedirectsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtRedirectsPanel" title="Habilitar para próximas requisições">



`    `<div class="djdt-contentless djdt-disabled">



`  `Interceptar redirecionamentos





`    `</div>



</li>





<li id="djdt-ProfilingPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtProfilingPanel" title="Habilitar para próximas requisições">



`    `<div class="djdt-contentless djdt-disabled">



`  `Profiling





`    `</div>



</li>



`    `</ul>

`  `</div>

`  `<div class="" id="djDebugToolbarHandle" style="top: 265px;">

`    `<div title="Mostrar barra de ferramentas" id="djShowToolBarButton">

`      `<span id="djShowToolBarD">D</span><span id="djShowToolBarJ">J</span>DT

`    `</div>

`  `</div>






`  `<div id="HistoryPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Histórico</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="VersionsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Versões</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>













`  `<div id="SettingsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Settings from omaum.settings</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="HeadersPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Cabeçalhos</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="RequestPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Requisição</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="SQLPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>SQL queries from 1 connection</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="StaticFilesPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Arquivos estáticos (154 encontrados, 6 sendo utilizados)</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="TemplatesPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Templates (12 renderizados)</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="AlertsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Alerts</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="CachePanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Chamadas ao cache de 1 backend</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="SignalsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Sinais</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>
















`  `<div id="djDebugWindow" class="djdt-panelContent djdt-hidden"></div>

</div>


</body>

<body>

`    `<!-- Cabeçalho/Barra de Navegação -->

`    `<header>

`        `<nav class="navbar navbar-expand-lg navbar-dark bg-primary">

`            `<div class="container">

`                `<a class="navbar-brand" href="/">

`                    `<img src="/static/img/logo.png" alt="OMAUM Logo" height="40">

`                `</a>

`                `<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">

`                    `<span class="navbar-toggler-icon"></span>

`                `</button>



`                `<div class="collapse navbar-collapse" id="navbarNav">

`                    `<ul class="navbar-nav me-auto">

`                        `<li class="nav-item">

`                            `<a class="nav-link " href="/">

`                                `<i class="fas fa-home"></i> Início

`                            `</a>

`                        `</li>





`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/alunos/">

`                                    `<i class="fas fa-user-graduate"></i> Alunos

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/cursos/">

`                                    `<i class="fas fa-book"></i> Cursos

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/turmas/">

`                                    `<i class="fas fa-users"></i> Turmas

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/matriculas/">

`                                    `<i class="fas fa-clipboard-list"></i> Matrículas

`                                `</a>

`                            `</li>

`                            `<li class="nav-item dropdown">

`                                `<a class="nav-link dropdown-toggle" href="#" id="navbarDropdownAtividades" role="button" data-bs-toggle="dropdown" aria-expanded="false">

`                                   `<i class="fas fa-calendar-alt"></i> Atividades

`                                `</a>

`                                `<ul class="dropdown-menu" aria-labelledby="navbarDropdownAtividades">

`                                    `<li>

`                                        `<a class="dropdown-item" href="/atividades/academicas/">

`                                            `<i class="fas fa-school"></i> Acadêmicas

`                                        `</a>

`                                    `</li>

`                                    `<li>

`                                        `<a class="dropdown-item" href="/atividades/ritualisticas/">

`                                            `<i class="fas fa-pray"></i> Ritualísticas

`                                        `</a>

`                                    `</li>

`                                `</ul>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/frequencias/">

`                                    `<i class="fas fa-check-square"></i> Frequências

`                                `</a>

`                            `</li>



`                    `</ul>



`                    `<ul class="navbar-nav">





`                                `<li class="nav-item">

`                                    `<a class="nav-link" href="/painel-controle/">

`                                        `<i class="fas fa-cog"></i> Painel de Controle

`                                    `</a>

`                                `</li>



`                            `<li class="nav-item dropdown">

`                                `<a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">

`                                   `<i class="fas fa-user-circle"></i> lcsilv3

`                                `</a>

`                                `<ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">

`                                    `<li><a class="dropdown-item" href="#">Meu Perfil</a></li>

`                                    `<li><hr class="dropdown-divider"></li>

`                                    `<li>

`                                        `<form method="post" action="/sair/" class="d-inline">

`                                            `<input type="hidden" name="csrfmiddlewaretoken" value="nRmcyCC9ObNvtmKBw37C8lxVfksDoCBOMR9ZaaCw8zMqQ0YbxBChHjJ1lvReDJ2v">

`                                            `<button type="submit" class="dropdown-item">

`                                                `<i class="fas fa-sign-out-alt"></i> Sair

`                                            `</button>

`                                        `</form>

`                                    `</li>

`                                `</ul>

`                            `</li>



`                    `</ul>

`                `</div>

`            `</div>

`        `</nav>

`    `</header>



`    `<!-- Mensagens do sistema (flash messages) -->

`    `<div class="message-container">



`    `</div>



`    `<!-- Conteúdo principal -->

`    `<main id="main-content" class="py-4">



<div class="container mt-4">

`    `<div class="d-flex justify-content-between align-items-center mb-4">

`        `<h1>Relatório de Atividades</h1>

`        `<div>

`            `<a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>

`            `<a href="/atividades/calendario/" class="btn btn-info me-2">

`                `<i class="fas fa-calendar-alt"></i> Calendário

`            `</a>

`            `<a href="/atividades/dashboard/" class="btn btn-success me-2">

`                `<i class="fas fa-chart-bar"></i> Dashboard

`            `</a>

`            `<div class="btn-group">

`                `<a href="/atividades/academicas/" class="btn btn-outline-primary">Atividades Acadêmicas</a>

`                `<a href="/atividades/ritualisticas/" class="btn btn-outline-info">Atividades Ritualísticas</a>

`            `</div>

`        `</div>

`    `</div>



`    `<!-- Filtros -->

`    `<div class="card mb-4">

`        `<div class="card-header">

`            `<h5 class="mb-0">Filtros</h5>

`        `</div>

`        `<div class="card-body">

`            `<form method="get" class="row g-3">

`                `<div class="col-md-3">

`                    `<label for="tipo" class="form-label">Tipo de Atividade</label>

`                    `<select name="tipo" id="tipo" class="form-select">

`                        `<option value="todas" selected="">Todas</option>

`                        `<option value="academicas">Acadêmicas</option>

`                        `<option value="ritualisticas">Ritualísticas</option>

`                    `</select>

`                `</div>

`                `<div class="col-md-3">

`                    `<label for="status" class="form-label">Status</label>

`                    `<select name="status" id="status" class="form-select">

`                        `<option value="">Todos</option>

`                        `<option value="agendada">Agendada</option>

`                        `<option value="em\_andamento">Em Andamento</option>

`                        `<option value="concluida">Concluída</option>

`                        `<option value="cancelada">Cancelada</option>

`                    `</select>

`                `</div>

`                `<div class="col-md-3">

`                    `<label for="data\_inicio" class="form-label">Data Início</label>

`                    `<input type="date" name="data\_inicio" id="data\_inicio" class="form-control" value="">

`                `</div>

`                `<div class="col-md-3">

`                    `<label for="data\_fim" class="form-label">Data Fim</label>

`                    `<input type="date" name="data\_fim" id="data\_fim" class="form-control" value="">

`                `</div>

`                `<div class="col-md-12 d-flex justify-content-end">

`                    `<button type="submit" class="btn btn-primary me-2">Filtrar</button>

`                    `<a href="/atividades/relatorio/" class="btn btn-secondary">Limpar Filtros</a>

`                `</div>

`            `</form>

`        `</div>

`    `</div>



`    `<!-- Botões de exportação -->

`    `<div class="mb-4">

`        `<a href="/atividades/exportar/pdf/?" class="btn btn-danger me-2">

`            `<i class="fas fa-file-pdf"></i> Exportar PDF

`        `</a>

`        `<a href="/atividades/exportar/excel/?" class="btn btn-success me-2">

`            `<i class="fas fa-file-excel"></i> Exportar Excel

`        `</a>

`        `<a href="/atividades/exportar/csv/?" class="btn btn-info">

`            `<i class="fas fa-file-csv"></i> Exportar CSV

`        `</a>

`    `</div>



`    `<!-- Resumo -->

`    `<div class="row mb-4">

`        `<div class="col-md-4">

`            `<div class="card bg-light">

`                `<div class="card-body text-center">

`                    `<h5 class="card-title">Total de Atividades</h5>

`                    `<p class="display-4">2</p>

`                `</div>

`            `</div>

`        `</div>

`        `<div class="col-md-4">

`            `<div class="card bg-primary text-white">

`                `<div class="card-body text-center">

`                    `<h5 class="card-title">Atividades Acadêmicas</h5>

`                    `<p class="display-4">2</p>

`                `</div>

`            `</div>

`        `</div>

`        `<div class="col-md-4">

`            `<div class="card bg-info text-white">

`                `<div class="card-body text-center">

`                    `<h5 class="card-title">Atividades Ritualísticas</h5>

`                    `<p class="display-4">0</p>

`                `</div>

`            `</div>

`        `</div>

`    `</div>



`    `<!-- Tabela de resultados -->

`    `<div class="card">

`        `<div class="card-header">

`            `<h5 class="mb-0">Resultados</h5>

`        `</div>

`        `<div class="card-body">

`            `<ul class="nav nav-tabs mb-3" id="myTab" role="tablist">

`                `<li class="nav-item" role="presentation">

`                    `<button class="nav-link active" id="academicas-tab" data-bs-toggle="tab" data-bs-target="#academicas" type="button" role="tab" aria-controls="academicas" aria-selected="true">

`                        `Atividades Acadêmicas

`                    `</button>

`                `</li>

`                `<li class="nav-item" role="presentation">

`                    `<button class="nav-link" id="ritualisticas-tab" data-bs-toggle="tab" data-bs-target="#ritualisticas" type="button" role="tab" aria-controls="ritualisticas" aria-selected="false">

`                        `Atividades Ritualísticas

`                    `</button>

`                `</li>

`            `</ul>

`            `<div class="tab-content" id="myTabContent">

`                `<!-- Atividades Acadêmicas -->

`                `<div class="tab-pane fade show active" id="academicas" role="tabpanel" aria-labelledby="academicas-tab">

`                    `<div class="table-responsive">

`                        `<table class="table table-striped">

`                            `<thead>

`                                `<tr>

`                                    `<th>Nome</th>

`                                    `<th>Tipo</th>

`                                    `<th>Data de Início</th>

`                                    `<th>Status</th>

`                                    `<th>Responsável</th>

`                                    `<th>Turmas</th>

`                                `</tr>

`                            `</thead>

`                            `<tbody>



`                                `<tr>

`                                    `<td>

`                                        `<a href="/atividades/academicas/detalhar/1/">

`                                            `Aula

`                                        `</a>

`                                    `</td>

`                                    `<td>Aula</td>

`                                    `<td>26/10/2024</td>

`                                    `<td>

`                                        `<span class="badge bg-warning">

`                                            `Agendada

`                                        `</span>

`                                    `</td>

`                                    `<td>Não informado</td>

`                                    `<td>



`                                            `<span class="badge bg-primary">A</span>



`                                    `</td>

`                                `</tr>



`                                `<tr>

`                                    `<td>

`                                        `<a href="/atividades/academicas/detalhar/2/">

`                                            `Plenilúnio

`                                        `</a>

`                                    `</td>

`                                    `<td>Aula</td>

`                                    `<td>26/10/2026</td>

`                                    `<td>

`                                        `<span class="badge bg-warning">

`                                            `Agendada

`                                        `</span>

`                                    `</td>

`                                    `<td>Não informado</td>

`                                    `<td>



`                                            `<span class="badge bg-primary">A</span>



`                                    `</td>

`                                `</tr>



`                            `</tbody>

`                        `</table>

`                    `</div>

`                `</div>



`                `<!-- Atividades Ritualísticas -->

`                `<div class="tab-pane fade" id="ritualisticas" role="tabpanel" aria-labelledby="ritualisticas-tab">

`                    `<div class="table-responsive">

`                        `<table class="table table-striped">

`                            `<thead>

`                                `<tr>

`                                    `<th>Nome</th>

`                                    `<th>Data</th>

`                                    `<th>Horário</th>

`                                    `<th>Local</th>

`                                    `<th>Turma</th>

`                                    `<th>Participantes</th>

`                                `</tr>

`                            `</thead>

`                            `<tbody>



`                                `<tr>

`                                    `<td colspan="6" class="text-center">Nenhuma atividade ritualística encontrada.</td>

`                                `</tr>



`                            `</tbody>

`                        `</table>

`                    `</div>

`                `</div>

`            `</div>

`        `</div>

`    `</div>

</div>

`    `</main>



`    `<!-- Rodapé -->

`    `<footer class="footer mt-auto py-3 bg-light">

`        `<div class="container text-center">

`            `<span class="text-muted">© 2025 OMAUM - Sistema de Gestão de Iniciados</span>

`        `</div>

`    `</footer>



`    `<!-- Scripts de componentes globais -->

`    `<script src="/static/js/modules/dias-semana.js"></script>



`    `<!-- Scripts específicos da página -->





`    `<!-- Script global do sistema -->

`    `<script>

`        `// Inicialização global do site

`        `document.addEventListener('DOMContentLoaded', function() {

`            `// Inicializar tooltips do Bootstrap

`            `var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));

`            `var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {

`                `return new bootstrap.Tooltip(tooltipTriggerEl);

`            `});



`            `// Inicializar popovers do Bootstrap

`            `var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));

`            `var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {

`                `return new bootstrap.Popover(popoverTriggerEl);

`            `});



`            `// Verificação CSRF para AJAX

`            `function getCookie(name) {

`                `let cookieValue = null;

`                `if (document.cookie && document.cookie !== '') {

`                    `const cookies = document.cookie.split(';');

`                    `for (let i = 0; i < cookies.length; i++) {

`                        `const cookie = cookies[i].trim();

`                        `if (cookie.substring(0, name.length + 1) === (name + '=')) {

`                            `cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

`                            `break;

`                        `}

`                    `}

`                `}

`                `return cookieValue;

`            `}



`            `// Configuração global do AJAX para incluir o token CSRF

`            `$.ajaxSetup({

`                `beforeSend: function(xhr, settings) {

`                    `if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {

`                        `xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));

`                    `}

`                `}

`            `});



`            `// Verificação periódica do token CSRF para sessões longas

`            `setInterval(function() {

`                `$.get("/csrf\_check/");

`            `}, 3600000); // A cada hora



`            `// Aplicar máscaras globais

`            `if (typeof $.fn.mask === 'function') {

`                `$('.cpf-mask').mask('000.000.000-00');

`                `$('.cep-mask').mask('00000-000');

`                `$('.phone-mask').mask('(00) 0000-00009');

`                `$('.phone-mask').blur(function(event) {

`                    `if($(this).val().length == 15){

`                        `$('.phone-mask').mask('(00) 00000-0009');

`                    `} else {

`                        `$('.phone-mask').mask('(00) 0000-00009');

`                    `}

`                `});

`                `$('.date-mask').mask('00/00/0000');

`                `$('.time-mask').mask('00:00 às 00:00');

`            `}



`            `// Inicialização global do Select2

`            `if (typeof $.fn.select2 === 'function') {

`                `$('.select2').select2({

`                    `theme: 'bootstrap4',

`                    `width: '100%'

`                `});

`            `}

`        `});

`    `</script>

`    `<script src="/static/js/inicializar\_select2.js"></script>


<link rel="stylesheet" href="/static/debug\_toolbar/css/print.css" media="print">

<link rel="stylesheet" href="/static/debug\_toolbar/css/toolbar.css">


<script type="module" src="/static/debug\_toolbar/js/toolbar.js" async=""></script>

<div id="djDebug" class="" dir="ltr" data-store-id="da6b22b7f46245dcbe37321fb00d3705" data-render-panel-url="/\_\_debug\_\_/render\_panel/" data-sidebar-url="/\_\_debug\_\_/history\_sidebar/" data-default-show="true" data-update-on-fetch="False" data-theme="auto">

`  `<div class="djdt-hidden" id="djDebugToolbar">

`    `<ul id="djDebugPanelList">

`      `<li><a id="djHideToolBarButton" href="#" title="Ocultar barra de ferramentas">Esconder »</a></li>

`      `<li>

`        `<a id="djToggleThemeButton" href="#" title="Toggle Theme">

`          `Toggle Theme <svg aria-hidden="true" class="djdt-hidden theme-auto" fill="currentColor" viewBox="0 0 32 32" version="1.1" xmlns="http://www.w3.org/2000/svg">

`  `<path d="M0 16q0 3.264 1.28 6.24t3.392 5.088 5.12 3.424 6.208 1.248q3.264 0 6.24-1.248t5.088-3.424 3.392-5.088 1.28-6.24-1.28-6.208-3.392-5.12-5.088-3.392-6.24-1.28q-3.264 0-6.208 1.28t-5.12 3.392-3.392 5.12-1.28 6.208zM4 16q0-3.264 1.6-6.016t4.384-4.352 6.016-1.632 6.016 1.632 4.384 4.352 1.6 6.016-1.6 6.048-4.384 4.352-6.016 1.6-6.016-1.6-4.384-4.352-1.6-6.048zM16 26.016q2.72 0 5.024-1.344t3.648-3.648 1.344-5.024-1.344-4.992-3.648-3.648-5.024-1.344v20z"></path>

</svg>

<svg aria-hidden="true" class="djdt-hidden theme-light" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">

`  `<path fill-rule="evenodd" clip-rule="evenodd" d="M12 1.25C12.4142 1.25 12.75 1.58579 12.75 2V4C12.75 4.41421 12.4142 4.75 12 4.75C11.5858 4.75 11.25 4.41421 11.25 4V2C11.25 1.58579 11.5858 1.25 12 1.25ZM3.66865 3.71609C3.94815 3.41039 4.42255 3.38915 4.72825 3.66865L6.95026 5.70024C7.25596 5.97974 7.2772 6.45413 6.9977 6.75983C6.7182 7.06553 6.2438 7.08677 5.9381 6.80727L3.71609 4.77569C3.41039 4.49619 3.38915 4.02179 3.66865 3.71609ZM20.3314 3.71609C20.6109 4.02179 20.5896 4.49619 20.2839 4.77569L18.0619 6.80727C17.7562 7.08677 17.2818 7.06553 17.0023 6.75983C16.7228 6.45413 16.744 5.97974 17.0497 5.70024L19.2718 3.66865C19.5775 3.38915 20.0518 3.41039 20.3314 3.71609ZM12 7.75C9.65279 7.75 7.75 9.65279 7.75 12C7.75 14.3472 9.65279 16.25 12 16.25C14.3472 16.25 16.25 14.3472 16.25 12C16.25 9.65279 14.3472 7.75 12 7.75ZM6.25 12C6.25 8.82436 8.82436 6.25 12 6.25C15.1756 6.25 17.75 8.82436 17.75 12C17.75 15.1756 15.1756 17.75 12 17.75C8.82436 17.75 6.25 15.1756 6.25 12ZM1.25 12C1.25 11.5858 1.58579 11.25 2 11.25H4C4.41421 11.25 4.75 11.5858 4.75 12C4.75 12.4142 4.41421 12.75 4 12.75H2C1.58579 12.75 1.25 12.4142 1.25 12ZM19.25 12C19.25 11.5858 19.5858 11.25 20 11.25H22C22.4142 11.25 22.75 11.5858 22.75 12C22.75 12.4142 22.4142 12.75 22 12.75H20C19.5858 12.75 19.25 12.4142 19.25 12ZM17.0255 17.0252C17.3184 16.7323 17.7933 16.7323 18.0862 17.0252L20.3082 19.2475C20.6011 19.5404 20.601 20.0153 20.3081 20.3082C20.0152 20.6011 19.5403 20.601 19.2475 20.3081L17.0255 18.0858C16.7326 17.7929 16.7326 17.3181 17.0255 17.0252ZM6.97467 17.0253C7.26756 17.3182 7.26756 17.7931 6.97467 18.086L4.75244 20.3082C4.45955 20.6011 3.98468 20.6011 3.69178 20.3082C3.39889 20.0153 3.39889 19.5404 3.69178 19.2476L5.91401 17.0253C6.2069 16.7324 6.68177 16.7324 6.97467 17.0253ZM12 19.25C12.4142 19.25 12.75 19.5858 12.75 20V22C12.75 22.4142 12.4142 22.75 12 22.75C11.5858 22.75 11.25 22.4142 11.25 22V20C11.25 19.5858 11.5858 19.25 12 19.25Z" fill="currentColor"></path>

</svg>

<svg aria-hidden="true" class="djdt-hidden theme-dark" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">

`  `<path d="M3.32031 11.6835C3.32031 16.6541 7.34975 20.6835 12.3203 20.6835C16.1075 20.6835 19.3483 18.3443 20.6768 15.032C19.6402 15.4486 18.5059 15.6834 17.3203 15.6834C12.3497 15.6834 8.32031 11.654 8.32031 6.68342C8.32031 5.50338 8.55165 4.36259 8.96453 3.32996C5.65605 4.66028 3.32031 7.89912 3.32031 11.6835Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>

</svg>

`        `</a>

`      `</li>





<li id="djdt-HistoryPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtHistoryPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Histórico" class="HistoryPanel">



`  `Histórico





`      `<br><small>/atividades/relatorio/</small>







`    `</a>



</li>





<li id="djdt-VersionsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtVersionsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Versões" class="VersionsPanel">



`  `Versões





`      `<br><small>Django 5.1.7</small>







`    `</a>



</li>





<li id="djdt-TimerPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtTimerPanel" checked="" title="Desativar para próximas requisições">



`    `<div class="djdt-contentless">



`  `Tempo





`      `<br><small>Total: 123.09ms</small>







`    `</div>



</li>





<li id="djdt-SettingsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSettingsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Settings from omaum.settings" class="SettingsPanel">



`  `Configurações













`    `</a>



</li>





<li id="djdt-HeadersPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtHeadersPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Cabeçalhos" class="HeadersPanel">



`  `Cabeçalhos













`    `</a>



</li>





<li id="djdt-RequestPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtRequestPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Requisição" class="RequestPanel">



`  `Requisição





`      `<br><small>relatorio\_atividades</small>







`    `</a>



</li>





<li id="djdt-SQLPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSQLPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="SQL queries from 1 connection" class="SQLPanel">



`  `SQL





`      `<br><small>8 queries in 8.78ms</small>







`    `</a>



</li>





<li id="djdt-StaticFilesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtStaticFilesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Arquivos estáticos (154 encontrados, 6 sendo utilizados)" class="StaticFilesPanel">



`  `Arquivos estáticos





`      `<br><small>6 arquivos utilizados</small>







`    `</a>



</li>





<li id="djdt-TemplatesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtTemplatesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Templates (2 renderizados)" class="TemplatesPanel">



`  `Templates





`      `<br><small>atividades/relatorio\_atividades.html</small>







`    `</a>



</li>





<li id="djdt-AlertsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtAlertsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Alerts" class="AlertsPanel">



`  `Alerts













`    `</a>



</li>





<li id="djdt-CachePanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtCachePanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Chamadas ao cache de 1 backend" class="CachePanel">



`  `Cache





`      `<br><small>0 chamada em 0.00ms</small>







`    `</a>



</li>





<li id="djdt-SignalsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSignalsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Sinais" class="SignalsPanel">



`  `Sinais





`      `<br><small>35 receptores de 15 sinais</small>







`    `</a>



</li>





<li id="djdt-RedirectsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtRedirectsPanel" title="Habilitar para próximas requisições">



`    `<div class="djdt-contentless djdt-disabled">



`  `Interceptar redirecionamentos





`    `</div>



</li>





<li id="djdt-ProfilingPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtProfilingPanel" title="Habilitar para próximas requisições">



`    `<div class="djdt-contentless djdt-disabled">



`  `Profiling





`    `</div>



</li>



`    `</ul>

`  `</div>

`  `<div class="" id="djDebugToolbarHandle" style="top: 265px;">

`    `<div title="Mostrar barra de ferramentas" id="djShowToolBarButton">

`      `<span id="djShowToolBarD">D</span><span id="djShowToolBarJ">J</span>DT

`    `</div>

`  `</div>






`  `<div id="HistoryPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Histórico</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="VersionsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Versões</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>













`  `<div id="SettingsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Settings from omaum.settings</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="HeadersPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Cabeçalhos</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="RequestPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Requisição</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="SQLPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>SQL queries from 1 connection</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="StaticFilesPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Arquivos estáticos (154 encontrados, 6 sendo utilizados)</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="TemplatesPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Templates (2 renderizados)</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="AlertsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Alerts</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="CachePanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Chamadas ao cache de 1 backend</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="SignalsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Sinais</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>
















`  `<div id="djDebugWindow" class="djdt-panelContent djdt-hidden"></div>

</div>


</body>

<body>

`    `<!-- Cabeçalho/Barra de Navegação -->

`    `<header>

`        `<nav class="navbar navbar-expand-lg navbar-dark bg-primary">

`            `<div class="container">

`                `<a class="navbar-brand" href="/">

`                    `<img src="/static/img/logo.png" alt="OMAUM Logo" height="40">

`                `</a>

`                `<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">

`                    `<span class="navbar-toggler-icon"></span>

`                `</button>



`                `<div class="collapse navbar-collapse" id="navbarNav">

`                    `<ul class="navbar-nav me-auto">

`                        `<li class="nav-item">

`                            `<a class="nav-link " href="/">

`                                `<i class="fas fa-home"></i> Início

`                            `</a>

`                        `</li>





`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/alunos/">

`                                    `<i class="fas fa-user-graduate"></i> Alunos

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/cursos/">

`                                    `<i class="fas fa-book"></i> Cursos

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/turmas/">

`                                    `<i class="fas fa-users"></i> Turmas

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/matriculas/">

`                                    `<i class="fas fa-clipboard-list"></i> Matrículas

`                                `</a>

`                            `</li>

`                            `<li class="nav-item dropdown">

`                                `<a class="nav-link dropdown-toggle" href="#" id="navbarDropdownAtividades" role="button" data-bs-toggle="dropdown" aria-expanded="false">

`                                   `<i class="fas fa-calendar-alt"></i> Atividades

`                                `</a>

`                                `<ul class="dropdown-menu" aria-labelledby="navbarDropdownAtividades">

`                                    `<li>

`                                        `<a class="dropdown-item" href="/atividades/academicas/">

`                                            `<i class="fas fa-school"></i> Acadêmicas

`                                        `</a>

`                                    `</li>

`                                    `<li>

`                                        `<a class="dropdown-item" href="/atividades/ritualisticas/">

`                                            `<i class="fas fa-pray"></i> Ritualísticas

`                                        `</a>

`                                    `</li>

`                                `</ul>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/frequencias/">

`                                    `<i class="fas fa-check-square"></i> Frequências

`                                `</a>

`                            `</li>



`                    `</ul>



`                    `<ul class="navbar-nav">





`                                `<li class="nav-item">

`                                    `<a class="nav-link" href="/painel-controle/">

`                                        `<i class="fas fa-cog"></i> Painel de Controle

`                                    `</a>

`                                `</li>



`                            `<li class="nav-item dropdown">

`                                `<a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">

`                                   `<i class="fas fa-user-circle"></i> lcsilv3

`                                `</a>

`                                `<ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">

`                                    `<li><a class="dropdown-item" href="#">Meu Perfil</a></li>

`                                    `<li><hr class="dropdown-divider"></li>

`                                    `<li>

`                                        `<form method="post" action="/sair/" class="d-inline">

`                                            `<input type="hidden" name="csrfmiddlewaretoken" value="cnH00f43AXD6kXdwAoUekRTgRbL6nIwHBnuNCN4qUlC1HBr6BWpTTP5mXmaHCPXo">

`                                            `<button type="submit" class="dropdown-item">

`                                                `<i class="fas fa-sign-out-alt"></i> Sair

`                                            `</button>

`                                        `</form>

`                                    `</li>

`                                `</ul>

`                            `</li>



`                    `</ul>

`                `</div>

`            `</div>

`        `</nav>

`    `</header>



`    `<!-- Mensagens do sistema (flash messages) -->

`    `<div class="message-container">



`    `</div>



`    `<!-- Conteúdo principal -->

`    `<main id="main-content" class="py-4">



<div class="container mt-4">

`    `<!-- Cabeçalho com título e botões na mesma linha -->

`    `<div class="d-flex justify-content-between align-items-center mb-3">

`        `<h1>Lista de Atividades Ritualísticas</h1>

`        `<div class="btn-group">

`            `<a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>

`            `<!-- Botão para criar nova atividade ritualística -->

`            `<a href="/atividades/ritualisticas/criar/?return\_url=/atividades/ritualisticas/" class="btn btn-primary me-2">

`                `<i class="fas fa-plus"></i> Nova Atividade

`            `</a>



`            `<!-- Botões para as novas funcionalidades -->

`            `<a href="/atividades/calendario/" class="btn btn-info me-2">

`                `<i class="fas fa-calendar-alt"></i> Calendário

`            `</a>



`            `<a href="/atividades/dashboard/" class="btn btn-success me-2">

`                `<i class="fas fa-chart-bar"></i> Dashboard

`            `</a>



`            `<a href="/atividades/relatorio/" class="btn btn-warning">

`                `<i class="fas fa-file-alt"></i> Relatórios

`            `</a>

`        `</div>

`    `</div>    

`    `<!-- Barra de busca e filtros -->

`    `<div class="card mb-4">

`        `<div class="card-header">

`            `<form method="get" class="row g-3">

`                `<div class="col-md-6">

`                    `<input type="text" name="q" class="form-control" placeholder="Buscar por nome, descrição ou local..." value="">

`                `</div>

`                `<div class="col-md-2">

`                    `<button type="submit" class="btn btn-primary w-100">Filtrar</button>

`                `</div>

`            `</form>

`        `</div>

`        `<div class="card-body">

`            `<div class="table-responsive">

`                `<table class="table table-striped">

`                    `<thead>

`                        `<tr>

`                            `<th>Nome</th>

`                            `<th>Data</th>

`                            `<th>Horário</th>

`                            `<th>Local</th>

`                            `<th>Turma</th>

`                            `<th>Ações</th>

`                        `</tr>

`                    `</thead>

`                    `<tbody>



`                            `<tr>

`                                `<td colspan="6" class="text-center">

`                                    `<p class="my-3">Nenhuma atividade ritualística cadastrada.</p>

`                                `</td>

`                            `</tr>



`                    `</tbody>

`                `</table>

`            `</div>

`        `</div>

`        `<div class="card-footer">

`            `<p class="text-muted mb-0">Total: 0 atividade(s)</p>



`        `</div>

`    `</div>

</div>

`    `</main>



`    `<!-- Rodapé -->

`    `<footer class="footer mt-auto py-3 bg-light">

`        `<div class="container text-center">

`            `<span class="text-muted">© 2025 OMAUM - Sistema de Gestão de Iniciados</span>

`        `</div>

`    `</footer>



`    `<!-- Scripts de componentes globais -->

`    `<script src="/static/js/modules/dias-semana.js"></script>



`    `<!-- Scripts específicos da página -->





`    `<!-- Script global do sistema -->

`    `<script>

`        `// Inicialização global do site

`        `document.addEventListener('DOMContentLoaded', function() {

`            `// Inicializar tooltips do Bootstrap

`            `var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));

`            `var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {

`                `return new bootstrap.Tooltip(tooltipTriggerEl);

`            `});



`            `// Inicializar popovers do Bootstrap

`            `var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));

`            `var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {

`                `return new bootstrap.Popover(popoverTriggerEl);

`            `});



`            `// Verificação CSRF para AJAX

`            `function getCookie(name) {

`                `let cookieValue = null;

`                `if (document.cookie && document.cookie !== '') {

`                    `const cookies = document.cookie.split(';');

`                    `for (let i = 0; i < cookies.length; i++) {

`                        `const cookie = cookies[i].trim();

`                        `if (cookie.substring(0, name.length + 1) === (name + '=')) {

`                            `cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

`                            `break;

`                        `}

`                    `}

`                `}

`                `return cookieValue;

`            `}



`            `// Configuração global do AJAX para incluir o token CSRF

`            `$.ajaxSetup({

`                `beforeSend: function(xhr, settings) {

`                    `if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {

`                        `xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));

`                    `}

`                `}

`            `});



`            `// Verificação periódica do token CSRF para sessões longas

`            `setInterval(function() {

`                `$.get("/csrf\_check/");

`            `}, 3600000); // A cada hora



`            `// Aplicar máscaras globais

`            `if (typeof $.fn.mask === 'function') {

`                `$('.cpf-mask').mask('000.000.000-00');

`                `$('.cep-mask').mask('00000-000');

`                `$('.phone-mask').mask('(00) 0000-00009');

`                `$('.phone-mask').blur(function(event) {

`                    `if($(this).val().length == 15){

`                        `$('.phone-mask').mask('(00) 00000-0009');

`                    `} else {

`                        `$('.phone-mask').mask('(00) 0000-00009');

`                    `}

`                `});

`                `$('.date-mask').mask('00/00/0000');

`                `$('.time-mask').mask('00:00 às 00:00');

`            `}



`            `// Inicialização global do Select2

`            `if (typeof $.fn.select2 === 'function') {

`                `$('.select2').select2({

`                    `theme: 'bootstrap4',

`                    `width: '100%'

`                `});

`            `}

`        `});

`    `</script>

`    `<script src="/static/js/inicializar\_select2.js"></script>


<link rel="stylesheet" href="/static/debug\_toolbar/css/print.css" media="print">

<link rel="stylesheet" href="/static/debug\_toolbar/css/toolbar.css">


<script type="module" src="/static/debug\_toolbar/js/toolbar.js" async=""></script>

<div id="djDebug" class="" dir="ltr" data-store-id="bf0458403d2a4680a4c92b444bfebbac" data-render-panel-url="/\_\_debug\_\_/render\_panel/" data-sidebar-url="/\_\_debug\_\_/history\_sidebar/" data-default-show="true" data-update-on-fetch="False" data-theme="auto">

`  `<div class="djdt-hidden" id="djDebugToolbar">

`    `<ul id="djDebugPanelList">

`      `<li><a id="djHideToolBarButton" href="#" title="Ocultar barra de ferramentas">Esconder »</a></li>

`      `<li>

`        `<a id="djToggleThemeButton" href="#" title="Toggle Theme">

`          `Toggle Theme <svg aria-hidden="true" class="djdt-hidden theme-auto" fill="currentColor" viewBox="0 0 32 32" version="1.1" xmlns="http://www.w3.org/2000/svg">

`  `<path d="M0 16q0 3.264 1.28 6.24t3.392 5.088 5.12 3.424 6.208 1.248q3.264 0 6.24-1.248t5.088-3.424 3.392-5.088 1.28-6.24-1.28-6.208-3.392-5.12-5.088-3.392-6.24-1.28q-3.264 0-6.208 1.28t-5.12 3.392-3.392 5.12-1.28 6.208zM4 16q0-3.264 1.6-6.016t4.384-4.352 6.016-1.632 6.016 1.632 4.384 4.352 1.6 6.016-1.6 6.048-4.384 4.352-6.016 1.6-6.016-1.6-4.384-4.352-1.6-6.048zM16 26.016q2.72 0 5.024-1.344t3.648-3.648 1.344-5.024-1.344-4.992-3.648-3.648-5.024-1.344v20z"></path>

</svg>

<svg aria-hidden="true" class="djdt-hidden theme-light" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">

`  `<path fill-rule="evenodd" clip-rule="evenodd" d="M12 1.25C12.4142 1.25 12.75 1.58579 12.75 2V4C12.75 4.41421 12.4142 4.75 12 4.75C11.5858 4.75 11.25 4.41421 11.25 4V2C11.25 1.58579 11.5858 1.25 12 1.25ZM3.66865 3.71609C3.94815 3.41039 4.42255 3.38915 4.72825 3.66865L6.95026 5.70024C7.25596 5.97974 7.2772 6.45413 6.9977 6.75983C6.7182 7.06553 6.2438 7.08677 5.9381 6.80727L3.71609 4.77569C3.41039 4.49619 3.38915 4.02179 3.66865 3.71609ZM20.3314 3.71609C20.6109 4.02179 20.5896 4.49619 20.2839 4.77569L18.0619 6.80727C17.7562 7.08677 17.2818 7.06553 17.0023 6.75983C16.7228 6.45413 16.744 5.97974 17.0497 5.70024L19.2718 3.66865C19.5775 3.38915 20.0518 3.41039 20.3314 3.71609ZM12 7.75C9.65279 7.75 7.75 9.65279 7.75 12C7.75 14.3472 9.65279 16.25 12 16.25C14.3472 16.25 16.25 14.3472 16.25 12C16.25 9.65279 14.3472 7.75 12 7.75ZM6.25 12C6.25 8.82436 8.82436 6.25 12 6.25C15.1756 6.25 17.75 8.82436 17.75 12C17.75 15.1756 15.1756 17.75 12 17.75C8.82436 17.75 6.25 15.1756 6.25 12ZM1.25 12C1.25 11.5858 1.58579 11.25 2 11.25H4C4.41421 11.25 4.75 11.5858 4.75 12C4.75 12.4142 4.41421 12.75 4 12.75H2C1.58579 12.75 1.25 12.4142 1.25 12ZM19.25 12C19.25 11.5858 19.5858 11.25 20 11.25H22C22.4142 11.25 22.75 11.5858 22.75 12C22.75 12.4142 22.4142 12.75 22 12.75H20C19.5858 12.75 19.25 12.4142 19.25 12ZM17.0255 17.0252C17.3184 16.7323 17.7933 16.7323 18.0862 17.0252L20.3082 19.2475C20.6011 19.5404 20.601 20.0153 20.3081 20.3082C20.0152 20.6011 19.5403 20.601 19.2475 20.3081L17.0255 18.0858C16.7326 17.7929 16.7326 17.3181 17.0255 17.0252ZM6.97467 17.0253C7.26756 17.3182 7.26756 17.7931 6.97467 18.086L4.75244 20.3082C4.45955 20.6011 3.98468 20.6011 3.69178 20.3082C3.39889 20.0153 3.39889 19.5404 3.69178 19.2476L5.91401 17.0253C6.2069 16.7324 6.68177 16.7324 6.97467 17.0253ZM12 19.25C12.4142 19.25 12.75 19.5858 12.75 20V22C12.75 22.4142 12.4142 22.75 12 22.75C11.5858 22.75 11.25 22.4142 11.25 22V20C11.25 19.5858 11.5858 19.25 12 19.25Z" fill="currentColor"></path>

</svg>

<svg aria-hidden="true" class="djdt-hidden theme-dark" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">

`  `<path d="M3.32031 11.6835C3.32031 16.6541 7.34975 20.6835 12.3203 20.6835C16.1075 20.6835 19.3483 18.3443 20.6768 15.032C19.6402 15.4486 18.5059 15.6834 17.3203 15.6834C12.3497 15.6834 8.32031 11.654 8.32031 6.68342C8.32031 5.50338 8.55165 4.36259 8.96453 3.32996C5.65605 4.66028 3.32031 7.89912 3.32031 11.6835Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>

</svg>

`        `</a>

`      `</li>





<li id="djdt-HistoryPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtHistoryPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Histórico" class="HistoryPanel">



`  `Histórico





`      `<br><small>/atividades/ritualisticas/</small>







`    `</a>



</li>





<li id="djdt-VersionsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtVersionsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Versões" class="VersionsPanel">



`  `Versões





`      `<br><small>Django 5.1.7</small>







`    `</a>



</li>





<li id="djdt-TimerPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtTimerPanel" checked="" title="Desativar para próximas requisições">



`    `<div class="djdt-contentless">



`  `Tempo





`      `<br><small>Total: 116.99ms</small>







`    `</div>



</li>





<li id="djdt-SettingsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSettingsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Settings from omaum.settings" class="SettingsPanel">



`  `Configurações













`    `</a>



</li>





<li id="djdt-HeadersPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtHeadersPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Cabeçalhos" class="HeadersPanel">



`  `Cabeçalhos













`    `</a>



</li>





<li id="djdt-RequestPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtRequestPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Requisição" class="RequestPanel">



`  `Requisição





`      `<br><small>listar\_atividades\_ritualisticas</small>







`    `</a>



</li>





<li id="djdt-SQLPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSQLPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="SQL queries from 1 connection" class="SQLPanel">



`  `SQL





`      `<br><small>3 queries in 3.63ms</small>







`    `</a>



</li>





<li id="djdt-StaticFilesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtStaticFilesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Arquivos estáticos (154 encontrados, 6 sendo utilizados)" class="StaticFilesPanel">



`  `Arquivos estáticos





`      `<br><small>6 arquivos utilizados</small>







`    `</a>



</li>





<li id="djdt-TemplatesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtTemplatesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Templates (2 renderizados)" class="TemplatesPanel">



`  `Templates





`      `<br><small>atividades/listar\_atividades\_ritualisticas.html</small>







`    `</a>



</li>





<li id="djdt-AlertsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtAlertsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Alerts" class="AlertsPanel">



`  `Alerts













`    `</a>



</li>





<li id="djdt-CachePanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtCachePanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Chamadas ao cache de 1 backend" class="CachePanel">



`  `Cache





`      `<br><small>0 chamada em 0.00ms</small>







`    `</a>



</li>





<li id="djdt-SignalsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSignalsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Sinais" class="SignalsPanel">



`  `Sinais





`      `<br><small>35 receptores de 15 sinais</small>







`    `</a>



</li>





<li id="djdt-RedirectsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtRedirectsPanel" title="Habilitar para próximas requisições">



`    `<div class="djdt-contentless djdt-disabled">



`  `Interceptar redirecionamentos





`    `</div>



</li>





<li id="djdt-ProfilingPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtProfilingPanel" title="Habilitar para próximas requisições">



`    `<div class="djdt-contentless djdt-disabled">



`  `Profiling





`    `</div>



</li>



`    `</ul>

`  `</div>

`  `<div class="" id="djDebugToolbarHandle" style="top: 265px;">

`    `<div title="Mostrar barra de ferramentas" id="djShowToolBarButton">

`      `<span id="djShowToolBarD">D</span><span id="djShowToolBarJ">J</span>DT

`    `</div>

`  `</div>






`  `<div id="HistoryPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Histórico</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="VersionsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Versões</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>













`  `<div id="SettingsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Settings from omaum.settings</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="HeadersPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Cabeçalhos</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="RequestPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Requisição</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="SQLPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>SQL queries from 1 connection</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="StaticFilesPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Arquivos estáticos (154 encontrados, 6 sendo utilizados)</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="TemplatesPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Templates (2 renderizados)</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="AlertsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Alerts</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="CachePanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Chamadas ao cache de 1 backend</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="SignalsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Sinais</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>
















`  `<div id="djDebugWindow" class="djdt-panelContent djdt-hidden"></div>

</div>


</body>

<body>

`    `<!-- Cabeçalho/Barra de Navegação -->

`    `<header>

`        `<nav class="navbar navbar-expand-lg navbar-dark bg-primary">

`            `<div class="container">

`                `<a class="navbar-brand" href="/">

`                    `<img src="/static/img/logo.png" alt="OMAUM Logo" height="40">

`                `</a>

`                `<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">

`                    `<span class="navbar-toggler-icon"></span>

`                `</button>



`                `<div class="collapse navbar-collapse" id="navbarNav">

`                    `<ul class="navbar-nav me-auto">

`                        `<li class="nav-item">

`                            `<a class="nav-link " href="/">

`                                `<i class="fas fa-home"></i> Início

`                            `</a>

`                        `</li>





`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/alunos/">

`                                    `<i class="fas fa-user-graduate"></i> Alunos

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/cursos/">

`                                    `<i class="fas fa-book"></i> Cursos

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/turmas/">

`                                    `<i class="fas fa-users"></i> Turmas

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/matriculas/">

`                                    `<i class="fas fa-clipboard-list"></i> Matrículas

`                                `</a>

`                            `</li>

`                            `<li class="nav-item dropdown">

`                                `<a class="nav-link dropdown-toggle" href="#" id="navbarDropdownAtividades" role="button" data-bs-toggle="dropdown" aria-expanded="false">

`                                   `<i class="fas fa-calendar-alt"></i> Atividades

`                                `</a>

`                                `<ul class="dropdown-menu" aria-labelledby="navbarDropdownAtividades">

`                                    `<li>

`                                        `<a class="dropdown-item" href="/atividades/academicas/">

`                                            `<i class="fas fa-school"></i> Acadêmicas

`                                        `</a>

`                                    `</li>

`                                    `<li>

`                                        `<a class="dropdown-item" href="/atividades/ritualisticas/">

`                                            `<i class="fas fa-pray"></i> Ritualísticas

`                                        `</a>

`                                    `</li>

`                                `</ul>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/frequencias/">

`                                    `<i class="fas fa-check-square"></i> Frequências

`                                `</a>

`                            `</li>



`                    `</ul>



`                    `<ul class="navbar-nav">





`                                `<li class="nav-item">

`                                    `<a class="nav-link" href="/painel-controle/">

`                                        `<i class="fas fa-cog"></i> Painel de Controle

`                                    `</a>

`                                `</li>



`                            `<li class="nav-item dropdown">

`                                `<a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">

`                                   `<i class="fas fa-user-circle"></i> lcsilv3

`                                `</a>

`                                `<ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">

`                                    `<li><a class="dropdown-item" href="#">Meu Perfil</a></li>

`                                    `<li><hr class="dropdown-divider"></li>

`                                    `<li>

`                                        `<form method="post" action="/sair/" class="d-inline">

`                                            `<input type="hidden" name="csrfmiddlewaretoken" value="OwaXVydyhGzFf9ZLvlreoxIYmx432OkUdwXKx6dVB4yACNdlwTWTXvU4sItEhVLB">

`                                            `<button type="submit" class="dropdown-item">

`                                                `<i class="fas fa-sign-out-alt"></i> Sair

`                                            `</button>

`                                        `</form>

`                                    `</li>

`                                `</ul>

`                            `</li>



`                    `</ul>

`                `</div>

`            `</div>

`        `</nav>

`    `</header>



`    `<!-- Mensagens do sistema (flash messages) -->

`    `<div class="message-container">



`    `</div>



`    `<!-- Conteúdo principal -->

`    `<main id="main-content" class="py-4">



<div class="container mt-4">

`    `<div class="d-flex justify-content-between align-items-center mb-4">

`        `<h1>Criar Nova Atividade Ritualística</h1>

`        `<a href="/atividades/ritualisticas/" class="btn btn-secondary">Voltar para a lista</a>

`    `</div>







`    `<form method="post">

`        `<input type="hidden" name="csrfmiddlewaretoken" value="OwaXVydyhGzFf9ZLvlreoxIYmx432OkUdwXKx6dVB4yACNdlwTWTXvU4sItEhVLB">





`        `<div class="card mb-4">

`            `<div class="card-header">

`                `<h5>Informações Básicas</h5>

`            `</div>

`            `<div class="card-body">

`                `<div class="row">

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_nome" class="form-label">Nome</label>

`    `<input type="text" name="nome" class="form-control" maxlength="100" required="" id="id\_nome">





</div>

`                    `</div>

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_local" class="form-label">Local</label>

`    `<input type="text" name="local" class="form-control" maxlength="100" required="" id="id\_local">





</div>

`                    `</div>

`                `</div>

`                `<div class="row">

`                    `<div class="col-md-12">

`                        `<div class="mb-3">

`    `<label for="id\_descricao" class="form-label">Descrição</label>

`    `<textarea name="descricao" cols="40" rows="3" class="form-control" id="id\_descricao"></textarea>





</div>

`                    `</div>

`                `</div>

`            `</div>

`        `</div>



`        `<div class="card mb-4">

`            `<div class="card-header">

`                `<h5>Data e Horário</h5>

`            `</div>

`            `<div class="card-body">

`                `<div class="row">

`                    `<div class="col-md-4">

`                        `<div class="mb-3">

`    `<label for="id\_data" class="form-label">Data</label>

`    `<input type="date" name="data" class="form-control" required="" id="id\_data">





</div>

`                    `</div>

`                    `<div class="col-md-4">

`                        `<div class="mb-3">

`    `<label for="id\_hora\_inicio" class="form-label">Hora de Início</label>

`    `<input type="time" name="hora\_inicio" class="form-control" required="" id="id\_hora\_inicio">





</div>

`                    `</div>

`                    `<div class="col-md-4">

`                        `<div class="mb-3">

`    `<label for="id\_hora\_fim" class="form-label">Hora de Término</label>

`    `<input type="time" name="hora\_fim" class="form-control" required="" id="id\_hora\_fim">





</div>

`                    `</div>

`                `</div>

`            `</div>

`        `</div>



`        `<div class="card mb-4">

`            `<div class="card-header">

`                `<h5>Turma e Participantes</h5>

`            `</div>

`            `<div class="card-body">

`                `<div class="row">

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_turma" class="form-label">Turma</label>

`    `<select name="turma" class="form-control" required="" id="id\_turma">

`  `<option value="" selected="">---------</option>

`  `<option value="6">D - Introdução à Meditação</option>

`  `<option value="2">A - Introdução à Meditação</option>

`  `<option value="4">B - Introdução à Meditação</option>

`  `<option value="5">C - Introdução à Meditação</option>

</select>





</div>

`                    `</div>

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_todos\_alunos" class="form-label">Incluir todos os alunos da turma</label>

`    `<input type="checkbox" name="todos\_alunos" id="id\_todos\_alunos">





</div>

`                        `<small class="form-text text-muted">Marque esta opção para incluir automaticamente todos os alunos da turma.</small>

`                    `</div>

`                `</div>



`                `<div class="row mt-3" id="participantes-container" style="display: block;">

`                    `<div class="col-md-12">

`                        `<label for="id\_participantes">Participantes</label>

`                        `<div class="border p-3 rounded">

`                            `<select name="participantes" class="form-control select2-hidden-accessible" id="id\_participantes" multiple="" data-select2-id="select2-data-id\_participantes" tabindex="-1" aria-hidden="true">

`  `<option value="18027737038">Aline Souza</option>

`  `<option value="71012661207">Ana Ferreira</option>

`  `<option value="61714562670">Ana Pereira</option>

`  `<option value="96931040271">André Costa</option>

`  `<option value="57431572587">Bruno Ribeiro</option>

`  `<option value="15645038797">Caic Passos Cardoso Da Silva</option>

`  `<option value="16335805186">Camila Oliveira</option>

`  `<option value="19529676522">Daniela Mendes</option>

`  `<option value="37663960965">Felipe Costa</option>

`  `<option value="25185348461">Felipe Souza</option>

`  `<option value="51286148744">Fernanda Costa</option>

`  `<option value="29807388257">Fernanda Martins</option>

`  `<option value="19403318172">Gustavo Araújo</option>

`  `<option value="08832339202">Gustavo Barbosa</option>

`  `<option value="60795674660">Gustavo Rocha</option>

`  `<option value="52551221829">João Pereira</option>

`  `<option value="12345678901">João Silva</option>

`  `<option value="85736517952">Juliana Lima</option>

`  `<option value="30624167050">Lucas Araújo</option>

`  `<option value="81991045700">Luis Carlos Da Silva</option>

`  `<option value="27789400090">Marcelo Nascimento</option>

`  `<option value="21451098237">Marcelo Oliveira</option>

`  `<option value="05584938593">Maria Carvalho</option>

`  `<option value="98765432109">Maria Oliveira</option>

`  `<option value="11129399978">Maria Rodrigues</option>

`  `<option value="11794022817">Mariana Ribeiro</option>

`  `<option value="49405540240">Mariana Rocha</option>

`  `<option value="40518102926">Pedro Araújo</option>

`  `<option value="03404794223">Pedro Carvalho</option>

`  `<option value="97794010840">Pedro Mendes</option>

`  `<option value="70010205369">Pedro Nascimento</option>

`  `<option value="89748235253">Rodrigo Araújo</option>

`  `<option value="51727155004">Rodrigo Carvalho</option>

`  `<option value="51623759179">Rodrigo Nascimento</option>

`  `<option value="12331179719">Thays Passos Da Silva</option>

</select><span class="select2 select2-container select2-container--bootstrap4" dir="ltr" data-select2-id="select2-data-1-r65q" style="width: 100%;"><span class="selection"><span class="select2-selection select2-selection--multiple" role="combobox" aria-haspopup="true" aria-expanded="false" tabindex="-1" aria-disabled="false"><ul class="select2-selection\_\_rendered" id="select2-id\_participantes-container"></ul><span class="select2-search select2-search--inline"><textarea class="select2-search\_\_field" type="search" tabindex="0" autocorrect="off" autocapitalize="none" spellcheck="false" role="searchbox" aria-autocomplete="list" autocomplete="off" aria-label="Search" aria-describedby="select2-id\_participantes-container" placeholder="Selecione as opções" style="width: 100%;"></textarea></span></span></span><span class="dropdown-wrapper" aria-hidden="true"></span></span>

`                        `</div>



`                    `</div>

`                `</div>

`            `</div>

`        `</div>



`        `<div class="d-flex justify-content-between mb-5">

`            `<a href="/atividades/ritualisticas/" class="btn btn-secondary">Cancelar</a>

`            `<button type="submit" class="btn btn-primary">Criar Atividade</button>

`        `</div>

`    `</form>

</div>

`    `</main>



`    `<!-- Rodapé -->

`    `<footer class="footer mt-auto py-3 bg-light">

`        `<div class="container text-center">

`            `<span class="text-muted">© 2025 OMAUM - Sistema de Gestão de Iniciados</span>

`        `</div>

`    `</footer>



`    `<!-- Scripts de componentes globais -->

`    `<script src="/static/js/modules/dias-semana.js"></script>



`    `<!-- Scripts específicos da página -->



<script>

`    `document.addEventListener('DOMContentLoaded', function() {

`        `const todosAlunosCheckbox = document.getElementById('id\_todos\_alunos');

`        `const participantesContainer = document.getElementById('participantes-container');



`        `function toggleParticipantes() {

`            `if (todosAlunosCheckbox.checked) {

`                `participantesContainer.style.display = 'none';

`            `} else {

`                `participantesContainer.style.display = 'block';

`            `}

`        `}



`        `// Inicializar

`        `toggleParticipantes();



`        `// Adicionar listener para mudanças

`        `todosAlunosCheckbox.addEventListener('change', toggleParticipantes);

`    `});

</script>



`    `<!-- Script global do sistema -->

`    `<script>

`        `// Inicialização global do site

`        `document.addEventListener('DOMContentLoaded', function() {

`            `// Inicializar tooltips do Bootstrap

`            `var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));

`            `var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {

`                `return new bootstrap.Tooltip(tooltipTriggerEl);

`            `});



`            `// Inicializar popovers do Bootstrap

`            `var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));

`            `var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {

`                `return new bootstrap.Popover(popoverTriggerEl);

`            `});



`            `// Verificação CSRF para AJAX

`            `function getCookie(name) {

`                `let cookieValue = null;

`                `if (document.cookie && document.cookie !== '') {

`                    `const cookies = document.cookie.split(';');

`                    `for (let i = 0; i < cookies.length; i++) {

`                        `const cookie = cookies[i].trim();

`                        `if (cookie.substring(0, name.length + 1) === (name + '=')) {

`                            `cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

`                            `break;

`                        `}

`                    `}

`                `}

`                `return cookieValue;

`            `}



`            `// Configuração global do AJAX para incluir o token CSRF

`            `$.ajaxSetup({

`                `beforeSend: function(xhr, settings) {

`                    `if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {

`                        `xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));

`                    `}

`                `}

`            `});



`            `// Verificação periódica do token CSRF para sessões longas

`            `setInterval(function() {

`                `$.get("/csrf\_check/");

`            `}, 3600000); // A cada hora



`            `// Aplicar máscaras globais

`            `if (typeof $.fn.mask === 'function') {

`                `$('.cpf-mask').mask('000.000.000-00');

`                `$('.cep-mask').mask('00000-000');

`                `$('.phone-mask').mask('(00) 0000-00009');

`                `$('.phone-mask').blur(function(event) {

`                    `if($(this).val().length == 15){

`                        `$('.phone-mask').mask('(00) 00000-0009');

`                    `} else {

`                        `$('.phone-mask').mask('(00) 0000-00009');

`                    `}

`                `});

`                `$('.date-mask').mask('00/00/0000');

`                `$('.time-mask').mask('00:00 às 00:00');

`            `}



`            `// Inicialização global do Select2

`            `if (typeof $.fn.select2 === 'function') {

`                `$('.select2').select2({

`                    `theme: 'bootstrap4',

`                    `width: '100%'

`                `});

`            `}

`        `});

`    `</script>

`    `<script src="/static/js/inicializar\_select2.js"></script>


<link rel="stylesheet" href="/static/debug\_toolbar/css/print.css" media="print">

<link rel="stylesheet" href="/static/debug\_toolbar/css/toolbar.css">


<script type="module" src="/static/debug\_toolbar/js/toolbar.js" async=""></script>

<div id="djDebug" class="" dir="ltr" data-store-id="93e89f7bddd44cd2a61ee5d7589d0a43" data-render-panel-url="/\_\_debug\_\_/render\_panel/" data-sidebar-url="/\_\_debug\_\_/history\_sidebar/" data-default-show="true" data-update-on-fetch="False" data-theme="auto">

`  `<div class="djdt-hidden" id="djDebugToolbar">

`    `<ul id="djDebugPanelList">

`      `<li><a id="djHideToolBarButton" href="#" title="Ocultar barra de ferramentas">Esconder »</a></li>

`      `<li>

`        `<a id="djToggleThemeButton" href="#" title="Toggle Theme">

`          `Toggle Theme <svg aria-hidden="true" class="djdt-hidden theme-auto" fill="currentColor" viewBox="0 0 32 32" version="1.1" xmlns="http://www.w3.org/2000/svg">

`  `<path d="M0 16q0 3.264 1.28 6.24t3.392 5.088 5.12 3.424 6.208 1.248q3.264 0 6.24-1.248t5.088-3.424 3.392-5.088 1.28-6.24-1.28-6.208-3.392-5.12-5.088-3.392-6.24-1.28q-3.264 0-6.208 1.28t-5.12 3.392-3.392 5.12-1.28 6.208zM4 16q0-3.264 1.6-6.016t4.384-4.352 6.016-1.632 6.016 1.632 4.384 4.352 1.6 6.016-1.6 6.048-4.384 4.352-6.016 1.6-6.016-1.6-4.384-4.352-1.6-6.048zM16 26.016q2.72 0 5.024-1.344t3.648-3.648 1.344-5.024-1.344-4.992-3.648-3.648-5.024-1.344v20z"></path>

</svg>

<svg aria-hidden="true" class="djdt-hidden theme-light" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">

`  `<path fill-rule="evenodd" clip-rule="evenodd" d="M12 1.25C12.4142 1.25 12.75 1.58579 12.75 2V4C12.75 4.41421 12.4142 4.75 12 4.75C11.5858 4.75 11.25 4.41421 11.25 4V2C11.25 1.58579 11.5858 1.25 12 1.25ZM3.66865 3.71609C3.94815 3.41039 4.42255 3.38915 4.72825 3.66865L6.95026 5.70024C7.25596 5.97974 7.2772 6.45413 6.9977 6.75983C6.7182 7.06553 6.2438 7.08677 5.9381 6.80727L3.71609 4.77569C3.41039 4.49619 3.38915 4.02179 3.66865 3.71609ZM20.3314 3.71609C20.6109 4.02179 20.5896 4.49619 20.2839 4.77569L18.0619 6.80727C17.7562 7.08677 17.2818 7.06553 17.0023 6.75983C16.7228 6.45413 16.744 5.97974 17.0497 5.70024L19.2718 3.66865C19.5775 3.38915 20.0518 3.41039 20.3314 3.71609ZM12 7.75C9.65279 7.75 7.75 9.65279 7.75 12C7.75 14.3472 9.65279 16.25 12 16.25C14.3472 16.25 16.25 14.3472 16.25 12C16.25 9.65279 14.3472 7.75 12 7.75ZM6.25 12C6.25 8.82436 8.82436 6.25 12 6.25C15.1756 6.25 17.75 8.82436 17.75 12C17.75 15.1756 15.1756 17.75 12 17.75C8.82436 17.75 6.25 15.1756 6.25 12ZM1.25 12C1.25 11.5858 1.58579 11.25 2 11.25H4C4.41421 11.25 4.75 11.5858 4.75 12C4.75 12.4142 4.41421 12.75 4 12.75H2C1.58579 12.75 1.25 12.4142 1.25 12ZM19.25 12C19.25 11.5858 19.5858 11.25 20 11.25H22C22.4142 11.25 22.75 11.5858 22.75 12C22.75 12.4142 22.4142 12.75 22 12.75H20C19.5858 12.75 19.25 12.4142 19.25 12ZM17.0255 17.0252C17.3184 16.7323 17.7933 16.7323 18.0862 17.0252L20.3082 19.2475C20.6011 19.5404 20.601 20.0153 20.3081 20.3082C20.0152 20.6011 19.5403 20.601 19.2475 20.3081L17.0255 18.0858C16.7326 17.7929 16.7326 17.3181 17.0255 17.0252ZM6.97467 17.0253C7.26756 17.3182 7.26756 17.7931 6.97467 18.086L4.75244 20.3082C4.45955 20.6011 3.98468 20.6011 3.69178 20.3082C3.39889 20.0153 3.39889 19.5404 3.69178 19.2476L5.91401 17.0253C6.2069 16.7324 6.68177 16.7324 6.97467 17.0253ZM12 19.25C12.4142 19.25 12.75 19.5858 12.75 20V22C12.75 22.4142 12.4142 22.75 12 22.75C11.5858 22.75 11.25 22.4142 11.25 22V20C11.25 19.5858 11.5858 19.25 12 19.25Z" fill="currentColor"></path>

</svg>

<svg aria-hidden="true" class="djdt-hidden theme-dark" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">

`  `<path d="M3.32031 11.6835C3.32031 16.6541 7.34975 20.6835 12.3203 20.6835C16.1075 20.6835 19.3483 18.3443 20.6768 15.032C19.6402 15.4486 18.5059 15.6834 17.3203 15.6834C12.3497 15.6834 8.32031 11.654 8.32031 6.68342C8.32031 5.50338 8.55165 4.36259 8.96453 3.32996C5.65605 4.66028 3.32031 7.89912 3.32031 11.6835Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>

</svg>

`        `</a>

`      `</li>





<li id="djdt-HistoryPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtHistoryPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Histórico" class="HistoryPanel">



`  `Histórico





`      `<br><small>/atividades/ritualisticas/criar/?return\_url=/atividades/ritualisticas/</small>







`    `</a>



</li>





<li id="djdt-VersionsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtVersionsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Versões" class="VersionsPanel">



`  `Versões





`      `<br><small>Django 5.1.7</small>







`    `</a>



</li>





<li id="djdt-TimerPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtTimerPanel" checked="" title="Desativar para próximas requisições">



`    `<div class="djdt-contentless">



`  `Tempo





`      `<br><small>Total: 373.88ms</small>







`    `</div>



</li>





<li id="djdt-SettingsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSettingsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Settings from omaum.settings" class="SettingsPanel">



`  `Configurações













`    `</a>



</li>





<li id="djdt-HeadersPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtHeadersPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Cabeçalhos" class="HeadersPanel">



`  `Cabeçalhos













`    `</a>



</li>





<li id="djdt-RequestPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtRequestPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Requisição" class="RequestPanel">



`  `Requisição





`      `<br><small>criar\_atividade\_ritualistica</small>







`    `</a>



</li>





<li id="djdt-SQLPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSQLPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="SQL queries from 1 connection" class="SQLPanel">



`  `SQL





`      `<br><small>8 queries in 22.69ms</small>







`    `</a>



</li>





<li id="djdt-StaticFilesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtStaticFilesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Arquivos estáticos (154 encontrados, 6 sendo utilizados)" class="StaticFilesPanel">



`  `Arquivos estáticos





`      `<br><small>6 arquivos utilizados</small>







`    `</a>



</li>





<li id="djdt-TemplatesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtTemplatesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Templates (11 renderizados)" class="TemplatesPanel">



`  `Templates





`      `<br><small>atividades/criar\_atividade\_ritualistica.html</small>







`    `</a>



</li>





<li id="djdt-AlertsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtAlertsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Alerts" class="AlertsPanel">



`  `Alerts













`    `</a>



</li>





<li id="djdt-CachePanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtCachePanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Chamadas ao cache de 1 backend" class="CachePanel">



`  `Cache





`      `<br><small>0 chamada em 0.00ms</small>







`    `</a>



</li>





<li id="djdt-SignalsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSignalsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Sinais" class="SignalsPanel">



`  `Sinais





`      `<br><small>35 receptores de 15 sinais</small>







`    `</a>



</li>





<li id="djdt-RedirectsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtRedirectsPanel" title="Habilitar para próximas requisições">



`    `<div class="djdt-contentless djdt-disabled">



`  `Interceptar redirecionamentos





`    `</div>



</li>





<li id="djdt-ProfilingPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtProfilingPanel" title="Habilitar para próximas requisições">



`    `<div class="djdt-contentless djdt-disabled">



`  `Profiling





`    `</div>



</li>



`    `</ul>

`  `</div>

`  `<div class="" id="djDebugToolbarHandle" style="top: 265px;">

`    `<div title="Mostrar barra de ferramentas" id="djShowToolBarButton">

`      `<span id="djShowToolBarD">D</span><span id="djShowToolBarJ">J</span>DT

`    `</div>

`  `</div>






`  `<div id="HistoryPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Histórico</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="VersionsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Versões</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>













`  `<div id="SettingsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Settings from omaum.settings</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="HeadersPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Cabeçalhos</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="RequestPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Requisição</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="SQLPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>SQL queries from 1 connection</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="StaticFilesPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Arquivos estáticos (154 encontrados, 6 sendo utilizados)</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="TemplatesPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Templates (11 renderizados)</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="AlertsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Alerts</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="CachePanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Chamadas ao cache de 1 backend</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="SignalsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Sinais</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>
















`  `<div id="djDebugWindow" class="djdt-panelContent djdt-hidden"></div>

</div>


</body>

<body>

`    `<!-- Cabeçalho/Barra de Navegação -->

`    `<header>

`        `<nav class="navbar navbar-expand-lg navbar-dark bg-primary">

`            `<div class="container">

`                `<a class="navbar-brand" href="/">

`                    `<img src="/static/img/logo.png" alt="OMAUM Logo" height="40">

`                `</a>

`                `<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">

`                    `<span class="navbar-toggler-icon"></span>

`                `</button>



`                `<div class="collapse navbar-collapse" id="navbarNav">

`                    `<ul class="navbar-nav me-auto">

`                        `<li class="nav-item">

`                            `<a class="nav-link " href="/">

`                                `<i class="fas fa-home"></i> Início

`                            `</a>

`                        `</li>





`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/alunos/">

`                                    `<i class="fas fa-user-graduate"></i> Alunos

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/cursos/">

`                                    `<i class="fas fa-book"></i> Cursos

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/turmas/">

`                                    `<i class="fas fa-users"></i> Turmas

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/matriculas/">

`                                    `<i class="fas fa-clipboard-list"></i> Matrículas

`                                `</a>

`                            `</li>

`                            `<li class="nav-item dropdown">

`                                `<a class="nav-link dropdown-toggle" href="#" id="navbarDropdownAtividades" role="button" data-bs-toggle="dropdown" aria-expanded="false">

`                                   `<i class="fas fa-calendar-alt"></i> Atividades

`                                `</a>

`                                `<ul class="dropdown-menu" aria-labelledby="navbarDropdownAtividades">

`                                    `<li>

`                                        `<a class="dropdown-item" href="/atividades/academicas/">

`                                            `<i class="fas fa-school"></i> Acadêmicas

`                                        `</a>

`                                    `</li>

`                                    `<li>

`                                        `<a class="dropdown-item" href="/atividades/ritualisticas/">

`                                            `<i class="fas fa-pray"></i> Ritualísticas

`                                        `</a>

`                                    `</li>

`                                `</ul>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/frequencias/">

`                                    `<i class="fas fa-check-square"></i> Frequências

`                                `</a>

`                            `</li>



`                    `</ul>



`                    `<ul class="navbar-nav">





`                                `<li class="nav-item">

`                                    `<a class="nav-link" href="/painel-controle/">

`                                        `<i class="fas fa-cog"></i> Painel de Controle

`                                    `</a>

`                                `</li>



`                            `<li class="nav-item dropdown">

`                                `<a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">

`                                   `<i class="fas fa-user-circle"></i> lcsilv3

`                                `</a>

`                                `<ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">

`                                    `<li><a class="dropdown-item" href="#">Meu Perfil</a></li>

`                                    `<li><hr class="dropdown-divider"></li>

`                                    `<li>

`                                        `<form method="post" action="/sair/" class="d-inline">

`                                            `<input type="hidden" name="csrfmiddlewaretoken" value="3gbVR2nAJvzFzVfKxce9ZGO5Xz2XmfU5sgYItAnX3TyAWztkyKJOyE0b3KryBmlM">

`                                            `<button type="submit" class="dropdown-item">

`                                                `<i class="fas fa-sign-out-alt"></i> Sair

`                                            `</button>

`                                        `</form>

`                                    `</li>

`                                `</ul>

`                            `</li>



`                    `</ul>

`                `</div>

`            `</div>

`        `</nav>

`    `</header>



`    `<!-- Mensagens do sistema (flash messages) -->

`    `<div class="message-container">



`    `</div>



`    `<!-- Conteúdo principal -->

`    `<main id="main-content" class="py-4">



<div class="container-fluid mt-4">

`    `<div class="d-flex justify-content-between align-items-center mb-4">

`        `<h1>Dashboard de Atividades</h1>

`        `<div>

`            `<a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>

`            `<a href="/atividades/calendario/" class="btn btn-primary me-2">Calendário</a>

`            `<a href="/atividades/relatorio/" class="btn btn-success">Relatório</a>

`        `</div>

`    `</div>



`    `<!-- Cards de estatísticas -->

`    `<div class="row mb-4">

`        `<div class="col-md-3">

`            `<div class="card stat-card bg-primary text-white">

`                `<div class="card-body text-center">

`                    `<h5 class="card-title">Total de Atividades</h5>

`                    `<p class="display-4">2</p>

`                `</div>

`            `</div>

`        `</div>

`        `<div class="col-md-3">

`            `<div class="card stat-card bg-success text-white">

`                `<div class="card-body text-center">

`                    `<h5 class="card-title">Atividades Acadêmicas</h5>

`                    `<p class="display-4">2</p>

`                `</div>

`            `</div>

`        `</div>

`        `<div class="col-md-3">

`            `<div class="card stat-card bg-info text-white">

`                `<div class="card-body text-center">

`                    `<h5 class="card-title">Atividades Ritualísticas</h5>

`                    `<p class="display-4">0</p>

`                `</div>

`            `</div>

`        `</div>

`        `<div class="col-md-3">

`            `<div class="card stat-card bg-warning text-dark">

`                `<div class="card-body text-center">

`                    `<h5 class="card-title">Atividades Agendadas</h5>

`                    `<p class="display-4">2</p>

`                `</div>

`            `</div>

`        `</div>

`    `</div>



`    `<!-- Gráficos -->

`    `<div class="row mb-4">

`        `<div class="col-md-6">

`            `<div class="card">

`                `<div class="card-header">

`                    `<h5>Atividades por Tipo</h5>

`                `</div>

`                `<div class="card-body">

`                    `<div class="chart-container">

`                        `<canvas id="tipoAtividadesChart"></canvas>

`                    `</div>

`                `</div>

`            `</div>

`        `</div>

`        `<div class="col-md-6">

`            `<div class="card">

`                `<div class="card-header">

`                    `<h5>Atividades por Status</h5>

`                `</div>

`                `<div class="card-body">

`                    `<div class="chart-container">

`                        `<canvas id="statusAtividadesChart"></canvas>

`                    `</div>

`                `</div>

`            `</div>

`        `</div>

`    `</div>



`    `<div class="row mb-4">

`        `<div class="col-md-12">

`            `<div class="card">

`                `<div class="card-header">

`                    `<h5>Atividades por Mês</h5>

`                `</div>

`                `<div class="card-body">

`                    `<div class="chart-container">

`                        `<canvas id="atividadesPorMesChart"></canvas>

`                    `</div>

`                `</div>

`            `</div>

`        `</div>

`    `</div>



`    `<!-- Próximas atividades e atividades recentes -->

`    `<div class="row">

`        `<div class="col-md-6">

`            `<div class="card">

`                `<div class="card-header">

`                    `<h5>Próximas Atividades</h5>

`                `</div>

`                `<div class="card-body">





`                            `<div class="activity-item academica">

`                                `<div class="date">



`                                        `26/10/2026



`                                `</div>

`                                `<div class="title">Plenilúnio</div>

`                                `<div class="details">



`                                        `<span class="badge bg-primary">Acadêmica</span>

`                                        `<span class="badge bg-warning">

`                                            `Agendada

`                                        `</span>



`                                `</div>

`                                `<div class="mt-2">



`                                        `<a href="/atividades/academicas/detalhar/2/" class="btn btn-sm btn-outline-primary">Ver Detalhes</a>



`                                `</div>

`                            `</div>





`                `</div>

`            `</div>

`        `</div>

`        `<div class="col-md-6">

`            `<div class="card">

`                `<div class="card-header">

`                    `<h5>Atividades Recentes</h5>

`                `</div>

`                `<div class="card-body">





`                            `<div class="activity-item academica">

`                                `<div class="date">



`                                        `26/10/2024



`                                `</div>

`                                `<div class="title">Aula</div>

`                                `<div class="details">



`                                        `<span class="badge bg-primary">Acadêmica</span>

`                                        `<span class="badge bg-warning">

`                                            `Agendada

`                                        `</span>



`                                `</div>

`                                `<div class="mt-2">



`                                        `<a href="/atividades/academicas/detalhar/1/" class="btn btn-sm btn-outline-primary">Ver Detalhes</a>



`                                `</div>

`                            `</div>





`                `</div>

`            `</div>

`        `</div>

`    `</div>

</div>

`    `</main>



`    `<!-- Rodapé -->

`    `<footer class="footer mt-auto py-3 bg-light">

`        `<div class="container text-center">

`            `<span class="text-muted">© 2025 OMAUM - Sistema de Gestão de Iniciados</span>

`        `</div>

`    `</footer>



`    `<!-- Scripts de componentes globais -->

`    `<script src="/static/js/modules/dias-semana.js"></script>



`    `<!-- Scripts específicos da página -->



<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<script>

`    `document.addEventListener('DOMContentLoaded', function() {

`        `// Gráfico de atividades por tipo

`        `var tipoCtx = document.getElementById('tipoAtividadesChart').getContext('2d');

`        `var tipoChart = new Chart(tipoCtx, {

`            `type: 'pie',

`            `data: {

`                `labels: ['Acadêmicas', 'Ritualísticas'],

`                `datasets: [{

`                    `data: [2, 0],

`                    `backgroundColor: [

`                        `'rgba(13, 110, 253, 0.8)',

`                        `'rgba(23, 162, 184, 0.8)'

`                    `],

`                    `borderColor: [

`                        `'rgba(13, 110, 253, 1)',

`                        `'rgba(23, 162, 184, 1)'

`                    `],

`                    `borderWidth: 1

`                `}]

`            `},

`            `options: {

`                `responsive: true,

`                `maintainAspectRatio: false,

`                `plugins: {

`                    `legend: {

`                        `position: 'top',

`                    `},

`                    `title: {

`                        `display: true,

`                        `text: 'Distribuição por Tipo de Atividade'

`                    `}

`                `}

`            `}

`        `});



`        `// Gráfico de atividades por status

`        `var statusCtx = document.getElementById('statusAtividadesChart').getContext('2d');

`        `var statusChart = new Chart(statusCtx, {

`            `type: 'doughnut',

`            `data: {

`                `labels: ['Agendadas', 'Em Andamento', 'Concluídas', 'Canceladas'],

`                `datasets: [{

`                    `data: [

`                        `0, 

`                        `0, 

`                        `0, 

`                        `0

`                    `],

`                    `backgroundColor: [

`                        `'rgba(255, 193, 7, 0.8)',

`                        `'rgba(13, 202, 240, 0.8)',

`                        `'rgba(25, 135, 84, 0.8)',

`                        `'rgba(220, 53, 69, 0.8)'

`                    `],

`                    `borderColor: [

`                        `'rgba(255, 193, 7, 1)',

`                        `'rgba(13, 202, 240, 1)',

`                        `'rgba(25, 135, 84, 1)',

`                        `'rgba(220, 53, 69, 1)'

`                    `],

`                    `borderWidth: 1

`                `}]

`            `},

`            `options: {

`                `responsive: true,

`                `maintainAspectRatio: false,

`                `plugins: {

`                    `legend: {

`                        `position: 'top',

`                    `},

`                    `title: {

`                        `display: true,

`                        `text: 'Distribuição por Status'

`                    `}

`                `}

`            `}

`        `});



`        `// Gráfico de atividades por mês

`        `var mesCtx = document.getElementById('atividadesPorMesChart').getContext('2d');

`        `var mesChart = new Chart(mesCtx, {

`            `type: 'bar',

`            `data: {

`                `labels: ["Dec/2024", "Jan/2025", "Jan/2025", "Mar/2025", "Apr/2025", "May/2025"],

`                `datasets: [

`                    `{

`                        `label: 'Atividades Acadêmicas',

`                        `data: ,

`                        `backgroundColor: 'rgba(13, 110, 253, 0.5)',

`                        `borderColor: 'rgba(13, 110, 253, 1)',

`                        `borderWidth: 1

`                    `},

`                    `{

`                        `label: 'Atividades Ritualísticas',

`                        `data: ,

`                        `backgroundColor: 'rgba(23, 162, 184, 0.5)',

`                        `borderColor: 'rgba(23, 162, 184, 1)',

`                        `borderWidth: 1

`                    `}

`                `]

`            `},

`            `options: {

`                `responsive: true,

`                `maintainAspectRatio: false,

`                `scales: {

`                    `y: {

`                        `beginAtZero: true,

`                        `ticks: {

`                            `precision: 0

`                        `}

`                    `}

`                `},

`                `plugins: {

`                    `legend: {

`                        `position: 'top',

`                    `},

`                    `title: {

`                        `display: true,

`                        `text: 'Atividades por Mês'

`                    `}

`                `}

`            `}

`        `});

`    `});

</script>



`    `<!-- Script global do sistema -->

`    `<script>

`        `// Inicialização global do site

`        `document.addEventListener('DOMContentLoaded', function() {

`            `// Inicializar tooltips do Bootstrap

`            `var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));

`            `var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {

`                `return new bootstrap.Tooltip(tooltipTriggerEl);

`            `});



`            `// Inicializar popovers do Bootstrap

`            `var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));

`            `var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {

`                `return new bootstrap.Popover(popoverTriggerEl);

`            `});



`            `// Verificação CSRF para AJAX

`            `function getCookie(name) {

`                `let cookieValue = null;

`                `if (document.cookie && document.cookie !== '') {

`                    `const cookies = document.cookie.split(';');

`                    `for (let i = 0; i < cookies.length; i++) {

`                        `const cookie = cookies[i].trim();

`                        `if (cookie.substring(0, name.length + 1) === (name + '=')) {

`                            `cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

`                            `break;

`                        `}

`                    `}

`                `}

`                `return cookieValue;

`            `}



`            `// Configuração global do AJAX para incluir o token CSRF

`            `$.ajaxSetup({

`                `beforeSend: function(xhr, settings) {

`                    `if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {

`                        `xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));

`                    `}

`                `}

`            `});



`            `// Verificação periódica do token CSRF para sessões longas

`            `setInterval(function() {

`                `$.get("/csrf\_check/");

`            `}, 3600000); // A cada hora



`            `// Aplicar máscaras globais

`            `if (typeof $.fn.mask === 'function') {

`                `$('.cpf-mask').mask('000.000.000-00');

`                `$('.cep-mask').mask('00000-000');

`                `$('.phone-mask').mask('(00) 0000-00009');

`                `$('.phone-mask').blur(function(event) {

`                    `if($(this).val().length == 15){

`                        `$('.phone-mask').mask('(00) 00000-0009');

`                    `} else {

`                        `$('.phone-mask').mask('(00) 0000-00009');

`                    `}

`                `});

`                `$('.date-mask').mask('00/00/0000');

`                `$('.time-mask').mask('00:00 às 00:00');

`            `}



`            `// Inicialização global do Select2

`            `if (typeof $.fn.select2 === 'function') {

`                `$('.select2').select2({

`                    `theme: 'bootstrap4',

`                    `width: '100%'

`                `});

`            `}

`        `});

`    `</script>

`    `<script src="/static/js/inicializar\_select2.js"></script>


<link rel="stylesheet" href="/static/debug\_toolbar/css/print.css" media="print">

<link rel="stylesheet" href="/static/debug\_toolbar/css/toolbar.css">


<script type="module" src="/static/debug\_toolbar/js/toolbar.js" async=""></script>

<div id="djDebug" class="" dir="ltr" data-store-id="07f6aaec3c6c400f978eb46db6466549" data-render-panel-url="/\_\_debug\_\_/render\_panel/" data-sidebar-url="/\_\_debug\_\_/history\_sidebar/" data-default-show="true" data-update-on-fetch="False" data-theme="auto">

`  `<div class="djdt-hidden" id="djDebugToolbar">

`    `<ul id="djDebugPanelList">

`      `<li><a id="djHideToolBarButton" href="#" title="Ocultar barra de ferramentas">Esconder »</a></li>

`      `<li>

`        `<a id="djToggleThemeButton" href="#" title="Toggle Theme">

`          `Toggle Theme <svg aria-hidden="true" class="djdt-hidden theme-auto" fill="currentColor" viewBox="0 0 32 32" version="1.1" xmlns="http://www.w3.org/2000/svg">

`  `<path d="M0 16q0 3.264 1.28 6.24t3.392 5.088 5.12 3.424 6.208 1.248q3.264 0 6.24-1.248t5.088-3.424 3.392-5.088 1.28-6.24-1.28-6.208-3.392-5.12-5.088-3.392-6.24-1.28q-3.264 0-6.208 1.28t-5.12 3.392-3.392 5.12-1.28 6.208zM4 16q0-3.264 1.6-6.016t4.384-4.352 6.016-1.632 6.016 1.632 4.384 4.352 1.6 6.016-1.6 6.048-4.384 4.352-6.016 1.6-6.016-1.6-4.384-4.352-1.6-6.048zM16 26.016q2.72 0 5.024-1.344t3.648-3.648 1.344-5.024-1.344-4.992-3.648-3.648-5.024-1.344v20z"></path>

</svg>

<svg aria-hidden="true" class="djdt-hidden theme-light" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">

`  `<path fill-rule="evenodd" clip-rule="evenodd" d="M12 1.25C12.4142 1.25 12.75 1.58579 12.75 2V4C12.75 4.41421 12.4142 4.75 12 4.75C11.5858 4.75 11.25 4.41421 11.25 4V2C11.25 1.58579 11.5858 1.25 12 1.25ZM3.66865 3.71609C3.94815 3.41039 4.42255 3.38915 4.72825 3.66865L6.95026 5.70024C7.25596 5.97974 7.2772 6.45413 6.9977 6.75983C6.7182 7.06553 6.2438 7.08677 5.9381 6.80727L3.71609 4.77569C3.41039 4.49619 3.38915 4.02179 3.66865 3.71609ZM20.3314 3.71609C20.6109 4.02179 20.5896 4.49619 20.2839 4.77569L18.0619 6.80727C17.7562 7.08677 17.2818 7.06553 17.0023 6.75983C16.7228 6.45413 16.744 5.97974 17.0497 5.70024L19.2718 3.66865C19.5775 3.38915 20.0518 3.41039 20.3314 3.71609ZM12 7.75C9.65279 7.75 7.75 9.65279 7.75 12C7.75 14.3472 9.65279 16.25 12 16.25C14.3472 16.25 16.25 14.3472 16.25 12C16.25 9.65279 14.3472 7.75 12 7.75ZM6.25 12C6.25 8.82436 8.82436 6.25 12 6.25C15.1756 6.25 17.75 8.82436 17.75 12C17.75 15.1756 15.1756 17.75 12 17.75C8.82436 17.75 6.25 15.1756 6.25 12ZM1.25 12C1.25 11.5858 1.58579 11.25 2 11.25H4C4.41421 11.25 4.75 11.5858 4.75 12C4.75 12.4142 4.41421 12.75 4 12.75H2C1.58579 12.75 1.25 12.4142 1.25 12ZM19.25 12C19.25 11.5858 19.5858 11.25 20 11.25H22C22.4142 11.25 22.75 11.5858 22.75 12C22.75 12.4142 22.4142 12.75 22 12.75H20C19.5858 12.75 19.25 12.4142 19.25 12ZM17.0255 17.0252C17.3184 16.7323 17.7933 16.7323 18.0862 17.0252L20.3082 19.2475C20.6011 19.5404 20.601 20.0153 20.3081 20.3082C20.0152 20.6011 19.5403 20.601 19.2475 20.3081L17.0255 18.0858C16.7326 17.7929 16.7326 17.3181 17.0255 17.0252ZM6.97467 17.0253C7.26756 17.3182 7.26756 17.7931 6.97467 18.086L4.75244 20.3082C4.45955 20.6011 3.98468 20.6011 3.69178 20.3082C3.39889 20.0153 3.39889 19.5404 3.69178 19.2476L5.91401 17.0253C6.2069 16.7324 6.68177 16.7324 6.97467 17.0253ZM12 19.25C12.4142 19.25 12.75 19.5858 12.75 20V22C12.75 22.4142 12.4142 22.75 12 22.75C11.5858 22.75 11.25 22.4142 11.25 22V20C11.25 19.5858 11.5858 19.25 12 19.25Z" fill="currentColor"></path>

</svg>

<svg aria-hidden="true" class="djdt-hidden theme-dark" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">

`  `<path d="M3.32031 11.6835C3.32031 16.6541 7.34975 20.6835 12.3203 20.6835C16.1075 20.6835 19.3483 18.3443 20.6768 15.032C19.6402 15.4486 18.5059 15.6834 17.3203 15.6834C12.3497 15.6834 8.32031 11.654 8.32031 6.68342C8.32031 5.50338 8.55165 4.36259 8.96453 3.32996C5.65605 4.66028 3.32031 7.89912 3.32031 11.6835Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>

</svg>

`        `</a>

`      `</li>





<li id="djdt-HistoryPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtHistoryPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Histórico" class="HistoryPanel">



`  `Histórico





`      `<br><small>/atividades/dashboard/</small>







`    `</a>



</li>





<li id="djdt-VersionsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtVersionsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Versões" class="VersionsPanel">



`  `Versões





`      `<br><small>Django 5.1.7</small>







`    `</a>



</li>





<li id="djdt-TimerPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtTimerPanel" checked="" title="Desativar para próximas requisições">



`    `<div class="djdt-contentless">



`  `Tempo





`      `<br><small>Total: 172.67ms</small>







`    `</div>



</li>





<li id="djdt-SettingsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSettingsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Settings from omaum.settings" class="SettingsPanel">



`  `Configurações













`    `</a>



</li>





<li id="djdt-HeadersPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtHeadersPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Cabeçalhos" class="HeadersPanel">



`  `Cabeçalhos













`    `</a>



</li>





<li id="djdt-RequestPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtRequestPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Requisição" class="RequestPanel">



`  `Requisição





`      `<br><small>dashboard\_atividades</small>







`    `</a>



</li>





<li id="djdt-SQLPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSQLPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="SQL queries from 1 connection" class="SQLPanel">



`  `SQL





`      `<br><small>11 queries in 11.41ms</small>







`    `</a>



</li>





<li id="djdt-StaticFilesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtStaticFilesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Arquivos estáticos (154 encontrados, 6 sendo utilizados)" class="StaticFilesPanel">



`  `Arquivos estáticos





`      `<br><small>6 arquivos utilizados</small>







`    `</a>



</li>





<li id="djdt-TemplatesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtTemplatesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Templates (2 renderizados)" class="TemplatesPanel">



`  `Templates





`      `<br><small>atividades/dashboard\_atividades.html</small>







`    `</a>



</li>





<li id="djdt-AlertsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtAlertsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Alerts" class="AlertsPanel">



`  `Alerts













`    `</a>



</li>





<li id="djdt-CachePanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtCachePanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Chamadas ao cache de 1 backend" class="CachePanel">



`  `Cache





`      `<br><small>0 chamada em 0.00ms</small>







`    `</a>



</li>





<li id="djdt-SignalsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSignalsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Sinais" class="SignalsPanel">



`  `Sinais





`      `<br><small>35 receptores de 15 sinais</small>







`    `</a>



</li>





<li id="djdt-RedirectsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtRedirectsPanel" title="Habilitar para próximas requisições">



`    `<div class="djdt-contentless djdt-disabled">



`  `Interceptar redirecionamentos





`    `</div>



</li>





<li id="djdt-ProfilingPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtProfilingPanel" title="Habilitar para próximas requisições">



`    `<div class="djdt-contentless djdt-disabled">



`  `Profiling





`    `</div>



</li>



`    `</ul>

`  `</div>

`  `<div class="" id="djDebugToolbarHandle" style="top: 265px;">

`    `<div title="Mostrar barra de ferramentas" id="djShowToolBarButton">

`      `<span id="djShowToolBarD">D</span><span id="djShowToolBarJ">J</span>DT

`    `</div>

`  `</div>






`  `<div id="HistoryPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Histórico</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="VersionsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Versões</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>













`  `<div id="SettingsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Settings from omaum.settings</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="HeadersPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Cabeçalhos</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="RequestPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Requisição</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="SQLPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>SQL queries from 1 connection</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="StaticFilesPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Arquivos estáticos (154 encontrados, 6 sendo utilizados)</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="TemplatesPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Templates (2 renderizados)</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="AlertsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Alerts</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="CachePanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Chamadas ao cache de 1 backend</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="SignalsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Sinais</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>
















`  `<div id="djDebugWindow" class="djdt-panelContent djdt-hidden"></div>

</div>


</body>

<body>

`    `<!-- Cabeçalho/Barra de Navegação -->

`    `<header>

`        `<nav class="navbar navbar-expand-lg navbar-dark bg-primary">

`            `<div class="container">

`                `<a class="navbar-brand" href="/">

`                    `<img src="/static/img/logo.png" alt="OMAUM Logo" height="40">

`                `</a>

`                `<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">

`                    `<span class="navbar-toggler-icon"></span>

`                `</button>



`                `<div class="collapse navbar-collapse" id="navbarNav">

`                    `<ul class="navbar-nav me-auto">

`                        `<li class="nav-item">

`                            `<a class="nav-link " href="/">

`                                `<i class="fas fa-home"></i> Início

`                            `</a>

`                        `</li>





`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/alunos/">

`                                    `<i class="fas fa-user-graduate"></i> Alunos

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/cursos/">

`                                    `<i class="fas fa-book"></i> Cursos

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/turmas/">

`                                    `<i class="fas fa-users"></i> Turmas

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/matriculas/">

`                                    `<i class="fas fa-clipboard-list"></i> Matrículas

`                                `</a>

`                            `</li>

`                            `<li class="nav-item dropdown">

`                                `<a class="nav-link dropdown-toggle" href="#" id="navbarDropdownAtividades" role="button" data-bs-toggle="dropdown" aria-expanded="false">

`                                   `<i class="fas fa-calendar-alt"></i> Atividades

`                                `</a>

`                                `<ul class="dropdown-menu" aria-labelledby="navbarDropdownAtividades">

`                                    `<li>

`                                        `<a class="dropdown-item" href="/atividades/academicas/">

`                                            `<i class="fas fa-school"></i> Acadêmicas

`                                        `</a>

`                                    `</li>

`                                    `<li>

`                                        `<a class="dropdown-item" href="/atividades/ritualisticas/">

`                                            `<i class="fas fa-pray"></i> Ritualísticas

`                                        `</a>

`                                    `</li>

`                                `</ul>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/frequencias/">

`                                    `<i class="fas fa-check-square"></i> Frequências

`                                `</a>

`                            `</li>



`                    `</ul>



`                    `<ul class="navbar-nav">





`                                `<li class="nav-item">

`                                    `<a class="nav-link" href="/painel-controle/">

`                                        `<i class="fas fa-cog"></i> Painel de Controle

`                                    `</a>

`                                `</li>



`                            `<li class="nav-item dropdown">

`                                `<a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">

`                                   `<i class="fas fa-user-circle"></i> lcsilv3

`                                `</a>

`                                `<ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">

`                                    `<li><a class="dropdown-item" href="#">Meu Perfil</a></li>

`                                    `<li><hr class="dropdown-divider"></li>

`                                    `<li>

`                                        `<form method="post" action="/sair/" class="d-inline">

`                                            `<input type="hidden" name="csrfmiddlewaretoken" value="WxFAOCDJ3IF7PmXlr4rBubM8HTQHyGx0lxsnqaD6n6E2c0bVsCWg39YeN4fiNNYH">

`                                            `<button type="submit" class="dropdown-item">

`                                                `<i class="fas fa-sign-out-alt"></i> Sair

`                                            `</button>

`                                        `</form>

`                                    `</li>

`                                `</ul>

`                            `</li>



`                    `</ul>

`                `</div>

`            `</div>

`        `</nav>

`    `</header>



`    `<!-- Mensagens do sistema (flash messages) -->

`    `<div class="message-container">



`    `</div>



`    `<!-- Conteúdo principal -->

`    `<main id="main-content" class="py-4">



<div class="container-fluid mt-4">

`    `<div class="d-flex justify-content-between align-items-center mb-4">

`        `<h1>Calendário de Atividades</h1>

`        `<div>

`            `<a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>

`            `<a href="/atividades/dashboard/" class="btn btn-success me-2">

`                `<i class="fas fa-chart-bar"></i> Dashboard

`            `</a>

`            `<a href="/atividades/relatorio/" class="btn btn-warning me-2">

`                `<i class="fas fa-file-alt"></i> Relatórios

`            `</a>

`            `<div class="btn-group">

`                `<a href="/atividades/academicas/" class="btn btn-outline-primary">Atividades Acadêmicas</a>

`                `<a href="/atividades/ritualisticas/" class="btn btn-outline-info">Atividades Ritualísticas</a>

`            `</div>

`        `</div>

`    `</div>



`    `<div class="card mb-4">

`        `<div class="card-header">

`            `<div class="d-flex justify-content-between align-items-center">

`                `<h5 class="mb-0">Filtros</h5>

`                `<div class="form-check form-switch">

`                    `<input class="form-check-input" type="checkbox" id="mostrar-concluidas" checked="">

`                    `<label class="form-check-label" for="mostrar-concluidas">Mostrar atividades concluídas</label>

`                `</div>

`            `</div>

`        `</div>

`        `<div class="card-body">

`            `<div class="row">

`                `<div class="col-md-6">

`                    `<div class="mb-3">

`                        `<label for="filtro-tipo" class="form-label">Tipo de Atividade</label>

`                        `<select id="filtro-tipo" class="form-select">

`                            `<option value="todas" selected="">Todas</option>

`                            `<option value="academicas">Acadêmicas</option>

`                            `<option value="ritualisticas">Ritualísticas</option>

`                        `</select>

`                    `</div>

`                `</div>

`                `<div class="col-md-6">

`                    `<div class="mb-3">

`                        `<label for="filtro-turma" class="form-label">Turma</label>

`                        `<select id="filtro-turma" class="form-select">

`                            `<option value="todas" selected="">Todas</option>



`                                `<option value="6">D</option>



`                                `<option value="2">A</option>



`                                `<option value="4">B</option>



`                                `<option value="5">C</option>



`                        `</select>

`                    `</div>

`                `</div>

`            `</div>

`        `</div>

`    `</div>



`    `<div class="card">

`        `<div class="card-body">

`            `<div id="calendar" class="fc fc-media-screen fc-direction-ltr fc-theme-standard fc-liquid-hack"><div class="fc-header-toolbar fc-toolbar fc-toolbar-ltr"><div class="fc-toolbar-chunk"><div class="fc-button-group"><button type="button" title="Anterior" aria-pressed="false" class="fc-prev-button fc-button fc-button-primary"><span class="fc-icon fc-icon-chevron-left"></span></button><button type="button" title="Próximo" aria-pressed="false" class="fc-next-button fc-button fc-button-primary"><span class="fc-icon fc-icon-chevron-right"></span></button></div><button type="button" title="Hoje" disabled="" aria-pressed="false" class="fc-today-button fc-button fc-button-primary">Hoje</button></div><div class="fc-toolbar-chunk"><h2 class="fc-toolbar-title" id="fc-dom-1">maio de 2025</h2></div><div class="fc-toolbar-chunk"><div class="fc-button-group"><button type="button" title="Mês" aria-pressed="true" class="fc-dayGridMonth-button fc-button fc-button-primary fc-button-active">Mês</button><button type="button" title="Semana" aria-pressed="false" class="fc-timeGridWeek-button fc-button fc-button-primary">Semana</button><button type="button" title="Dia" aria-pressed="false" class="fc-timeGridDay-button fc-button fc-button-primary">Dia</button><button type="button" title="Lista" aria-pressed="false" class="fc-listMonth-button fc-button fc-button-primary">Lista</button></div></div></div><div aria-labelledby="fc-dom-1" class="fc-view-harness fc-view-harness-active" style="height: 814.815px;"><div class="fc-daygrid fc-dayGridMonth-view fc-view"><table role="grid" class="fc-scrollgrid  fc-scrollgrid-liquid"><tbody role="rowgroup"><tr role="presentation" class="fc-scrollgrid-section fc-scrollgrid-section-header "><th role="presentation"><div class="fc-scroller-harness"><div class="fc-scroller" style="overflow: hidden;"><table role="presentation" class="fc-col-header " style="width: 1097px;"><colgroup></colgroup><thead role="presentation"><tr role="row"><th role="columnheader" class="fc-col-header-cell fc-day fc-day-sun"><div class="fc-scrollgrid-sync-inner"><a aria-label="domingo" class="fc-col-header-cell-cushion ">dom.</a></div></th><th role="columnheader" class="fc-col-header-cell fc-day fc-day-mon"><div class="fc-scrollgrid-sync-inner"><a aria-label="segunda-feira" class="fc-col-header-cell-cushion ">seg.</a></div></th><th role="columnheader" class="fc-col-header-cell fc-day fc-day-tue"><div class="fc-scrollgrid-sync-inner"><a aria-label="terça-feira" class="fc-col-header-cell-cushion ">ter.</a></div></th><th role="columnheader" class="fc-col-header-cell fc-day fc-day-wed"><div class="fc-scrollgrid-sync-inner"><a aria-label="quarta-feira" class="fc-col-header-cell-cushion ">qua.</a></div></th><th role="columnheader" class="fc-col-header-cell fc-day fc-day-thu"><div class="fc-scrollgrid-sync-inner"><a aria-label="quinta-feira" class="fc-col-header-cell-cushion ">qui.</a></div></th><th role="columnheader" class="fc-col-header-cell fc-day fc-day-fri"><div class="fc-scrollgrid-sync-inner"><a aria-label="sexta-feira" class="fc-col-header-cell-cushion ">sex.</a></div></th><th role="columnheader" class="fc-col-header-cell fc-day fc-day-sat"><div class="fc-scrollgrid-sync-inner"><a aria-label="sábado" class="fc-col-header-cell-cushion ">sáb.</a></div></th></tr></thead></table></div></div></th></tr><tr role="presentation" class="fc-scrollgrid-section fc-scrollgrid-section-body  fc-scrollgrid-section-liquid"><td role="presentation"><div class="fc-scroller-harness fc-scroller-harness-liquid"><div class="fc-scroller fc-scroller-liquid-absolute" style="overflow: hidden auto;"><div class="fc-daygrid-body fc-daygrid-body-unbalanced " style="width: 1097px;"><table role="presentation" class="fc-scrollgrid-sync-table" style="width: 1097px; height: 780px;"><colgroup></colgroup><tbody role="presentation"><tr role="row"><td role="gridcell" class="fc-daygrid-day fc-day fc-day-sun fc-day-past fc-day-other" data-date="2025-04-27" aria-labelledby="fc-dom-2"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-2" class="fc-daygrid-day-number" aria-label="27 de abril de 2025">27</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-mon fc-day-past fc-day-other" data-date="2025-04-28" aria-labelledby="fc-dom-4"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-4" class="fc-daygrid-day-number" aria-label="28 de abril de 2025">28</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-tue fc-day-past fc-day-other" data-date="2025-04-29" aria-labelledby="fc-dom-6"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-6" class="fc-daygrid-day-number" aria-label="29 de abril de 2025">29</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-wed fc-day-past fc-day-other" data-date="2025-04-30" aria-labelledby="fc-dom-8"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-8" class="fc-daygrid-day-number" aria-label="30 de abril de 2025">30</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-thu fc-day-past" data-date="2025-05-01" aria-labelledby="fc-dom-10"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-10" class="fc-daygrid-day-number" aria-label="1 de maio de 2025">1</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-fri fc-day-past" data-date="2025-05-02" aria-labelledby="fc-dom-12"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-12" class="fc-daygrid-day-number" aria-label="2 de maio de 2025">2</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-sat fc-day-past" data-date="2025-05-03" aria-labelledby="fc-dom-14"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-14" class="fc-daygrid-day-number" aria-label="3 de maio de 2025">3</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td></tr><tr role="row"><td role="gridcell" class="fc-daygrid-day fc-day fc-day-sun fc-day-past" data-date="2025-05-04" aria-labelledby="fc-dom-16"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-16" class="fc-daygrid-day-number" aria-label="4 de maio de 2025">4</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-mon fc-day-past" data-date="2025-05-05" aria-labelledby="fc-dom-18"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-18" class="fc-daygrid-day-number" aria-label="5 de maio de 2025">5</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-tue fc-day-today " data-date="2025-05-06" aria-labelledby="fc-dom-20"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-20" class="fc-daygrid-day-number" aria-label="6 de maio de 2025">6</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-wed fc-day-future" data-date="2025-05-07" aria-labelledby="fc-dom-22"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-22" class="fc-daygrid-day-number" aria-label="7 de maio de 2025">7</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-thu fc-day-future" data-date="2025-05-08" aria-labelledby="fc-dom-24"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-24" class="fc-daygrid-day-number" aria-label="8 de maio de 2025">8</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-fri fc-day-future" data-date="2025-05-09" aria-labelledby="fc-dom-26"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-26" class="fc-daygrid-day-number" aria-label="9 de maio de 2025">9</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-sat fc-day-future" data-date="2025-05-10" aria-labelledby="fc-dom-28"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-28" class="fc-daygrid-day-number" aria-label="10 de maio de 2025">10</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td></tr><tr role="row"><td role="gridcell" class="fc-daygrid-day fc-day fc-day-sun fc-day-future" data-date="2025-05-11" aria-labelledby="fc-dom-30"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-30" class="fc-daygrid-day-number" aria-label="11 de maio de 2025">11</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-mon fc-day-future" data-date="2025-05-12" aria-labelledby="fc-dom-32"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-32" class="fc-daygrid-day-number" aria-label="12 de maio de 2025">12</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-tue fc-day-future" data-date="2025-05-13" aria-labelledby="fc-dom-34"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-34" class="fc-daygrid-day-number" aria-label="13 de maio de 2025">13</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-wed fc-day-future" data-date="2025-05-14" aria-labelledby="fc-dom-36"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-36" class="fc-daygrid-day-number" aria-label="14 de maio de 2025">14</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-thu fc-day-future" data-date="2025-05-15" aria-labelledby="fc-dom-38"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-38" class="fc-daygrid-day-number" aria-label="15 de maio de 2025">15</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-fri fc-day-future" data-date="2025-05-16" aria-labelledby="fc-dom-40"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-40" class="fc-daygrid-day-number" aria-label="16 de maio de 2025">16</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-sat fc-day-future" data-date="2025-05-17" aria-labelledby="fc-dom-42"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-42" class="fc-daygrid-day-number" aria-label="17 de maio de 2025">17</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td></tr><tr role="row"><td role="gridcell" class="fc-daygrid-day fc-day fc-day-sun fc-day-future" data-date="2025-05-18" aria-labelledby="fc-dom-44"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-44" class="fc-daygrid-day-number" aria-label="18 de maio de 2025">18</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-mon fc-day-future" data-date="2025-05-19" aria-labelledby="fc-dom-46"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-46" class="fc-daygrid-day-number" aria-label="19 de maio de 2025">19</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-tue fc-day-future" data-date="2025-05-20" aria-labelledby="fc-dom-48"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-48" class="fc-daygrid-day-number" aria-label="20 de maio de 2025">20</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-wed fc-day-future" data-date="2025-05-21" aria-labelledby="fc-dom-50"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-50" class="fc-daygrid-day-number" aria-label="21 de maio de 2025">21</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-thu fc-day-future" data-date="2025-05-22" aria-labelledby="fc-dom-52"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-52" class="fc-daygrid-day-number" aria-label="22 de maio de 2025">22</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-fri fc-day-future" data-date="2025-05-23" aria-labelledby="fc-dom-54"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-54" class="fc-daygrid-day-number" aria-label="23 de maio de 2025">23</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-sat fc-day-future" data-date="2025-05-24" aria-labelledby="fc-dom-56"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-56" class="fc-daygrid-day-number" aria-label="24 de maio de 2025">24</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td></tr><tr role="row"><td role="gridcell" class="fc-daygrid-day fc-day fc-day-sun fc-day-future" data-date="2025-05-25" aria-labelledby="fc-dom-58"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-58" class="fc-daygrid-day-number" aria-label="25 de maio de 2025">25</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-mon fc-day-future" data-date="2025-05-26" aria-labelledby="fc-dom-60"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-60" class="fc-daygrid-day-number" aria-label="26 de maio de 2025">26</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-tue fc-day-future" data-date="2025-05-27" aria-labelledby="fc-dom-62"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-62" class="fc-daygrid-day-number" aria-label="27 de maio de 2025">27</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-wed fc-day-future" data-date="2025-05-28" aria-labelledby="fc-dom-64"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-64" class="fc-daygrid-day-number" aria-label="28 de maio de 2025">28</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-thu fc-day-future" data-date="2025-05-29" aria-labelledby="fc-dom-66"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-66" class="fc-daygrid-day-number" aria-label="29 de maio de 2025">29</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-fri fc-day-future" data-date="2025-05-30" aria-labelledby="fc-dom-68"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-68" class="fc-daygrid-day-number" aria-label="30 de maio de 2025">30</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-sat fc-day-future" data-date="2025-05-31" aria-labelledby="fc-dom-70"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-70" class="fc-daygrid-day-number" aria-label="31 de maio de 2025">31</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td></tr><tr role="row"><td role="gridcell" class="fc-daygrid-day fc-day fc-day-sun fc-day-future fc-day-other" data-date="2025-06-01" aria-labelledby="fc-dom-72"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-72" class="fc-daygrid-day-number" aria-label="1 de junho de 2025">1</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-mon fc-day-future fc-day-other" data-date="2025-06-02" aria-labelledby="fc-dom-74"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-74" class="fc-daygrid-day-number" aria-label="2 de junho de 2025">2</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-tue fc-day-future fc-day-other" data-date="2025-06-03" aria-labelledby="fc-dom-76"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-76" class="fc-daygrid-day-number" aria-label="3 de junho de 2025">3</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-wed fc-day-future fc-day-other" data-date="2025-06-04" aria-labelledby="fc-dom-78"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-78" class="fc-daygrid-day-number" aria-label="4 de junho de 2025">4</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-thu fc-day-future fc-day-other" data-date="2025-06-05" aria-labelledby="fc-dom-80"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-80" class="fc-daygrid-day-number" aria-label="5 de junho de 2025">5</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-fri fc-day-future fc-day-other" data-date="2025-06-06" aria-labelledby="fc-dom-82"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-82" class="fc-daygrid-day-number" aria-label="6 de junho de 2025">6</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td><td role="gridcell" class="fc-daygrid-day fc-day fc-day-sat fc-day-future fc-day-other" data-date="2025-06-07" aria-labelledby="fc-dom-84"><div class="fc-daygrid-day-frame fc-scrollgrid-sync-inner"><div class="fc-daygrid-day-top"><a id="fc-dom-84" class="fc-daygrid-day-number" aria-label="7 de junho de 2025">7</a></div><div class="fc-daygrid-day-events"><div class="fc-daygrid-day-bottom" style="margin-top: 0px;"></div></div><div class="fc-daygrid-day-bg"></div></div></td></tr></tbody></table></div></div></div></td></tr></tbody></table></div></div></div>

`        `</div>

`    `</div>



`    `<!-- Modal para detalhes da atividade -->

`    `<div class="modal fade" id="atividadeModal" tabindex="-1" aria-labelledby="atividadeModalLabel" aria-hidden="true">

`        `<div class="modal-dialog modal-lg">

`            `<div class="modal-content">

`                `<div class="modal-header">

`                    `<h5 class="modal-title" id="atividadeModalLabel">Detalhes da Atividade</h5>

`                    `<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fechar"></button>

`                `</div>

`                `<div class="modal-body" id="atividadeModalBody">

`                    `<div class="text-center">

`                        `<div class="spinner-border text-primary" role="status">

`                            `<span class="visually-hidden">Carregando...</span>

`                        `</div>

`                        `<p>Carregando detalhes da atividade...</p>

`                    `</div>

`                `</div>

`                `<div class="modal-footer">

`                    `<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>

`                    `<a href="#" class="btn btn-primary" id="verDetalhesBtn">Ver Detalhes Completos</a>

`                `</div>

`            `</div>

`        `</div>

`    `</div>

</div>

`    `</main>



`    `<!-- Rodapé -->

`    `<footer class="footer mt-auto py-3 bg-light">

`        `<div class="container text-center">

`            `<span class="text-muted">© 2025 OMAUM - Sistema de Gestão de Iniciados</span>

`        `</div>

`    `</footer>



`    `<!-- Scripts de componentes globais -->

`    `<script src="/static/js/modules/dias-semana.js"></script>



`    `<!-- Scripts específicos da página -->



<script src="https://cdn.jsdelivr.net/npm/fullcalendar@5.10.1/main.min.js"></script>

<script src="https://cdn.jsdelivr.net/npm/fullcalendar@5.10.1/locales-all.min.js"></script>

<script>

`    `document.addEventListener('DOMContentLoaded', function() {

`        `// Inicializar o calendário

`        `var calendarEl = document.getElementById('calendar');

`        `var calendar = new FullCalendar.Calendar(calendarEl, {

`            `initialView: 'dayGridMonth',

`            `headerToolbar: {

`                `left: 'prev,next today',

`                `center: 'title',

`                `right: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth'

`            `},

`            `locale: 'pt-br',

`            `buttonText: {

`                `today: 'Hoje',

`                `month: 'Mês',

`                `week: 'Semana',

`                `day: 'Dia',

`                `list: 'Lista'

`            `},

`            `events: function(info, successCallback, failureCallback) {

`                `// Obter filtros

`                `const tipoFiltro = document.getElementById('filtro-tipo').value;

`                `const turmaFiltro = document.getElementById('filtro-turma').value;

`                `const mostrarConcluidas = document.getElementById('mostrar-concluidas').checked;



`                `// Construir URL com parâmetros de filtro

`                `let url = '/atividades/api/eventos/';

`                `url += '?start=' + info.startStr + '&end=' + info.endStr;

`                `url += '&tipo=' + tipoFiltro;

`                `url += '&turma=' + turmaFiltro;

`                `url += '&concluidas=' + (mostrarConcluidas ? '1' : '0');



`                `// Fazer requisição AJAX

`                `fetch(url)

.then(response => response.json())

.then(data => {

`                        `successCallback(data);

`                    `})

.catch(error => {

`                        `console.error('Erro ao carregar eventos:', error);

`                        `failureCallback(error);

`                    `});

`            `},

`            `eventClick: function(info) {

`                `// Abrir modal com detalhes do evento

`                `const modal = new bootstrap.Modal(document.getElementById('atividadeModal'));

`                `const modalBody = document.getElementById('atividadeModalBody');

`                `const verDetalhesBtn = document.getElementById('verDetalhesBtn');



`                `// Limpar conteúdo anterior e mostrar loader

`                `modalBody.innerHTML = `

`                    `<div class="text-center">

`                        `<div class="spinner-border text-primary" role="status">

`                            `<span class="visually-hidden">Carregando...</span>

`                        `</div>

`                        `<p>Carregando detalhes da atividade...</p>

`                    `</div>

`                ``;



`                `// Configurar link para detalhes completos

`                `const eventoId = info.event.id;

`                `const tipoEvento = info.event.extendedProps.tipo;



`                `if (tipoEvento === 'academica') {

`                    `verDetalhesBtn.href = '/atividades/academicas/detalhar/0/'.replace('0', eventoId);

`                `} else {

`                    `verDetalhesBtn.href = '/atividades/ritualisticas/detalhar/0/'.replace('0', eventoId);

`                `}



`                `// Carregar detalhes do evento via AJAX

`                `fetch(`/atividades/api/evento/${eventoId}/?tipo=${tipoEvento}`)

.then(response => response.json())

.then(data => {

`                        `if (data.success) {

`                            `// Renderizar detalhes do evento

`                            `if (tipoEvento === 'academica') {

`                                `modalBody.innerHTML = `

`                                    `<div class="row">

`                                        `<div class="col-md-6">

`                                            `<p><strong>Nome:</strong> ${data.evento.nome}</p>

`                                            `<p><strong>Tipo:</strong> ${data.evento.tipo\_display}</p>

`                                            `<p><strong>Status:</strong> <span class="badge ${getStatusBadgeClass(data.evento.status)}">${data.evento.status\_display}</span></p>

`                                            `<p><strong>Responsável:</strong> ${data.evento.responsavel || 'Não informado'}</p>

`                                        `</div>

`                                        `<div class="col-md-6">

`                                            `<p><strong>Data de Início:</strong> ${data.evento.data\_inicio}</p>

`                                            `<p><strong>Data de Término:</strong> ${data.evento.data\_fim || 'Não definida'}</p>

`                                            `<p><strong>Local:</strong> ${data.evento.local || 'Não informado'}</p>

`                                            `<p><strong>Turma:</strong> ${data.evento.turma}</p>

`                                        `</div>

`                                    `</div>

`                                    `<hr>

`                                    `<div>

`                                        `<h6>Descrição:</h6>

`                                        `<p>${data.evento.descricao || 'Sem descrição'}</p>

`                                    `</div>

`                                ``;

`                            `} else {

`                                `modalBody.innerHTML = `

`                                    `<div class="row">

`                                        `<div class="col-md-6">

`                                            `<p><strong>Nome:</strong> ${data.evento.nome}</p>

`                                            `<p><strong>Data:</strong> ${data.evento.data}</p>

`                                            `<p><strong>Horário:</strong> ${data.evento.hora\_inicio} - ${data.evento.hora\_fim}</p>

`                                            `<p><strong>Local:</strong> ${data.evento.local}</p>

`                                        `</div>

`                                        `<div class="col-md-6">

`                                            `<p><strong>Turma:</strong> ${data.evento.turma}</p>

`                                            `<p><strong>Total de Participantes:</strong> ${data.evento.total\_participantes}</p>

`                                        `</div>

`                                    `</div>

`                                    `<hr>

`                                    `<div>

`                                        `<h6>Descrição:</h6>

`                                        `<p>${data.evento.descricao || 'Sem descrição'}</p>

`                                    `</div>

`                                ``;

`                            `}

`                        `} else {

`                            `modalBody.innerHTML = `<div class="alert alert-danger">Erro ao carregar detalhes: ${data.error}</div>`;

`                        `}

`                    `})

.catch(error => {

`                        `console.error('Erro ao carregar detalhes do evento:', error);

`                        `modalBody.innerHTML = `<div class="alert alert-danger">Erro ao carregar detalhes do evento.</div>`;

`                    `});



`                `modal.show();

`            `},

`            `eventClassNames: function(arg) {

`                `const classes = [];



`                `// Adicionar classe baseada no tipo de atividade

`                `if (arg.event.extendedProps.tipo === 'academica') {

`                    `classes.push('academica-event');

`                `} else {

`                    `classes.push('ritualistica-event');

`                `}



`                `// Adicionar classe baseada no status (apenas para atividades acadêmicas)

`                `if (arg.event.extendedProps.status) {

`                    `classes.push(arg.event.extendedProps.status + '-event');

`                `}



`                `return classes;

`            `}

`        `});



`        `calendar.render();



`        `// Função auxiliar para obter classe CSS do badge de status

`        `function getStatusBadgeClass(status) {

`            `switch (status) {

`                `case 'agendada': return 'bg-warning';

`                `case 'em\_andamento': return 'bg-info';

`                `case 'concluida': return 'bg-success';

`                `case 'cancelada': return 'bg-secondary';

`                `default: return 'bg-secondary';

`            `}

`        `}



`        `// Atualizar calendário quando os filtros mudarem

`        `document.getElementById('filtro-tipo').addEventListener('change', function() {

`            `calendar.refetchEvents();

`        `});



`        `document.getElementById('filtro-turma').addEventListener('change', function() {

`            `calendar.refetchEvents();

`        `});



`        `document.getElementById('mostrar-concluidas').addEventListener('change', function() {

`            `calendar.refetchEvents();

`        `});

`    `});

</script>



`    `<!-- Script global do sistema -->

`    `<script>

`        `// Inicialização global do site

`        `document.addEventListener('DOMContentLoaded', function() {

`            `// Inicializar tooltips do Bootstrap

`            `var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));

`            `var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {

`                `return new bootstrap.Tooltip(tooltipTriggerEl);

`            `});



`            `// Inicializar popovers do Bootstrap

`            `var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));

`            `var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {

`                `return new bootstrap.Popover(popoverTriggerEl);

`            `});



`            `// Verificação CSRF para AJAX

`            `function getCookie(name) {

`                `let cookieValue = null;

`                `if (document.cookie && document.cookie !== '') {

`                    `const cookies = document.cookie.split(';');

`                    `for (let i = 0; i < cookies.length; i++) {

`                        `const cookie = cookies[i].trim();

`                        `if (cookie.substring(0, name.length + 1) === (name + '=')) {

`                            `cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

`                            `break;

`                        `}

`                    `}

`                `}

`                `return cookieValue;

`            `}



`            `// Configuração global do AJAX para incluir o token CSRF

`            `$.ajaxSetup({

`                `beforeSend: function(xhr, settings) {

`                    `if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {

`                        `xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));

`                    `}

`                `}

`            `});



`            `// Verificação periódica do token CSRF para sessões longas

`            `setInterval(function() {

`                `$.get("/csrf\_check/");

`            `}, 3600000); // A cada hora



`            `// Aplicar máscaras globais

`            `if (typeof $.fn.mask === 'function') {

`                `$('.cpf-mask').mask('000.000.000-00');

`                `$('.cep-mask').mask('00000-000');

`                `$('.phone-mask').mask('(00) 0000-00009');

`                `$('.phone-mask').blur(function(event) {

`                    `if($(this).val().length == 15){

`                        `$('.phone-mask').mask('(00) 00000-0009');

`                    `} else {

`                        `$('.phone-mask').mask('(00) 0000-00009');

`                    `}

`                `});

`                `$('.date-mask').mask('00/00/0000');

`                `$('.time-mask').mask('00:00 às 00:00');

`            `}



`            `// Inicialização global do Select2

`            `if (typeof $.fn.select2 === 'function') {

`                `$('.select2').select2({

`                    `theme: 'bootstrap4',

`                    `width: '100%'

`                `});

`            `}

`        `});

`    `</script>

`    `<script src="/static/js/inicializar\_select2.js"></script>


<link rel="stylesheet" href="/static/debug\_toolbar/css/print.css" media="print">

<link rel="stylesheet" href="/static/debug\_toolbar/css/toolbar.css">


<script type="module" src="/static/debug\_toolbar/js/toolbar.js" async=""></script>

<div id="djDebug" class="" dir="ltr" data-store-id="8ddaa38ed68e4049a7933db183829c29" data-render-panel-url="/\_\_debug\_\_/render\_panel/" data-sidebar-url="/\_\_debug\_\_/history\_sidebar/" data-default-show="true" data-update-on-fetch="False" data-theme="auto">

`  `<div class="djdt-hidden" id="djDebugToolbar">

`    `<ul id="djDebugPanelList">

`      `<li><a id="djHideToolBarButton" href="#" title="Ocultar barra de ferramentas">Esconder »</a></li>

`      `<li>

`        `<a id="djToggleThemeButton" href="#" title="Toggle Theme">

`          `Toggle Theme <svg aria-hidden="true" class="djdt-hidden theme-auto" fill="currentColor" viewBox="0 0 32 32" version="1.1" xmlns="http://www.w3.org/2000/svg">

`  `<path d="M0 16q0 3.264 1.28 6.24t3.392 5.088 5.12 3.424 6.208 1.248q3.264 0 6.24-1.248t5.088-3.424 3.392-5.088 1.28-6.24-1.28-6.208-3.392-5.12-5.088-3.392-6.24-1.28q-3.264 0-6.208 1.28t-5.12 3.392-3.392 5.12-1.28 6.208zM4 16q0-3.264 1.6-6.016t4.384-4.352 6.016-1.632 6.016 1.632 4.384 4.352 1.6 6.016-1.6 6.048-4.384 4.352-6.016 1.6-6.016-1.6-4.384-4.352-1.6-6.048zM16 26.016q2.72 0 5.024-1.344t3.648-3.648 1.344-5.024-1.344-4.992-3.648-3.648-5.024-1.344v20z"></path>

</svg>

<svg aria-hidden="true" class="djdt-hidden theme-light" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">

`  `<path fill-rule="evenodd" clip-rule="evenodd" d="M12 1.25C12.4142 1.25 12.75 1.58579 12.75 2V4C12.75 4.41421 12.4142 4.75 12 4.75C11.5858 4.75 11.25 4.41421 11.25 4V2C11.25 1.58579 11.5858 1.25 12 1.25ZM3.66865 3.71609C3.94815 3.41039 4.42255 3.38915 4.72825 3.66865L6.95026 5.70024C7.25596 5.97974 7.2772 6.45413 6.9977 6.75983C6.7182 7.06553 6.2438 7.08677 5.9381 6.80727L3.71609 4.77569C3.41039 4.49619 3.38915 4.02179 3.66865 3.71609ZM20.3314 3.71609C20.6109 4.02179 20.5896 4.49619 20.2839 4.77569L18.0619 6.80727C17.7562 7.08677 17.2818 7.06553 17.0023 6.75983C16.7228 6.45413 16.744 5.97974 17.0497 5.70024L19.2718 3.66865C19.5775 3.38915 20.0518 3.41039 20.3314 3.71609ZM12 7.75C9.65279 7.75 7.75 9.65279 7.75 12C7.75 14.3472 9.65279 16.25 12 16.25C14.3472 16.25 16.25 14.3472 16.25 12C16.25 9.65279 14.3472 7.75 12 7.75ZM6.25 12C6.25 8.82436 8.82436 6.25 12 6.25C15.1756 6.25 17.75 8.82436 17.75 12C17.75 15.1756 15.1756 17.75 12 17.75C8.82436 17.75 6.25 15.1756 6.25 12ZM1.25 12C1.25 11.5858 1.58579 11.25 2 11.25H4C4.41421 11.25 4.75 11.5858 4.75 12C4.75 12.4142 4.41421 12.75 4 12.75H2C1.58579 12.75 1.25 12.4142 1.25 12ZM19.25 12C19.25 11.5858 19.5858 11.25 20 11.25H22C22.4142 11.25 22.75 11.5858 22.75 12C22.75 12.4142 22.4142 12.75 22 12.75H20C19.5858 12.75 19.25 12.4142 19.25 12ZM17.0255 17.0252C17.3184 16.7323 17.7933 16.7323 18.0862 17.0252L20.3082 19.2475C20.6011 19.5404 20.601 20.0153 20.3081 20.3082C20.0152 20.6011 19.5403 20.601 19.2475 20.3081L17.0255 18.0858C16.7326 17.7929 16.7326 17.3181 17.0255 17.0252ZM6.97467 17.0253C7.26756 17.3182 7.26756 17.7931 6.97467 18.086L4.75244 20.3082C4.45955 20.6011 3.98468 20.6011 3.69178 20.3082C3.39889 20.0153 3.39889 19.5404 3.69178 19.2476L5.91401 17.0253C6.2069 16.7324 6.68177 16.7324 6.97467 17.0253ZM12 19.25C12.4142 19.25 12.75 19.5858 12.75 20V22C12.75 22.4142 12.4142 22.75 12 22.75C11.5858 22.75 11.25 22.4142 11.25 22V20C11.25 19.5858 11.5858 19.25 12 19.25Z" fill="currentColor"></path>

</svg>

<svg aria-hidden="true" class="djdt-hidden theme-dark" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">

`  `<path d="M3.32031 11.6835C3.32031 16.6541 7.34975 20.6835 12.3203 20.6835C16.1075 20.6835 19.3483 18.3443 20.6768 15.032C19.6402 15.4486 18.5059 15.6834 17.3203 15.6834C12.3497 15.6834 8.32031 11.654 8.32031 6.68342C8.32031 5.50338 8.55165 4.36259 8.96453 3.32996C5.65605 4.66028 3.32031 7.89912 3.32031 11.6835Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>

</svg>

`        `</a>

`      `</li>





<li id="djdt-HistoryPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtHistoryPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Histórico" class="HistoryPanel">



`  `Histórico





`      `<br><small>/atividades/calendario/</small>







`    `</a>



</li>





<li id="djdt-VersionsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtVersionsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Versões" class="VersionsPanel">



`  `Versões





`      `<br><small>Django 5.1.7</small>







`    `</a>



</li>





<li id="djdt-TimerPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtTimerPanel" checked="" title="Desativar para próximas requisições">



`    `<div class="djdt-contentless">



`  `Tempo





`      `<br><small>Total: 108.01ms</small>







`    `</div>



</li>





<li id="djdt-SettingsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSettingsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Settings from omaum.settings" class="SettingsPanel">



`  `Configurações













`    `</a>



</li>





<li id="djdt-HeadersPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtHeadersPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Cabeçalhos" class="HeadersPanel">



`  `Cabeçalhos













`    `</a>



</li>





<li id="djdt-RequestPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtRequestPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Requisição" class="RequestPanel">



`  `Requisição





`      `<br><small>calendario\_atividades</small>







`    `</a>



</li>





<li id="djdt-SQLPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSQLPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="SQL queries from 1 connection" class="SQLPanel">



`  `SQL





`      `<br><small>3 queries in 4.11ms</small>







`    `</a>



</li>





<li id="djdt-StaticFilesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtStaticFilesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Arquivos estáticos (154 encontrados, 6 sendo utilizados)" class="StaticFilesPanel">



`  `Arquivos estáticos





`      `<br><small>6 arquivos utilizados</small>







`    `</a>



</li>





<li id="djdt-TemplatesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtTemplatesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Templates (2 renderizados)" class="TemplatesPanel">



`  `Templates





`      `<br><small>atividades/calendario\_atividades.html</small>







`    `</a>



</li>





<li id="djdt-AlertsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtAlertsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Alerts" class="AlertsPanel">



`  `Alerts













`    `</a>



</li>





<li id="djdt-CachePanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtCachePanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Chamadas ao cache de 1 backend" class="CachePanel">



`  `Cache





`      `<br><small>0 chamada em 0.00ms</small>







`    `</a>



</li>





<li id="djdt-SignalsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSignalsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Sinais" class="SignalsPanel">



`  `Sinais





`      `<br><small>35 receptores de 15 sinais</small>







`    `</a>



</li>





<li id="djdt-RedirectsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtRedirectsPanel" title="Habilitar para próximas requisições">



`    `<div class="djdt-contentless djdt-disabled">



`  `Interceptar redirecionamentos





`    `</div>



</li>





<li id="djdt-ProfilingPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtProfilingPanel" title="Habilitar para próximas requisições">



`    `<div class="djdt-contentless djdt-disabled">



`  `Profiling





`    `</div>



</li>



`    `</ul>

`  `</div>

`  `<div class="" id="djDebugToolbarHandle" style="top: 265px;">

`    `<div title="Mostrar barra de ferramentas" id="djShowToolBarButton">

`      `<span id="djShowToolBarD">D</span><span id="djShowToolBarJ">J</span>DT

`    `</div>

`  `</div>






`  `<div id="HistoryPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Histórico</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="VersionsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Versões</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>













`  `<div id="SettingsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Settings from omaum.settings</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="HeadersPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Cabeçalhos</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="RequestPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Requisição</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="SQLPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>SQL queries from 1 connection</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="StaticFilesPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Arquivos estáticos (154 encontrados, 6 sendo utilizados)</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="TemplatesPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Templates (2 renderizados)</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="AlertsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Alerts</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="CachePanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Chamadas ao cache de 1 backend</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="SignalsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Sinais</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>
















`  `<div id="djDebugWindow" class="djdt-panelContent djdt-hidden"></div>

</div>


</body>

<body>

`    `<!-- Cabeçalho/Barra de Navegação -->

`    `<header>

`        `<nav class="navbar navbar-expand-lg navbar-dark bg-primary">

`            `<div class="container">

`                `<a class="navbar-brand" href="/">

`                    `<img src="/static/img/logo.png" alt="OMAUM Logo" height="40">

`                `</a>

`                `<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">

`                    `<span class="navbar-toggler-icon"></span>

`                `</button>



`                `<div class="collapse navbar-collapse" id="navbarNav">

`                    `<ul class="navbar-nav me-auto">

`                        `<li class="nav-item">

`                            `<a class="nav-link " href="/">

`                                `<i class="fas fa-home"></i> Início

`                            `</a>

`                        `</li>





`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/alunos/">

`                                    `<i class="fas fa-user-graduate"></i> Alunos

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/cursos/">

`                                    `<i class="fas fa-book"></i> Cursos

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/turmas/">

`                                    `<i class="fas fa-users"></i> Turmas

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/matriculas/">

`                                    `<i class="fas fa-clipboard-list"></i> Matrículas

`                                `</a>

`                            `</li>

`                            `<li class="nav-item dropdown">

`                                `<a class="nav-link dropdown-toggle" href="#" id="navbarDropdownAtividades" role="button" data-bs-toggle="dropdown" aria-expanded="false">

`                                   `<i class="fas fa-calendar-alt"></i> Atividades

`                                `</a>

`                                `<ul class="dropdown-menu" aria-labelledby="navbarDropdownAtividades">

`                                    `<li>

`                                        `<a class="dropdown-item" href="/atividades/academicas/">

`                                            `<i class="fas fa-school"></i> Acadêmicas

`                                        `</a>

`                                    `</li>

`                                    `<li>

`                                        `<a class="dropdown-item" href="/atividades/ritualisticas/">

`                                            `<i class="fas fa-pray"></i> Ritualísticas

`                                        `</a>

`                                    `</li>

`                                `</ul>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/frequencias/">

`                                    `<i class="fas fa-check-square"></i> Frequências

`                                `</a>

`                            `</li>



`                    `</ul>



`                    `<ul class="navbar-nav">





`                                `<li class="nav-item">

`                                    `<a class="nav-link" href="/painel-controle/">

`                                        `<i class="fas fa-cog"></i> Painel de Controle

`                                    `</a>

`                                `</li>



`                            `<li class="nav-item dropdown">

`                                `<a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">

`                                   `<i class="fas fa-user-circle"></i> lcsilv3

`                                `</a>

`                                `<ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">

`                                    `<li><a class="dropdown-item" href="#">Meu Perfil</a></li>

`                                    `<li><hr class="dropdown-divider"></li>

`                                    `<li>

`                                        `<form method="post" action="/sair/" class="d-inline">

`                                            `<input type="hidden" name="csrfmiddlewaretoken" value="JqDXJa0ien34m3tSQrtNQISq9tHBUxIY8qqKlI0FyL2ZJHHsRZYspG4wfE6c9E9F">

`                                            `<button type="submit" class="dropdown-item">

`                                                `<i class="fas fa-sign-out-alt"></i> Sair

`                                            `</button>

`                                        `</form>

`                                    `</li>

`                                `</ul>

`                            `</li>



`                    `</ul>

`                `</div>

`            `</div>

`        `</nav>

`    `</header>



`    `<!-- Mensagens do sistema (flash messages) -->

`    `<div class="message-container">



`    `</div>



`    `<!-- Conteúdo principal -->

`    `<main id="main-content" class="py-4">



<div class="container mt-4">

`    `<div class="d-flex justify-content-between align-items-center mb-4">

`        `<h1>Relatório de Atividades</h1>

`        `<div>

`            `<a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>

`            `<a href="/atividades/calendario/" class="btn btn-info me-2">

`                `<i class="fas fa-calendar-alt"></i> Calendário

`            `</a>

`            `<a href="/atividades/dashboard/" class="btn btn-success me-2">

`                `<i class="fas fa-chart-bar"></i> Dashboard

`            `</a>

`            `<div class="btn-group">

`                `<a href="/atividades/academicas/" class="btn btn-outline-primary">Atividades Acadêmicas</a>

`                `<a href="/atividades/ritualisticas/" class="btn btn-outline-info">Atividades Ritualísticas</a>

`            `</div>

`        `</div>

`    `</div>



`    `<!-- Filtros -->

`    `<div class="card mb-4">

`        `<div class="card-header">

`            `<h5 class="mb-0">Filtros</h5>

`        `</div>

`        `<div class="card-body">

`            `<form method="get" class="row g-3">

`                `<div class="col-md-3">

`                    `<label for="tipo" class="form-label">Tipo de Atividade</label>

`                    `<select name="tipo" id="tipo" class="form-select">

`                        `<option value="todas" selected="">Todas</option>

`                        `<option value="academicas">Acadêmicas</option>

`                        `<option value="ritualisticas">Ritualísticas</option>

`                    `</select>

`                `</div>

`                `<div class="col-md-3">

`                    `<label for="status" class="form-label">Status</label>

`                    `<select name="status" id="status" class="form-select">

`                        `<option value="">Todos</option>

`                        `<option value="agendada">Agendada</option>

`                        `<option value="em\_andamento">Em Andamento</option>

`                        `<option value="concluida">Concluída</option>

`                        `<option value="cancelada">Cancelada</option>

`                    `</select>

`                `</div>

`                `<div class="col-md-3">

`                    `<label for="data\_inicio" class="form-label">Data Início</label>

`                    `<input type="date" name="data\_inicio" id="data\_inicio" class="form-control" value="">

`                `</div>

`                `<div class="col-md-3">

`                    `<label for="data\_fim" class="form-label">Data Fim</label>

`                    `<input type="date" name="data\_fim" id="data\_fim" class="form-control" value="">

`                `</div>

`                `<div class="col-md-12 d-flex justify-content-end">

`                    `<button type="submit" class="btn btn-primary me-2">Filtrar</button>

`                    `<a href="/atividades/relatorio/" class="btn btn-secondary">Limpar Filtros</a>

`                `</div>

`            `</form>

`        `</div>

`    `</div>



`    `<!-- Botões de exportação -->

`    `<div class="mb-4">

`        `<a href="/atividades/exportar/pdf/?" class="btn btn-danger me-2">

`            `<i class="fas fa-file-pdf"></i> Exportar PDF

`        `</a>

`        `<a href="/atividades/exportar/excel/?" class="btn btn-success me-2">

`            `<i class="fas fa-file-excel"></i> Exportar Excel

`        `</a>

`        `<a href="/atividades/exportar/csv/?" class="btn btn-info">

`            `<i class="fas fa-file-csv"></i> Exportar CSV

`        `</a>

`    `</div>



`    `<!-- Resumo -->

`    `<div class="row mb-4">

`        `<div class="col-md-4">

`            `<div class="card bg-light">

`                `<div class="card-body text-center">

`                    `<h5 class="card-title">Total de Atividades</h5>

`                    `<p class="display-4">2</p>

`                `</div>

`            `</div>

`        `</div>

`        `<div class="col-md-4">

`            `<div class="card bg-primary text-white">

`                `<div class="card-body text-center">

`                    `<h5 class="card-title">Atividades Acadêmicas</h5>

`                    `<p class="display-4">2</p>

`                `</div>

`            `</div>

`        `</div>

`        `<div class="col-md-4">

`            `<div class="card bg-info text-white">

`                `<div class="card-body text-center">

`                    `<h5 class="card-title">Atividades Ritualísticas</h5>

`                    `<p class="display-4">0</p>

`                `</div>

`            `</div>

`        `</div>

`    `</div>



`    `<!-- Tabela de resultados -->

`    `<div class="card">

`        `<div class="card-header">

`            `<h5 class="mb-0">Resultados</h5>

`        `</div>

`        `<div class="card-body">

`            `<ul class="nav nav-tabs mb-3" id="myTab" role="tablist">

`                `<li class="nav-item" role="presentation">

`                    `<button class="nav-link active" id="academicas-tab" data-bs-toggle="tab" data-bs-target="#academicas" type="button" role="tab" aria-controls="academicas" aria-selected="true">

`                        `Atividades Acadêmicas

`                    `</button>

`                `</li>

`                `<li class="nav-item" role="presentation">

`                    `<button class="nav-link" id="ritualisticas-tab" data-bs-toggle="tab" data-bs-target="#ritualisticas" type="button" role="tab" aria-controls="ritualisticas" aria-selected="false">

`                        `Atividades Ritualísticas

`                    `</button>

`                `</li>

`            `</ul>

`            `<div class="tab-content" id="myTabContent">

`                `<!-- Atividades Acadêmicas -->

`                `<div class="tab-pane fade show active" id="academicas" role="tabpanel" aria-labelledby="academicas-tab">

`                    `<div class="table-responsive">

`                        `<table class="table table-striped">

`                            `<thead>

`                                `<tr>

`                                    `<th>Nome</th>

`                                    `<th>Tipo</th>

`                                    `<th>Data de Início</th>

`                                    `<th>Status</th>

`                                    `<th>Responsável</th>

`                                    `<th>Turmas</th>

`                                `</tr>

`                            `</thead>

`                            `<tbody>



`                                `<tr>

`                                    `<td>

`                                        `<a href="/atividades/academicas/detalhar/1/">

`                                            `Aula

`                                        `</a>

`                                    `</td>

`                                    `<td>Aula</td>

`                                    `<td>26/10/2024</td>

`                                    `<td>

`                                        `<span class="badge bg-warning">

`                                            `Agendada

`                                        `</span>

`                                    `</td>

`                                    `<td>Não informado</td>

`                                    `<td>



`                                            `<span class="badge bg-primary">A</span>



`                                    `</td>

`                                `</tr>



`                                `<tr>

`                                    `<td>

`                                        `<a href="/atividades/academicas/detalhar/2/">

`                                            `Plenilúnio

`                                        `</a>

`                                    `</td>

`                                    `<td>Aula</td>

`                                    `<td>26/10/2026</td>

`                                    `<td>

`                                        `<span class="badge bg-warning">

`                                            `Agendada

`                                        `</span>

`                                    `</td>

`                                    `<td>Não informado</td>

`                                    `<td>



`                                            `<span class="badge bg-primary">A</span>



`                                    `</td>

`                                `</tr>



`                            `</tbody>

`                        `</table>

`                    `</div>

`                `</div>



`                `<!-- Atividades Ritualísticas -->

`                `<div class="tab-pane fade" id="ritualisticas" role="tabpanel" aria-labelledby="ritualisticas-tab">

`                    `<div class="table-responsive">

`                        `<table class="table table-striped">

`                            `<thead>

`                                `<tr>

`                                    `<th>Nome</th>

`                                    `<th>Data</th>

`                                    `<th>Horário</th>

`                                    `<th>Local</th>

`                                    `<th>Turma</th>

`                                    `<th>Participantes</th>

`                                `</tr>

`                            `</thead>

`                            `<tbody>



`                                `<tr>

`                                    `<td colspan="6" class="text-center">Nenhuma atividade ritualística encontrada.</td>

`                                `</tr>



`                            `</tbody>

`                        `</table>

`                    `</div>

`                `</div>

`            `</div>

`        `</div>

`    `</div>

</div>

`    `</main>



`    `<!-- Rodapé -->

`    `<footer class="footer mt-auto py-3 bg-light">

`        `<div class="container text-center">

`            `<span class="text-muted">© 2025 OMAUM - Sistema de Gestão de Iniciados</span>

`        `</div>

`    `</footer>



`    `<!-- Scripts de componentes globais -->

`    `<script src="/static/js/modules/dias-semana.js"></script>



`    `<!-- Scripts específicos da página -->





`    `<!-- Script global do sistema -->

`    `<script>

`        `// Inicialização global do site

`        `document.addEventListener('DOMContentLoaded', function() {

`            `// Inicializar tooltips do Bootstrap

`            `var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));

`            `var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {

`                `return new bootstrap.Tooltip(tooltipTriggerEl);

`            `});



`            `// Inicializar popovers do Bootstrap

`            `var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));

`            `var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {

`                `return new bootstrap.Popover(popoverTriggerEl);

`            `});



`            `// Verificação CSRF para AJAX

`            `function getCookie(name) {

`                `let cookieValue = null;

`                `if (document.cookie && document.cookie !== '') {

`                    `const cookies = document.cookie.split(';');

`                    `for (let i = 0; i < cookies.length; i++) {

`                        `const cookie = cookies[i].trim();

`                        `if (cookie.substring(0, name.length + 1) === (name + '=')) {

`                            `cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

`                            `break;

`                        `}

`                    `}

`                `}

`                `return cookieValue;

`            `}



`            `// Configuração global do AJAX para incluir o token CSRF

`            `$.ajaxSetup({

`                `beforeSend: function(xhr, settings) {

`                    `if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {

`                        `xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));

`                    `}

`                `}

`            `});



`            `// Verificação periódica do token CSRF para sessões longas

`            `setInterval(function() {

`                `$.get("/csrf\_check/");

`            `}, 3600000); // A cada hora



`            `// Aplicar máscaras globais

`            `if (typeof $.fn.mask === 'function') {

`                `$('.cpf-mask').mask('000.000.000-00');

`                `$('.cep-mask').mask('00000-000');

`                `$('.phone-mask').mask('(00) 0000-00009');

`                `$('.phone-mask').blur(function(event) {

`                    `if($(this).val().length == 15){

`                        `$('.phone-mask').mask('(00) 00000-0009');

`                    `} else {

`                        `$('.phone-mask').mask('(00) 0000-00009');

`                    `}

`                `});

`                `$('.date-mask').mask('00/00/0000');

`                `$('.time-mask').mask('00:00 às 00:00');

`            `}



`            `// Inicialização global do Select2

`            `if (typeof $.fn.select2 === 'function') {

`                `$('.select2').select2({

`                    `theme: 'bootstrap4',

`                    `width: '100%'

`                `});

`            `}

`        `});

`    `</script>

`    `<script src="/static/js/inicializar\_select2.js"></script>


<link rel="stylesheet" href="/static/debug\_toolbar/css/print.css" media="print">

<link rel="stylesheet" href="/static/debug\_toolbar/css/toolbar.css">


<script type="module" src="/static/debug\_toolbar/js/toolbar.js" async=""></script>

<div id="djDebug" class="" dir="ltr" data-store-id="9e121781098b4378ac4eb695869319a2" data-render-panel-url="/\_\_debug\_\_/render\_panel/" data-sidebar-url="/\_\_debug\_\_/history\_sidebar/" data-default-show="true" data-update-on-fetch="False" data-theme="auto">

`  `<div class="djdt-hidden" id="djDebugToolbar">

`    `<ul id="djDebugPanelList">

`      `<li><a id="djHideToolBarButton" href="#" title="Ocultar barra de ferramentas">Esconder »</a></li>

`      `<li>

`        `<a id="djToggleThemeButton" href="#" title="Toggle Theme">

`          `Toggle Theme <svg aria-hidden="true" class="djdt-hidden theme-auto" fill="currentColor" viewBox="0 0 32 32" version="1.1" xmlns="http://www.w3.org/2000/svg">

`  `<path d="M0 16q0 3.264 1.28 6.24t3.392 5.088 5.12 3.424 6.208 1.248q3.264 0 6.24-1.248t5.088-3.424 3.392-5.088 1.28-6.24-1.28-6.208-3.392-5.12-5.088-3.392-6.24-1.28q-3.264 0-6.208 1.28t-5.12 3.392-3.392 5.12-1.28 6.208zM4 16q0-3.264 1.6-6.016t4.384-4.352 6.016-1.632 6.016 1.632 4.384 4.352 1.6 6.016-1.6 6.048-4.384 4.352-6.016 1.6-6.016-1.6-4.384-4.352-1.6-6.048zM16 26.016q2.72 0 5.024-1.344t3.648-3.648 1.344-5.024-1.344-4.992-3.648-3.648-5.024-1.344v20z"></path>

</svg>

<svg aria-hidden="true" class="djdt-hidden theme-light" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">

`  `<path fill-rule="evenodd" clip-rule="evenodd" d="M12 1.25C12.4142 1.25 12.75 1.58579 12.75 2V4C12.75 4.41421 12.4142 4.75 12 4.75C11.5858 4.75 11.25 4.41421 11.25 4V2C11.25 1.58579 11.5858 1.25 12 1.25ZM3.66865 3.71609C3.94815 3.41039 4.42255 3.38915 4.72825 3.66865L6.95026 5.70024C7.25596 5.97974 7.2772 6.45413 6.9977 6.75983C6.7182 7.06553 6.2438 7.08677 5.9381 6.80727L3.71609 4.77569C3.41039 4.49619 3.38915 4.02179 3.66865 3.71609ZM20.3314 3.71609C20.6109 4.02179 20.5896 4.49619 20.2839 4.77569L18.0619 6.80727C17.7562 7.08677 17.2818 7.06553 17.0023 6.75983C16.7228 6.45413 16.744 5.97974 17.0497 5.70024L19.2718 3.66865C19.5775 3.38915 20.0518 3.41039 20.3314 3.71609ZM12 7.75C9.65279 7.75 7.75 9.65279 7.75 12C7.75 14.3472 9.65279 16.25 12 16.25C14.3472 16.25 16.25 14.3472 16.25 12C16.25 9.65279 14.3472 7.75 12 7.75ZM6.25 12C6.25 8.82436 8.82436 6.25 12 6.25C15.1756 6.25 17.75 8.82436 17.75 12C17.75 15.1756 15.1756 17.75 12 17.75C8.82436 17.75 6.25 15.1756 6.25 12ZM1.25 12C1.25 11.5858 1.58579 11.25 2 11.25H4C4.41421 11.25 4.75 11.5858 4.75 12C4.75 12.4142 4.41421 12.75 4 12.75H2C1.58579 12.75 1.25 12.4142 1.25 12ZM19.25 12C19.25 11.5858 19.5858 11.25 20 11.25H22C22.4142 11.25 22.75 11.5858 22.75 12C22.75 12.4142 22.4142 12.75 22 12.75H20C19.5858 12.75 19.25 12.4142 19.25 12ZM17.0255 17.0252C17.3184 16.7323 17.7933 16.7323 18.0862 17.0252L20.3082 19.2475C20.6011 19.5404 20.601 20.0153 20.3081 20.3082C20.0152 20.6011 19.5403 20.601 19.2475 20.3081L17.0255 18.0858C16.7326 17.7929 16.7326 17.3181 17.0255 17.0252ZM6.97467 17.0253C7.26756 17.3182 7.26756 17.7931 6.97467 18.086L4.75244 20.3082C4.45955 20.6011 3.98468 20.6011 3.69178 20.3082C3.39889 20.0153 3.39889 19.5404 3.69178 19.2476L5.91401 17.0253C6.2069 16.7324 6.68177 16.7324 6.97467 17.0253ZM12 19.25C12.4142 19.25 12.75 19.5858 12.75 20V22C12.75 22.4142 12.4142 22.75 12 22.75C11.5858 22.75 11.25 22.4142 11.25 22V20C11.25 19.5858 11.5858 19.25 12 19.25Z" fill="currentColor"></path>

</svg>

<svg aria-hidden="true" class="djdt-hidden theme-dark" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">

`  `<path d="M3.32031 11.6835C3.32031 16.6541 7.34975 20.6835 12.3203 20.6835C16.1075 20.6835 19.3483 18.3443 20.6768 15.032C19.6402 15.4486 18.5059 15.6834 17.3203 15.6834C12.3497 15.6834 8.32031 11.654 8.32031 6.68342C8.32031 5.50338 8.55165 4.36259 8.96453 3.32996C5.65605 4.66028 3.32031 7.89912 3.32031 11.6835Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>

</svg>

`        `</a>

`      `</li>





<li id="djdt-HistoryPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtHistoryPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Histórico" class="HistoryPanel">



`  `Histórico





`      `<br><small>/atividades/relatorio/</small>







`    `</a>



</li>





<li id="djdt-VersionsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtVersionsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Versões" class="VersionsPanel">



`  `Versões





`      `<br><small>Django 5.1.7</small>







`    `</a>



</li>





<li id="djdt-TimerPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtTimerPanel" checked="" title="Desativar para próximas requisições">



`    `<div class="djdt-contentless">



`  `Tempo





`      `<br><small>Total: 74.76ms</small>







`    `</div>



</li>





<li id="djdt-SettingsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSettingsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Settings from omaum.settings" class="SettingsPanel">



`  `Configurações













`    `</a>



</li>





<li id="djdt-HeadersPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtHeadersPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Cabeçalhos" class="HeadersPanel">



`  `Cabeçalhos













`    `</a>



</li>





<li id="djdt-RequestPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtRequestPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Requisição" class="RequestPanel">



`  `Requisição





`      `<br><small>relatorio\_atividades</small>







`    `</a>



</li>





<li id="djdt-SQLPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSQLPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="SQL queries from 1 connection" class="SQLPanel">



`  `SQL





`      `<br><small>8 queries in 5.92ms</small>







`    `</a>



</li>





<li id="djdt-StaticFilesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtStaticFilesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Arquivos estáticos (154 encontrados, 6 sendo utilizados)" class="StaticFilesPanel">



`  `Arquivos estáticos





`      `<br><small>6 arquivos utilizados</small>







`    `</a>



</li>





<li id="djdt-TemplatesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtTemplatesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Templates (2 renderizados)" class="TemplatesPanel">



`  `Templates





`      `<br><small>atividades/relatorio\_atividades.html</small>







`    `</a>



</li>





<li id="djdt-AlertsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtAlertsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Alerts" class="AlertsPanel">



`  `Alerts













`    `</a>



</li>





<li id="djdt-CachePanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtCachePanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Chamadas ao cache de 1 backend" class="CachePanel">



`  `Cache





`      `<br><small>0 chamada em 0.00ms</small>







`    `</a>



</li>





<li id="djdt-SignalsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSignalsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Sinais" class="SignalsPanel">



`  `Sinais





`      `<br><small>35 receptores de 15 sinais</small>







`    `</a>



</li>





<li id="djdt-RedirectsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtRedirectsPanel" title="Habilitar para próximas requisições">



`    `<div class="djdt-contentless djdt-disabled">



`  `Interceptar redirecionamentos





`    `</div>



</li>





<li id="djdt-ProfilingPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtProfilingPanel" title="Habilitar para próximas requisições">



`    `<div class="djdt-contentless djdt-disabled">



`  `Profiling





`    `</div>



</li>



`    `</ul>

`  `</div>

`  `<div class="" id="djDebugToolbarHandle" style="top: 265px;">

`    `<div title="Mostrar barra de ferramentas" id="djShowToolBarButton">

`      `<span id="djShowToolBarD">D</span><span id="djShowToolBarJ">J</span>DT

`    `</div>

`  `</div>






`  `<div id="HistoryPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Histórico</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="VersionsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Versões</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>













`  `<div id="SettingsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Settings from omaum.settings</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="HeadersPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Cabeçalhos</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="RequestPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Requisição</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="SQLPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>SQL queries from 1 connection</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="StaticFilesPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Arquivos estáticos (154 encontrados, 6 sendo utilizados)</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="TemplatesPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Templates (2 renderizados)</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="AlertsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Alerts</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="CachePanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Chamadas ao cache de 1 backend</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="SignalsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Sinais</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>
















`  `<div id="djDebugWindow" class="djdt-panelContent djdt-hidden"></div>

</div>


</body>
<main id="main-content" class="py-4">



<div class="container mt-4">

`    `<div class="d-flex justify-content-between align-items-center mb-4">

`        `<h1>teste</h1>

`        `<div>

`            `<a href="/atividades/ritualisticas/" class="btn btn-secondary me-2">Voltar</a>

`            `<a href="/atividades/ritualisticas/" class="btn btn-secondary me-2">Lista de Atividades</a>

`            `<a href="/atividades/ritualisticas/editar/1/?return\_url=/atividades/ritualisticas/detalhar/1/" class="btn btn-warning me-2">Editar</a>

`            `<!-- Novo botão para copiar atividade -->

`            `<a href="/atividades/ritualisticas/1/copiar/" class="btn btn-secondary me-2">Copiar</a>

`            `<a href="/atividades/ritualisticas/confirmar-exclusao/1/?return\_url=/atividades/ritualisticas/detalhar/1/" class="btn btn-danger">Excluir</a>

`        `</div>

`    `</div>    





`    `<div class="row">

`        `<div class="col-md-8">

`            `<div class="card mb-4">

`                `<div class="card-header">

`                    `<h5>Informações Básicas</h5>

`                `</div>

`                `<div class="card-body">

`                    `<p><strong>Descrição:</strong> teste</p>

`                    `<p><strong>Data:</strong> 06/02/2025</p>

`                    `<p><strong>Horário:</strong> 10:00 - 20:00</p>

`                    `<p><strong>Local:</strong> teste</p>

`                    `<p><strong>Turma:</strong> D - Introdução à Meditação</p>

`                `</div>

`            `</div>

`        `</div>



`        `<div class="col-md-4">

`            `<div class="card mb-4">

`                `<div class="card-header">

`                    `<h5>Estatísticas</h5>

`                `</div>

`                `<div class="card-body">

`                    `<p><strong>Total de Participantes:</strong> 4</p>

`                `</div>

`            `</div>

`        `</div>

`    `</div>



`    `<div class="card mb-4">

`        `<div class="card-header">

`            `<h5>Participantes</h5>

`        `</div>

`        `<div class="card-body">

`            `<div class="table-responsive">

`                `<table class="table table-striped">

`                    `<thead>

`                        `<tr>

`                            `<th>Nome</th>

`                            `<th>Número Iniciático</th>

`                            `<th>Email</th>

`                        `</tr>

`                    `</thead>

`                    `<tbody>



`                            `<tr>

`                                `<td>Ana Pereira</td>

`                                `<td>560H</td>

`                                `<td>ana.pereira@exemplo.com</td>

`                            `</tr>



`                            `<tr>

`                                `<td>Bruno Ribeiro</td>

`                                `<td>940F</td>

`                                `<td>bruno.ribeiro@exemplo.com</td>

`                            `</tr>



`                            `<tr>

`                                `<td>Caic Passos Cardoso Da Silva</td>

`                                `<td>157</td>

`                                `<td>caicpassos4@gmail.com</td>

`                            `</tr>



`                            `<tr>

`                                `<td>Marcelo Nascimento</td>

`                                `<td>271E</td>

`                                `<td>marcelo.nascimento@exemplo.com</td>

`                            `</tr>



`                    `</tbody>

`                `</table>

`            `</div>

`        `</div>

`    `</div>

</div>

`    `</main>

<body>

`    `<!-- Cabeçalho/Barra de Navegação -->

`    `<header>

`        `<nav class="navbar navbar-expand-lg navbar-dark bg-primary">

`            `<div class="container">

`                `<a class="navbar-brand" href="/">

`                    `<img src="/static/img/logo.png" alt="OMAUM Logo" height="40">

`                `</a>

`                `<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">

`                    `<span class="navbar-toggler-icon"></span>

`                `</button>



`                `<div class="collapse navbar-collapse" id="navbarNav">

`                    `<ul class="navbar-nav me-auto">

`                        `<li class="nav-item">

`                            `<a class="nav-link " href="/">

`                                `<i class="fas fa-home"></i> Início

`                            `</a>

`                        `</li>





`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/alunos/">

`                                    `<i class="fas fa-user-graduate"></i> Alunos

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/cursos/">

`                                    `<i class="fas fa-book"></i> Cursos

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/turmas/">

`                                    `<i class="fas fa-users"></i> Turmas

`                                `</a>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/matriculas/">

`                                    `<i class="fas fa-clipboard-list"></i> Matrículas

`                                `</a>

`                            `</li>

`                            `<li class="nav-item dropdown">

`                                `<a class="nav-link dropdown-toggle" href="#" id="navbarDropdownAtividades" role="button" data-bs-toggle="dropdown" aria-expanded="false">

`                                   `<i class="fas fa-calendar-alt"></i> Atividades

`                                `</a>

`                                `<ul class="dropdown-menu" aria-labelledby="navbarDropdownAtividades">

`                                    `<li>

`                                        `<a class="dropdown-item" href="/atividades/academicas/">

`                                            `<i class="fas fa-school"></i> Acadêmicas

`                                        `</a>

`                                    `</li>

`                                    `<li>

`                                        `<a class="dropdown-item" href="/atividades/ritualisticas/">

`                                            `<i class="fas fa-pray"></i> Ritualísticas

`                                        `</a>

`                                    `</li>

`                                `</ul>

`                            `</li>

`                            `<li class="nav-item">

`                                `<a class="nav-link " href="/frequencias/">

`                                    `<i class="fas fa-check-square"></i> Frequências

`                                `</a>

`                            `</li>



`                    `</ul>



`                    `<ul class="navbar-nav">





`                                `<li class="nav-item">

`                                    `<a class="nav-link" href="/painel-controle/">

`                                        `<i class="fas fa-cog"></i> Painel de Controle

`                                    `</a>

`                                `</li>



`                            `<li class="nav-item dropdown">

`                                `<a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">

`                                   `<i class="fas fa-user-circle"></i> lcsilv3

`                                `</a>

`                                `<ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">

`                                    `<li><a class="dropdown-item" href="#">Meu Perfil</a></li>

`                                    `<li><hr class="dropdown-divider"></li>

`                                    `<li>

`                                        `<form method="post" action="/sair/" class="d-inline">

`                                            `<input type="hidden" name="csrfmiddlewaretoken" value="qcKgH1yoCHabcinwwHMVqWcagigKXyVSPcx3jzyLW596zWB6xfhAZUogmtFlcFmz">

`                                            `<button type="submit" class="dropdown-item">

`                                                `<i class="fas fa-sign-out-alt"></i> Sair

`                                            `</button>

`                                        `</form>

`                                    `</li>

`                                `</ul>

`                            `</li>



`                    `</ul>

`                `</div>

`            `</div>

`        `</nav>

`    `</header>



`    `<!-- Mensagens do sistema (flash messages) -->

`    `<div class="message-container">



`    `</div>



`    `<!-- Conteúdo principal -->

`    `<main id="main-content" class="py-4">



<div class="container mt-4">

`    `<div class="d-flex justify-content-between align-items-center mb-4">

`        `<h1>Editar Atividade Ritualística</h1>

`        `<a href="/atividades/ritualisticas/detalhar/1/" class="btn btn-secondary">Voltar para detalhes</a>

`    `</div>







`    `<form method="post">

`        `<input type="hidden" name="csrfmiddlewaretoken" value="qcKgH1yoCHabcinwwHMVqWcagigKXyVSPcx3jzyLW596zWB6xfhAZUogmtFlcFmz">





`        `<div class="card mb-4">

`            `<div class="card-header">

`                `<h5>Informações Básicas</h5>

`            `</div>

`            `<div class="card-body">

`                `<div class="row">

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_nome" class="form-label">Nome</label>

`    `<input type="text" name="nome" value="teste" class="form-control" maxlength="100" required="" id="id\_nome">





</div>

`                    `</div>

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_local" class="form-label">Local</label>

`    `<input type="text" name="local" value="teste" class="form-control" maxlength="100" required="" id="id\_local">





</div>

`                    `</div>

`                `</div>

`                `<div class="row">

`                    `<div class="col-md-12">

`                        `<div class="mb-3">

`    `<label for="id\_descricao" class="form-label">Descrição</label>

`    `<textarea name="descricao" cols="40" rows="3" class="form-control" id="id\_descricao">teste</textarea>





</div>

`                    `</div>

`                `</div>

`            `</div>

`        `</div>



`        `<div class="card mb-4">

`            `<div class="card-header">

`                `<h5>Data e Horário</h5>

`            `</div>

`            `<div class="card-body">

`                `<div class="row">

`                    `<div class="col-md-4">

`                        `<div class="mb-3">

`    `<label for="id\_data" class="form-label">Data</label>

`    `<input type="date" name="data" value="06/02/2025" class="form-control" required="" id="id\_data">





</div>

`                    `</div>

`                    `<div class="col-md-4">

`                        `<div class="mb-3">

`    `<label for="id\_hora\_inicio" class="form-label">Hora de Início</label>

`    `<input type="time" name="hora\_inicio" value="10:00:00" class="form-control" required="" id="id\_hora\_inicio">





</div>

`                    `</div>

`                    `<div class="col-md-4">

`                        `<div class="mb-3">

`    `<label for="id\_hora\_fim" class="form-label">Hora de Término</label>

`    `<input type="time" name="hora\_fim" value="20:00:00" class="form-control" required="" id="id\_hora\_fim">





</div>

`                    `</div>

`                `</div>

`            `</div>

`        `</div>



`        `<div class="card mb-4">

`            `<div class="card-header">

`                `<h5>Turma e Participantes</h5>

`            `</div>

`            `<div class="card-body">

`                `<div class="row">

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_turma" class="form-label">Turma</label>

`    `<select name="turma" class="form-control" required="" id="id\_turma">

`  `<option value="">---------</option>

`  `<option value="6" selected="">D - Introdução à Meditação</option>

`  `<option value="2">A - Introdução à Meditação</option>

`  `<option value="4">B - Introdução à Meditação</option>

`  `<option value="5">C - Introdução à Meditação</option>

</select>





</div>

`                    `</div>

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_todos\_alunos" class="form-label">Incluir todos os alunos da turma</label>

`    `<input type="checkbox" name="todos\_alunos" id="id\_todos\_alunos">





</div>

`                        `<small class="form-text text-muted">Marque esta opção para incluir automaticamente todos os alunos da turma.</small>

`                    `</div>

`                `</div>



`                `<div class="row mt-3" id="participantes-container" style="display: block;">

`                    `<div class="col-md-12">

`                        `<label for="id\_participantes">Participantes</label>

`                        `<div class="border p-3 rounded">

`                            `<select name="participantes" class="form-control select2-hidden-accessible" id="id\_participantes" multiple="" data-select2-id="select2-data-id\_participantes" tabindex="-1" aria-hidden="true">

`  `<option value="18027737038">Aline Souza</option>

`  `<option value="71012661207">Ana Ferreira</option>

`  `<option value="61714562670" selected="" data-select2-id="select2-data-2-ayq0">Ana Pereira</option>

`  `<option value="96931040271">André Costa</option>

`  `<option value="57431572587" selected="" data-select2-id="select2-data-3-pdl5">Bruno Ribeiro</option>

`  `<option value="15645038797" selected="" data-select2-id="select2-data-4-j4d3">Caic Passos Cardoso Da Silva</option>

`  `<option value="16335805186">Camila Oliveira</option>

`  `<option value="19529676522">Daniela Mendes</option>

`  `<option value="37663960965">Felipe Costa</option>

`  `<option value="25185348461">Felipe Souza</option>

`  `<option value="51286148744">Fernanda Costa</option>

`  `<option value="29807388257">Fernanda Martins</option>

`  `<option value="19403318172">Gustavo Araújo</option>

`  `<option value="08832339202">Gustavo Barbosa</option>

`  `<option value="60795674660">Gustavo Rocha</option>

`  `<option value="52551221829">João Pereira</option>

`  `<option value="12345678901">João Silva</option>

`  `<option value="85736517952">Juliana Lima</option>

`  `<option value="30624167050">Lucas Araújo</option>

`  `<option value="81991045700">Luis Carlos Da Silva</option>

`  `<option value="27789400090" selected="" data-select2-id="select2-data-5-m10n">Marcelo Nascimento</option>

`  `<option value="21451098237">Marcelo Oliveira</option>

`  `<option value="05584938593">Maria Carvalho</option>

`  `<option value="98765432109">Maria Oliveira</option>

`  `<option value="11129399978">Maria Rodrigues</option>

`  `<option value="11794022817">Mariana Ribeiro</option>

`  `<option value="49405540240">Mariana Rocha</option>

`  `<option value="40518102926">Pedro Araújo</option>

`  `<option value="03404794223">Pedro Carvalho</option>

`  `<option value="97794010840">Pedro Mendes</option>

`  `<option value="70010205369">Pedro Nascimento</option>

`  `<option value="89748235253">Rodrigo Araújo</option>

`  `<option value="51727155004">Rodrigo Carvalho</option>

`  `<option value="51623759179">Rodrigo Nascimento</option>

`  `<option value="12331179719">Thays Passos Da Silva</option>

</select><span class="select2 select2-container select2-container--bootstrap4" dir="ltr" data-select2-id="select2-data-1-qix4" style="width: 100%;"><span class="selection"><span class="select2-selection select2-selection--multiple select2-selection--clearable" role="combobox" aria-haspopup="true" aria-expanded="false" tabindex="-1" aria-disabled="false"><button type="button" class="select2-selection\_\_clear" tabindex="-1" title="Remove all items" aria-label="Remove all items" aria-describedby="select2-id\_participantes-container" data-select2-id="select2-data-10-cp9t"><span aria-hidden="true">×</span></button><ul class="select2-selection\_\_rendered" id="select2-id\_participantes-container"><li class="select2-selection\_\_choice" title="Ana Pereira" data-select2-id="select2-data-6-qtge"><button type="button" class="select2-selection\_\_choice\_\_remove" tabindex="-1" title="Remove item" aria-label="Remove item" aria-describedby="select2-id\_participantes-container-choice-cc77-61714562670"><span aria-hidden="true">×</span></button><span class="select2-selection\_\_choice\_\_display" id="select2-id\_participantes-container-choice-cc77-61714562670">Ana Pereira</span></li><li class="select2-selection\_\_choice" title="Bruno Ribeiro" data-select2-id="select2-data-7-fmbf"><button type="button" class="select2-selection\_\_choice\_\_remove" tabindex="-1" title="Remove item" aria-label="Remove item" aria-describedby="select2-id\_participantes-container-choice-anht-57431572587"><span aria-hidden="true">×</span></button><span class="select2-selection\_\_choice\_\_display" id="select2-id\_participantes-container-choice-anht-57431572587">Bruno Ribeiro</span></li><li class="select2-selection\_\_choice" title="Caic Passos Cardoso Da Silva" data-select2-id="select2-data-8-nyfd"><button type="button" class="select2-selection\_\_choice\_\_remove" tabindex="-1" title="Remove item" aria-label="Remove item" aria-describedby="select2-id\_participantes-container-choice-c0uj-15645038797"><span aria-hidden="true">×</span></button><span class="select2-selection\_\_choice\_\_display" id="select2-id\_participantes-container-choice-c0uj-15645038797">Caic Passos Cardoso Da Silva</span></li><li class="select2-selection\_\_choice" title="Marcelo Nascimento" data-select2-id="select2-data-9-2oz7"><button type="button" class="select2-selection\_\_choice\_\_remove" tabindex="-1" title="Remove item" aria-label="Remove item" aria-describedby="select2-id\_participantes-container-choice-10dm-27789400090"><span aria-hidden="true">×</span></button><span class="select2-selection\_\_choice\_\_display" id="select2-id\_participantes-container-choice-10dm-27789400090">Marcelo Nascimento</span></li></ul><span class="select2-search select2-search--inline"><textarea class="select2-search\_\_field" type="search" tabindex="0" autocorrect="off" autocapitalize="none" spellcheck="false" role="searchbox" aria-autocomplete="list" autocomplete="off" aria-label="Search" aria-describedby="select2-id\_participantes-container" placeholder="" style="width: 0.75em;"></textarea></span></span></span><span class="dropdown-wrapper" aria-hidden="true"></span></span>

`                        `</div>



`                    `</div>

`                `</div>

`            `</div>

`        `</div>



`        `<div class="d-flex justify-content-between mb-5">

`            `<a href="/atividades/ritualisticas/detalhar/1/" class="btn btn-secondary">Cancelar</a>

`            `<button type="submit" class="btn btn-primary">Atualizar Atividade</button>

`        `</div>

`    `</form>

</div>

`    `</main>



`    `<!-- Rodapé -->

`    `<footer class="footer mt-auto py-3 bg-light">

`        `<div class="container text-center">

`            `<span class="text-muted">© 2025 OMAUM - Sistema de Gestão de Iniciados</span>

`        `</div>

`    `</footer>



`    `<!-- Scripts de componentes globais -->

`    `<script src="/static/js/modules/dias-semana.js"></script>



`    `<!-- Scripts específicos da página -->



<script>

`    `document.addEventListener('DOMContentLoaded', function() {

`        `const todosAlunosCheckbox = document.getElementById('id\_todos\_alunos');

`        `const participantesContainer = document.getElementById('participantes-container');



`        `function toggleParticipantes() {

`            `if (todosAlunosCheckbox.checked) {

`                `participantesContainer.style.display = 'none';

`            `} else {

`                `participantesContainer.style.display = 'block';

`            `}

`        `}



`        `// Inicializar

`        `toggleParticipantes();



`        `// Adicionar listener para mudanças

`        `todosAlunosCheckbox.addEventListener('change', toggleParticipantes);

`    `});

</script>



`    `<!-- Script global do sistema -->

`    `<script>

`        `// Inicialização global do site

`        `document.addEventListener('DOMContentLoaded', function() {

`            `// Inicializar tooltips do Bootstrap

`            `var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));

`            `var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {

`                `return new bootstrap.Tooltip(tooltipTriggerEl);

`            `});



`            `// Inicializar popovers do Bootstrap

`            `var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));

`            `var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {

`                `return new bootstrap.Popover(popoverTriggerEl);

`            `});



`            `// Verificação CSRF para AJAX

`            `function getCookie(name) {

`                `let cookieValue = null;

`                `if (document.cookie && document.cookie !== '') {

`                    `const cookies = document.cookie.split(';');

`                    `for (let i = 0; i < cookies.length; i++) {

`                        `const cookie = cookies[i].trim();

`                        `if (cookie.substring(0, name.length + 1) === (name + '=')) {

`                            `cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

`                            `break;

`                        `}

`                    `}

`                `}

`                `return cookieValue;

`            `}



`            `// Configuração global do AJAX para incluir o token CSRF

`            `$.ajaxSetup({

`                `beforeSend: function(xhr, settings) {

`                    `if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {

`                        `xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));

`                    `}

`                `}

`            `});



`            `// Verificação periódica do token CSRF para sessões longas

`            `setInterval(function() {

`                `$.get("/csrf\_check/");

`            `}, 3600000); // A cada hora



`            `// Aplicar máscaras globais

`            `if (typeof $.fn.mask === 'function') {

`                `$('.cpf-mask').mask('000.000.000-00');

`                `$('.cep-mask').mask('00000-000');

`                `$('.phone-mask').mask('(00) 0000-00009');

`                `$('.phone-mask').blur(function(event) {

`                    `if($(this).val().length == 15){

`                        `$('.phone-mask').mask('(00) 00000-0009');

`                    `} else {

`                        `$('.phone-mask').mask('(00) 0000-00009');

`                    `}

`                `});

`                `$('.date-mask').mask('00/00/0000');

`                `$('.time-mask').mask('00:00 às 00:00');

`            `}



`            `// Inicialização global do Select2

`            `if (typeof $.fn.select2 === 'function') {

`                `$('.select2').select2({

`                    `theme: 'bootstrap4',

`                    `width: '100%'

`                `});

`            `}

`        `});

`    `</script>

`    `<script src="/static/js/inicializar\_select2.js"></script>


<link rel="stylesheet" href="/static/debug\_toolbar/css/print.css" media="print">

<link rel="stylesheet" href="/static/debug\_toolbar/css/toolbar.css">


<script type="module" src="/static/debug\_toolbar/js/toolbar.js" async=""></script>

<div id="djDebug" class="" dir="ltr" data-store-id="ac64da500e8f4ca798ae32e62209d395" data-render-panel-url="/\_\_debug\_\_/render\_panel/" data-sidebar-url="/\_\_debug\_\_/history\_sidebar/" data-default-show="true" data-update-on-fetch="False" data-theme="auto">

`  `<div class="djdt-hidden" id="djDebugToolbar">

`    `<ul id="djDebugPanelList">

`      `<li><a id="djHideToolBarButton" href="#" title="Ocultar barra de ferramentas">Esconder »</a></li>

`      `<li>

`        `<a id="djToggleThemeButton" href="#" title="Toggle Theme">

`          `Toggle Theme <svg aria-hidden="true" class="djdt-hidden theme-auto" fill="currentColor" viewBox="0 0 32 32" version="1.1" xmlns="http://www.w3.org/2000/svg">

`  `<path d="M0 16q0 3.264 1.28 6.24t3.392 5.088 5.12 3.424 6.208 1.248q3.264 0 6.24-1.248t5.088-3.424 3.392-5.088 1.28-6.24-1.28-6.208-3.392-5.12-5.088-3.392-6.24-1.28q-3.264 0-6.208 1.28t-5.12 3.392-3.392 5.12-1.28 6.208zM4 16q0-3.264 1.6-6.016t4.384-4.352 6.016-1.632 6.016 1.632 4.384 4.352 1.6 6.016-1.6 6.048-4.384 4.352-6.016 1.6-6.016-1.6-4.384-4.352-1.6-6.048zM16 26.016q2.72 0 5.024-1.344t3.648-3.648 1.344-5.024-1.344-4.992-3.648-3.648-5.024-1.344v20z"></path>

</svg>

<svg aria-hidden="true" class="djdt-hidden theme-light" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">

`  `<path fill-rule="evenodd" clip-rule="evenodd" d="M12 1.25C12.4142 1.25 12.75 1.58579 12.75 2V4C12.75 4.41421 12.4142 4.75 12 4.75C11.5858 4.75 11.25 4.41421 11.25 4V2C11.25 1.58579 11.5858 1.25 12 1.25ZM3.66865 3.71609C3.94815 3.41039 4.42255 3.38915 4.72825 3.66865L6.95026 5.70024C7.25596 5.97974 7.2772 6.45413 6.9977 6.75983C6.7182 7.06553 6.2438 7.08677 5.9381 6.80727L3.71609 4.77569C3.41039 4.49619 3.38915 4.02179 3.66865 3.71609ZM20.3314 3.71609C20.6109 4.02179 20.5896 4.49619 20.2839 4.77569L18.0619 6.80727C17.7562 7.08677 17.2818 7.06553 17.0023 6.75983C16.7228 6.45413 16.744 5.97974 17.0497 5.70024L19.2718 3.66865C19.5775 3.38915 20.0518 3.41039 20.3314 3.71609ZM12 7.75C9.65279 7.75 7.75 9.65279 7.75 12C7.75 14.3472 9.65279 16.25 12 16.25C14.3472 16.25 16.25 14.3472 16.25 12C16.25 9.65279 14.3472 7.75 12 7.75ZM6.25 12C6.25 8.82436 8.82436 6.25 12 6.25C15.1756 6.25 17.75 8.82436 17.75 12C17.75 15.1756 15.1756 17.75 12 17.75C8.82436 17.75 6.25 15.1756 6.25 12ZM1.25 12C1.25 11.5858 1.58579 11.25 2 11.25H4C4.41421 11.25 4.75 11.5858 4.75 12C4.75 12.4142 4.41421 12.75 4 12.75H2C1.58579 12.75 1.25 12.4142 1.25 12ZM19.25 12C19.25 11.5858 19.5858 11.25 20 11.25H22C22.4142 11.25 22.75 11.5858 22.75 12C22.75 12.4142 22.4142 12.75 22 12.75H20C19.5858 12.75 19.25 12.4142 19.25 12ZM17.0255 17.0252C17.3184 16.7323 17.7933 16.7323 18.0862 17.0252L20.3082 19.2475C20.6011 19.5404 20.601 20.0153 20.3081 20.3082C20.0152 20.6011 19.5403 20.601 19.2475 20.3081L17.0255 18.0858C16.7326 17.7929 16.7326 17.3181 17.0255 17.0252ZM6.97467 17.0253C7.26756 17.3182 7.26756 17.7931 6.97467 18.086L4.75244 20.3082C4.45955 20.6011 3.98468 20.6011 3.69178 20.3082C3.39889 20.0153 3.39889 19.5404 3.69178 19.2476L5.91401 17.0253C6.2069 16.7324 6.68177 16.7324 6.97467 17.0253ZM12 19.25C12.4142 19.25 12.75 19.5858 12.75 20V22C12.75 22.4142 12.4142 22.75 12 22.75C11.5858 22.75 11.25 22.4142 11.25 22V20C11.25 19.5858 11.5858 19.25 12 19.25Z" fill="currentColor"></path>

</svg>

<svg aria-hidden="true" class="djdt-hidden theme-dark" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">

`  `<path d="M3.32031 11.6835C3.32031 16.6541 7.34975 20.6835 12.3203 20.6835C16.1075 20.6835 19.3483 18.3443 20.6768 15.032C19.6402 15.4486 18.5059 15.6834 17.3203 15.6834C12.3497 15.6834 8.32031 11.654 8.32031 6.68342C8.32031 5.50338 8.55165 4.36259 8.96453 3.32996C5.65605 4.66028 3.32031 7.89912 3.32031 11.6835Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>

</svg>

`        `</a>

`      `</li>





<li id="djdt-HistoryPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtHistoryPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Histórico" class="HistoryPanel">



`  `Histórico





`      `<br><small>/atividades/ritualisticas/editar/1/?return\_url=/atividades/ritualisticas/detalhar/1/</small>







`    `</a>



</li>





<li id="djdt-VersionsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtVersionsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Versões" class="VersionsPanel">



`  `Versões





`      `<br><small>Django 5.1.7</small>







`    `</a>



</li>





<li id="djdt-TimerPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtTimerPanel" checked="" title="Desativar para próximas requisições">



`    `<div class="djdt-contentless">



`  `Tempo





`      `<br><small>Total: 277.98ms</small>







`    `</div>



</li>





<li id="djdt-SettingsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSettingsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Settings from omaum.settings" class="SettingsPanel">



`  `Configurações













`    `</a>



</li>





<li id="djdt-HeadersPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtHeadersPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Cabeçalhos" class="HeadersPanel">



`  `Cabeçalhos













`    `</a>



</li>





<li id="djdt-RequestPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtRequestPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Requisição" class="RequestPanel">



`  `Requisição





`      `<br><small>editar\_atividade\_ritualistica</small>







`    `</a>



</li>





<li id="djdt-SQLPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSQLPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="SQL queries from 1 connection" class="SQLPanel">



`  `SQL





`      `<br><small>10 queries in 13.41ms</small>







`    `</a>



</li>





<li id="djdt-StaticFilesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtStaticFilesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Arquivos estáticos (154 encontrados, 6 sendo utilizados)" class="StaticFilesPanel">



`  `Arquivos estáticos





`      `<br><small>6 arquivos utilizados</small>







`    `</a>



</li>





<li id="djdt-TemplatesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtTemplatesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Templates (11 renderizados)" class="TemplatesPanel">



`  `Templates





`      `<br><small>atividades/editar\_atividade\_ritualistica.html</small>







`    `</a>



</li>





<li id="djdt-AlertsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtAlertsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Alerts" class="AlertsPanel">



`  `Alerts













`    `</a>



</li>





<li id="djdt-CachePanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtCachePanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Chamadas ao cache de 1 backend" class="CachePanel">



`  `Cache





`      `<br><small>0 chamada em 0.00ms</small>







`    `</a>



</li>





<li id="djdt-SignalsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSignalsPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Sinais" class="SignalsPanel">



`  `Sinais





`      `<br><small>35 receptores de 15 sinais</small>







`    `</a>



</li>





<li id="djdt-RedirectsPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtRedirectsPanel" title="Habilitar para próximas requisições">



`    `<div class="djdt-contentless djdt-disabled">



`  `Interceptar redirecionamentos





`    `</div>



</li>





<li id="djdt-ProfilingPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtProfilingPanel" title="Habilitar para próximas requisições">



`    `<div class="djdt-contentless djdt-disabled">



`  `Profiling





`    `</div>



</li>



`    `</ul>

`  `</div>

`  `<div class="" id="djDebugToolbarHandle" style="top: 265px;">

`    `<div title="Mostrar barra de ferramentas" id="djShowToolBarButton">

`      `<span id="djShowToolBarD">D</span><span id="djShowToolBarJ">J</span>DT

`    `</div>

`  `</div>






`  `<div id="HistoryPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Histórico</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="VersionsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Versões</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>













`  `<div id="SettingsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Settings from omaum.settings</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="HeadersPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Cabeçalhos</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="RequestPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Requisição</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="SQLPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>SQL queries from 1 connection</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="StaticFilesPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Arquivos estáticos (154 encontrados, 6 sendo utilizados)</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="TemplatesPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Templates (11 renderizados)</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="AlertsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Alerts</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="CachePanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Chamadas ao cache de 1 backend</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="SignalsPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Sinais</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>
















`  `<div id="djDebugWindow" class="djdt-panelContent djdt-hidden"></div>

</div>


</body>


