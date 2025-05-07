<main id="main-content" class="py-4">



<div class="container mt-4">

`    `<!-- Cabeçalho com título e botões na mesma linha -->

`    `<div class="d-flex justify-content-between align-items-center mb-3">

`        `<h1>Lista de Turmas</h1>

`        `<div>

`            `<a href="javascript:history.back()" class="btn btn-secondary me-2">Voltar</a>

`            `<a href="/turmas/criar/" class="btn btn-primary">Nova Turma</a>

`        `</div>

`    `</div>



`    `<!-- Barra de busca e filtros -->

`    `<div class="card mb-4">

`        `<div class="card-header">

`            `<form method="get" class="row g-3">

`                `<div class="col-md-6">

`                    `<input type="text" name="q" class="form-control" placeholder="Buscar por nome, curso ou instrutor..." value="">

`                `</div>

`                `<div class="col-md-4">

`                    `<select name="curso" class="form-select" title="Selecione um curso" aria-label="Selecione um curso">

`                        `<option value="">Todos os cursos</option>



`                            `<option value="35">Básico do Básico</option>



`                            `<option value="999">Curso Teste</option>



`                            `<option value="104">Filosofia Oriental</option>



`                            `<option value="101">Introdução à Meditação</option>



`                            `<option value="102">Meditação Avançada</option>



`                            `<option value="105">Práticas de Mindfulness</option>



`                            `<option value="103">Yoga para Iniciantes</option>



`                    `</select>

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

`                            `<th>Curso</th>

`                            `<th>Nome da Turma</th>

`                            `<th>Instrutor</th>

`                            `<th>Status</th>

`                            `<th>Data Início</th>

`                            `<th>Ações</th>

`                        `</tr>

`                    `</thead>

`                    `<tbody>



`                            `<tr>

`                                `<td>Introdução à Meditação</td>

`                                `<td>A</td>

`                                `<td>Não definido</td>

`                                `<td>

`                                    `<span class="badge bg-success">

`                                        `Ativa

`                                    `</span>

`                                `</td>

`                                `<td>26/10/2024</td>

`                                `<td>

`                                    `<a href="/turmas/2/" class="btn btn-sm btn-info" title="Ver detalhes completos da turma">Detalhes</a>

`                                    `<a href="/turmas/2/editar/" class="btn btn-sm btn-warning" title="Editar informações da turma">Editar</a>

`                                    `<a href="/turmas/2/excluir/" class="btn btn-sm btn-danger" title="Excluir esta turma">Excluir</a>

`                                `</td>

`                            `</tr>



`                            `<tr>

`                                `<td>Introdução à Meditação</td>

`                                `<td>B</td>

`                                `<td>Não definido</td>

`                                `<td>

`                                    `<span class="badge bg-success">

`                                        `Ativa

`                                    `</span>

`                                `</td>

`                                `<td>26/10/2024</td>

`                                `<td>

`                                    `<a href="/turmas/4/" class="btn btn-sm btn-info" title="Ver detalhes completos da turma">Detalhes</a>

`                                    `<a href="/turmas/4/editar/" class="btn btn-sm btn-warning" title="Editar informações da turma">Editar</a>

`                                    `<a href="/turmas/4/excluir/" class="btn btn-sm btn-danger" title="Excluir esta turma">Excluir</a>

`                                `</td>

`                            `</tr>



`                            `<tr>

`                                `<td>Introdução à Meditação</td>

`                                `<td>C</td>

`                                `<td>Não definido</td>

`                                `<td>

`                                    `<span class="badge bg-success">

`                                        `Ativa

`                                    `</span>

`                                `</td>

`                                `<td>26/10/2024</td>

`                                `<td>

`                                    `<a href="/turmas/5/" class="btn btn-sm btn-info" title="Ver detalhes completos da turma">Detalhes</a>

`                                    `<a href="/turmas/5/editar/" class="btn btn-sm btn-warning" title="Editar informações da turma">Editar</a>

`                                    `<a href="/turmas/5/excluir/" class="btn btn-sm btn-danger" title="Excluir esta turma">Excluir</a>

`                                `</td>

`                            `</tr>



`                            `<tr>

`                                `<td>Introdução à Meditação</td>

`                                `<td>D</td>

`                                `<td>Aline Souza</td>

`                                `<td>

`                                    `<span class="badge bg-success">

`                                        `Ativa

`                                    `</span>

`                                `</td>

`                                `<td>24/04/2025</td>

`                                `<td>

`                                    `<a href="/turmas/6/" class="btn btn-sm btn-info" title="Ver detalhes completos da turma">Detalhes</a>

`                                    `<a href="/turmas/6/editar/" class="btn btn-sm btn-warning" title="Editar informações da turma">Editar</a>

`                                    `<a href="/turmas/6/excluir/" class="btn btn-sm btn-danger" title="Excluir esta turma">Excluir</a>

`                                `</td>

`                            `</tr>



`                    `</tbody>

`                `</table>

`            `</div>

`        `</div>

`        `<div class="card-footer">

`            `<p class="text-muted mb-0">Total: 4 turma(s)</p>



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

`                                `<a class="nav-link active" href="/turmas/">

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

`                                            `<input type="hidden" name="csrfmiddlewaretoken" value="jmrCxoxvLzlUsAezf21s9FzlNlC3SvL6Imep9WxS5XkPPes9gAw7IDLrTw1E7CcN">

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

`        `<h1>Nova Turma</h1>

`        `<a href="/turmas/" class="btn btn-secondary">Voltar para a lista</a>

`    `</div>







`    `<form method="post">

`        `<input type="hidden" name="csrfmiddlewaretoken" value="jmrCxoxvLzlUsAezf21s9FzlNlC3SvL6Imep9WxS5XkPPes9gAw7IDLrTw1E7CcN">





`        `<div class="card mb-4">

`            `<div class="card-header bg-primary text-white">

`                `<h5>Informações Básicas</h5>

`            `</div>

`            `<div class="card-body">

`                `<div class="row">

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_nome" class="form-label">Nome da Turma</label>

`    `<input type="text" name="nome" class="form-control" maxlength="100" required="" aria-describedby="id\_nome\_helptext" id="id\_nome">





`        `<small class="form-text text-muted">Digite um nome descritivo para a turma.</small>



</div>

`                    `</div>

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_curso" class="form-label">Curso</label>

`    `<select name="curso" class="form-select" required="" id="id\_curso">

`  `<option value="" selected="">---------</option>

`  `<option value="35">35 - Básico do Básico</option>

`  `<option value="101">101 - Introdução à Meditação</option>

`  `<option value="102">102 - Meditação Avançada</option>

`  `<option value="103">103 - Yoga para Iniciantes</option>

`  `<option value="104">104 - Filosofia Oriental</option>

`  `<option value="105">105 - Práticas de Mindfulness</option>

`  `<option value="999">999 - Curso Teste</option>

</select>





</div>

`                    `</div>

`                `</div>

`                `<div class="row">

`                    `<div class="col-md-4">

`                        `<div class="mb-3">

`    `<label for="id\_vagas" class="form-label">Número de Vagas</label>

`    `<input type="number" name="vagas" value="20" class="form-control" min="0" required="" aria-describedby="id\_vagas\_helptext" id="id\_vagas">





`        `<small class="form-text text-muted">Quantidade máxima de alunos na turma.</small>



</div>

`                    `</div>

`                    `<div class="col-md-4">

`                        `<div class="mb-3">

`    `<label for="id\_status" class="form-label">Status</label>

`    `<select name="status" class="form-select" aria-describedby="id\_status\_helptext" id="id\_status">

`  `<option value="A" selected="">Ativa</option>

`  `<option value="I">Inativa</option>

`  `<option value="C">Cancelada</option>

`  `<option value="F">Finalizada</option>

</select>





`        `<small class="form-text text-muted">Situação atual da turma.</small>



</div>

`                    `</div>

`                    `<div class="col-md-4">

`                        `<div class="mb-3">

`    `<label for="id\_dias\_semana" class="form-label">Dias da Semana</label>

`    `<input type="text" name="dias\_semana" class="form-control" maxlength="100" aria-describedby="id\_dias\_semana\_helptext" id="id\_dias\_semana">





`        `<small class="form-text text-muted">Exemplo: 'Segunda, Quarta e Sexta' ou 'Terças e Quintas'.</small>



</div>

`                    `</div>

`                `</div>

`                `<div class="row">

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_data\_inicio" class="form-label">Data de Início</label>

`    `<input type="date" name="data\_inicio" class="form-control" required="" aria-describedby="id\_data\_inicio\_helptext" id="id\_data\_inicio">





`        `<small class="form-text text-muted">Data prevista para início do curso.</small>



</div>

`                    `</div>

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_data\_fim" class="form-label">Data de Término</label>

`    `<input type="date" name="data\_fim" class="form-control" required="" aria-describedby="id\_data\_fim\_helptext" id="id\_data\_fim">





`        `<small class="form-text text-muted">Data prevista para término do curso.</small>



</div>

`                    `</div>

`                `</div>

`                `<div class="row">

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_local" class="form-label">Local</label>

`    `<input type="text" name="local" class="form-control" maxlength="200" id="id\_local">





</div>

`                    `</div>

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_horario" class="form-label">Horário</label>

`    `<input type="text" name="horario" class="form-control" maxlength="100" aria-describedby="id\_horario\_helptext" id="id\_horario">





`        `<small class="form-text text-muted">Exemplo: '19h às 21h'.</small>



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

`            `<div class="card-header bg-success text-white">

`                `<h5>Instrutores</h5>

`            `</div>

`            `<div class="card-body">

`                `<div class="row">

`                    `<!-- Instrutor Principal -->

`                    `<div class="col-md-4 mb-3">

`                        `<label for="search-instrutor" class="form-label">Instrutor Principal</label>

`                        `<input type="text" id="search-instrutor" class="form-control" placeholder="Digite parte do CPF, nome ou número iniciático..." autocomplete="off">

`                        `<div id="search-results-instrutor" class="list-group mt-2" style="display: none"></div>

`                        `<div id="selected-instrutor-container" class="p-3 border rounded mt-2 d-none">

`                            `<div id="selected-instrutor-info">

`                                `Nenhum instrutor selecionado

`                            `</div>

`                        `</div><button id="clear-instrutor-btn" type="button" class="btn btn-sm btn-outline-secondary mt-2" style="display: none;">Limpar seleção</button>

`                        `<div id="instrutor-error" class="alert alert-warning mt-2 d-none"></div>

`                        `<!-- Campo original oculto via CSS -->

`                        `<select name="instrutor" class="form-control" id="id\_instrutor">

`  `<option value="" selected="">---------</option>

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

</select>

`                    `</div>



`                    `<!-- Instrutor Auxiliar -->

`                    `<div class="col-md-4 mb-3">

`                        `<label for="search-instrutor-auxiliar" class="form-label">Instrutor Auxiliar</label>

`                        `<input type="text" id="search-instrutor-auxiliar" class="form-control" placeholder="Digite parte do CPF, nome ou número iniciático..." autocomplete="off">

`                        `<div id="search-results-instrutor-auxiliar" class="list-group mt-2" style="display: none;"></div>

`                        `<div id="selected-instrutor-auxiliar-container" class="p-3 border rounded mt-2 d-none">

`                            `<div id="selected-instrutor-auxiliar-info">

`                                `Nenhum instrutor auxiliar selecionado

`                            `</div>

`                        `</div><button id="clear-instrutor-auxiliar-btn" type="button" class="btn btn-sm btn-outline-secondary mt-2" style="display: none;">Limpar seleção</button>

`                        `<div id="instrutor-auxiliar-error" class="alert alert-warning mt-2 d-none"></div>

`                        `<!-- Campo original oculto via CSS -->

`                        `<select name="instrutor\_auxiliar" class="form-control" id="id\_instrutor\_auxiliar">

`  `<option value="" selected="">---------</option>

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

</select>

`                    `</div>



`                    `<!-- Auxiliar de Instrução -->

`                    `<div class="col-md-4 mb-3">

`                        `<label for="search-auxiliar-instrucao" class="form-label">Auxiliar de Instrução</label>

`                        `<input type="text" id="search-auxiliar-instrucao" class="form-control" placeholder="Digite parte do CPF, nome ou número iniciático..." autocomplete="off">

`                        `<div id="search-results-auxiliar-instrucao" class="list-group mt-2" style="display: none;"></div>

`                        `<div id="selected-auxiliar-instrucao-container" class="p-3 border rounded mt-2 d-none">

`                            `<div id="selected-auxiliar-instrucao-info">

`                                `Nenhum auxiliar de instrução selecionado

`                            `</div>

`                        `</div><button id="clear-auxiliar-instrucao-btn" type="button" class="btn btn-sm btn-outline-secondary mt-2" style="display: none;">Limpar seleção</button>

`                        `<div id="auxiliar-instrucao-error" class="alert alert-warning mt-2 d-none"></div>

`                        `<!-- Campo original oculto via CSS -->

`                        `<select name="auxiliar\_instrucao" class="form-control" id="id\_auxiliar\_instrucao">

`  `<option value="" selected="">---------</option>

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

</select>

`                    `</div>

`                `</div>

`                `<div class="alert alert-info">

`                    `<i class="fas fa-info-circle"></i> Você pode selecionar qualquer aluno como instrutor.

`                    `O sistema verificará a elegibilidade e mostrará um aviso caso o aluno não atenda aos requisitos.

`                `</div>

`            `</div>

`        `</div>



`        `<div class="d-flex justify-content-between mb-5">

`            `<a href="/turmas/" class="btn btn-secondary">Cancelar</a>

`            `<button type="submit" class="btn btn-primary">Criar Turma</button>

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



<script src="/static/js/instrutor\_search.js"></script>



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

<div id="djDebug" class="" dir="ltr" data-store-id="fcc7d0ddebfb4ebeb4b50f62ffee8546" data-render-panel-url="/\_\_debug\_\_/render\_panel/" data-sidebar-url="/\_\_debug\_\_/history\_sidebar/" data-default-show="true" data-update-on-fetch="False" data-theme="auto">

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





`      `<br><small>/turmas/criar/</small>







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





`      `<br><small>Total: 393.38ms</small>







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





`      `<br><small>criar\_turma</small>







`    `</a>



</li>





<li id="djdt-SQLPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSQLPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="SQL queries from 1 connection" class="SQLPanel">



`  `SQL





`      `<br><small>6 queries in 9.34ms</small>







`    `</a>



</li>





<li id="djdt-StaticFilesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtStaticFilesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Arquivos estáticos (154 encontrados, 7 sendo utilizados)" class="StaticFilesPanel">



`  `Arquivos estáticos





`      `<br><small>7 arquivos utilizados</small>







`    `</a>



</li>





<li id="djdt-TemplatesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtTemplatesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Templates (13 renderizados)" class="TemplatesPanel">



`  `Templates





`      `<br><small>turmas/criar\_turma.html</small>







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

`      `<h3>Arquivos estáticos (154 encontrados, 7 sendo utilizados)</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="TemplatesPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Templates (13 renderizados)</h3>

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

`                                `<a class="nav-link active" href="/turmas/">

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

`                                            `<input type="hidden" name="csrfmiddlewaretoken" value="hAmnQx8HhFivnAIWTm5YuNFVSkeRW2CGGA9as584B3hqKeWwUUAD3LR1YvDsb93n">

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

`    `<!-- Cabeçalho com título e botões de ação -->

`    `<div class="d-flex justify-content-between align-items-center mb-4">

`        `<h1>Detalhes da Turma: A</h1>

`        `<div>

`            `<a href="/turmas/" class="btn btn-secondary me-2">

`                `<i class="fas fa-arrow-left"></i> Voltar

`            `</a>

`            `<a href="/turmas/2/editar/" class="btn btn-warning me-2">

`                `<i class="fas fa-edit"></i> Editar

`            `</a>



`        `</div>

`    `</div>





`    `<div class="alert alert-danger text-center mb-4 blink">

`        `<h5 class="mb-0"><strong>Pendência na Instrutoria</strong></h5>

`    `</div>





`    `<!-- Card de informações da turma com layout em colunas -->

`    `<div class="card mb-4 border-primary">

`        `<div class="card-header bg-primary text-white">

`            `<h5 class="card-title mb-0">Informações da Turma</h5>

`        `</div>

`        `<div class="card-body">

`            `<div class="row">

`                `<!-- Coluna 1 -->

`                `<div class="col-md-4">

`                    `<div class="mb-3">

`                        `<h6 class="text-muted">Curso</h6>

`                        `<p class="fs-5">101 - Introdução à Meditação</p>

`                    `</div>

`                    `<div class="mb-3">

`                        `<h6 class="text-muted">Status</h6>

`                        `<p>



`                                `<span class="badge bg-success">Ativa</span>



`                        `</p>

`                    `</div>

`                `</div>



`                `<!-- Coluna 2 -->

`                `<div class="col-md-4">

`                    `<div class="mb-3">

`                        `<h6 class="text-muted">Data de Início</h6>

`                        `<p>26/10/2024</p>

`                    `</div>

`                    `<div class="mb-3">

`                        `<h6 class="text-muted">Data de Término</h6>

`                        `<p>26/10/2026</p>

`                    `</div>

`                    `<div class="mb-3">

`                        `<h6 class="text-muted">Local</h6>

`                        `<p>Não informado</p>

`                    `</div>

`                `</div>



`                `<!-- Coluna 3 - Estatísticas -->

`                `<div class="col-md-4">

`                    `<div class="card bg-light">

`                        `<div class="card-body text-center">

`                            `<h6 class="text-muted">Ocupação</h6>

`                            `<div class="d-flex justify-content-around mb-2">

`                                `<div>

`                                    `<h3 class="mb-0">5</h3>

`                                    `<small class="text-muted">Matriculados</small>

`                                `</div>

`                                `<div>

`                                    `<h3 class="mb-0">30</h3>

`                                    `<small class="text-muted">Total</small>

`                                `</div>

`                                `<div>

`                                    `<h3 class="mb-0">25</h3>

`                                    `<small class="text-muted">Disponíveis</small>

`                                `</div>

`                            `</div>



`                            `<!-- Barra de progresso -->

`                            `<div class="progress" style="height: 10px;">

`                                `<div class="progress-bar bg-primary" role="progressbar" style="width: 17%;" aria-valuenow="5" aria-valuemin="0" aria-valuemax="30">

`                                `</div>

`                            `</div>

`                            `<small class="text-muted">17% ocupado</small>

`                        `</div>

`                    `</div>

`                `</div>

`            `</div>



`            `<!-- Linha para Dias da Semana e Horário -->

`            `<div class="row mt-3">

`                `<div class="col-md-6">

`                    `<h6 class="text-muted">Dias da Semana</h6>

`                    `<p>Não informado</p>

`                `</div>

`                `<div class="col-md-6">

`                    `<h6 class="text-muted">Horário</h6>

`                    `<p>Não informado</p>

`                `</div>

`            `</div>



`            `<!-- Descrição em linha separada -->



`        `</div>

`    `</div>



`    `<!-- Card de instrutores -->

`    `<div class="card mb-4 border-success">

`        `<div class="card-header bg-success text-white">

`            `<h5 class="card-title mb-0">Instrutoria</h5>

`        `</div>

`        `<div class="card-body">

`            `<div class="row">

`                `<!-- Instrutor Principal -->

`                `<div class="col-md-4">

`                    `<div class="card h-100">

`                        `<div class="card-header bg-light">

`                            `<h6 class="mb-0">Instrutor Principal</h6>

`                        `</div>

`                        `<div class="card-body text-center">



`                                `<div class="text-muted py-4">

`                                    `<i class="fas fa-user-slash fa-3x mb-3"></i>

`                                    `<p>Nenhum instrutor designado</p>

`                                `</div>



`                        `</div>

`                    `</div>

`                `</div>



`                `<!-- Instrutor Auxiliar -->

`                `<div class="col-md-4">

`                    `<div class="card h-100">

`                        `<div class="card-header bg-light">

`                            `<h6 class="mb-0">Instrutor Auxiliar</h6>

`                        `</div>

`                        `<div class="card-body text-center">



`                                `<div class="text-muted py-4">

`                                    `<i class="fas fa-user-slash fa-3x mb-3"></i>

`                                    `<p>Nenhum instrutor designado</p>

`                                `</div>



`                        `</div>

`                    `</div>

`                `</div>



`                `<!-- Auxiliar de Instrução -->

`                `<div class="col-md-4">

`                    `<div class="card h-100">

`                        `<div class="card-header bg-light">

`                            `<h6 class="mb-0">Auxiliar de Instrução</h6>

`                        `</div>

`                        `<div class="card-body text-center">



`                                `<div class="text-muted py-4">

`                                    `<i class="fas fa-user-slash fa-3x mb-3"></i>

`                                    `<p>Nenhum auxiliar designado</p>

`                                `</div>



`                        `</div>

`                    `</div>

`                `</div>

`            `</div>

`        `</div>

`    `</div>



`    `<!-- Card de alunos matriculados -->

`    `<div class="card mb-4 border-primary">

`        `<div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">

`            `<h5 class="mb-0">Alunos Matriculados</h5>

`            `<a href="/turmas/2/matricular/" class="btn btn-light">

`                `<i class="fas fa-user-plus"></i> Matricular Aluno

`            `</a>

`        `</div>

`        `<div class="card-body">



`                `<div class="table-responsive">

`                    `<table class="table table-hover">

`                        `<thead class="table-light">

`                            `<tr>

`                                `<th>Nome</th>

`                                `<th>CPF</th>

`                                `<th>Nº Iniciático</th>

`                                `<th class="text-end">Ações</th>

`                            `</tr>

`                        `</thead>

`                        `<tbody>



`                            `<tr>

`                                `<td>

`                                    `<div class="d-flex align-items-center">

`                                        `<div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center me-2" style="width: 32px; height: 32px; font-size: 14px;">

`                                            `L

`                                        `</div>

`                                        `Lucas Araújo

`                                    `</div>

`                                `</td>

`                                `<td>30624167050</td>

`                                `<td>874M</td>

`                                `<td class="text-end">

`                                    `<a href="/alunos/30624167050/detalhes/" class="btn btn-sm btn-info">

`                                        `<i class="fas fa-eye"></i> Ver

`                                    `</a>

`                                    `<a href="/matriculas/turma/2/aluno/30624167050/cancelar/" class="btn btn-sm btn-danger" onclick="return confirm('Tem certeza que deseja cancelar esta matrícula?');">

`                                        `<i class="fas fa-times"></i> Cancelar

`                                    `</a>

`                                `</td>

`                            `</tr>



`                            `<tr>

`                                `<td>

`                                    `<div class="d-flex align-items-center">

`                                        `<div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center me-2" style="width: 32px; height: 32px; font-size: 14px;">

`                                            `F

`                                        `</div>

`                                        `Felipe Costa

`                                    `</div>

`                                `</td>

`                                `<td>37663960965</td>

`                                `<td>728C</td>

`                                `<td class="text-end">

`                                    `<a href="/alunos/37663960965/detalhes/" class="btn btn-sm btn-info">

`                                        `<i class="fas fa-eye"></i> Ver

`                                    `</a>

`                                    `<a href="/matriculas/turma/2/aluno/37663960965/cancelar/" class="btn btn-sm btn-danger" onclick="return confirm('Tem certeza que deseja cancelar esta matrícula?');">

`                                        `<i class="fas fa-times"></i> Cancelar

`                                    `</a>

`                                `</td>

`                            `</tr>



`                            `<tr>

`                                `<td>

`                                    `<div class="d-flex align-items-center">

`                                        `<div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center me-2" style="width: 32px; height: 32px; font-size: 14px;">

`                                            `A

`                                        `</div>

`                                        `Aline Souza

`                                    `</div>

`                                `</td>

`                                `<td>18027737038</td>

`                                `<td>608N</td>

`                                `<td class="text-end">

`                                    `<a href="/alunos/18027737038/detalhes/" class="btn btn-sm btn-info">

`                                        `<i class="fas fa-eye"></i> Ver

`                                    `</a>

`                                    `<a href="/matriculas/turma/2/aluno/18027737038/cancelar/" class="btn btn-sm btn-danger" onclick="return confirm('Tem certeza que deseja cancelar esta matrícula?');">

`                                        `<i class="fas fa-times"></i> Cancelar

`                                    `</a>

`                                `</td>

`                            `</tr>



`                            `<tr>

`                                `<td>

`                                    `<div class="d-flex align-items-center">

`                                        `<div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center me-2" style="width: 32px; height: 32px; font-size: 14px;">

`                                            `F

`                                        `</div>

`                                        `Felipe Souza

`                                    `</div>

`                                `</td>

`                                `<td>25185348461</td>

`                                `<td>715O</td>

`                                `<td class="text-end">

`                                    `<a href="/alunos/25185348461/detalhes/" class="btn btn-sm btn-info">

`                                        `<i class="fas fa-eye"></i> Ver

`                                    `</a>

`                                    `<a href="/matriculas/turma/2/aluno/25185348461/cancelar/" class="btn btn-sm btn-danger" onclick="return confirm('Tem certeza que deseja cancelar esta matrícula?');">

`                                        `<i class="fas fa-times"></i> Cancelar

`                                    `</a>

`                                `</td>

`                            `</tr>



`                            `<tr>

`                                `<td>

`                                    `<div class="d-flex align-items-center">

`                                        `<div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center me-2" style="width: 32px; height: 32px; font-size: 14px;">

`                                            `G

`                                        `</div>

`                                        `Gustavo Rocha

`                                    `</div>

`                                `</td>

`                                `<td>60795674660</td>

`                                `<td>775U</td>

`                                `<td class="text-end">

`                                    `<a href="/alunos/60795674660/detalhes/" class="btn btn-sm btn-info">

`                                        `<i class="fas fa-eye"></i> Ver

`                                    `</a>

`                                    `<a href="/matriculas/turma/2/aluno/60795674660/cancelar/" class="btn btn-sm btn-danger" onclick="return confirm('Tem certeza que deseja cancelar esta matrícula?');">

`                                        `<i class="fas fa-times"></i> Cancelar

`                                    `</a>

`                                `</td>

`                            `</tr>



`                        `</tbody>

`                    `</table>

`                `</div>



`        `</div>



`        `<div class="card-footer text-muted">

`            `<small>Total: 5 aluno(s)</small>

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

`    `// Adicione aqui qualquer JavaScript específico para esta página

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

<div id="djDebug" class="" dir="ltr" data-store-id="2563528697f3458b81f45930e4bb40e6" data-render-panel-url="/\_\_debug\_\_/render\_panel/" data-sidebar-url="/\_\_debug\_\_/history\_sidebar/" data-default-show="true" data-update-on-fetch="False" data-theme="auto">

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





`      `<br><small>/turmas/2/</small>







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





`      `<br><small>Total: 294.65ms</small>







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





`      `<br><small>detalhar\_turma</small>







`    `</a>



</li>





<li id="djdt-SQLPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSQLPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="SQL queries from 1 connection" class="SQLPanel">



`  `SQL





`      `<br><small>11 queries in 12.99ms</small>







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





`      `<br><small>turmas/detalhar\_turma.html</small>







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

`                                `<a class="nav-link active" href="/turmas/">

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

`                                            `<input type="hidden" name="csrfmiddlewaretoken" value="ANaPa4fumdK2uGk0gKm70vg20kFTvtykZNXCMCfRGBJXRkyAhiRMzts86v4uKAZ1">

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

`    `<h1>Matricular Aluno na Turma: A</h1>



`    `<div class="card mb-4">

`        `<div class="card-header">

`            `<h5>Informações da Turma</h5>

`        `</div>

`        `<div class="card-body">

`            `<p><strong>Nome:</strong> A</p>

`            `<p><strong>Curso:</strong> Introdução à Meditação</p>

`            `<p><strong>Vagas Disponíveis:</strong> 25</p>

`        `</div>

`    `</div>



`    `<form method="post" id="matricula-form">

`        `<input type="hidden" name="csrfmiddlewaretoken" value="ANaPa4fumdK2uGk0gKm70vg20kFTvtykZNXCMCfRGBJXRkyAhiRMzts86v4uKAZ1">

`        `<div class="mb-3">

`            `<label for="aluno-search" class="form-label">Buscar Aluno</label>

`            `<div class="input-group">

`                `<input type="text" class="form-control" id="aluno-search" placeholder="Digite o nome, CPF ou número iniciático do aluno...">

`                `<button class="btn btn-outline-secondary" type="button" id="limpar-aluno">

`                    `<i class="fas fa-times"></i>

`                `</button>

`            `</div>

`            `<div id="aluno-results" class="list-group mt-2 d-none"></div>

`            `<div id="aluno-selected" class="mt-2 d-none">

`                `<div class="card">

`                    `<div class="card-body d-flex align-items-center">

`                        `<div id="aluno-avatar" class="me-3">

`                            `<!-- Avatar do aluno será inserido aqui -->

`                        `</div>

`                        `<div>

`                            `<h5 id="aluno-nome" class="mb-1"></h5>

`                            `<p id="aluno-info" class="mb-0 text-muted"></p>

`                        `</div>

`                    `</div>

`                `</div>

`            `</div>

`            `<input type="hidden" name="aluno" id="aluno-id" required="">

`        `</div>



`        `<div class="d-flex justify-content-between">

`            `<a href="/turmas/2/" class="btn btn-secondary">Cancelar</a>

`            `<button type="submit" class="btn btn-primary">Matricular Aluno</button>

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

`        `const alunoSearch = document.getElementById('aluno-search');

`        `const alunoResults = document.getElementById('aluno-results');

`        `const alunoSelected = document.getElementById('aluno-selected');

`        `const alunoId = document.getElementById('aluno-id');

`        `const alunoNome = document.getElementById('aluno-nome');

`        `const alunoInfo = document.getElementById('aluno-info');

`        `const alunoAvatar = document.getElementById('aluno-avatar');

`        `const limparAluno = document.getElementById('limpar-aluno');

`        `const form = document.getElementById('matricula-form');



`        `let searchTimeout;



`        `// Função para buscar alunos

`        `function buscarAlunos(query) {

`            `if (query.length < 2) {

`                `alunoResults.classList.add('d-none');

`                `return;

`            `}



`            `fetch(`/alunos/search/?q=${encodeURIComponent(query)}`)

.then(response => response.json())

.then(data => {

`                    `alunoResults.innerHTML = '';



`                    `if (data.length === 0) {

`                        `const noResult = document.createElement('div');

`                        `noResult.className = 'list-group-item';

`                        `noResult.textContent = 'Nenhum aluno encontrado';

`                        `alunoResults.appendChild(noResult);

`                    `} else {

`                        `data.forEach(aluno => {

`                            `const item = document.createElement('a');

`                            `item.href = '#';

`                            `item.className = 'list-group-item list-group-item-action';

`                            `item.dataset.id = aluno.cpf;

`                            `item.dataset.nome = aluno.nome;

`                            `item.dataset.numero = aluno.numero\_iniciatico;

`                            `item.dataset.foto = aluno.foto || '';



`                            `// Criar conteúdo do item

`                            `let avatarHtml = '';

`                            `if (aluno.foto) {

`                                `avatarHtml = `<img src="${aluno.foto}" alt="${aluno.nome}" class="rounded-circle me-2" width="32" height="32">`;

`                            `} else {

`                                `avatarHtml = `<div class="rounded-circle bg-secondary text-white d-inline-flex align-items-center justify-content-center me-2" style="width: 32px; height: 32px;">${aluno.nome.charAt(0)}</div>`;

`                            `}



`                            `item.innerHTML = `

`                                `${avatarHtml}

`                                `<div>

`                                    `<div class="fw-bold">${aluno.nome}</div>

`                                    `<small class="text-muted">CPF: ${aluno.cpf} | Nº Iniciático: ${aluno.numero\_iniciatico || 'N/A'}</small>

`                                `</div>

`                            ``;



`                            `item.addEventListener('click', function(e) {

`                                `e.preventDefault();

`                                `selecionarAluno(this.dataset);

`                            `});



`                            `alunoResults.appendChild(item);

`                        `});

`                    `}



`                    `alunoResults.classList.remove('d-none');

`                `})

.catch(error => {

`                    `console.error('Erro ao buscar alunos:', error);

`                `});

`        `}



`        `// Função para selecionar um aluno

`        `function selecionarAluno(dados) {

`            `alunoId.value = dados.id;

`            `alunoNome.textContent = dados.nome;

`            `alunoInfo.textContent = `CPF: ${dados.id} | Nº Iniciático: ${dados.numero || 'N/A'}`;



`            `// Configurar avatar

`            `if (dados.foto) {

`                `alunoAvatar.innerHTML = `<img src="${dados.foto}" alt="${dados.nome}" class="rounded-circle" width="48" height="48">`;

`            `} else {

`                `alunoAvatar.innerHTML = `<div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center" style="width: 48px; height: 48px; font-size: 20px;">${dados.nome.charAt(0)}</div>`;

`            `}



`            `// Mostrar seleção e esconder resultados

`            `alunoSelected.classList.remove('d-none');

`            `alunoResults.classList.add('d-none');

`            `alunoSearch.value = '';

`        `}



`        `// Função para limpar seleção

`        `function limparSelecao() {

`            `alunoId.value = '';

`            `alunoSelected.classList.add('d-none');

`            `alunoSearch.value = '';

`            `alunoResults.classList.add('d-none');

`        `}



`        `// Event listeners

`        `alunoSearch.addEventListener('input', function() {

`            `clearTimeout(searchTimeout);

`            `searchTimeout = setTimeout(() => {

`                `buscarAlunos(this.value);

`            `}, 300);

`        `});



`        `limparAluno.addEventListener('click', limparSelecao);



`        `// Fechar resultados ao clicar fora

`        `document.addEventListener('click', function(e) {

`            `if (!alunoSearch.contains(e.target) && !alunoResults.contains(e.target)) {

`                `alunoResults.classList.add('d-none');

`            `}

`        `});



`        `// Validar formulário antes de enviar

`        `form.addEventListener('submit', function(e) {

`            `if (!alunoId.value) {

`                `e.preventDefault();

`                `alert('Por favor, selecione um aluno para matricular.');

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

<div id="djDebug" class="" dir="ltr" data-store-id="f7ddda83d4644b54a43e15d6eeeee0e8" data-render-panel-url="/\_\_debug\_\_/render\_panel/" data-sidebar-url="/\_\_debug\_\_/history\_sidebar/" data-default-show="true" data-update-on-fetch="False" data-theme="auto">

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





`      `<br><small>/turmas/2/matricular/</small>







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





`      `<br><small>Total: 128.55ms</small>







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





`      `<br><small>matricular\_aluno</small>







`    `</a>



</li>





<li id="djdt-SQLPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSQLPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="SQL queries from 1 connection" class="SQLPanel">



`  `SQL





`      `<br><small>5 queries in 8.24ms</small>







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





`      `<br><small>turmas/matricular\_aluno.html</small>







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

`                                `<a class="nav-link active" href="/turmas/">

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

`                                            `<input type="hidden" name="csrfmiddlewaretoken" value="5PbqE2M0OGnmvD90RHVDUuNGwlIa52NYuPYdgAMn84mhShnASfqitsZMCw7Lk9eF">

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

`        `<h1>Editar Turma: A</h1>

`        `<a href="/turmas/" class="btn btn-secondary">Voltar para a lista</a>

`    `</div>







`    `<form method="post">

`        `<input type="hidden" name="csrfmiddlewaretoken" value="5PbqE2M0OGnmvD90RHVDUuNGwlIa52NYuPYdgAMn84mhShnASfqitsZMCw7Lk9eF">





`        `<!-- Seção de Informações Básicas -->

`        `<div class="card mb-4">

`            `<div class="card-header bg-primary text-white">

`                `<h5>Informações Básicas</h5>

`            `</div>

`            `<div class="card-body">

`                `<div class="row">

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_nome" class="form-label">Nome da Turma</label>

`    `<input type="text" name="nome" value="A" class="form-control" maxlength="100" required="" aria-describedby="id\_nome\_helptext" id="id\_nome">





`        `<small class="form-text text-muted">Digite um nome descritivo para a turma.</small>



</div>

`                    `</div>

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_curso" class="form-label">Curso</label>

`    `<select name="curso" class="form-select" required="" id="id\_curso">

`  `<option value="">---------</option>

`  `<option value="35">35 - Básico do Básico</option>

`  `<option value="101" selected="">101 - Introdução à Meditação</option>

`  `<option value="102">102 - Meditação Avançada</option>

`  `<option value="103">103 - Yoga para Iniciantes</option>

`  `<option value="104">104 - Filosofia Oriental</option>

`  `<option value="105">105 - Práticas de Mindfulness</option>

`  `<option value="999">999 - Curso Teste</option>

</select>





</div>

`                    `</div>

`                `</div>

`                `<div class="row">

`                    `<div class="col-md-4">

`                        `<div class="mb-3">

`    `<label for="id\_vagas" class="form-label">Número de Vagas</label>

`    `<input type="number" name="vagas" value="30" class="form-control" min="0" required="" aria-describedby="id\_vagas\_helptext" id="id\_vagas">





`        `<small class="form-text text-muted">Quantidade máxima de alunos na turma.</small>



</div>

`                    `</div>

`                    `<div class="col-md-4">

`                        `<div class="mb-3">

`    `<label for="id\_status" class="form-label">Status</label>

`    `<select name="status" class="form-select" aria-describedby="id\_status\_helptext" id="id\_status">

`  `<option value="A" selected="">Ativa</option>

`  `<option value="I">Inativa</option>

`  `<option value="C">Cancelada</option>

`  `<option value="F">Finalizada</option>

</select>





`        `<small class="form-text text-muted">Situação atual da turma.</small>



</div>

`                    `</div>

`                    `<div class="col-md-4">

`                        `<div class="mb-3">

`    `<label for="id\_dias\_semana" class="form-label">Dias da Semana</label>

`    `<input type="text" name="dias\_semana" class="form-control" maxlength="100" aria-describedby="id\_dias\_semana\_helptext" id="id\_dias\_semana">





`        `<small class="form-text text-muted">Exemplo: 'Segunda, Quarta e Sexta' ou 'Terças e Quintas'.</small>



</div>

`                    `</div>

`                `</div>

`                `<div class="row">

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_data\_inicio" class="form-label">Data de Início</label>

`    `<input type="date" name="data\_inicio" value="2024-10-26" class="form-control" required="" aria-describedby="id\_data\_inicio\_helptext" id="id\_data\_inicio">





`        `<small class="form-text text-muted">Data prevista para início do curso.</small>



</div>

`                    `</div>

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_data\_fim" class="form-label">Data de Término</label>

`    `<input type="date" name="data\_fim" value="2026-10-26" class="form-control" required="" aria-describedby="id\_data\_fim\_helptext" id="id\_data\_fim">





`        `<small class="form-text text-muted">Data prevista para término do curso.</small>



</div>

`                    `</div>

`                `</div>

`                `<div class="row">

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_local" class="form-label">Local</label>

`    `<input type="text" name="local" class="form-control" maxlength="200" id="id\_local">





</div>

`                    `</div>

`                    `<div class="col-md-6">

`                        `<div class="mb-3">

`    `<label for="id\_horario" class="form-label">Horário</label>

`    `<input type="text" name="horario" class="form-control" maxlength="100" aria-describedby="id\_horario\_helptext" id="id\_horario">





`        `<small class="form-text text-muted">Exemplo: '19h às 21h'.</small>



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



`        `<!-- Seção de Instrutores -->

`        `<div class="card mb-4">

`            `<div class="card-header bg-success text-white">

`                `<h5>Instrutores</h5>

`            `</div>

`            `<div class="card-body">

`                `<div class="row">

`                    `<!-- Instrutor Principal -->

`                    `<div class="col-md-4 mb-3">

`                        `<label for="search-instrutor" class="form-label">Instrutor Principal</label>

`                        `<input type="text" id="search-instrutor" class="form-control" placeholder="Digite parte do CPF, nome ou número iniciático..." autocomplete="off">

`                        `<div id="search-results-instrutor" class="list-group mt-2" style="display: none"></div>

`                        `<div id="selected-instrutor-container" class="p-3 border rounded mt-2 d-none">

`                            `<div id="selected-instrutor-info">

`                                `Nenhum instrutor selecionado

`                            `</div>

`                        `</div><button id="clear-instrutor-btn" type="button" class="btn btn-sm btn-outline-secondary mt-2" style="display: none;">Limpar seleção</button>

`                        `<div id="instrutor-error" class="alert alert-warning mt-2 d-none"></div>

`                        `<!-- Campo original oculto via CSS -->

`                        `<select name="instrutor" class="form-control" id="id\_instrutor">

`  `<option value="" selected="">---------</option>

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

</select>

`                    `</div>



`                    `<!-- Instrutor Auxiliar -->

`                    `<div class="col-md-4 mb-3">

`                        `<label for="search-instrutor-auxiliar" class="form-label">Instrutor Auxiliar</label>

`                        `<input type="text" id="search-instrutor-auxiliar" class="form-control" placeholder="Digite parte do CPF, nome ou número iniciático..." autocomplete="off">

`                        `<div id="search-results-instrutor-auxiliar" class="list-group mt-2" style="display: none;"></div>

`                        `<div id="selected-instrutor-auxiliar-container" class="p-3 border rounded mt-2 d-none">

`                            `<div id="selected-instrutor-auxiliar-info">

`                                `Nenhum instrutor auxiliar selecionado

`                            `</div>

`                        `</div><button id="clear-instrutor-auxiliar-btn" type="button" class="btn btn-sm btn-outline-secondary mt-2" style="display: none;">Limpar seleção</button>

`                        `<div id="instrutor-auxiliar-error" class="alert alert-warning mt-2 d-none"></div>

`                        `<!-- Campo original oculto via CSS -->

`                        `<select name="instrutor\_auxiliar" class="form-control" id="id\_instrutor\_auxiliar">

`  `<option value="" selected="">---------</option>

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

</select>

`                    `</div>



`                    `<!-- Auxiliar de Instrução -->

`                    `<div class="col-md-4 mb-3">

`                        `<label for="search-auxiliar-instrucao" class="form-label">Auxiliar de Instrução</label>

`                        `<input type="text" id="search-auxiliar-instrucao" class="form-control" placeholder="Digite parte do CPF, nome ou número iniciático..." autocomplete="off">

`                        `<div id="search-results-auxiliar-instrucao" class="list-group mt-2" style="display: none;"></div>

`                        `<div id="selected-auxiliar-instrucao-container" class="p-3 border rounded mt-2 d-none">

`                            `<div id="selected-auxiliar-instrucao-info">

`                                `Nenhum auxiliar de instrução selecionado

`                            `</div>

`                        `</div><button id="clear-auxiliar-instrucao-btn" type="button" class="btn btn-sm btn-outline-secondary mt-2" style="display: none;">Limpar seleção</button>

`                        `<div id="auxiliar-instrucao-error" class="alert alert-warning mt-2 d-none"></div>

`                        `<!-- Campo original oculto via CSS -->

`                        `<select name="auxiliar\_instrucao" class="form-control" id="id\_auxiliar\_instrucao">

`  `<option value="" selected="">---------</option>

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

</select>

`                    `</div>

`                `</div>

`                `<div class="alert alert-info">

`                    `<i class="fas fa-info-circle"></i> Você pode selecionar qualquer aluno como instrutor.

`                    `O sistema verificará a elegibilidade e mostrará um aviso caso o aluno não atenda aos requisitos.

`                `</div>

`            `</div>

`        `</div>



`        `<div class="d-flex justify-content-between mb-5">

`            `<a href="/turmas/" class="btn btn-secondary">Cancelar</a>

`            `<button type="submit" class="btn btn-primary">Atualizar Turma</button>

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



<script src="/static/js/instrutor\_search.js"></script>



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

<div id="djDebug" class="" dir="ltr" data-store-id="d14e9ed7173448a1a10da24441ab2208" data-render-panel-url="/\_\_debug\_\_/render\_panel/" data-sidebar-url="/\_\_debug\_\_/history\_sidebar/" data-default-show="true" data-update-on-fetch="False" data-theme="auto">

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





`      `<br><small>/turmas/2/editar/</small>







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





`      `<br><small>Total: 123.49ms</small>







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





`      `<br><small>editar\_turma</small>







`    `</a>



</li>





<li id="djdt-SQLPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtSQLPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="SQL queries from 1 connection" class="SQLPanel">



`  `SQL





`      `<br><small>7 queries in 6.51ms</small>







`    `</a>



</li>





<li id="djdt-StaticFilesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtStaticFilesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Arquivos estáticos (154 encontrados, 7 sendo utilizados)" class="StaticFilesPanel">



`  `Arquivos estáticos





`      `<br><small>7 arquivos utilizados</small>







`    `</a>



</li>





<li id="djdt-TemplatesPanel" class="djDebugPanelButton">

`  `<input type="checkbox" data-cookie="djdtTemplatesPanel" checked="" title="Desativar para próximas requisições">



`    `<a href="#" title="Templates (13 renderizados)" class="TemplatesPanel">



`  `Templates





`      `<br><small>turmas/editar\_turma.html</small>







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

`      `<h3>Arquivos estáticos (154 encontrados, 7 sendo utilizados)</h3>

`    `</div>

`    `<div class="djDebugPanelContent">



`        `<div class="djdt-loader"></div>

`        `<div class="djdt-scroll"></div>



`    `</div>

`  `</div>







`  `<div id="TemplatesPanel" class="djdt-panelContent djdt-hidden">

`    `<div class="djDebugPanelTitle">

`      `<button type="button" class="djDebugClose">×</button>

`      `<h3>Templates (13 renderizados)</h3>

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

