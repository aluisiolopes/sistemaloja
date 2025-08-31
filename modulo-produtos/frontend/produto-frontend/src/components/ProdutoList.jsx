import React, { useState, useEffect } from 'react';
import { getProdutos, deleteProduto, inativarProduto, searchProdutos } from '../services/api';
import { formatCurrency, capitalizeFirstLetter } from '../utils/formatters';

const ProdutoList = ({ onEdit, onSelectProduto }) => {
    const [produtos, setProdutos] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [page, setPage] = useState(1);
    const [limit, setLimit] = useState(10);
    const [totalProdutos, setTotalProdutos] = useState(0);
    const [searchTerm, setSearchTerm] = useState('');
    const [filters, setFilters] = useState({});

    const fetchProdutos = async () => {
        setLoading(true);
        setError(null);
        try {
            const params = {
                skip: (page - 1) * limit,
                limit: limit,
                ...filters,
            };
            const data = await getProdutos(params);
            setProdutos(data.produtos);
            setTotalProdutos(data.total);
        } catch (err) {
            console.error("Erro ao buscar produtos:", err);
            setError(err.response?.data?.detail || "Erro ao carregar produtos.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchProdutos();
    }, [page, limit, filters]);

    const handleDelete = async (id) => {
        if (window.confirm("Tem certeza que deseja remover este produto?")) {
            try {
                await deleteProduto(id);
                fetchProdutos();
            } catch (err) {
                console.error("Erro ao remover produto:", err);
                setError(err.response?.data?.detail || "Erro ao remover produto.");
            }
        }
    };

    const handleInativar = async (id) => {
        if (window.confirm("Tem certeza que deseja inativar este produto?")) {
            try {
                await inativarProduto(id);
                fetchProdutos();
            } catch (err) {
                console.error("Erro ao inativar produto:", err);
                setError(err.response?.data?.detail || "Erro ao inativar produto.");
            }
        }
    };

    const handleSearch = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            if (searchTerm.trim() === '') {
                setFilters({});
                setPage(1);
                fetchProdutos();
                return;
            }
            const data = await searchProdutos(searchTerm);
            setProdutos(data);
            setTotalProdutos(data.length);
            setPage(1);
        } catch (err) {
            console.error("Erro ao buscar produtos:", err);
            setError(err.response?.data?.detail || "Erro ao buscar produtos.");
        } finally {
            setLoading(false);
        }
    };

    const handleFilterChange = (e) => {
        setFilters({
            ...filters,
            [e.target.name]: e.target.value || undefined,
        });
        setPage(1);
    };

    if (loading) return <div className="text-center p-4">Carregando produtos...</div>;
    if (error) return <div className="text-center p-4 text-red-500">Erro: {error}</div>;

    return (
        <div className="p-4 bg-white shadow rounded-lg">
            <h2 className="text-2xl font-bold mb-4">Lista de Produtos</h2>

            <form onSubmit={handleSearch} className="mb-4 flex space-x-2">
                <input
                    type="text"
                    placeholder="Buscar por nome, SKU, código de barras..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="flex-grow p-2 border border-gray-300 rounded-md shadow-sm"
                />
                <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded-md shadow-sm hover:bg-blue-700">
                    Buscar
                </button>
                <button type="button" onClick={() => {
                    setSearchTerm('');
                    setFilters({});
                    setPage(1);
                }} className="px-4 py-2 bg-gray-300 text-gray-800 rounded-md shadow-sm hover:bg-gray-400">
                    Limpar
                </button>
            </form>

            <div className="mb-4 grid grid-cols-1 md:grid-cols-3 gap-4">
                <select name="status" onChange={handleFilterChange} className="p-2 border border-gray-300 rounded-md shadow-sm">
                    <option value="">Filtrar por Status</option>
                    <option value="ativo">Ativo</option>
                    <option value="inativo">Inativo</option>
                    <option value="esgotado">Esgotado</option>
                    <option value="promocao">Promoção</option>
                </select>
                {/* Adicionar mais filtros aqui, como categoria, marca, etc. */}
            </div>

            {produtos.length === 0 ? (
                <p className="text-center text-gray-500">Nenhum produto encontrado.</p>
            ) : (
                <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                            <tr>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">SKU</th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Preço Venda</th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Unidade</th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                            {produtos.map((produto) => (
                                <tr key={produto.id} className="hover:bg-gray-100">
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{produto.nome}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{produto.sku}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{formatCurrency(produto.preco_venda)}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{capitalizeFirstLetter(produto.unidade_medida)}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{capitalizeFirstLetter(produto.status)}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                        <button onClick={() => onSelectProduto(produto)} className="text-blue-600 hover:text-blue-900 mr-2">Ver</button>
                                        <button onClick={() => onEdit(produto)} className="text-indigo-600 hover:text-indigo-900 mr-2">Editar</button>
                                        <button onClick={() => handleInativar(produto.id)} className="text-yellow-600 hover:text-yellow-900 mr-2">Inativar</button>
                                        <button onClick={() => handleDelete(produto.id)} className="text-red-600 hover:text-red-900">Remover</button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

            <div className="mt-4 flex justify-between items-center">
                <div>
                    Página {page} de {Math.ceil(totalProdutos / limit)}
                </div>
                <div className="flex space-x-2">
                    <button
                        onClick={() => setPage(prev => Math.max(prev - 1, 1))}
                        disabled={page === 1}
                        className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
                    >
                        Anterior
                    </button>
                    <button
                        onClick={() => setPage(prev => prev + 1)}
                        disabled={page * limit >= totalProdutos}
                        className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
                    >
                        Próxima
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ProdutoList;


