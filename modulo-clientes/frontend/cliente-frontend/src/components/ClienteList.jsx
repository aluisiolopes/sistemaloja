/**
 * Componente de listagem de clientes com filtros e paginação
 */

import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Alert, AlertDescription } from './ui/alert';
import { clienteService } from '../services/api'; // Linha adicionada pra resovler erro de import cliente
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from './ui/table';
import { 
  Search, 
  Filter, 
  Plus, 
  Edit, 
  Trash2, 
  Eye, 
  ChevronLeft, 
  ChevronRight,
  Loader2,
  UserX
} from 'lucide-react';
import { 
  formatarCpfCnpj, 
  formatarTelefone, 
  formatarDataHora,
  formatarStatus,
  formatarTipoCliente,
  truncarTexto
} from '../utils/formatters';

const ESTADOS_BRASIL = [
  'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
  'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
  'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
];

const ClienteList = ({ 
  onNovoCliente, 
  onEditarCliente, 
  onVisualizarCliente,
  onRemoverCliente,
  onInativarCliente
}) => {
  const [clientes, setClientes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filtrosVisiveis, setFiltrosVisiveis] = useState(false);

  // Estados para paginação
  const [paginaAtual, setPaginaAtual] = useState(1);
  const [totalPaginas, setTotalPaginas] = useState(1);
  const [totalRegistros, setTotalRegistros] = useState(0);
  const [itensPorPagina] = useState(20);

  // Estados para filtros
  const [filtros, setFiltros] = useState({
    nome: '',
    tipo_cliente: '',
    status: '',
    cidade: '',
    estado: '',
    cpf_cnpj: '',
    email: ''
  });

  const [termoBusca, setTermoBusca] = useState('');

  // Carrega a lista de clientes
  const carregarClientes = async (pagina = 1, filtrosAplicados = filtros) => {
    setLoading(true);
    setError(null);

    try {
      const params = {
        pagina,
        por_pagina: itensPorPagina,
        ...filtrosAplicados
      };

      // Remove filtros vazios
      Object.keys(params).forEach(key => {
        if (!params[key]) {
          delete params[key];
        }
      });

      const response = await clienteService.listar(params);
      
      setClientes(response.clientes);
      setTotalPaginas(response.total_paginas);
      setTotalRegistros(response.total);
      setPaginaAtual(response.pagina);
    } catch (err) {
      setError('Erro ao carregar clientes: ' + err.message);
      setClientes([]);
    } finally {
      setLoading(false);
    }
  };

  // Carrega clientes na inicialização
  useEffect(() => {
    carregarClientes();
  }, []);

  // Handlers para filtros
  const handleFiltroChange = (campo, valor) => {
    setFiltros(prev => ({
      ...prev,
      [campo]: valor
    }));
  };

  const aplicarFiltros = () => {
    setPaginaAtual(1);
    carregarClientes(1, filtros);
  };

  const limparFiltros = () => {
    const filtrosLimpos = {
      nome: '',
      tipo_cliente: '',
      status: '',
      cidade: '',
      estado: '',
      cpf_cnpj: '',
      email: ''
    };
    setFiltros(filtrosLimpos);
    setPaginaAtual(1);
    carregarClientes(1, filtrosLimpos);
  };

  // Busca rápida
  const handleBuscaRapida = async () => {
    if (!termoBusca.trim()) {
      carregarClientes();
      return;
    }

    setLoading(true);
    try {
      const response = await clienteService.buscar(termoBusca, 50);
      setClientes(response);
      setTotalPaginas(1);
      setTotalRegistros(response.length);
      setPaginaAtual(1);
    } catch (err) {
      setError('Erro na busca: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Navegação de páginas
  const irParaPagina = (pagina) => {
    if (pagina >= 1 && pagina <= totalPaginas) {
      carregarClientes(pagina, filtros);
    }
  };

  // Handlers para ações
  const handleRemover = async (cliente) => {
    if (window.confirm(`Tem certeza que deseja remover o cliente "${cliente.nome}"?`)) {
      try {
        await onRemoverCliente(cliente.id);
        carregarClientes(paginaAtual, filtros);
      } catch (err) {
        setError('Erro ao remover cliente: ' + err.message);
      }
    }
  };

  const handleInativar = async (cliente) => {
    if (window.confirm(`Tem certeza que deseja inativar o cliente "${cliente.nome}"?`)) {
      try {
        await onInativarCliente(cliente.id);
        carregarClientes(paginaAtual, filtros);
      } catch (err) {
        setError('Erro ao inativar cliente: ' + err.message);
      }
    }
  };

  // Componente de badge para status
  const StatusBadge = ({ status }) => {
    const variants = {
      'ativo': 'default',
      'inativo': 'secondary',
      'bloqueado': 'destructive'
    };

    return (
      <Badge variant={variants[status] || 'default'}>
        {formatarStatus(status)}
      </Badge>
    );
  };

  return (
    <div className="space-y-6">
      {/* Cabeçalho */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Clientes</h1>
          <p className="text-muted-foreground">
            {totalRegistros} cliente{totalRegistros !== 1 ? 's' : ''} encontrado{totalRegistros !== 1 ? 's' : ''}
          </p>
        </div>
        <Button onClick={onNovoCliente}>
          <Plus className="w-4 h-4 mr-2" />
          Novo Cliente
        </Button>
      </div>

      {/* Busca Rápida e Filtros */}
      <Card>
        <CardContent className="pt-6">
          <div className="space-y-4">
            {/* Busca Rápida */}
            <div className="flex space-x-2">
              <div className="flex-1">
                <Input
                  placeholder="Buscar por nome, email ou CPF/CNPJ..."
                  value={termoBusca}
                  onChange={(e) => setTermoBusca(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleBuscaRapida()}
                />
              </div>
              <Button onClick={handleBuscaRapida} disabled={loading}>
                <Search className="w-4 h-4" />
              </Button>
              <Button 
                variant="outline" 
                onClick={() => setFiltrosVisiveis(!filtrosVisiveis)}
              >
                <Filter className="w-4 h-4 mr-2" />
                Filtros
              </Button>
            </div>

            {/* Filtros Avançados */}
            {filtrosVisiveis && (
              <div className="border-t pt-4 space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
                  <div className="space-y-2">
                    <Label>Nome</Label>
                    <Input
                      placeholder="Nome do cliente"
                      value={filtros.nome}
                      onChange={(e) => handleFiltroChange('nome', e.target.value)}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label>Tipo</Label>
                    <Select
                      value={filtros.tipo_cliente}
                      onValueChange={(value) => handleFiltroChange('tipo_cliente', value)}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Todos" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="">Todos</SelectItem>
                        <SelectItem value="pessoa_fisica">Pessoa Física</SelectItem>
                        <SelectItem value="pessoa_juridica">Pessoa Jurídica</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label>Status</Label>
                    <Select
                      value={filtros.status}
                      onValueChange={(value) => handleFiltroChange('status', value)}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Todos" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="">Todos</SelectItem>
                        <SelectItem value="ativo">Ativo</SelectItem>
                        <SelectItem value="inativo">Inativo</SelectItem>
                        <SelectItem value="bloqueado">Bloqueado</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label>Estado</Label>
                    <Select
                      value={filtros.estado}
                      onValueChange={(value) => handleFiltroChange('estado', value)}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Todos" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="">Todos</SelectItem>
                        {ESTADOS_BRASIL.map(estado => (
                          <SelectItem key={estado} value={estado}>
                            {estado}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label>Cidade</Label>
                    <Input
                      placeholder="Cidade"
                      value={filtros.cidade}
                      onChange={(e) => handleFiltroChange('cidade', e.target.value)}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label>CPF/CNPJ</Label>
                    <Input
                      placeholder="CPF ou CNPJ"
                      value={filtros.cpf_cnpj}
                      onChange={(e) => handleFiltroChange('cpf_cnpj', e.target.value)}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label>Email</Label>
                    <Input
                      placeholder="Email"
                      value={filtros.email}
                      onChange={(e) => handleFiltroChange('email', e.target.value)}
                    />
                  </div>
                </div>

                <div className="flex space-x-2">
                  <Button onClick={aplicarFiltros} disabled={loading}>
                    Aplicar Filtros
                  </Button>
                  <Button variant="outline" onClick={limparFiltros}>
                    Limpar
                  </Button>
                </div>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Mensagem de Erro */}
      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Tabela de Clientes */}
      <Card>
        <CardContent className="p-0">
          {loading ? (
            <div className="flex justify-center items-center py-8">
              <Loader2 className="w-8 h-8 animate-spin" />
            </div>
          ) : clientes.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-muted-foreground">Nenhum cliente encontrado</p>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Nome</TableHead>
                  <TableHead>Tipo</TableHead>
                  <TableHead>CPF/CNPJ</TableHead>
                  <TableHead>Email</TableHead>
                  <TableHead>Telefone</TableHead>
                  <TableHead>Cidade</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Criado em</TableHead>
                  <TableHead className="text-right">Ações</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {clientes.map((cliente) => (
                  <TableRow key={cliente.id}>
                    <TableCell className="font-medium">
                      {truncarTexto(cliente.nome, 30)}
                    </TableCell>
                    <TableCell>
                      {formatarTipoCliente(cliente.tipo_cliente)}
                    </TableCell>
                    <TableCell>
                      {formatarCpfCnpj(cliente.cpf_cnpj)}
                    </TableCell>
                    <TableCell>
                      {truncarTexto(cliente.email, 25)}
                    </TableCell>
                    <TableCell>
                      {formatarTelefone(cliente.celular || cliente.telefone)}
                    </TableCell>
                    <TableCell>
                      {cliente.cidade} - {cliente.estado}
                    </TableCell>
                    <TableCell>
                      <StatusBadge status={cliente.status} />
                    </TableCell>
                    <TableCell>
                      {formatarDataHora(cliente.data_criacao)}
                    </TableCell>
                    <TableCell className="text-right">
                      <div className="flex justify-end space-x-1">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => onVisualizarCliente(cliente)}
                        >
                          <Eye className="w-4 h-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => onEditarCliente(cliente)}
                        >
                          <Edit className="w-4 h-4" />
                        </Button>
                        {cliente.status === 'ativo' && (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleInativar(cliente)}
                          >
                            <UserX className="w-4 h-4" />
                          </Button>
                        )}
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleRemover(cliente)}
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>

      {/* Paginação */}
      {totalPaginas > 1 && (
        <div className="flex justify-between items-center">
          <p className="text-sm text-muted-foreground">
            Página {paginaAtual} de {totalPaginas}
          </p>
          <div className="flex space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => irParaPagina(paginaAtual - 1)}
              disabled={paginaAtual === 1 || loading}
            >
              <ChevronLeft className="w-4 h-4" />
              Anterior
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => irParaPagina(paginaAtual + 1)}
              disabled={paginaAtual === totalPaginas || loading}
            >
              Próxima
              <ChevronRight className="w-4 h-4" />
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ClienteList;

