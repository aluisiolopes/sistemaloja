/**
 * Serviço de API para comunicação com o backend do módulo de clientes
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  /**
   * Faz uma requisição HTTP
   * @param {string} endpoint - Endpoint da API
   * @param {object} options - Opções da requisição
   * @returns {Promise} - Resposta da API
   */
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Erro HTTP: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Erro na requisição:', error);
      throw error;
    }
  }

  /**
   * Requisição GET
   */
  async get(endpoint, params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const url = queryString ? `${endpoint}?${queryString}` : endpoint;
    
    return this.request(url, {
      method: 'GET',
    });
  }

  /**
   * Requisição POST
   */
  async post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  /**
   * Requisição PUT
   */
  async put(endpoint, data) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  /**
   * Requisição DELETE
   */
  async delete(endpoint) {
    return this.request(endpoint, {
      method: 'DELETE',
    });
  }

  /**
   * Requisição PATCH
   */
  async patch(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }
}

// Instância singleton da API
const apiService = new ApiService();

/**
 * Serviços específicos para clientes
 */
export const clienteService = {
  /**
   * Lista clientes com paginação e filtros
   */
  async listar(params = {}) {
    return apiService.get('/clientes', params);
  },

  /**
   * Busca um cliente por ID
   */
  async buscarPorId(id) {
    return apiService.get(`/clientes/${id}`);
  },

  /**
   * Cria um novo cliente
   */
  async criar(dadosCliente) {
    return apiService.post('/clientes', dadosCliente);
  },

  /**
   * Atualiza um cliente existente
   */
  async atualizar(id, dadosCliente) {
    return apiService.put(`/clientes/${id}`, dadosCliente);
  },

  /**
   * Remove um cliente
   */
  async remover(id) {
    return apiService.delete(`/clientes/${id}`);
  },

  /**
   * Inativa um cliente (soft delete)
   */
  async inativar(id, usuario = null) {
    const params = usuario ? { usuario } : {};
    return apiService.patch(`/clientes/${id}/inativar`, params);
  },

  /**
   * Busca clientes por termo
   */
  async buscar(termo, limite = 10) {
    return apiService.get(`/clientes/buscar/${encodeURIComponent(termo)}`, { limite });
  },

  /**
   * Busca cliente por CPF/CNPJ
   */
  async buscarPorCpfCnpj(documento) {
    return apiService.get(`/clientes/cpf-cnpj/${encodeURIComponent(documento)}`);
  },

  /**
   * Busca cliente por email
   */
  async buscarPorEmail(email) {
    return apiService.get(`/clientes/email/${encodeURIComponent(email)}`);
  },

  /**
   * Obtém estatísticas de clientes
   */
  async obterEstatisticas() {
    return apiService.get('/clientes/stats/resumo');
  },
};

export default apiService;

