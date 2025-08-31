import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001/api/v1';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// --- Categorias ---
export const getCategorias = async () => {
    const response = await api.get('/categorias/');
    return response.data;
};

export const createCategoria = async (categoriaData) => {
    const response = await api.post('/categorias/', categoriaData);
    return response.data;
};

export const updateCategoria = async (id, categoriaData) => {
    const response = await api.put(`/categorias/${id}`, categoriaData);
    return response.data;
};

export const deleteCategoria = async (id) => {
    const response = await api.delete(`/categorias/${id}`);
    return response.data;
};

// --- Marcas ---
export const getMarcas = async () => {
    const response = await api.get('/marcas/');
    return response.data;
};

export const createMarca = async (marcaData) => {
    const response = await api.post('/marcas/', marcaData);
    return response.data;
};

export const updateMarca = async (id, marcaData) => {
    const response = await api.put(`/marcas/${id}`, marcaData);
    return response.data;
};

export const deleteMarca = async (id) => {
    const response = await api.delete(`/marcas/${id}`);
    return response.data;
};

// --- Produtos ---
export const getProdutos = async (params) => {
    const response = await api.get('/produtos/', { params });
    return response.data;
};

export const getProdutoById = async (id) => {
    const response = await api.get(`/produtos/${id}`);
    return response.data;
};

export const createProduto = async (produtoData) => {
    const response = await api.post('/produtos/', produtoData);
    return response.data;
};

export const updateProduto = async (id, produtoData) => {
    const response = await api.put(`/produtos/${id}`, produtoData);
    return response.data;
};

export const deleteProduto = async (id) => {
    const response = await api.delete(`/produtos/${id}`);
    return response.data;
};

export const inativarProduto = async (id) => {
    const response = await api.patch(`/produtos/${id}/inativar`);
    return response.data;
};

export const searchProdutos = async (termo, limit = 10) => {
    const response = await api.get(`/produtos/search/${termo}`, { params: { limit } });
    return response.data;
};

export const getProdutoStats = async () => {
    const response = await api.get('/produtos/stats/resumo');
    return response.data;
};

export const uploadProdutoImagem = async (produtoId, file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post(`/produtos/${produtoId}/upload-imagem`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

export default api;


