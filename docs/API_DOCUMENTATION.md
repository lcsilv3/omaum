# Documentação da API - Sistema de Presenças OMAUM

## Visão Geral

A API REST do Sistema de Presenças OMAUM fornece endpoints para integração com sistemas externos, aplicações mobile e automações. A API segue os padrões REST e retorna dados em formato JSON.

### Informações Gerais
- **Base URL**: `https://seu-dominio.com/presencas/api/`
- **Versão**: v1.0
- **Formato**: JSON
- **Autenticação**: Token-based Authentication
- **Rate Limiting**: 1000 requests/hour por usuário

## Autenticação

### Token Authentication

```http
Authorization: Token your-api-token-here
```

### Obter Token
```http
POST /auth/token/
Content-Type: application/json

{
    "username": "seu_usuario",
    "password": "sua_senha"
}
```

**Resposta:**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user_id": 1,
    "username": "seu_usuario"
}
```

## Endpoints Principais

### 1. Presenças

#### Listar Presenças
```http
GET /api/presencas/
```

**Parâmetros de Query:**
- `turma_id` (int): ID da turma
- `aluno_id` (int): ID do aluno
- `data_inicio` (date): Data início (YYYY-MM-DD)
- `data_fim` (date): Data fim (YYYY-MM-DD)
- `presente` (bool): Filtrar por presente/ausente
- `page` (int): Número da página
- `page_size` (int): Itens por página (max: 100)

**Exemplo:**
```http
GET /api/presencas/?turma_id=1&data_inicio=2024-01-01&data_fim=2024-01-31&page=1&page_size=20
```

**Resposta:**
```json
{
    "count": 150,
    "next": "http://example.com/api/presencas/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "aluno": {
                "id": 1,
                "nome": "João Silva",
                "cpf": "123.456.789-00"
            },
            "turma": {
                "id": 1,
                "nome": "Turma 2024-1",
                "codigo": "T2024001"
            },
            "atividade": {
                "id": 1,
                "nome": "Aula Teórica",
                "tipo": "academica"
            },
            "data": "2024-01-15",
            "presente": true,
            "justificativa": null,
            "registrado_por": "Admin",
            "data_registro": "2024-01-15T10:30:00Z"
        }
    ]
}
```

#### Criar Presença
```http
POST /api/presencas/
Content-Type: application/json
```

**Body:**
```json
{
    "aluno_id": 1,
    "turma_id": 1,
    "atividade_id": 1,
    "data": "2024-01-15",
    "presente": true,
    "justificativa": "Participou ativamente da aula"
}
```

**Resposta (201 Created):**
```json
{
    "id": 123,
    "aluno": {
        "id": 1,
        "nome": "João Silva"
    },
    "turma": {
        "id": 1,
        "nome": "Turma 2024-1"
    },
    "atividade": {
        "id": 1,
        "nome": "Aula Teórica"
    },
    "data": "2024-01-15",
    "presente": true,
    "justificativa": "Participou ativamente da aula",
    "registrado_por": "API_User",
    "data_registro": "2024-01-15T14:22:33Z"
}
```

#### Atualizar Presença
```http
PUT /api/presencas/{id}/
PATCH /api/presencas/{id}/
Content-Type: application/json
```

**Body (PATCH - atualização parcial):**
```json
{
    "presente": false,
    "justificativa": "Falta médica - atestado anexado"
}
```

#### Excluir Presença
```http
DELETE /api/presencas/{id}/
```

**Resposta (204 No Content)**

### 2. Presenças Detalhadas

#### Listar Presenças Detalhadas
```http
GET /api/presencas-detalhadas/
```

**Parâmetros:**
- `turma_id` (int): ID da turma
- `periodo` (date): Período (primeiro dia do mês)
- `atividade_id` (int): ID da atividade

**Resposta:**
```json
{
    "count": 25,
    "results": [
        {
            "id": 1,
            "aluno": {
                "id": 1,
                "nome": "João Silva"
            },
            "turma": {
                "id": 1,
                "nome": "Turma 2024-1"
            },
            "atividade": {
                "id": 1,
                "nome": "Aula Teórica"
            },
            "periodo": "2024-01-01",
            "convocacoes": 20,
            "presencas": 18,
            "faltas": 2,
            "voluntario_extra": 3,
            "voluntario_simples": 1,
            "percentual_presenca": "90.00",
            "total_voluntarios": 4,
            "carencias": 0,
            "data_registro": "2024-01-31T23:59:59Z"
        }
    ]
}
```

#### Criar/Atualizar Presença Detalhada
```http
POST /api/presencas-detalhadas/
PUT /api/presencas-detalhadas/{id}/
Content-Type: application/json
```

**Body:**
```json
{
    "aluno_id": 1,
    "turma_id": 1,
    "atividade_id": 1,
    "periodo": "2024-01-01",
    "convocacoes": 20,
    "presencas": 18,
    "faltas": 2,
    "voluntario_extra": 3,
    "voluntario_simples": 1
}
```

### 3. Estatísticas

#### Calcular Estatísticas
```http
POST /api/calcular-estatisticas/
Content-Type: application/json
```

**Body:**
```json
{
    "turma_id": 1,
    "periodo_inicio": "2024-01-01",
    "periodo_fim": "2024-01-31",
    "atividades": [1, 2, 3]
}
```

**Resposta:**
```json
{
    "periodo": {
        "inicio": "2024-01-01",
        "fim": "2024-01-31"
    },
    "turma": {
        "id": 1,
        "nome": "Turma 2024-1",
        "total_alunos": 25
    },
    "estatisticas_gerais": {
        "total_presencas": 450,
        "total_faltas": 50,
        "total_convocacoes": 500,
        "percentual_geral": "90.00",
        "alunos_com_carencia": 3
    },
    "por_aluno": [
        {
            "aluno_id": 1,
            "nome": "João Silva",
            "total_convocacoes": 20,
            "total_presencas": 18,
            "total_faltas": 2,
            "percentual": "90.00",
            "carencias": 0,
            "status": "regular"
        }
    ],
    "por_atividade": [
        {
            "atividade_id": 1,
            "nome": "Aula Teórica",
            "total_convocacoes": 300,
            "total_presencas": 270,
            "percentual": "90.00"
        }
    ]
}
```

### 4. Busca e Filtros

#### Buscar Alunos
```http
GET /api/buscar-alunos/?q=joao&turma_id=1
```

**Resposta:**
```json
{
    "results": [
        {
            "id": 1,
            "nome": "João Silva",
            "cpf": "123.456.789-00",
            "turma": {
                "id": 1,
                "nome": "Turma 2024-1"
            }
        }
    ]
}
```

#### Atividades por Turma
```http
GET /api/atividades-turma/?turma_id=1
```

**Resposta:**
```json
{
    "turma_id": 1,
    "atividades": [
        {
            "id": 1,
            "nome": "Aula Teórica",
            "tipo": "academica",
            "obrigatoria": true
        },
        {
            "id": 2,
            "nome": "Ritual Mensal",
            "tipo": "ritualistica",
            "obrigatoria": true
        }
    ]
}
```

### 5. Configurações

#### Obter Configuração de Presença
```http
GET /api/configuracao-presenca/?turma_id=1&atividade_id=1
```

**Resposta:**
```json
{
    "id": 1,
    "turma_id": 1,
    "atividade_id": 1,
    "limite_carencia_0_25": 0,
    "limite_carencia_26_50": 1,
    "limite_carencia_51_75": 2,
    "limite_carencia_76_100": 3,
    "obrigatoria": true,
    "peso_calculo": "1.00",
    "ativo": true
}
```

#### Atualizar Configuração
```http
PUT /api/configuracao-presenca/{id}/
Content-Type: application/json
```

**Body:**
```json
{
    "limite_carencia_0_25": 0,
    "limite_carencia_26_50": 1,
    "limite_carencia_51_75": 3,
    "limite_carencia_76_100": 5,
    "peso_calculo": "1.50"
}
```

### 6. Validação de Dados

#### Validar Dados de Presença
```http
POST /api/validar-dados/
Content-Type: application/json
```

**Body:**
```json
{
    "aluno_id": 1,
    "turma_id": 1,
    "atividade_id": 1,
    "data": "2024-01-15",
    "convocacoes": 20,
    "presencas": 21,
    "faltas": 2
}
```

**Resposta (Dados Válidos):**
```json
{
    "valido": true,
    "mensagens": [],
    "sugestoes": []
}
```

**Resposta (Dados Inválidos):**
```json
{
    "valido": false,
    "mensagens": [
        "A soma de presenças e faltas (23) não pode ser maior que convocações (20)"
    ],
    "sugestoes": [
        "Verifique se o número de convocações está correto",
        "Reduza o número de presenças ou faltas"
    ]
}
```

## Atualização em Lote

### Atualizar Múltiplas Presenças
```http
POST /api/atualizar-presencas/
Content-Type: application/json
```

**Body:**
```json
{
    "presencas": [
        {
            "aluno_id": 1,
            "turma_id": 1,
            "atividade_id": 1,
            "data": "2024-01-15",
            "presente": true
        },
        {
            "aluno_id": 2,
            "turma_id": 1,
            "atividade_id": 1,
            "data": "2024-01-15",
            "presente": false,
            "justificativa": "Falta médica"
        }
    ]
}
```

**Resposta:**
```json
{
    "processadas": 2,
    "criadas": 1,
    "atualizadas": 1,
    "erros": 0,
    "detalhes": [
        {
            "aluno_id": 1,
            "status": "criada",
            "id": 123
        },
        {
            "aluno_id": 2,
            "status": "atualizada",
            "id": 124
        }
    ]
}
```

## Códigos de Erro HTTP

### Códigos de Sucesso
- **200 OK**: Requisição bem-sucedida
- **201 Created**: Recurso criado com sucesso
- **204 No Content**: Recurso excluído com sucesso

### Códigos de Erro do Cliente
- **400 Bad Request**: Dados inválidos na requisição
- **401 Unauthorized**: Token de autenticação inválido
- **403 Forbidden**: Sem permissão para acessar o recurso
- **404 Not Found**: Recurso não encontrado
- **409 Conflict**: Conflito com o estado atual do recurso
- **429 Too Many Requests**: Rate limit excedido

### Códigos de Erro do Servidor
- **500 Internal Server Error**: Erro interno do servidor
- **502 Bad Gateway**: Erro de gateway
- **503 Service Unavailable**: Serviço temporariamente indisponível

## Formato de Erro

```json
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Dados de entrada inválidos",
        "details": {
            "presente": ["Este campo é obrigatório"],
            "data": ["Data não pode ser futura"]
        }
    },
    "timestamp": "2024-01-15T14:22:33Z",
    "path": "/api/presencas/"
}
```

## Rate Limiting

### Limites por Endpoint
- **GET**: 1000 requests/hour
- **POST/PUT/PATCH**: 500 requests/hour
- **DELETE**: 100 requests/hour

### Headers de Rate Limit
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642262400
```

## Exemplos de Uso

### Python (requests)
```python
import requests

# Configuração
BASE_URL = 'https://seu-dominio.com/presencas/api'
TOKEN = 'your-api-token-here'

headers = {
    'Authorization': f'Token {TOKEN}',
    'Content-Type': 'application/json'
}

# Listar presenças
response = requests.get(
    f'{BASE_URL}/presencas/',
    headers=headers,
    params={'turma_id': 1, 'data_inicio': '2024-01-01'}
)

presencas = response.json()
print(f"Total: {presencas['count']}")

# Criar presença
nova_presenca = {
    'aluno_id': 1,
    'turma_id': 1,
    'atividade_id': 1,
    'data': '2024-01-15',
    'presente': True
}

response = requests.post(
    f'{BASE_URL}/presencas/',
    headers=headers,
    json=nova_presenca
)

if response.status_code == 201:
    print("Presença criada com sucesso!")
    print(response.json())
```

### JavaScript (fetch)
```javascript
const BASE_URL = 'https://seu-dominio.com/presencas/api';
const TOKEN = 'your-api-token-here';

const headers = {
    'Authorization': `Token ${TOKEN}`,
    'Content-Type': 'application/json'
};

// Buscar estatísticas
async function calcularEstatisticas(turmaId, inicio, fim) {
    const response = await fetch(`${BASE_URL}/calcular-estatisticas/`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({
            turma_id: turmaId,
            periodo_inicio: inicio,
            periodo_fim: fim
        })
    });
    
    if (response.ok) {
        return await response.json();
    } else {
        throw new Error(`Erro: ${response.status} ${response.statusText}`);
    }
}

// Usar a função
calcularEstatisticas(1, '2024-01-01', '2024-01-31')
    .then(stats => console.log('Estatísticas:', stats))
    .catch(error => console.error('Erro:', error));
```

### cURL
```bash
# Listar presenças
curl -H "Authorization: Token your-api-token-here" \
     -H "Content-Type: application/json" \
     "https://seu-dominio.com/presencas/api/presencas/?turma_id=1"

# Criar presença
curl -X POST \
     -H "Authorization: Token your-api-token-here" \
     -H "Content-Type: application/json" \
     -d '{"aluno_id":1,"turma_id":1,"atividade_id":1,"data":"2024-01-15","presente":true}' \
     "https://seu-dominio.com/presencas/api/presencas/"

# Calcular estatísticas
curl -X POST \
     -H "Authorization: Token your-api-token-here" \
     -H "Content-Type: application/json" \
     -d '{"turma_id":1,"periodo_inicio":"2024-01-01","periodo_fim":"2024-01-31"}' \
     "https://seu-dominio.com/presencas/api/calcular-estatisticas/"
```

## WebHooks (Futuro)

### Eventos Disponíveis
- `presenca.criada`: Nova presença registrada
- `presenca.atualizada`: Presença modificada
- `presenca.excluida`: Presença removida
- `estatisticas.calculadas`: Estatísticas recalculadas

### Formato do WebHook
```json
{
    "event": "presenca.criada",
    "timestamp": "2024-01-15T14:22:33Z",
    "data": {
        "id": 123,
        "aluno_id": 1,
        "turma_id": 1,
        "data": "2024-01-15",
        "presente": true
    }
}
```

## Versioning

### URL Versioning
```http
GET /api/v1/presencas/
GET /api/v2/presencas/
```

### Header Versioning
```http
Accept: application/vnd.omaum.v1+json
Accept: application/vnd.omaum.v2+json
```

## Suporte

### Documentação Interativa
- **Swagger UI**: `https://seu-dominio.com/api/docs/`
- **ReDoc**: `https://seu-dominio.com/api/redoc/`

### Contato
- **Email**: api-support@omaum.edu.br
- **GitHub**: https://github.com/lcsilv3/omaum/issues
- **Slack**: #api-support no workspace OMAUM

### Status da API
- **Status Page**: https://status.omaum.edu.br
- **Uptime**: 99.9%
- **Response Time**: < 200ms (média)
