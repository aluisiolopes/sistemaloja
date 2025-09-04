import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Search, ShoppingCart, Trash2, Plus, Minus, CreditCard, Banknote, Smartphone } from 'lucide-react';
import './PDVInterface.css';

const PDVInterface = () => {
  const [carrinho, setCarrinho] = useState([]);
  const [busca, setBusca] = useState('');
  const [cliente, setCliente] = useState(null);
  const [desconto, setDesconto] = useState(0);
  const [formaPagamento, setFormaPagamento] = useState('dinheiro');
  const [valorRecebido, setValorRecebido] = useState('');
  const [produtos] = useState([
    { id: 1, nome: 'Produto A', preco: 1500, codigo: '123456789', estoque: 10 },
    { id: 2, nome: 'Produto B', preco: 2500, codigo: '987654321', estoque: 5 },
    { id: 3, nome: 'Produto C', preco: 3000, codigo: '456789123', estoque: 8 },
  ]);

  const adicionarProduto = (produto) => {
    const itemExistente = carrinho.find(item => item.id === produto.id);
    if (itemExistente) {
      setCarrinho(carrinho.map(item =>
        item.id === produto.id
          ? { ...item, quantidade: item.quantidade + 1 }
          : item
      ));
    } else {
      setCarrinho([...carrinho, { ...produto, quantidade: 1 }]);
    }
  };

  const removerProduto = (produtoId) => {
    setCarrinho(carrinho.filter(item => item.id !== produtoId));
  };

  const alterarQuantidade = (produtoId, novaQuantidade) => {
    if (novaQuantidade <= 0) {
      removerProduto(produtoId);
      return;
    }
    setCarrinho(carrinho.map(item =>
      item.id === produtoId
        ? { ...item, quantidade: novaQuantidade }
        : item
    ));
  };

  const calcularSubtotal = () => {
    return carrinho.reduce((total, item) => total + (item.preco * item.quantidade), 0);
  };

  const calcularTotal = () => {
    return calcularSubtotal() - desconto;
  };

  const calcularTroco = () => {
    if (formaPagamento === 'dinheiro' && valorRecebido) {
      return parseFloat(valorRecebido) * 100 - calcularTotal();
    }
    return 0;
  };

  const formatarMoeda = (valor) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(valor / 100);
  };

  const produtosFiltrados = produtos.filter(produto =>
    produto.nome.toLowerCase().includes(busca.toLowerCase()) ||
    produto.codigo.includes(busca)
  );

  const finalizarVenda = () => {
    if (carrinho.length === 0) {
      alert('Carrinho vazio!');
      return;
    }

    const venda = {
      itens: carrinho.map(item => ({
        produto_id: item.id,
        quantidade: item.quantidade,
        preco_unitario: item.preco,
        desconto_item: 0
      })),
      pagamentos: [{
        forma_pagamento: formaPagamento,
        valor_pago: calcularTotal(),
        valor_recebido: formaPagamento === 'dinheiro' ? parseFloat(valorRecebido) * 100 : null
      }],
      desconto_total: desconto,
      cliente_id: cliente?.id || null
    };

    console.log('Venda finalizada:', venda);
    alert('Venda finalizada com sucesso!');
    
    // Limpar carrinho
    setCarrinho([]);
    setDesconto(0);
    setValorRecebido('');
    setCliente(null);
  };

  return (
    <div className="pdv-container">
      <div className="pdv-header">
        <h1 className="pdv-title">Sistema PDV - Ponto de Venda</h1>
        <Badge variant="outline" className="pdv-status">
          Online
        </Badge>
      </div>

      <div className="pdv-main">
        {/* Seção de Busca de Produtos */}
        <div className="pdv-search-section">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Search className="h-5 w-5" />
                Buscar Produtos
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Input
                placeholder="Digite o nome ou código do produto..."
                value={busca}
                onChange={(e) => setBusca(e.target.value)}
                className="mb-4"
              />
              <div className="produtos-grid">
                {produtosFiltrados.map(produto => (
                  <Card key={produto.id} className="produto-card">
                    <CardContent className="p-4">
                      <h3 className="font-semibold">{produto.nome}</h3>
                      <p className="text-sm text-gray-600">Código: {produto.codigo}</p>
                      <p className="text-lg font-bold text-green-600">
                        {formatarMoeda(produto.preco)}
                      </p>
                      <p className="text-sm">Estoque: {produto.estoque}</p>
                      <Button
                        onClick={() => adicionarProduto(produto)}
                        className="w-full mt-2"
                        size="sm"
                      >
                        <Plus className="h-4 w-4 mr-1" />
                        Adicionar
                      </Button>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Seção do Carrinho */}
        <div className="pdv-cart-section">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <ShoppingCart className="h-5 w-5" />
                Carrinho de Compras
              </CardTitle>
            </CardHeader>
            <CardContent>
              {carrinho.length === 0 ? (
                <p className="text-center text-gray-500 py-8">
                  Carrinho vazio
                </p>
              ) : (
                <div className="carrinho-items">
                  {carrinho.map(item => (
                    <div key={item.id} className="carrinho-item">
                      <div className="item-info">
                        <h4 className="font-semibold">{item.nome}</h4>
                        <p className="text-sm text-gray-600">
                          {formatarMoeda(item.preco)} cada
                        </p>
                      </div>
                      <div className="item-controls">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => alterarQuantidade(item.id, item.quantidade - 1)}
                        >
                          <Minus className="h-4 w-4" />
                        </Button>
                        <span className="quantidade">{item.quantidade}</span>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => alterarQuantidade(item.id, item.quantidade + 1)}
                        >
                          <Plus className="h-4 w-4" />
                        </Button>
                        <Button
                          variant="destructive"
                          size="sm"
                          onClick={() => removerProduto(item.id)}
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                      <div className="item-total">
                        {formatarMoeda(item.preco * item.quantidade)}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              <Separator className="my-4" />

              {/* Totais */}
              <div className="totais">
                <div className="total-line">
                  <span>Subtotal:</span>
                  <span>{formatarMoeda(calcularSubtotal())}</span>
                </div>
                <div className="total-line">
                  <span>Desconto:</span>
                  <Input
                    type="number"
                    value={desconto / 100}
                    onChange={(e) => setDesconto(parseFloat(e.target.value || 0) * 100)}
                    className="w-24 text-right"
                    step="0.01"
                  />
                </div>
                <div className="total-line total-final">
                  <span>Total:</span>
                  <span>{formatarMoeda(calcularTotal())}</span>
                </div>
              </div>

              <Separator className="my-4" />

              {/* Formas de Pagamento */}
              <div className="pagamento-section">
                <h3 className="font-semibold mb-3">Forma de Pagamento</h3>
                <div className="pagamento-opcoes">
                  <Button
                    variant={formaPagamento === 'dinheiro' ? 'default' : 'outline'}
                    onClick={() => setFormaPagamento('dinheiro')}
                    className="pagamento-btn"
                  >
                    <Banknote className="h-4 w-4 mr-2" />
                    Dinheiro
                  </Button>
                  <Button
                    variant={formaPagamento === 'cartao_credito' ? 'default' : 'outline'}
                    onClick={() => setFormaPagamento('cartao_credito')}
                    className="pagamento-btn"
                  >
                    <CreditCard className="h-4 w-4 mr-2" />
                    Cartão
                  </Button>
                  <Button
                    variant={formaPagamento === 'pix' ? 'default' : 'outline'}
                    onClick={() => setFormaPagamento('pix')}
                    className="pagamento-btn"
                  >
                    <Smartphone className="h-4 w-4 mr-2" />
                    PIX
                  </Button>
                </div>

                {formaPagamento === 'dinheiro' && (
                  <div className="dinheiro-section">
                    <Input
                      type="number"
                      placeholder="Valor recebido"
                      value={valorRecebido}
                      onChange={(e) => setValorRecebido(e.target.value)}
                      className="mt-3"
                      step="0.01"
                    />
                    {valorRecebido && (
                      <div className="troco-info">
                        <span>Troco: {formatarMoeda(calcularTroco())}</span>
                      </div>
                    )}
                  </div>
                )}
              </div>

              <Button
                onClick={finalizarVenda}
                className="w-full mt-4 finalizar-btn"
                size="lg"
                disabled={carrinho.length === 0}
              >
                Finalizar Venda
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default PDVInterface;

