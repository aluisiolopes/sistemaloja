import React from 'react';
import { formatCurrency, formatDate, capitalizeFirstLetter } from '../utils/formatters';

const ProdutoDetails = ({ produto, onBack }) => {
    if (!produto) {
        return (
            <div className="p-4 bg-white shadow rounded-lg">
                <p className="text-center text-gray-500">Nenhum produto selecionado.</p>
                <div className="mt-4 flex justify-end">
                    <button onClick={onBack} className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
                        Voltar para a Lista
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="p-4 bg-white shadow rounded-lg">
            <h2 className="text-2xl font-bold mb-4">Detalhes do Produto: {produto.nome}</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-gray-700">
                <div>
                    <p><strong>ID:</strong> {produto.id}</p>
                    <p><strong>Nome:</strong> {produto.nome}</p>
                    <p><strong>Descrição:</strong> {produto.descricao || 'N/A'}</p>
                    <p><strong>Código de Barras:</strong> {produto.codigo_barras || 'N/A'}</p>
                    <p><strong>SKU:</strong> {produto.sku || 'N/A'}</p>
                    <p><strong>Preço de Venda:</strong> {formatCurrency(produto.preco_venda)}</p>
                    <p><strong>Preço de Custo:</strong> {formatCurrency(produto.preco_custo)}</p>
                    <p><strong>Unidade de Medida:</strong> {capitalizeFirstLetter(produto.unidade_medida)}</p>
                </div>
                <div>
                    <p><strong>Categoria:</strong> {produto.categoria_nome || 'N/A'}</p>
                    <p><strong>Marca:</strong> {produto.marca_nome || 'N/A'}</p>
                    <p><strong>Status:</strong> {capitalizeFirstLetter(produto.status)}</p>
                    <p><strong>URL da Imagem:</strong> {produto.imagem_url ? <a href={produto.imagem_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">Ver Imagem</a> : 'N/A'}</p>
                    <p><strong>Observações:</strong> {produto.observacoes || 'N/A'}</p>
                    <p><strong>Data de Criação:</strong> {formatDate(produto.data_criacao)}</p>
                    <p><strong>Última Atualização:</strong> {produto.data_atualizacao ? formatDate(produto.data_atualizacao) : 'N/A'}</p>
                    <p><strong>Criado Por:</strong> {produto.criado_por || 'N/A'}</p>
                    <p><strong>Atualizado Por:</strong> {produto.atualizado_por || 'N/A'}</p>
                </div>
            </div>
            {produto.imagem_url && (
                <div className="mt-4 text-center">
                    <img src={produto.imagem_url} alt={produto.nome} className="max-w-xs mx-auto rounded-lg shadow-md" />
                </div>
            )}
            <div className="mt-6 flex justify-end space-x-2">
                <button onClick={onBack} className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                    Voltar para a Lista
                </button>
            </div>
        </div>
    );
};

export default ProdutoDetails;


