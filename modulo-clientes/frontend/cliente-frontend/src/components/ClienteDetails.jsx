/**
 * Componente para visualização detalhada de um cliente
 */

import React from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Separator } from './ui/separator';
import { Edit, ArrowLeft, UserX, Trash2 } from 'lucide-react';
import { 
  formatarCpfCnpj, 
  formatarTelefone, 
  formatarCEP,
  formatarData,
  formatarDataHora,
  formatarMoeda,
  formatarPontos,
  formatarStatus,
  formatarTipoCliente
} from '../utils/formatters';

const ClienteDetails = ({ 
  cliente, 
  onVoltar, 
  onEditar, 
  onInativar, 
  onRemover 
}) => {
  if (!cliente) {
    return (
      <div className="text-center py-8">
        <p className="text-muted-foreground">Cliente não encontrado</p>
      </div>
    );
  }

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

  const InfoItem = ({ label, value, className = "" }) => (
    <div className={`space-y-1 ${className}`}>
      <p className="text-sm font-medium text-muted-foreground">{label}</p>
      <p className="text-sm">{value || '-'}</p>
    </div>
  );

  const handleInativar = () => {
    if (window.confirm(`Tem certeza que deseja inativar o cliente "${cliente.nome}"?`)) {
      onInativar(cliente.id);
    }
  };

  const handleRemover = () => {
    if (window.confirm(`Tem certeza que deseja remover o cliente "${cliente.nome}"?`)) {
      onRemover(cliente.id);
    }
  };

  return (
    <div className="space-y-6">
      {/* Cabeçalho */}
      <div className="flex justify-between items-start">
        <div className="flex items-center space-x-4">
          <Button variant="ghost" onClick={onVoltar}>
            <ArrowLeft className="w-4 h-4 mr-2" />
            Voltar
          </Button>
          <div>
            <h1 className="text-3xl font-bold">{cliente.nome}</h1>
            <div className="flex items-center space-x-2 mt-1">
              <StatusBadge status={cliente.status} />
              <Badge variant="outline">
                {formatarTipoCliente(cliente.tipo_cliente)}
              </Badge>
            </div>
          </div>
        </div>
        
        <div className="flex space-x-2">
          <Button onClick={() => onEditar(cliente)}>
            <Edit className="w-4 h-4 mr-2" />
            Editar
          </Button>
          {cliente.status === 'ativo' && (
            <Button variant="outline" onClick={handleInativar}>
              <UserX className="w-4 h-4 mr-2" />
              Inativar
            </Button>
          )}
          <Button variant="destructive" onClick={handleRemover}>
            <Trash2 className="w-4 h-4 mr-2" />
            Remover
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Dados Básicos */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Dados Básicos</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <InfoItem 
                label="Nome Completo" 
                value={cliente.nome} 
              />
              <InfoItem 
                label="Tipo de Cliente" 
                value={formatarTipoCliente(cliente.tipo_cliente)} 
              />
            </div>

            <Separator />

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <InfoItem 
                label={cliente.tipo_cliente === 'pessoa_fisica' ? 'CPF' : 'CNPJ'} 
                value={formatarCpfCnpj(cliente.cpf_cnpj)} 
              />
              <InfoItem 
                label={cliente.tipo_cliente === 'pessoa_fisica' ? 'RG' : 'Inscrição Estadual'} 
                value={cliente.rg_ie} 
              />
            </div>

            {cliente.tipo_cliente === 'pessoa_fisica' && (
              <>
                <Separator />
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <InfoItem 
                    label="Data de Nascimento" 
                    value={formatarData(cliente.data_nascimento)} 
                  />
                  <InfoItem 
                    label="Profissão" 
                    value={cliente.profissao} 
                  />
                </div>
              </>
            )}
          </CardContent>
        </Card>

        {/* Resumo */}
        <Card>
          <CardHeader>
            <CardTitle>Resumo</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <InfoItem 
              label="Status" 
              value={<StatusBadge status={cliente.status} />} 
            />
            <InfoItem 
              label="Limite de Crédito" 
              value={formatarMoeda(cliente.limite_credito)} 
            />
            <InfoItem 
              label="Pontos de Fidelidade" 
              value={formatarPontos(cliente.pontos_fidelidade)} 
            />
            <InfoItem 
              label="Cliente desde" 
              value={formatarData(cliente.data_criacao)} 
            />
          </CardContent>
        </Card>

        {/* Contato */}
        <Card>
          <CardHeader>
            <CardTitle>Contato</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <InfoItem 
              label="Email" 
              value={cliente.email} 
            />
            <InfoItem 
              label="Telefone" 
              value={formatarTelefone(cliente.telefone)} 
            />
            <InfoItem 
              label="Celular" 
              value={formatarTelefone(cliente.celular)} 
            />
          </CardContent>
        </Card>

        {/* Endereço */}
        <Card>
          <CardHeader>
            <CardTitle>Endereço</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <InfoItem 
              label="Logradouro" 
              value={cliente.endereco ? `${cliente.endereco}, ${cliente.numero}` : null} 
            />
            <InfoItem 
              label="Complemento" 
              value={cliente.complemento} 
            />
            <InfoItem 
              label="Bairro" 
              value={cliente.bairro} 
            />
            <div className="grid grid-cols-2 gap-4">
              <InfoItem 
                label="Cidade" 
                value={cliente.cidade} 
              />
              <InfoItem 
                label="Estado" 
                value={cliente.estado} 
              />
            </div>
            <InfoItem 
              label="CEP" 
              value={formatarCEP(cliente.cep)} 
            />
          </CardContent>
        </Card>

        {/* Observações */}
        {cliente.observacoes && (
          <Card className="lg:col-span-3">
            <CardHeader>
              <CardTitle>Observações</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm whitespace-pre-wrap">{cliente.observacoes}</p>
            </CardContent>
          </Card>
        )}

        {/* Auditoria */}
        <Card className="lg:col-span-3">
          <CardHeader>
            <CardTitle>Informações de Auditoria</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <InfoItem 
                label="Criado em" 
                value={formatarDataHora(cliente.data_criacao)} 
              />
              <InfoItem 
                label="Criado por" 
                value={cliente.criado_por} 
              />
              <InfoItem 
                label="Atualizado em" 
                value={formatarDataHora(cliente.data_atualizacao)} 
              />
              <InfoItem 
                label="Atualizado por" 
                value={cliente.atualizado_por} 
              />
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ClienteDetails;

