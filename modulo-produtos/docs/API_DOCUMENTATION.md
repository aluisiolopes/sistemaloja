# Documentação da API - Módulo de Produtos

## Visão Geral

A API do Módulo de Produtos oferece endpoints RESTful para gerenciamento completo de produtos, categorias e marcas. Construída com FastAPI, oferece documentação automática, validação de dados e performance otimizada.

**Base URL**: `http://localhost:8001/api/v1`

**Documentação Interativa**: 
- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

## Autenticação

Atualmente, a API não requer autenticação. Em versões futuras, será implementado sistema de tokens JWT.

## Formatos de Resposta

### Sucesso
```json
{
  "id": "uuid",
  "nome": "string",
  "data_criacao": "2024-01-01T00:00:00Z",
  ...
}
```

### Erro
```json
{
  "detail": "Mensagem de erro descritiva"
}
```

### Lista Paginada
```json
{
  "produtos": [...],
  "total": 100,
  "pagina": 1,
  "limite": 10,
  "total_paginas": 10
}
```

## Endpoints de Produtos

### Listar Produtos

**GET** `/produtos/`

Lista produtos com paginação e filtros opcionais.

#### Parâmetros de Query

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|---------|
| `skip` | integer | Número de registros para pular | 0 |
| `limit` | integer | Número máximo de registros | 10 |
| `nome` | string | Filtro por nome (busca parcial) | - |
| `categoria_id` | uuid | Filtro por categoria | - |
| `marca_id` | uuid | Filtro por marca | - |
| `status` | enum | Filtro por status | - |
| `preco_min` | integer | Preço mínimo (em centavos) | - |
| `preco_max` | integer | Preço máximo (em centavos) | - |

#### Exemplo de Requisição

```bash
curl -X GET "http://localhost:8001/api/v1/produtos/?skip=0&limit=10&status=ativo" \
  -H "Content-Type: application/json"
```

#### Exemplo de Resposta

```json
{
  "produtos": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "nome": "Smartphone Galaxy S23",
      "descricao": "Celular de última geração",
      "codigo_barras": "7891234567890",
      "sku": "SMART-S23",
      "preco_venda": 500000,
      "preco_custo": 350000,
      "unidade_medida": "unidade",
      "categoria_id": "456e7890-e89b-12d3-a456-426614174001",
      "categoria_nome": "Eletrônicos",
      "marca_id": "789e0123-e89b-12d3-a456-426614174002",
      "marca_nome": "Samsung",
      "status": "ativo",
      "imagem_url": "https://exemplo.com/imagem.jpg",
      "observacoes": "Produto em destaque",
      "data_criacao": "2024-01-01T10:00:00Z",
      "data_atualizacao": "2024-01-02T15:30:00Z",
      "criado_por": "admin",
      "atualizado_por": "admin"
    }
  ],
  "total": 1,
  "pagina": 1,
  "limite": 10,
  "total_paginas": 1
}
```

### Criar Produto

**POST** `/produtos/`

Cria um novo produto.

#### Corpo da Requisição

```json
{
  "nome": "Produto Exemplo",
  "descricao": "Descrição do produto",
  "codigo_barras": "1234567890123",
  "sku": "PROD-001",
  "preco_venda": 10000,
  "preco_custo": 6000,
  "unidade_medida": "unidade",
  "categoria_id": "uuid-opcional",
  "marca_id": "uuid-opcional",
  "status": "ativo",
  "imagem_url": "https://exemplo.com/imagem.jpg",
  "observacoes": "Observações opcionais",
  "criado_por": "usuario"
}
```

#### Validações

- `nome`: Obrigatório, 2-255 caracteres
- `preco_venda`: Obrigatório, >= 0 (em centavos)
- `preco_custo`: Obrigatório, >= 0 (em centavos)
- `codigo_barras`: Opcional, único se fornecido
- `sku`: Opcional, único se fornecido
- `unidade_medida`: Enum válido
- `status`: Enum válido

#### Códigos de Resposta

- `201`: Produto criado com sucesso
- `400`: Dados inválidos
- `409`: SKU ou código de barras duplicado
- `422`: Erro de validação

### Buscar Produto por ID

**GET** `/produtos/{id}`

Retorna um produto específico pelo ID.

#### Parâmetros de Path

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `id` | uuid | ID único do produto |

#### Códigos de Resposta

- `200`: Produto encontrado
- `404`: Produto não encontrado
- `422`: ID inválido

### Atualizar Produto

**PUT** `/produtos/{id}`

Atualiza um produto existente.

#### Corpo da Requisição

Mesma estrutura do POST, mas todos os campos são opcionais.

```json
{
  "nome": "Novo nome",
  "preco_venda": 12000,
  "status": "promocao"
}
```

#### Códigos de Resposta

- `200`: Produto atualizado
- `404`: Produto não encontrado
- `409`: Conflito de dados únicos
- `422`: Dados inválidos

### Inativar Produto

**PATCH** `/produtos/{id}/inativar`

Marca um produto como inativo (soft delete).

#### Códigos de Resposta

- `200`: Produto inativado
- `404`: Produto não encontrado

### Remover Produto

**DELETE** `/produtos/{id}`

Remove permanentemente um produto.

#### Códigos de Resposta

- `200`: Produto removido
- `404`: Produto não encontrado

### Buscar Produtos

**GET** `/produtos/search/{termo}`

Busca produtos por termo textual.

#### Parâmetros de Path

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `termo` | string | Termo de busca |

#### Parâmetros de Query

| Parâmetro | Tipo | Descrição | Padrão |
|-----------|------|-----------|---------|
| `limit` | integer | Número máximo de resultados | 10 |

#### Busca em Campos

- Nome do produto
- Descrição
- SKU
- Código de barras
- Nome da categoria
- Nome da marca

### Estatísticas de Produtos

**GET** `/produtos/stats/resumo`

Retorna estatísticas gerais dos produtos.

#### Exemplo de Resposta

```json
{
  "total_produtos": 150,
  "por_status": {
    "ativo": 120,
    "inativo": 20,
    "esgotado": 8,
    "promocao": 2
  },
  "por_categoria": {
    "Eletrônicos": 45,
    "Roupas": 30,
    "Livros": 25,
    "Casa": 50
  },
  "por_marca": {
    "Samsung": 20,
    "Apple": 15,
    "Nike": 25,
    "Outras": 90
  },
  "valor_total_estoque": 1500000,
  "ticket_medio": 10000
}
```

## Endpoints de Categorias

### Listar Categorias

**GET** `/categorias/`

Lista todas as categorias disponíveis.

#### Exemplo de Resposta

```json
[
  {
    "id": "uuid",
    "nome": "Eletrônicos",
    "descricao": "Produtos eletrônicos em geral",
    "data_criacao": "2024-01-01T10:00:00Z",
    "data_atualizacao": null
  }
]
```

### Criar Categoria

**POST** `/categorias/`

Cria uma nova categoria.

#### Corpo da Requisição

```json
{
  "nome": "Nova Categoria",
  "descricao": "Descrição opcional"
}
```

#### Validações

- `nome`: Obrigatório, único, 2-255 caracteres
- `descricao`: Opcional, máximo 2000 caracteres

### Buscar Categoria por ID

**GET** `/categorias/{id}`

### Atualizar Categoria

**PUT** `/categorias/{id}`

### Remover Categoria

**DELETE** `/categorias/{id}`

## Endpoints de Marcas

### Listar Marcas

**GET** `/marcas/`

### Criar Marca

**POST** `/marcas/`

### Buscar Marca por ID

**GET** `/marcas/{id}`

### Atualizar Marca

**PUT** `/marcas/{id}`

### Remover Marca

**DELETE** `/marcas/{id}`

## Enums e Tipos

### UnidadeMedida

```python
enum UnidadeMedida:
    UNIDADE = "unidade"
    KG = "kg"
    G = "g"
    M = "m"
    CM = "cm"
    MM = "mm"
    L = "l"
    ML = "ml"
    CAIXA = "caixa"
    PACOTE = "pacote"
```

### StatusProduto

```python
enum StatusProduto:
    ATIVO = "ativo"
    INATIVO = "inativo"
    ESGOTADO = "esgotado"
    PROMOCAO = "promocao"
```

## Códigos de Status HTTP

| Código | Descrição |
|--------|-----------|
| 200 | Sucesso |
| 201 | Criado |
| 400 | Requisição inválida |
| 404 | Não encontrado |
| 409 | Conflito (dados duplicados) |
| 422 | Erro de validação |
| 500 | Erro interno do servidor |

## Tratamento de Erros

### Erro de Validação (422)

```json
{
  "detail": [
    {
      "loc": ["body", "preco_venda"],
      "msg": "ensure this value is greater than or equal to 0",
      "type": "value_error.number.not_ge",
      "ctx": {"limit_value": 0}
    }
  ]
}
```

### Erro de Conflito (409)

```json
{
  "detail": "Produto com este SKU já existe"
}
```

### Erro Não Encontrado (404)

```json
{
  "detail": "Produto não encontrado"
}
```

## Limitações e Quotas

- **Rate Limiting**: 1000 requisições por minuto por IP
- **Tamanho máximo**: 5MB para uploads de imagem
- **Paginação**: Máximo 100 itens por página
- **Busca**: Máximo 50 resultados por busca

## Versionamento

A API segue versionamento semântico:
- **v1.0.0**: Versão inicial
- **v1.1.0**: Funcionalidades de variações
- **v2.0.0**: Mudanças breaking (futuro)

## Exemplos de Uso

### Criar Produto Completo

```bash
curl -X POST "http://localhost:8001/api/v1/produtos/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "iPhone 15 Pro",
    "descricao": "Smartphone premium da Apple",
    "codigo_barras": "0194253000000",
    "sku": "IPHONE-15-PRO-128GB",
    "preco_venda": 899900,
    "preco_custo": 650000,
    "unidade_medida": "unidade",
    "status": "ativo",
    "criado_por": "admin"
  }'
```

### Buscar Produtos por Categoria

```bash
curl -X GET "http://localhost:8001/api/v1/produtos/?categoria_id=uuid-da-categoria&limit=20"
```

### Atualizar Preço de Produto

```bash
curl -X PUT "http://localhost:8001/api/v1/produtos/uuid-do-produto" \
  -H "Content-Type: application/json" \
  -d '{
    "preco_venda": 799900,
    "status": "promocao"
  }'
```

## SDKs e Bibliotecas

### JavaScript/TypeScript

```javascript
// Exemplo usando fetch
const api = {
  baseURL: 'http://localhost:8001/api/v1',
  
  async getProdutos(params = {}) {
    const url = new URL(`${this.baseURL}/produtos/`);
    Object.keys(params).forEach(key => 
      url.searchParams.append(key, params[key])
    );
    
    const response = await fetch(url);
    return response.json();
  },
  
  async createProduto(produto) {
    const response = await fetch(`${this.baseURL}/produtos/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(produto)
    });
    return response.json();
  }
};
```

### Python

```python
import requests

class ProdutosAPI:
    def __init__(self, base_url="http://localhost:8001/api/v1"):
        self.base_url = base_url
    
    def get_produtos(self, **params):
        response = requests.get(f"{self.base_url}/produtos/", params=params)
        return response.json()
    
    def create_produto(self, produto_data):
        response = requests.post(
            f"{self.base_url}/produtos/", 
            json=produto_data
        )
        return response.json()
```

## Monitoramento e Logs

### Métricas Disponíveis

- Tempo de resposta por endpoint
- Taxa de erro por endpoint
- Número de requisições por minuto
- Uso de memória e CPU

### Logs Estruturados

```json
{
  "timestamp": "2024-01-01T10:00:00Z",
  "level": "INFO",
  "method": "POST",
  "path": "/api/v1/produtos/",
  "status_code": 201,
  "response_time": 45.2,
  "user_agent": "curl/7.68.0",
  "ip": "192.168.1.100"
}
```

## Changelog da API

### v1.0.0 (2024-01-01)
- Lançamento inicial
- CRUD completo para produtos, categorias e marcas
- Busca e filtros
- Paginação
- Validações robustas

### Próximas Versões
- v1.1.0: Upload de imagens
- v1.2.0: Variações de produtos
- v1.3.0: Importação/exportação
- v2.0.0: GraphQL e WebSockets

