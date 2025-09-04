# Plano Detalhado: Módulo de Gestão de Vendas (PDV)

Este documento detalha o desenvolvimento do Módulo de Gestão de Vendas (PDV - Ponto de Venda), conforme a Fase 2 do Plano de Desenvolvimento Modular do Sistema de Gestão de Lojas. O foco é na usabilidade e agilidade para o operador de caixa, garantindo a precisão e eficiência das operações de venda.

## 2.1. Módulo de Gestão de Vendas (PDV - Ponto de Venda)

Este módulo abrange todo o processo de registro de vendas, desde a seleção de produtos até o processamento do pagamento, com foco na usabilidade e agilidade para o operador de caixa.

### 2.1.1. Registro de Vendas

O registro de vendas é a funcionalidade central do PDV, permitindo que os operadores de caixa processem transações de forma rápida e eficiente. A interface deve ser intuitiva e otimizada para minimizar o tempo de atendimento ao cliente.

#### Interface de PDV

A interface do Ponto de Venda será projetada para ser clara e responsiva, facilitando a interação do usuário. Será implementada com React.js no frontend, utilizando componentes Material-UI (MUI) para garantir uma experiência de usuário consistente e moderna. A busca de produtos será um elemento chave, permitindo a localização rápida de itens por nome, código de barras ou SKU, utilizando um campo de pesquisa com autocompletar e resultados em tempo real.

#### Adição/Remoção de Itens

Os produtos selecionados serão adicionados a um 


carrinho de compras virtual. Cada item adicionado exibirá o nome do produto, quantidade, preço unitário e subtotal. O operador poderá ajustar a quantidade de cada item diretamente no carrinho ou remover itens conforme necessário. A atualização do subtotal e do total da venda deve ser instantânea a cada alteração.

#### Cálculo Automático

O sistema realizará o cálculo automático do total da venda, considerando o preço unitário de cada produto, a quantidade e quaisquer impostos aplicáveis. Embora a emissão de NF-e seja uma fase posterior, o sistema deve estar preparado para integrar a lógica de cálculo de impostos desde o início, mesmo que inicialmente apenas para fins de exibição interna. O total da venda será exibido de forma proeminente na interface do PDV, atualizando-se dinamicamente.

#### Aplicação de Descontos

Será possível aplicar descontos tanto por item quanto no total da venda. Os descontos poderão ser configurados como percentuais ou valores fixos. A interface permitirá que o operador selecione o tipo de desconto e insira o valor correspondente, com o sistema recalculando automaticamente o total da venda após a aplicação do desconto. A lógica de desconto deve ser flexível para acomodar futuras regras de promoção.

#### Identificação do Cliente

O PDV permitirá associar a venda a um cliente cadastrado no sistema. Esta funcionalidade é opcional, mas altamente recomendada para construir o histórico de compras do cliente e habilitar programas de fidelidade futuros. O operador poderá buscar clientes existentes por nome, CPF/CNPJ ou e-mail, ou optar por registrar a venda sem associar a um cliente. A integração com o Módulo de Cadastro de Clientes (Fase 1) será fundamental aqui.

#### Vendedor

Cada transação de venda registrará o vendedor responsável. Isso é crucial para fins de comissionamento, acompanhamento de desempenho e auditoria. O sistema poderá pré-selecionar o vendedor logado ou permitir que o operador selecione um vendedor da lista de usuários cadastrados, garantindo que cada venda seja atribuída corretamente.




### 2.1.2. Formas de Pagamento

O módulo de PDV suportará uma variedade de formas de pagamento para atender às necessidades dos clientes e da loja, incluindo a possibilidade de pagamentos mistos.

#### Múltiplas Formas

O sistema será capaz de processar pagamentos em diversas modalidades, tais como:

*   **Dinheiro:** Com cálculo automático de troco.
*   **Cartão de Crédito:** Integração futura com TEF (Transferência Eletrônica de Fundos) para processamento seguro e eficiente.
*   **Cartão de Débito:** Similar ao cartão de crédito, com integração TEF.
*   **PIX:** Geração de QR Codes dinâmicos para pagamentos instantâneos, com conciliação automática.
*   **Vale-Presente:** Utilização de saldos de vales-presente emitidos pela própria loja.
*   **Crediário:** Para clientes com linha de crédito pré-aprovada na loja, com registro do valor a prazo.

#### Pagamento Misto

Será implementada a funcionalidade de pagamento misto, permitindo que o cliente utilize diferentes formas de pagamento para uma única transação. Por exemplo, parte em dinheiro e parte no cartão. O sistema deverá gerenciar os valores pagos em cada modalidade e calcular o saldo restante ou o troco, se aplicável.

#### Troco

Para pagamentos em dinheiro, o sistema calculará automaticamente o troco devido ao cliente, com base no valor total da venda e no valor recebido. Esta funcionalidade visa agilizar o processo de caixa e reduzir erros manuais.




### 2.1.3. Fechamento da Venda

O fechamento da venda é o passo final no processo de transação, onde a venda é confirmada, registrada e o comprovante é gerado.

#### Confirmação

Após a seleção dos produtos e o processamento do pagamento, o operador de caixa confirmará a transação. Este passo acionará o registro da venda no banco de dados, a baixa automática dos produtos do estoque e a atualização do histórico de compras do cliente, se aplicável. A confirmação deve ser rápida e com feedback visual claro para o operador.

#### Geração de Comprovante

O sistema gerará um comprovante de venda não fiscal (recibo simples) para o cliente. Este comprovante incluirá detalhes da transação, como itens comprados, quantidades, preços unitários, descontos aplicados, total da venda, forma(s) de pagamento e troco. O comprovante poderá ser impresso em uma impressora térmica de recibos ou enviado por e-mail ao cliente, se o e-mail estiver cadastrado.

### 2.1.4. Histórico de Vendas

O histórico de vendas permitirá a consulta e visualização de transações passadas, fornecendo informações valiosas para o gerenciamento da loja e o atendimento ao cliente.

#### Consulta e Visualização

Será desenvolvida uma interface para consulta do histórico de vendas, permitindo que os usuários (gerentes, administradores) visualizem todas as vendas realizadas. Cada registro de venda exibirá um resumo, e ao clicar, será possível acessar os detalhes completos da transação, incluindo todos os itens vendidos, o cliente associado, o vendedor responsável e as formas de pagamento utilizadas.

#### Filtros

Para facilitar a localização de vendas específicas, a interface de histórico de vendas incluirá filtros avançados. Os usuários poderão filtrar as vendas por:

*   **Período:** Seleção de datas de início e fim.
*   **Cliente:** Busca por nome ou CPF/CNPJ do cliente.
*   **Vendedor:** Filtragem por vendedor responsável pela transação.
*   **Status da Venda:** (ex: concluída, cancelada, estornada - a serem definidos conforme a evolução do módulo de devoluções/trocas).

Esses filtros permitirão uma análise granular do desempenho de vendas e facilitarão a auditoria e o suporte ao cliente.




## 2.1.5. Integração com o Módulo de Controle de Estoque Avançado

A integração do Módulo de Gestão de Vendas (PDV) com o Módulo de Controle de Estoque Avançado é crucial para garantir a precisão do inventário e evitar vendas de produtos indisponíveis. Esta integração será bidirecional e em tempo real.

#### Atualização Automática de Estoque

*   **Saída por Venda:** No momento da confirmação de uma venda no PDV, o sistema acionará automaticamente o Módulo de Controle de Estoque para registrar a baixa dos produtos vendidos. Esta operação deve ser atômica e transacional, garantindo que o estoque seja atualizado corretamente ou que a venda seja revertida em caso de falha na atualização do estoque.
*   **Verificação de Disponibilidade:** Antes de finalizar uma venda, o PDV consultará o estoque para verificar a disponibilidade dos produtos. Caso um produto não tenha estoque suficiente, o sistema alertará o operador, impedindo a conclusão da venda ou permitindo o ajuste da quantidade.

#### Movimentações de Estoque

Embora as movimentações manuais de estoque (entrada, saída, transferência) sejam gerenciadas diretamente no Módulo de Controle de Estoque, o PDV se beneficiará dessas atualizações em tempo real. Por exemplo, se um produto for recebido no estoque, ele estará imediatamente disponível para venda no PDV.

#### Alertas de Nível Mínimo

O PDV poderá exibir alertas visuais para o operador quando um produto adicionado ao carrinho estiver com estoque baixo ou atingir o nível mínimo configurado no Módulo de Controle de Estoque. Isso ajudará a equipe a identificar produtos que precisam ser reabastecidos.

#### Relatórios de Movimentação

As vendas registradas no PDV serão refletidas nos relatórios de movimentação de estoque, fornecendo uma visão completa das entradas e saídas de produtos, contribuindo para a análise de vendas e planejamento de compras.




## 2.1.6. Tecnologias e Ferramentas para o Módulo de Gestão de Vendas (PDV)

Para o desenvolvimento do Módulo de Gestão de Vendas (PDV), serão utilizadas as seguintes tecnologias e ferramentas, alinhadas com a stack tecnológica geral do sistema e otimizadas para a performance e usabilidade exigidas por um ponto de venda:

*   **Backend:** Python com FastAPI.
    *   **Função:** Responsável por expor as APIs RESTful para o registro de vendas, consulta de produtos e clientes, e atualização de estoque. Garantirá a lógica de negócio, validação de dados e persistência no banco de dados.
    *   **Bibliotecas Chave:** SQLAlchemy para ORM, Pydantic para validação de schemas, e possivelmente Redis para cache de produtos e otimização de consultas de alto volume no PDV.
*   **Frontend:** React.js com Material-UI (MUI).
    *   **Função:** Construção da interface de usuário intuitiva e responsiva para o PDV. O React permitirá a criação de componentes reutilizáveis e uma experiência de usuário dinâmica, enquanto o MUI fornecerá um conjunto robusto de componentes de UI pré-construídos e aderentes a um design moderno.
    *   **Bibliotecas Chave:** React Router para navegação, Fetch API ou Axios para requisições HTTP à API do backend.
*   **Banco de Dados:** PostgreSQL.
    *   **Função:** Persistência de todas as informações relacionadas às vendas, itens de venda, e o estado atual do estoque. O PostgreSQL é escolhido por sua robustez, conformidade ACID e capacidade de lidar com grandes volumes de dados transacionais.
*   **Cache (Opcional, mas recomendado para PDV de alto volume):** Redis.
    *   **Função:** Utilizado para armazenar em cache dados frequentemente acessados, como informações de produtos, para reduzir a carga sobre o banco de dados principal e acelerar o tempo de resposta das operações de busca no PDV. Isso é particularmente útil em ambientes de alto volume de vendas.
*   **Containerização:** Docker e Docker Compose.
    *   **Função:** Orquestração de todos os serviços (backend, frontend, banco de dados, Redis) em um ambiente de desenvolvimento e produção. Facilita a implantação, garante a consistência do ambiente e simplifica o gerenciamento de dependências.
*   **Controle de Versão:** Git.
    *   **Função:** Gerenciamento do código-fonte, permitindo o controle de versões, colaboração entre desenvolvedores e rastreamento de todas as alterações.
*   **Testes:** Pytest para backend, React Testing Library para frontend.
    *   **Função:** Garantir a qualidade e a confiabilidade do módulo. Serão implementados testes unitários para a lógica de negócio e testes de integração para os fluxos completos de venda e interação com a API e o banco de dados. Testes de UI com React Testing Library assegurarão a funcionalidade da interface do usuário.




## 2.1.7. Entregáveis Detalhados para o Módulo de Gestão de Vendas (PDV)

Ao final da implementação do Módulo de Gestão de Vendas (PDV), os seguintes entregáveis deverão estar concluídos e validados:

*   **Backend (APIs RESTful):**
    *   Endpoints para criação, leitura, atualização e exclusão de vendas.
    *   Endpoints para adição, remoção e atualização de itens em uma venda.
    *   Endpoints para processamento de diferentes formas de pagamento (dinheiro, cartão, PIX).
    *   Endpoints para consulta de histórico de vendas com filtros.
    *   Lógica de negócio para cálculo de totais, descontos e troco.
    *   Integração com o módulo de estoque para baixa automática de produtos.
    *   Testes unitários e de integração para todas as APIs do PDV.
    *   Documentação da API (Swagger/OpenAPI) atualizada com os novos endpoints.

*   **Frontend (Interface de Usuário):**
    *   Interface de PDV intuitiva e responsiva para registro de vendas.
    *   Funcionalidade de busca de produtos por nome, código de barras ou SKU.
    *   Exibição do carrinho de compras com detalhes dos itens, quantidades e subtotais.
    *   Controles para ajuste de quantidade e remoção de itens do carrinho.
    *   Campo para aplicação de descontos (percentual/valor fixo) por item ou total da venda.
    *   Interface para seleção de formas de pagamento e processamento de pagamentos mistos.
    *   Exibição do troco para pagamentos em dinheiro.
    *   Tela de histórico de vendas com filtros por data, cliente, vendedor e status.
    *   Componentes React reutilizáveis para o PDV.
    *   Testes de componentes e de integração da interface do usuário.

*   **Banco de Dados:**
    *   Tabelas e modelos de dados para vendas, itens de venda e pagamentos.
    *   Migrações Alembic para as novas estruturas de banco de dados.
    *   Índices otimizados para consultas de vendas e histórico.

*   **Infraestrutura (Docker Compose):**
    *   Atualização do `docker-compose.yml` para incluir quaisquer novos serviços ou configurações necessárias para o PDV (ex: Redis, se utilizado).
    *   Ambiente de desenvolvimento funcional com todos os serviços do PDV rodando.

*   **Documentação:**
    *   Atualização do `README.md` com instruções de uso e configuração do PDV.
    *   Documentação técnica detalhada do módulo PDV, incluindo diagramas de fluxo de dados e arquitetura.

*   **Qualidade:**
    *   Cobertura de testes adequada para o backend e frontend do PDV.
    *   Código limpo, modular e seguindo os padrões de codificação definidos.
    *   Performance otimizada para operações de alto volume no PDV.

Esses entregáveis garantirão que o Módulo de Gestão de Vendas (PDV) seja uma solução robusta, funcional e pronta para uso, alinhada com os requisitos do sistema de gestão de lojas.

