import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { createProduto, updateProduto, getCategorias, getMarcas, uploadProdutoImagem } from '../services/api';
import { formatCurrency } from '../utils/formatters';

const produtoSchema = z.object({
    nome: z.string().min(2, "Nome é obrigatório").max(255),
    descricao: z.string().max(2000).optional().nullable(),
    codigo_barras: z.string().max(255).optional().nullable(),
    sku: z.string().max(255).optional().nullable(),
    preco_venda: z.preprocess(
        (val) => parseInt(String(val).replace(/[^0-9]/g, ''), 10),
        z.number().int().min(0, "Preço de venda deve ser maior ou igual a zero")
    ),
    preco_custo: z.preprocess(
        (val) => parseInt(String(val).replace(/[^0-9]/g, ''), 10),
        z.number().int().min(0, "Preço de custo deve ser maior ou igual a zero")
    ),
    unidade_medida: z.enum(["unidade", "kg", "g", "m", "cm", "mm", "l", "ml", "caixa", "pacote"]),
    categoria_id: z.string().uuid("ID da categoria inválido").optional().nullable(),
    marca_id: z.string().uuid("ID da marca inválido").optional().nullable(),
    status: z.enum(["ativo", "inativo", "esgotado", "promocao"]),
    imagem_url: z.string().url("URL da imagem inválida").optional().nullable(),
    observacoes: z.string().max(2000).optional().nullable(),
});

const ProdutoForm = ({ produto, onSave, onCancel }) => {
    const [categorias, setCategorias] = useState([]);
    const [marcas, setMarcas] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [imageFile, setImageFile] = useState(null);

    const { register, handleSubmit, formState: { errors }, setValue, watch } = useForm({
        resolver: zodResolver(produtoSchema),
        defaultValues: {
            nome: '',
            descricao: '',
            codigo_barras: '',
            sku: '',
            preco_venda: 0,
            preco_custo: 0,
            unidade_medida: 'unidade',
            categoria_id: '',
            marca_id: '',
            status: 'ativo',
            imagem_url: '',
            observacoes: '',
        },
    });

    useEffect(() => {
        const fetchDependencies = async () => {
            try {
                const fetchedCategorias = await getCategorias();
                setCategorias(fetchedCategorias);
                const fetchedMarcas = await getMarcas();
                setMarcas(fetchedMarcas);
            } catch (err) {
                console.error("Erro ao carregar categorias/marcas:", err);
                setError("Não foi possível carregar categorias ou marcas.");
            }
        };
        fetchDependencies();
    }, []);

    useEffect(() => {
        if (produto) {
            for (const key in produto) {
                if (key === 'preco_venda' || key === 'preco_custo') {
                    setValue(key, produto[key]); // Manter como inteiro para edição
                } else if (key === 'categoria' && produto[key]) {
                    setValue('categoria_id', produto[key].id);
                } else if (key === 'marca' && produto[key]) {
                    setValue('marca_id', produto[key].id);
                } else if (key === 'unidade_medida' || key === 'status') {
                    setValue(key, produto[key].value || produto[key]);
                } else {
                    setValue(key, produto[key]);
                }
            }
        }
    }, [produto, setValue]);

    const onSubmit = async (data) => {
        setLoading(true);
        setError(null);
        try {
            let savedProduto;
            const payload = {
                ...data,
                categoria_id: data.categoria_id || null,
                marca_id: data.marca_id || null,
            };

            if (produto) {
                savedProduto = await updateProduto(produto.id, payload);
            } else {
                savedProduto = await createProduto(payload);
            }

            if (imageFile && savedProduto?.id) {
                await uploadProdutoImagem(savedProduto.id, imageFile);
            }

            onSave(savedProduto);
        } catch (err) {
            console.error("Erro ao salvar produto:", err);
            setError(err.response?.data?.detail || "Erro ao salvar produto.");
        } finally {
            setLoading(false);
        }
    };

    const handleImageChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            setImageFile(e.target.files[0]);
        }
    };

    const precoVendaWatch = watch('preco_venda');
    const precoCustoWatch = watch('preco_custo');

    return (
        <div className="p-4 bg-white shadow rounded-lg">
            <h2 className="text-2xl font-bold mb-4">{produto ? 'Editar Produto' : 'Novo Produto'}</h2>
            {error && <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">{error}</div>}
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                <div>
                    <label htmlFor="nome" className="block text-sm font-medium text-gray-700">Nome</label>
                    <input type="text" id="nome" {...register('nome')} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" />
                    {errors.nome && <p className="text-red-500 text-xs mt-1">{errors.nome.message}</p>}
                </div>
                <div>
                    <label htmlFor="descricao" className="block text-sm font-medium text-gray-700">Descrição</label>
                    <textarea id="descricao" {...register('descricao')} rows="3" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"></textarea>
                    {errors.descricao && <p className="text-red-500 text-xs mt-1">{errors.descricao.message}</p>}
                </div>
                <div>
                    <label htmlFor="codigo_barras" className="block text-sm font-medium text-gray-700">Código de Barras</label>
                    <input type="text" id="codigo_barras" {...register('codigo_barras')} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" />
                    {errors.codigo_barras && <p className="text-red-500 text-xs mt-1">{errors.codigo_barras.message}</p>}
                </div>
                <div>
                    <label htmlFor="sku" className="block text-sm font-medium text-gray-700">SKU</label>
                    <input type="text" id="sku" {...register('sku')} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" />
                    {errors.sku && <p className="text-red-500 text-xs mt-1">{errors.sku.message}</p>}
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label htmlFor="preco_venda" className="block text-sm font-medium text-gray-700">Preço de Venda (R$)</label>
                        <input
                            type="text"
                            id="preco_venda"
                            {...register('preco_venda')}
                            value={formatCurrency(precoVendaWatch)}
                            onChange={(e) => {
                                const rawValue = e.target.value.replace(/[^0-9]/g, '');
                                setValue('preco_venda', parseInt(rawValue || '0', 10));
                            }}
                            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                        />
                        {errors.preco_venda && <p className="text-red-500 text-xs mt-1">{errors.preco_venda.message}</p>}
                    </div>
                    <div>
                        <label htmlFor="preco_custo" className="block text-sm font-medium text-gray-700">Preço de Custo (R$)</label>
                        <input
                            type="text"
                            id="preco_custo"
                            {...register('preco_custo')}
                            value={formatCurrency(precoCustoWatch)}
                            onChange={(e) => {
                                const rawValue = e.target.value.replace(/[^0-9]/g, '');
                                setValue('preco_custo', parseInt(rawValue || '0', 10));
                            }}
                            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                        />
                        {errors.preco_custo && <p className="text-red-500 text-xs mt-1">{errors.preco_custo.message}</p>}
                    </div>
                </div>
                <div>
                    <label htmlFor="unidade_medida" className="block text-sm font-medium text-gray-700">Unidade de Medida</label>
                    <select id="unidade_medida" {...register('unidade_medida')} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2">
                        <option value="unidade">Unidade</option>
                        <option value="kg">Kilograma (kg)</option>
                        <option value="g">Grama (g)</option>
                        <option value="m">Metro (m)</option>
                        <option value="cm">Centímetro (cm)</option>
                        <option value="mm">Milímetro (mm)</option>
                        <option value="l">Litro (l)</option>
                        <option value="ml">Mililitro (ml)</option>
                        <option value="caixa">Caixa</option>
                        <option value="pacote">Pacote</option>
                    </select>
                    {errors.unidade_medida && <p className="text-red-500 text-xs mt-1">{errors.unidade_medida.message}</p>}
                </div>
                <div>
                    <label htmlFor="categoria_id" className="block text-sm font-medium text-gray-700">Categoria</label>
                    <select id="categoria_id" {...register('categoria_id')} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2">
                        <option value="">Selecione uma Categoria</option>
                        {categorias.map(cat => (
                            <option key={cat.id} value={cat.id}>{cat.nome}</option>
                        ))}
                    </select>
                    {errors.categoria_id && <p className="text-red-500 text-xs mt-1">{errors.categoria_id.message}</p>}
                </div>
                <div>
                    <label htmlFor="marca_id" className="block text-sm font-medium text-gray-700">Marca</label>
                    <select id="marca_id" {...register('marca_id')} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2">
                        <option value="">Selecione uma Marca</option>
                        {marcas.map(marc => (
                            <option key={marc.id} value={marc.id}>{marc.nome}</option>
                        ))}
                    </select>
                    {errors.marca_id && <p className="text-red-500 text-xs mt-1">{errors.marca_id.message}</p>}
                </div>
                <div>
                    <label htmlFor="status" className="block text-sm font-medium text-gray-700">Status</label>
                    <select id="status" {...register('status')} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2">
                        <option value="ativo">Ativo</option>
                        <option value="inativo">Inativo</option>
                        <option value="esgotado">Esgotado</option>
                        <option value="promocao">Promoção</option>
                    </select>
                    {errors.status && <p className="text-red-500 text-xs mt-1">{errors.status.message}</p>}
                </div>
                <div>
                    <label htmlFor="imagem_url" className="block text-sm font-medium text-gray-700">URL da Imagem</label>
                    <input type="text" id="imagem_url" {...register('imagem_url')} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" />
                    {errors.imagem_url && <p className="text-red-500 text-xs mt-1">{errors.imagem_url.message}</p>}
                </div>
                <div>
                    <label htmlFor="imagem_upload" className="block text-sm font-medium text-gray-700">Upload de Imagem</label>
                    <input type="file" id="imagem_upload" accept="image/*" onChange={handleImageChange} className="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100" />
                </div>
                <div>
                    <label htmlFor="observacoes" className="block text-sm font-medium text-gray-700">Observações</label>
                    <textarea id="observacoes" {...register('observacoes')} rows="3" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"></textarea>
                    {errors.observacoes && <p className="text-red-500 text-xs mt-1">{errors.observacoes.message}</p>}
                </div>

                <div className="flex justify-end space-x-2">
                    <button type="button" onClick={onCancel} className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                        Cancelar
                    </button>
                    <button type="submit" disabled={loading} className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                        {loading ? 'Salvando...' : 'Salvar Produto'}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default ProdutoForm;


