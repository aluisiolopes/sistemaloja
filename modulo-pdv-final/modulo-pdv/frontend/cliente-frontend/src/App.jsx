/**
 * Componente principal da aplicação de gestão de clientes
 */

import React, { useState } from 'react';
import { Toaster } from './components/ui/toaster';
import { useToast } from './hooks/use-toast';
import ClienteList from './components/ClienteList';
import ClienteForm from './components/ClienteForm';
import ClienteDetails from './components/ClienteDetails';
import { clienteService } from './services/api';
import './App.css';

function App() {
  const [view, setView] = useState('list'); // 'list', 'form', 'details'
  const [clienteSelecionado, setClienteSelecionado] = useState(null);
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();

  // Navegação entre views
  const irParaLista = () => {
    setView('list');
    setClienteSelecionado(null);
  };

  const irParaFormulario = (cliente = null) => {
    setClienteSelecionado(cliente);
    setView('form');
  };

  const irParaDetalhes = (cliente) => {
    setClienteSelecionado(cliente);
    setView('details');
  };

  // Handlers para operações CRUD
  const handleNovoCliente = () => {
    irParaFormulario();
  };

  const handleEditarCliente = (cliente) => {
    irParaFormulario(cliente);
  };

  const handleVisualizarCliente = (cliente) => {
    irParaDetalhes(cliente);
  };

  const handleSalvarCliente = async (dadosCliente) => {
    setLoading(true);
    
    try {
      if (clienteSelecionado) {
        // Edição
        await clienteService.atualizar(clienteSelecionado.id, dadosCliente);
        toast({
          title: "Sucesso",
          description: "Cliente atualizado com sucesso!",
        });
      } else {
        // Criação
        await clienteService.criar(dadosCliente);
        toast({
          title: "Sucesso",
          description: "Cliente criado com sucesso!",
        });
      }
      
      irParaLista();
    } catch (error) {
      toast({
        title: "Erro",
        description: error.message || "Erro ao salvar cliente",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleRemoverCliente = async (clienteId) => {
    try {
      await clienteService.remover(clienteId);
      toast({
        title: "Sucesso",
        description: "Cliente removido com sucesso!",
      });
      
      if (view === 'details') {
        irParaLista();
      }
    } catch (error) {
      toast({
        title: "Erro",
        description: error.message || "Erro ao remover cliente",
        variant: "destructive",
      });
      throw error; // Re-throw para que o componente possa tratar
    }
  };

  const handleInativarCliente = async (clienteId) => {
    try {
      await clienteService.inativar(clienteId);
      toast({
        title: "Sucesso",
        description: "Cliente inativado com sucesso!",
      });
      
      if (view === 'details') {
        // Recarrega os dados do cliente para mostrar o status atualizado
        const clienteAtualizado = await clienteService.buscarPorId(clienteId);
        setClienteSelecionado(clienteAtualizado);
      }
    } catch (error) {
      toast({
        title: "Erro",
        description: error.message || "Erro ao inativar cliente",
        variant: "destructive",
      });
      throw error; // Re-throw para que o componente possa tratar
    }
  };

  // Renderização condicional baseada na view atual
  const renderContent = () => {
    switch (view) {
      case 'form':
        return (
          <ClienteForm
            cliente={clienteSelecionado}
            onSubmit={handleSalvarCliente}
            onCancel={irParaLista}
            loading={loading}
          />
        );
      
      case 'details':
        return (
          <ClienteDetails
            cliente={clienteSelecionado}
            onVoltar={irParaLista}
            onEditar={handleEditarCliente}
            onInativar={handleInativarCliente}
            onRemover={handleRemoverCliente}
          />
        );
      
      default:
        return (
          <ClienteList
            onNovoCliente={handleNovoCliente}
            onEditarCliente={handleEditarCliente}
            onVisualizarCliente={handleVisualizarCliente}
            onRemoverCliente={handleRemoverCliente}
            onInativarCliente={handleInativarCliente}
          />
        );
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <h1 
                className="text-2xl font-bold cursor-pointer hover:text-primary"
                onClick={irParaLista}
              >
                Sistema de Gestão de Lojas
              </h1>
              <span className="text-muted-foreground">|</span>
              <span className="text-lg text-muted-foreground">Módulo Clientes</span>
            </div>
            
            {/* Breadcrumb */}
            <nav className="text-sm text-muted-foreground">
              {view === 'list' && 'Lista de Clientes'}
              {view === 'form' && (clienteSelecionado ? 'Editar Cliente' : 'Novo Cliente')}
              {view === 'details' && 'Detalhes do Cliente'}
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {renderContent()}
      </main>

      {/* Footer */}
      <footer className="border-t mt-16">
        <div className="container mx-auto px-4 py-6">
          <div className="text-center text-sm text-muted-foreground">
            <p>Sistema de Gestão de Lojas - Módulo Clientes v1.0.0</p>
            <p className="mt-1">
              Desenvolvido para gestão completa de clientes
            </p>
          </div>
        </div>
      </footer>

      {/* Toast Notifications */}
      <Toaster />
    </div>
  );
}

export default App;

