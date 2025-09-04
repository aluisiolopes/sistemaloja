# Documentação da API - Módulo Clientes

## Visão Geral

A API do Módulo de Clientes oferece endpoints RESTful para gerenciamento completo de clientes em sistemas de gestão de lojas. Esta documentação detalha todos os endpoints disponíveis, parâmetros, respostas e exemplos de uso.

## URL Base

```
http://localhost:8000/api/v1
```

## Autenticação

Atualmente, a API não requer autenticação. Em ambiente de produção, recomenda-se implementar autenticação JWT ou similar.

## Formato de Dados

- **Content-Type**: `application/json`
- **Charset**: UTF-8
- **Formato de Data**: ISO 8601 (YYYY-MM-DD)
- **Formato de Data/Hora**: ISO 8601 (YYYY-MM-DDTHH:MM:SS.sssZ)

## Códigos de Status HTTP

| Código | Descrição |
|--------|-----------|
| 200 | OK - Requisição bem-sucedida |
| 201 | Created - Recurso criado com sucesso |
| 400 | Bad Request - Dados inválidos |
| 404 | Not Found - Recurso não encontrado |
| 422 | Unprocessable Entity - Erro de validação |
| 500 | Internal Server Error - Erro interno do servidor |

## Endpoints

### 1. Listar Clientes

Lista clientes com suporte a paginação e filtros.

**Endpoint**: `GET /clientes/`

**Parâmetros de Query**:

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| pagina | integer | Não | Número da página (padrão: 1) |
| por_pagina | integer | Não | Itens por página (padrão: 20, máx: 100) |
| nome | string | Não | Filtro por nome (busca parcial) |
| tipo_cliente | string | Não | pessoa_fisica ou pessoa_juridica |
| status | string | Não | ativo, inativo ou bloqueado |
| cidade | string | Não | Filtro por cidade (busca parcial) |
| estado | string | Não | UF do estado |
| cpf_cnpj | string | Não | CPF ou CNPJ exato |
| email | string | Não | Filtro por email (busca parcial) |

**Exemplo de Requisição**:
```bash
GET /api/v1/clientes/?pagina=1&por_pagina=10&tipo_cliente=pessoa_fisica&status=ativo
```

**Resposta de Sucesso (200)**:
```json
{
  "clientes": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "nome": "João Silva",
      "tipo_cliente": "pessoa_fisica",
      "cpf_cnpj": "12345678901",
      "rg_ie": "123456789",
      "email": "joao@email.com",
      "telefone": "11987654321",
      "celular": "11999888777",
      "endereco": "Rua das Flores, 123",
      "numero": "123",
      "complemento": "Apto 45",
      "bairro": "Centro",
      "cidade": "São Paulo",
      "estado": "SP",
      "cep": "01234567",
      "data_nascimento": "1990-05-15",
      "profissao": "Engenheiro",
      "observacoes": "Cliente VIP",
      "status": "ativo",
      "limite_credito": 500000,
      "pontos_fidelidade": 1500,
      "data_criacao": "2024-01-15T10:30:00.000Z",
      "data_atualizacao": "2024-01-20T14:45:00.000Z",
      "criado_por": "admin",
      "atualizado_por": "admin"
    }
  ],
  "total": 1,
  "pagina": 1,
  "por_pagina": 10,
  "total_paginas": 1
}
```

### 2. Criar Cliente

Cria um novo cliente no sistema.

**Endpoint**: `POST /clientes/`

**Corpo da Requisição**:
```json
{
  "nome": "Maria Santos",
  "tipo_cliente": "pessoa_fisica",
  "cpf_cnpj": "98765432109",
  "rg_ie": "987654321",
  "email": "maria@email.com",
  "telefone": "11987654321",
  "celular": "11999888777",
  "endereco": "Av. Paulista, 1000",
  "numero": "1000",
  "complemento": "Sala 101",
  "bairro": "Bela Vista",
  "cidade": "São Paulo",
  "estado": "SP",
  "cep": "01310100",
  "data_nascimento": "1985-03-20",
  "profissao": "Advogada",
  "observacoes": "Cliente desde 2020",
  "status": "ativo",
  "limite_credito": 300000,
  "pontos_fidelidade": 0,
  "criado_por": "admin"
}
```

**Campos Obrigatórios**:
- `nome`: Nome completo do cliente

**Resposta de Sucesso (201)**:
```json
{
  "id": "456e7890-e89b-12d3-a456-426614174001",
  "nome": "Maria Santos",
  "tipo_cliente": "pessoa_fisica",
  // ... outros campos
  "data_criacao": "2024-01-21T09:15:00.000Z",
  "data_atualizacao": null
}
```

**Resposta de Erro (400)**:
```json
{
  "detail": "Cliente com CPF/CNPJ 98765432109 já existe",
  "error_code": "DUPLICATE_DOCUMENT",
  "timestamp": "2024-01-21T09:15:00.000Z"
}
```

### 3. Buscar Cliente por ID

Retorna os dados de um cliente específico.

**Endpoint**: `GET /clientes/{cliente_id}`

**Parâmetros de Path**:
- `cliente_id`: UUID do cliente

**Exemplo de Requisição**:
```bash
GET /api/v1/clientes/123e4567-e89b-12d3-a456-426614174000
```

**Resposta de Sucesso (200)**:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "nome": "João Silva",
  // ... todos os campos do cliente
}
```

**Resposta de Erro (404)**:
```json
{
  "detail": "Cliente não encontrado",
  "timestamp": "2024-01-21T09:15:00.000Z"
}
```

### 4. Atualizar Cliente

Atualiza os dados de um cliente existente.

**Endpoint**: `PUT /clientes/{cliente_id}`

**Parâmetros de Path**:
- `cliente_id`: UUID do cliente

**Corpo da Requisição**:
```json
{
  "nome": "João Silva Santos",
  "telefone": "11999888777",
  "atualizado_por": "admin"
}
```

**Nota**: Apenas os campos fornecidos serão atualizados.

**Resposta de Sucesso (200)**:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "nome": "João Silva Santos",
  "telefone": "11999888777",
  // ... outros campos inalterados
  "data_atualizacao": "2024-01-21T10:30:00.000Z",
  "atualizado_por": "admin"
}
```

### 5. Remover Cliente

Remove um cliente do sistema permanentemente.

**Endpoint**: `DELETE /clientes/{cliente_id}`

**Parâmetros de Path**:
- `cliente_id`: UUID do cliente

**Resposta de Sucesso (200)**:
```json
{
  "message": "Cliente removido com sucesso",
  "timestamp": "2024-01-21T11:00:00.000Z"
}
```

### 6. Inativar Cliente

Marca um cliente como inativo (soft delete).

**Endpoint**: `PATCH /clientes/{cliente_id}/inativar`

**Parâmetros de Path**:
- `cliente_id`: UUID do cliente

**Parâmetros de Query**:
- `usuario`: Usuário responsável pela operação (opcional)

**Resposta de Sucesso (200)**:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "nome": "João Silva",
  "status": "inativo",
  // ... outros campos
  "data_atualizacao": "2024-01-21T11:15:00.000Z",
  "atualizado_por": "admin"
}
```

### 7. Buscar Clientes por Termo

Busca clientes por termo de pesquisa (nome, email, CPF/CNPJ).

**Endpoint**: `GET /clientes/buscar/{termo}`

**Parâmetros de Path**:
- `termo`: Termo de busca

**Parâmetros de Query**:
- `limite`: Número máximo de resultados (padrão: 10, máx: 50)

**Exemplo de Requisição**:
```bash
GET /api/v1/clientes/buscar/João?limite=5
```

**Resposta de Sucesso (200)**:
```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "nome": "João Silva",
    // ... campos do cliente
  }
]
```

### 8. Buscar Cliente por CPF/CNPJ

Busca um cliente pelo documento (CPF ou CNPJ).

**Endpoint**: `GET /clientes/cpf-cnpj/{documento}`

**Parâmetros de Path**:
- `documento`: CPF (11 dígitos) ou CNPJ (14 dígitos)

**Exemplo de Requisição**:
```bash
GET /api/v1/clientes/cpf-cnpj/12345678901
```

**Resposta de Sucesso (200)**:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "nome": "João Silva",
  "cpf_cnpj": "12345678901",
  // ... outros campos
}
```

### 9. Buscar Cliente por Email

Busca um cliente pelo endereço de email.

**Endpoint**: `GET /clientes/email/{email}`

**Parâmetros de Path**:
- `email`: Endereço de email do cliente

**Exemplo de Requisição**:
```bash
GET /api/v1/clientes/email/joao@email.com
```

**Resposta de Sucesso (200)**:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "nome": "João Silva",
  "email": "joao@email.com",
  // ... outros campos
}
```

### 10. Estatísticas de Clientes

Retorna estatísticas gerais dos clientes.

**Endpoint**: `GET /clientes/stats/resumo`

**Resposta de Sucesso (200)**:
```json
{
  "total": 150,
  "por_status": {
    "ativos": 120,
    "inativos": 25,
    "bloqueados": 5
  },
  "por_tipo": {
    "pessoa_fisica": 100,
    "pessoa_juridica": 50
  }
}
```

## Schemas de Dados

### ClienteCreate

Schema para criação de cliente:

```json
{
  "nome": "string (obrigatório, 2-255 chars)",
  "tipo_cliente": "pessoa_fisica | pessoa_juridica",
  "cpf_cnpj": "string (11 ou 14 dígitos)",
  "rg_ie": "string (máx 20 chars)",
  "email": "string (formato email válido)",
  "telefone": "string (máx 20 chars)",
  "celular": "string (máx 20 chars)",
  "endereco": "string (máx 255 chars)",
  "numero": "string (máx 10 chars)",
  "complemento": "string (máx 100 chars)",
  "bairro": "string (máx 100 chars)",
  "cidade": "string (máx 100 chars)",
  "estado": "string (2 chars, UF válida)",
  "cep": "string (8 dígitos)",
  "data_nascimento": "date (YYYY-MM-DD)",
  "profissao": "string (máx 100 chars)",
  "observacoes": "string",
  "status": "ativo | inativo | bloqueado",
  "limite_credito": "integer (centavos, >= 0)",
  "pontos_fidelidade": "integer (>= 0)",
  "criado_por": "string (máx 100 chars)"
}
```

### ClienteUpdate

Schema para atualização de cliente (todos os campos opcionais):

```json
{
  "nome": "string (2-255 chars)",
  "tipo_cliente": "pessoa_fisica | pessoa_juridica",
  // ... outros campos opcionais
  "atualizado_por": "string (máx 100 chars)"
}
```

### ClienteResponse

Schema de resposta com todos os campos do cliente:

```json
{
  "id": "uuid",
  "nome": "string",
  "tipo_cliente": "string",
  // ... todos os campos
  "data_criacao": "datetime",
  "data_atualizacao": "datetime | null",
  "criado_por": "string | null",
  "atualizado_por": "string | null"
}
```

## Validações

### CPF/CNPJ

- **CPF**: 11 dígitos numéricos
- **CNPJ**: 14 dígitos numéricos
- Validação automática baseada no tipo de cliente
- Verificação de unicidade no sistema

### Email

- Formato RFC compliant
- Verificação de unicidade no sistema
- Conversão automática para lowercase

### CEP

- Exatamente 8 dígitos numéricos
- Formatação automática (remove caracteres especiais)

### Estado

- Validação contra lista de UFs brasileiras válidas
- Conversão automática para uppercase

### Telefones

- Formatação automática (remove caracteres especiais)
- Suporte a telefones fixos (10 dígitos) e celulares (11 dígitos)

## Tratamento de Erros

### Erro de Validação (422)

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "Email inválido",
      "type": "value_error"
    }
  ]
}
```

### Erro de Negócio (400)

```json
{
  "detail": "Cliente com CPF/CNPJ 12345678901 já existe",
  "error_code": "DUPLICATE_DOCUMENT",
  "timestamp": "2024-01-21T09:15:00.000Z"
}
```

### Erro Interno (500)

```json
{
  "detail": "Erro interno do servidor",
  "error_code": "INTERNAL_SERVER_ERROR",
  "timestamp": "2024-01-21T09:15:00.000Z"
}
```

## Exemplos de Integração

### JavaScript/Fetch

```javascript
// Listar clientes
const response = await fetch('/api/v1/clientes/?pagina=1&por_pagina=10');
const data = await response.json();

// Criar cliente
const novoCliente = {
  nome: "João Silva",
  tipo_cliente: "pessoa_fisica",
  cpf_cnpj: "12345678901",
  email: "joao@email.com"
};

const response = await fetch('/api/v1/clientes/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(novoCliente)
});
```

### Python/Requests

```python
import requests

# Listar clientes
response = requests.get('http://localhost:8000/api/v1/clientes/')
clientes = response.json()

# Criar cliente
novo_cliente = {
    "nome": "João Silva",
    "tipo_cliente": "pessoa_fisica",
    "cpf_cnpj": "12345678901",
    "email": "joao@email.com"
}

response = requests.post(
    'http://localhost:8000/api/v1/clientes/',
    json=novo_cliente
)
```

### cURL

```bash
# Listar clientes
curl -X GET "http://localhost:8000/api/v1/clientes/" \
  -H "Accept: application/json"

# Criar cliente
curl -X POST "http://localhost:8000/api/v1/clientes/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "tipo_cliente": "pessoa_fisica",
    "cpf_cnpj": "12345678901",
    "email": "joao@email.com"
  }'
```

## Rate Limiting

Atualmente não há limitação de taxa implementada. Em produção, recomenda-se implementar rate limiting para prevenir abuso da API.

## Versionamento

A API utiliza versionamento via URL (`/api/v1/`). Mudanças breaking resultarão em nova versão da API.

## Documentação Interativa

A documentação interativa da API está disponível em:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Suporte

Para dúvidas sobre a API:
- Documentação interativa: http://localhost:8000/docs
- Issues no repositório
- Email: api-support@gestaolojas.com

---

**Versão da API**: 1.0.0  
**Última Atualização**: 2024-01-21

