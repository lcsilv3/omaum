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

`                                `<a class="nav-link active" href="/frequencias/">

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

`                                            `<input type="hidden" name="csrfmiddlewaretoken" value="v4KzNmv7BivfHg9SxV25rGQygDoKmiF2U4xmpUvuVGua4UnsytxK0E2EmONlBp6J">

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

`    `<!-- Cabeçalho com título e botões -->

`    `<div class="d-flex justify-content-between align-items-center mb-3">

`        `<h1>Lista de Frequências Mensais</h1>

`        `<div class="btn-group">

`            `<a href="/frequencias/criar/" class="btn btn-primary">

`                `<i class="fas fa-plus"></i> Nova Frequência Mensal

`            `</a>

`            `<a href="/frequencias/painel/" class="btn btn-info">

`                `<i class="fas fa-chart-line"></i> Painel de Frequências

`            `</a>

`            `<a href="/frequencias/relatorio/" class="btn btn-warning">

`                `<i class="fas fa-chart-bar"></i> Relatório

`            `</a>

`        `</div>

`    `</div>



`    `<!-- Filtros -->

`    `<div class="card mb-4">

`        `<div class="card-header bg-light">

`            `<h5 class="mb-0">Filtros</h5>

`        `</div>

`        `<div class="card-body">

`            `<form method="get" class="row g-3">

`                `<div class="col-md-3">

`                    `<label for="turma" class="form-label">Turma</label>

`                    `<select name="turma" id="turma" class="form-select select2 select2-hidden-accessible" tabindex="-1" aria-hidden="true" data-select2-id="select2-data-turma">

`                        `<option value="" data-select2-id="select2-data-8-hff7">Todas as turmas</option>



`                        `<option value="6">

`                            `D

`                        `</option>



`                        `<option value="2">

`                            `A

`                        `</option>



`                        `<option value="4">

`                            `B

`                        `</option>



`                        `<option value="5">

`                            `C

`                        `</option>



`                    `</select><span class="select2 select2-container select2-container--bootstrap4 select2-hidden-accessible" dir="ltr" data-select2-id="select2-data-7-7er7" style="width: 100%;" tabindex="-1" aria-hidden="true"><span class="selection"><span class="select2-selection select2-selection--single" role="combobox" aria-haspopup="true" aria-expanded="false" tabindex="0" aria-disabled="false" aria-labelledby="select2-turma-container" aria-controls="select2-turma-container"><span class="select2-selection\_\_rendered" id="select2-turma-container" role="textbox" aria-readonly="true" title="Todas as turmas">Todas as turmas</span><span class="select2-selection\_\_arrow" role="presentation"><b role="presentation"></b></span></span></span><span class="dropdown-wrapper" aria-hidden="true"></span></span><span class="select2 select2-container select2-container--bootstrap4" dir="ltr" data-select2-id="select2-data-11-m2mc" style="width: 100%;"><span class="selection"><span class="select2-selection select2-selection--single" role="combobox" aria-haspopup="true" aria-expanded="false" tabindex="0" aria-disabled="false" aria-labelledby="select2-krtx-container" aria-controls="select2-krtx-container"><span class="select2-selection\_\_rendered" id="select2-krtx-container" role="textbox" aria-readonly="true"></span><span class="select2-selection\_\_arrow" role="presentation"><b role="presentation"></b></span></span></span><span class="dropdown-wrapper" aria-hidden="true"></span></span>

`                `</div>

`                `<div class="col-md-2">

`                    `<label for="mes" class="form-label">Mês</label>

`                    `<select name="mes" id="mes" class="form-select">

`                        `<option value="">Todos os meses</option>



`                    `</select>

`                `</div>

`                `<div class="col-md-2">

`                    `<label for="ano" class="form-label">Ano</label>

`                    `<select name="ano" id="ano" class="form-select">

`                        `<option value="">Todos os anos</option>



`                    `</select>

`                `</div>

`                `<div class="col-12 mt-3">

`                    `<button type="submit" class="btn btn-primary">

`                        `<i class="fas fa-filter"></i> Filtrar

`                    `</button>

`                    `<a href="/frequencias/" class="btn btn-secondary">

`                        `<i class="fas fa-broom"></i> Limpar Filtros

`                    `</a>

`                `</div>

`            `</form>

`        `</div>

`    `</div>



`    `<!-- Tabela de frequências -->

`    `<div class="card">

`        `<div class="card-body">

`            `<div class="table-responsive">

`                `<table class="table table-striped table-hover">

`                    `<thead class="table-dark">

`                        `<tr>

`                            `<th>Turma</th>

`                            `<th>Mês/Ano</th>

`                            `<th>Percentual Mínimo</th>

`                            `<th>Alunos em Carência</th>

`                            `<th>Última Atualização</th>

`                            `<th>Ações</th>

`                        `</tr>

`                    `</thead>

`                    `<tbody>



`                        `<tr>

`                            `<td colspan="6" class="text-center py-4">

`                                `<div class="alert alert-info mb-0">

`                                    `Nenhuma frequência mensal encontrada com os filtros selecionados.

`                                `</div>

`                            `</td>

`                        `</tr>



`                    `</tbody>

`                `</table>

`            `</div>



`            `<!-- Paginação -->



`        `</div>

`        `<div class="card-footer">

`            `<div class="d-flex justify-content-between align-items-center">

`                `<span>Total: 0 frequências mensais</span>

`                `<span>Página 1 de 1</span>

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



<script>

`    `document.addEventListener('DOMContentLoaded', function() {

`        `// Inicializar Select2 para melhorar a experiência de seleção

`        `$('.select2').select2({

`            `theme: 'bootstrap-5',

`            `width: '100%'

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

<div id="djDebug" class="" dir="ltr" data-store-id="f1d3801301864798a628397f502379b8" data-render-panel-url="/\_\_debug\_\_/render\_panel/" data-sidebar-url="/\_\_debug\_\_/history\_sidebar/" data-default-show="true" data-update-on-fetch="False" data-theme="auto">

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





`      `<br><small>/frequencias/</small>







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





`      `<br><small>Total: 148.01ms</small>







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





`      `<br><small>listar\_frequencias</small>







`    `</a>



</li>





<li id="djdt-SQLPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSQLPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="SQL queries from 1 connection" class="SQLPanel">



`  `SQL





`      `<br><small>5 queries in 6.83ms</small>







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





`      `<br><small>frequencias/listar\_frequencias.html</small>







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

`                                `<a class="nav-link active" href="/frequencias/">

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

`                                            `<input type="hidden" name="csrfmiddlewaretoken" value="to1r4Hb0xX0EbM62TyDMivnKNW2fT2RFSoOeGfbnRlZzyqkCU68rRtzQT7rQ89im">

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

`    `<div class="row justify-content-center">

`        `<div class="col-md-8">

`            `<div class="card">

`                `<div class="card-header bg-primary text-white">

`                    `<h4 class="mb-0">Criar Frequência Mensal</h4>

`                `</div>

`                `<div class="card-body">

`                    `<form method="post" novalidate="">

`                        `<input type="hidden" name="csrfmiddlewaretoken" value="to1r4Hb0xX0EbM62TyDMivnKNW2fT2RFSoOeGfbnRlZzyqkCU68rRtzQT7rQ89im">







`                        `<div class="mb-3">

`                            `<label for="id\_turma" class="form-label">Turma</label>

`                            `<select name="turma" class="form-control select2 select2-hidden-accessible" required="" id="id\_turma" tabindex="-1" aria-hidden="true" data-select2-id="select2-data-id\_turma">

`  `<option value="" selected="" data-select2-id="select2-data-8-o433">---------</option>

`  `<option value="6">D - Introdução à Meditação</option>

`  `<option value="2">A - Introdução à Meditação</option>

`  `<option value="4">B - Introdução à Meditação</option>

`  `<option value="5">C - Introdução à Meditação</option>

</select><span class="select2 select2-container select2-container--bootstrap4 select2-hidden-accessible" dir="ltr" data-select2-id="select2-data-7-svtk" style="width: 100%;" tabindex="-1" aria-hidden="true"><span class="selection"><span class="select2-selection select2-selection--single" role="combobox" aria-haspopup="true" aria-expanded="false" tabindex="0" aria-disabled="false" aria-labelledby="select2-id\_turma-container" aria-controls="select2-id\_turma-container"><span class="select2-selection\_\_rendered" id="select2-id\_turma-container" role="textbox" aria-readonly="true" title="---------">---------</span><span class="select2-selection\_\_arrow" role="presentation"><b role="presentation"></b></span></span></span><span class="dropdown-wrapper" aria-hidden="true"></span></span><span class="select2 select2-container select2-container--bootstrap4" dir="ltr" data-select2-id="select2-data-11-5b8y" style="width: 100%;"><span class="selection"><span class="select2-selection select2-selection--single" role="combobox" aria-haspopup="true" aria-expanded="false" tabindex="0" aria-disabled="false" aria-labelledby="select2-1fxj-container" aria-controls="select2-1fxj-container"><span class="select2-selection\_\_rendered" id="select2-1fxj-container" role="textbox" aria-readonly="true"></span><span class="select2-selection\_\_arrow" role="presentation"><b role="presentation"></b></span></span></span><span class="dropdown-wrapper" aria-hidden="true"></span></span>





`                        `</div>



`                        `<div class="row">

`                            `<div class="col-md-6">

`                                `<div class="mb-3">

`                                    `<label for="id\_mes" class="form-label">Mês</label>

`                                    `<select name="mes" class="form-control" required="" id="id\_mes">

`  `<option value="" selected="">---------</option>

`  `<option value="1">Janeiro</option>

`  `<option value="2">Fevereiro</option>

`  `<option value="3">Março</option>

`  `<option value="4">Abril</option>

`  `<option value="5">Maio</option>

`  `<option value="6">Junho</option>

`  `<option value="7">Julho</option>

`  `<option value="8">Agosto</option>

`  `<option value="9">Setembro</option>

`  `<option value="10">Outubro</option>

`  `<option value="11">Novembro</option>

`  `<option value="12">Dezembro</option>

</select>





`                                `</div>

`                            `</div>

`                            `<div class="col-md-6">

`                                `<div class="mb-3">

`                                    `<label for="id\_ano" class="form-label">Ano</label>

`                                    `<input type="number" name="ano" value="2025" class="form-control" min="2000" max="2100" required="" id="id\_ano">





`                                `</div>

`                            `</div>

`                        `</div>



`                        `<div class="mb-3">

`                            `<label for="id\_percentual\_minimo" class="form-label">

`                                `Percentual Mínimo (%)

`                            `</label>

`                            `<div class="input-group">

`                                `<input type="number" name="percentual\_minimo" value="75" class="form-control" min="0" max="100" required="" id="id\_percentual\_minimo">

`                                `<span class="input-group-text">%</span>

`                            `</div>





`                        `</div>



`                        `<div class="d-flex justify-content-between mt-4">

`                            `<a href="/frequencias/" class="btn btn-secondary">

`                                `<i class="fas fa-arrow-left"></i> Voltar

`                            `</a>

`                            `<button type="submit" class="btn btn-primary">

`                                `<i class="fas fa-save"></i> Salvar

`                            `</button>

`                        `</div>

`                    `</form>

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



<script>

`    `document.addEventListener('DOMContentLoaded', function() {

`        `// Inicializar Select2 para melhorar a experiência de seleção

`        `$('.select2').select2({

`            `theme: 'bootstrap-5',

`            `width: '100%'

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

<div id="djDebug" class="" dir="ltr" data-store-id="4719c1da23bb49a2b07ab2e26b8b5048" data-render-panel-url="/\_\_debug\_\_/render\_panel/" data-sidebar-url="/\_\_debug\_\_/history\_sidebar/" data-default-show="true" data-update-on-fetch="False" data-theme="auto">

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





`      `<br><small>/frequencias/criar/</small>







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





`      `<br><small>Total: 448.20ms</small>







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





`      `<br><small>criar\_frequencia\_mensal</small>







`    `</a>



</li>





<li id="djdt-SQLPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSQLPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="SQL queries from 1 connection" class="SQLPanel">



`  `SQL





`      `<br><small>7 queries in 70.06ms</small>







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





`      `<br><small>frequencias/formulario\_frequencia\_mensal.html</small>







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

`                                `<a class="nav-link active" href="/frequencias/">

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

`                                            `<input type="hidden" name="csrfmiddlewaretoken" value="jc8PV8tEcqBmI5knIn8C7qP5od7vZsOBIcVCxGt1wOAh5JyXJVDhGo1buow6ezfi">

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

`  `<div class="d-flex justify-content-between align-items-center mb-3">

`      `<h1>Relatório de Frequências</h1>

`      `<div class="btn-group">

`          `<a href="/frequencias/" class="btn btn-secondary">

`              `<i class="fas fa-arrow-left"></i> Voltar

`          `</a>

`          `<button id="btn-imprimir" class="btn btn-primary">

`              `<i class="fas fa-print"></i> Imprimir

`          `</button>

`          `<button id="btn-exportar-pdf" class="btn btn-danger">

`              `<i class="fas fa-file-pdf"></i> Exportar PDF

`          `</button>

`          `<button id="btn-exportar-excel" class="btn btn-success">

`              `<i class="fas fa-file-excel"></i> Exportar Excel

`          `</button>

`      `</div>

`  `</div>



`  `<!-- Filtros -->

`  `<div class="card mb-4 no-print">

`      `<div class="card-header bg-light">

`          `<h5 class="mb-0">Filtros</h5>

`      `</div>

`      `<div class="card-body">

`          `<form method="get" class="row g-3">

`              `<div class="col-md-3">

`                  `<label for="turma" class="form-label">Turma</label>

`                  `<select name="turma" id="turma" class="form-select select2 select2-hidden-accessible" data-select2-id="select2-data-turma" tabindex="-1" aria-hidden="true">

`                      `<option value="" data-select2-id="select2-data-2-87kg">Todas as turmas</option>



`                  `</select><span class="select2 select2-container select2-container--bootstrap4 select2-hidden-accessible" dir="ltr" data-select2-id="select2-data-1-ifmf" style="width: 100%;" tabindex="-1" aria-hidden="true"><span class="selection"><span class="select2-selection select2-selection--single" role="combobox" aria-haspopup="true" aria-expanded="false" tabindex="0" aria-disabled="false" aria-labelledby="select2-turma-container" aria-controls="select2-turma-container"><span class="select2-selection\_\_rendered" id="select2-turma-container" role="textbox" aria-readonly="true" title="Todas as turmas">Todas as turmas</span><span class="select2-selection\_\_arrow" role="presentation"><b role="presentation"></b></span></span></span><span class="dropdown-wrapper" aria-hidden="true"></span></span><span class="select2 select2-container select2-container--bootstrap4" dir="ltr" data-select2-id="select2-data-3-if02" style="width: 100%;"><span class="selection"><span class="select2-selection select2-selection--single" role="combobox" aria-haspopup="true" aria-expanded="false" tabindex="0" aria-disabled="false" aria-labelledby="select2-09or-container" aria-controls="select2-09or-container"><span class="select2-selection\_\_rendered" id="select2-09or-container" role="textbox" aria-readonly="true"></span><span class="select2-selection\_\_arrow" role="presentation"><b role="presentation"></b></span></span></span><span class="dropdown-wrapper" aria-hidden="true"></span></span>

`              `</div>

`              `<div class="col-md-2">

`                  `<label for="mes" class="form-label">Mês</label>

`                  `<select name="mes" id="mes" class="form-select">

`                      `<option value="">Todos os meses</option>



`                  `</select>

`              `</div>

`              `<div class="col-md-2">

`                  `<label for="ano" class="form-label">Ano</label>

`                  `<select name="ano" id="ano" class="form-select">

`                      `<option value="">Todos os anos</option>



`                  `</select>

`              `</div>

`              `<div class="col-md-3">

`                  `<label for="status" class="form-label">Status da Carência</label>

`                  `<select name="status" id="status" class="form-select">

`                      `<option value="">Todos os status</option>

`                      `<option value="PENDENTE">Pendente</option>

`                      `<option value="EM\_ACOMPANHAMENTO">Em Acompanhamento</option>

`                      `<option value="RESOLVIDO">Resolvido</option>

`                  `</select>

`              `</div>

`              `<div class="col-12 mt-3">

`                  `<button type="submit" class="btn btn-primary">

`                      `<i class="fas fa-filter"></i> Filtrar

`                  `</button>

`                  `<a href="/frequencias/relatorio/" class="btn btn-secondary">

`                      `<i class="fas fa-broom"></i> Limpar Filtros

`                  `</a>

`              `</div>

`          `</form>

`      `</div>

`  `</div>



`  `<!-- Cabeçalho do relatório -->

`  `<div class="card mb-4">

`      `<div class="card-body">

`          `<div class="d-flex justify-content-between align-items-center">

`              `<div>

`                  `<h2 class="mb-1">Relatório de Frequências</h2>

`                  `<p class="text-muted mb-0">Gerado em: </p>

`              `</div>

`              `<div class="text-end">

`                  `<h5>Filtros aplicados:</h5>

`                  `<p class="mb-0">

`                      `Turma: Todas |

`                      `Período: Todos os meses/Todos os anos |

`                      `Status: Todos

`                  `</p>

`              `</div>

`          `</div>

`      `</div>

`  `</div>



`  `<!-- Resumo estatístico -->

`  `<div class="card mb-4">

`      `<div class="card-header bg-light">

`          `<h5 class="mb-0">Resumo Estatístico</h5>

`      `</div>

`      `<div class="card-body">

`          `<div class="row">

`              `<div class="col-md-3">

`                  `<div class="card text-center mb-3">

`                      `<div class="card-body">

`                          `<h5 class="card-title">Total de Frequências</h5>

`                          `<p class="card-text display-4">0</p>

`                      `</div>

`                  `</div>

`              `</div>

`              `<div class="col-md-3">

`                  `<div class="card text-center mb-3">

`                      `<div class="card-body">

`                          `<h5 class="card-title">Total de Carências</h5>

`                          `<p class="card-text display-4">0</p>

`                      `</div>

`                  `</div>

`              `</div>

`              `<div class="col-md-3">

`                  `<div class="card text-center mb-3">

`                      `<div class="card-body">

`                          `<h5 class="card-title">Carências Pendentes</h5>

`                          `<p class="card-text display-4"></p>

`                      `</div>

`                  `</div>

`              `</div>

`              `<div class="col-md-3">

`                  `<div class="card text-center mb-3">

`                      `<div class="card-body">

`                          `<h5 class="card-title">Carências Resolvidas</h5>

`                          `<p class="card-text display-4"></p>

`                      `</div>

`                  `</div>

`              `</div>

`          `</div>

`      `</div>

`  `</div>



`  `<!-- Tabela de carências -->

`  `<div class="card mb-4">

`      `<div class="card-header bg-light">

`          `<h5 class="mb-0">Lista de Carências</h5>

`      `</div>

`      `<div class="card-body">

`          `<div class="table-responsive">

`              `<table class="table table-striped table-hover">

`                  `<thead class="table-dark">

`                      `<tr>

`                          `<th>Aluno</th>

`                          `<th>Turma</th>

`                          `<th>Período</th>

`                          `<th>Percentual</th>

`                          `<th>Status</th>

`                          `<th>Data de Resolução</th>

`                          `<th>Observações</th>

`                      `</tr>

`                  `</thead>

`                  `<tbody>



`                      `<tr>

`                          `<td colspan="7" class="text-center py-4">

`                              `<div class="alert alert-info mb-0">

`                                  `Nenhuma carência encontrada com os filtros selecionados.

`                              `</div>

`                          `</td>

`                      `</tr>



`                  `</tbody>

`              `</table>

`          `</div>



`          `<!-- Paginação -->



`      `</div>

`      `<div class="card-footer">

`          `<div class="d-flex justify-content-between align-items-center">

`              `<span>Total:  carências</span>

`              `<span class="no-print">Página  de </span>

`          `</div>

`      `</div>

`  `</div>



`  `<!-- Gráfico de carências por turma -->

`  `<div class="card mb-4">

`      `<div class="card-header bg-light">

`          `<h5 class="mb-0">Carências por Turma</h5>

`      `</div>

`      `<div class="card-body">

`          `<canvas id="grafico-carencias-turma" height="300"></canvas>

`      `</div>

`  `</div>



`  `<!-- Gráfico de evolução mensal -->

`  `<div class="card mb-4">

`      `<div class="card-header bg-light">

`          `<h5 class="mb-0">Evolução Mensal de Carências</h5>

`      `</div>

`      `<div class="card-body">

`          `<canvas id="grafico-evolucao-mensal" height="300"></canvas>

`      `</div>

`  `</div>



`  `<!-- Rodapé do relatório -->

`  `<div class="card mb-4">

`      `<div class="card-body">

`          `<div class="d-flex justify-content-between align-items-center">

`              `<div>

`                  `<p class="mb-0">Relatório gerado em: </p>

`              `</div>

`              `<div>

`                  `<p class="mb-0">Sistema de Gestão Acadêmica - OMAUM</p>

`              `</div>

`          `</div>

`      `</div>

`  `</div>

</div>

<!-- Estilos para impressão -->

<style>

`    `@media print {

.no-print {

`            `display: none !important;

`        `}



.container-fluid {

`            `width: 100%;

`            `padding: 0;

`            `margin: 0;

`        `}



.card {

`            `border: none !important;

`            `margin-bottom: 20px !important;

`        `}



.card-header {

`            `background-color: #f8f9fa !important;

`            `color: #000 !important;

`            `border-bottom: 1px solid #dee2e6 !important;

`        `}



.table {

`            `width: 100% !important;

`            `border-collapse: collapse !important;

`        `}



.table th, .table td {

`            `border: 1px solid #dee2e6 !important;

`            `padding: 8px !important;

`        `}



.table thead th {

`            `background-color: #f8f9fa !important;

`            `color: #000 !important;

`            `border-bottom: 2px solid #dee2e6 !important;

`        `}



.badge {

`            `border: 1px solid #000 !important;

`            `padding: 3px 6px !important;

`        `}



.badge-danger {

`            `background-color: #fff !important;

`            `color: #000 !important;

`            `border: 1px solid #dc3545 !important;

`        `}



.badge-warning {

`            `background-color: #fff !important;

`            `color: #000 !important;

`            `border: 1px solid #ffc107 !important;

`        `}



.badge-success {

`            `background-color: #fff !important;

`            `color: #000 !important;

`            `border: 1px solid #28a745 !important;

`        `}



.progress {

`            `border: 1px solid #dee2e6 !important;

`            `background-color: #f8f9fa !important;

`        `}



.progress-bar {

`            `background-color: #6c757d !important;

`            `color: #fff !important;

`        `}

`    `}

</style>

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

<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>

<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>

<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>

<script>

`    `document.addEventListener('DOMContentLoaded', function() {

`        `// Inicializar Select2 para melhorar a experiência de seleção

`        `$('.select2').select2({

`            `theme: 'bootstrap-5',

`            `width: '100%'

`        `});



`        `// Gráfico de carências por turma

`        `const ctxCarenciasTurma = document.getElementById('grafico-carencias-turma').getContext('2d');

`        `new Chart(ctxCarenciasTurma, {

`            `type: 'bar',

`            `data: {

`                `labels: ,

`                `datasets: [

`                    `{

`                        `label: 'Pendentes',

`                        `data: ,

`                        `backgroundColor: 'rgba(220, 53, 69, 0.7)',

`                        `borderColor: 'rgba(220, 53, 69, 1)',

`                        `borderWidth: 1

`                    `},

`                    `{

`                        `label: 'Em Acompanhamento',

`                        `data: ,

`                        `backgroundColor: 'rgba(255, 193, 7, 0.7)',

`                        `borderColor: 'rgba(255, 193, 7, 1)',

`                        `borderWidth: 1

`                    `},

`                    `{

`                        `label: 'Resolvidas',

`                        `data: ,

`                        `backgroundColor: 'rgba(40, 167, 69, 0.7)',

`                        `borderColor: 'rgba(40, 167, 69, 1)',

`                        `borderWidth: 1

`                    `}

`                `]

`            `},

`            `options: {

`                `responsive: true,

`                `plugins: {

`                    `legend: {

`                        `position: 'bottom'

`                    `}

`                `},

`                `scales: {

`                    `y: {

`                        `beginAtZero: true,

`                        `stacked: true

`                    `},

`                    `x: {

`                        `stacked: true

`                    `}

`                `}

`            `}

`        `});



`        `// Gráfico de evolução mensal

`        `const ctxEvolucaoMensal = document.getElementById('grafico-evolucao-mensal').getContext('2d');

`        `new Chart(ctxEvolucaoMensal, {

`            `type: 'line',

`            `data: {

`                `labels: ,

`                `datasets: [

`                    `{

`                        `label: 'Novas Carências',

`                        `data: ,

`                        `borderColor: 'rgba(220, 53, 69, 1)',

`                        `backgroundColor: 'rgba(220, 53, 69, 0.1)',

`                        `fill: true,

`                        `tension: 0.3

`                    `},

`                    `{

`                        `label: 'Carências Resolvidas',

`                        `data: ,

`                        `borderColor: 'rgba(40, 167, 69, 1)',

`                        `backgroundColor: 'rgba(40, 167, 69, 0.1)',

`                        `fill: true,

`                        `tension: 0.3

`                    `}

`                `]

`            `},

`            `options: {

`                `responsive: true,

`                `plugins: {

`                    `legend: {

`                        `position: 'bottom'

`                    `}

`                `},

`                `scales: {

`                    `y: {

`                        `beginAtZero: true

`                    `}

`                `}

`            `}

`        `});



`        `// Botão de impressão

`        `document.getElementById('btn-imprimir').addEventListener('click', function() {

`            `window.print();

`        `});



`        `// Botão de exportar para PDF

`        `document.getElementById('btn-exportar-pdf').addEventListener('click', function() {

`            `const { jsPDF } = window.jspdf;

`            `const doc = new jsPDF('p', 'mm', 'a4');



`            `// Título do documento

`            `doc.setFontSize(18);

`            `doc.text('Relatório de Frequências', 105, 15, { align: 'center' });



`            `// Data de geração

`            `doc.setFontSize(10);

`            `doc.text('Gerado em: ', 105, 22, { align: 'center' });



`            `// Filtros aplicados

`            `doc.setFontSize(12);

`            `doc.text('Filtros: Todas as turmas | Todos os meses/Todos os anos | Todos os status', 105, 30, { align: 'center' });



`            `// Resumo estatístico

`            `doc.setFontSize(14);

`            `doc.text('Resumo Estatístico', 14, 40);



`            `doc.setFontSize(12);

`            `doc.text('Total de Frequências: 0', 14, 50);

`            `doc.text('Total de Carências: 0', 14, 58);

`            `doc.text('Carências Pendentes: ', 14, 66);

`            `doc.text('Carências Resolvidas: ', 14, 74);



`            `// Capturar gráficos

`            `html2canvas(document.getElementById('grafico-carencias-turma')).then(function(canvas) {

`                `const imgData = canvas.toDataURL('image/png');

`                `doc.addPage();

`                `doc.text('Carências por Turma', 105, 15, { align: 'center' });

`                `doc.addImage(imgData, 'PNG', 10, 30, 190, 100);



`                `html2canvas(document.getElementById('grafico-evolucao-mensal')).then(function(canvas) {

`                    `const imgData = canvas.toDataURL('image/png');

`                    `doc.addPage();

`                    `doc.text('Evolução Mensal de Carências', 105, 15, { align: 'center' });

`                    `doc.addImage(imgData, 'PNG', 10, 30, 190, 100);



`                    `// Salvar o PDF

`                    `doc.save('relatorio-frequencias.pdf');

`                `});

`            `});

`        `});



`        `// Botão de exportar para Excel

`        `document.getElementById('btn-exportar-excel').addEventListener('click', function() {

`            `// Preparar dados para o Excel

`            `const dados = [

`                `['Relatório de Frequências - '],

`                `['Filtros: Todas as turmas | Todos os meses/Todos os anos | Todos os status'],

`                `[''],

`                `['Resumo Estatístico'],

`                `['Total de Frequências', '0'],

`                `['Total de Carências', '0'],

`                `['Carências Pendentes', ''],

`                `['Carências Resolvidas', ''],

`                `[''],

`                `['Lista de Carências'],

`                `['Aluno', 'CPF', 'Turma', 'Período', 'Percentual', 'Status', 'Data de Resolução', 'Observações']

`            `];



`            `// Adicionar dados das carências





`            `// Criar planilha

`            `const ws = XLSX.utils.aoa\_to\_sheet(dados);

`            `const wb = XLSX.utils.book\_new();

`            `XLSX.utils.book\_append\_sheet(wb, ws, "Relatório de Frequências");



`            `// Ajustar largura das colunas

`            `const wscols = [

`                `{wch: 30}, // Aluno

`                `{wch: 15}, // CPF

`                `{wch: 25}, // Turma

`                `{wch: 15}, // Período

`                `{wch: 12}, // Percentual

`                `{wch: 20}, // Status

`                `{wch: 15}, // Data de Resolução

`                `{wch: 40}  // Observações

`            `];

`            `ws['!cols'] = wscols;



`            `// Salvar arquivo

`            `XLSX.writeFile(wb, "relatorio-frequencias.xlsx");

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

<div id="djDebug" class="" dir="ltr" data-store-id="d149c124d5d74d049b887b7f4d701b90" data-render-panel-url="/\_\_debug\_\_/render\_panel/" data-sidebar-url="/\_\_debug\_\_/history\_sidebar/" data-default-show="true" data-update-on-fetch="False" data-theme="auto">

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





`      `<br><small>/frequencias/relatorio/</small>







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





`      `<br><small>Total: 184.41ms</small>







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





`      `<br><small>relatorio\_frequencias</small>







`    `</a>



</li>





<li id="djdt-SQLPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSQLPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="SQL queries from 1 connection" class="SQLPanel">



`  `SQL





`      `<br><small>6 queries in 5.73ms</small>







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





`      `<br><small>frequencias/relatorio\_frequencias.html</small>







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
