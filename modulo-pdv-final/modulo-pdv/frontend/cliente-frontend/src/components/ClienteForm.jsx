/**
 * Componente de formulário para criação e edição de clientes
 */

import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Alert, AlertDescription } from './ui/alert';
import { Loader2, Save, X } from 'lucide-react';
import { 
  formatarCpfCnpj, 
  formatarTelefone, 
  formatarCEP,
  limparDocumento,
  limparTelefone,
  limparCEP,
  validarEmail,
  validarCPF,
  validarCNPJ
} from '../utils/formatters';

const ESTADOS_BRASIL = [
  'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
  'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
  'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
];

const ClienteForm = ({ 
  cliente = null, 
  onSubmit, 
  onCancel, 
  loading = false 
}) => {
  const [formData, setFormData] = useState({
    nome: '',
    tipo_cliente: 'pessoa_fisica',
    cpf_cnpj: '',
    rg_ie: '',
    email: '',
    telefone: '',
    celular: '',
    endereco: '',
    numero: '',
    complemento: '',
    bairro: '',
    cidade: '',
    estado: '',
    cep: '',
    data_nascimento: '',
    profissao: '',
    observacoes: '',
    status: 'ativo',
    limite_credito: 0,
    pontos_fidelidade: 0
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Preenche o formulário quando há um cliente para edição
  useEffect(() => {
    if (cliente) {
      setFormData({
        nome: cliente.nome || '',
        tipo_cliente: cliente.tipo_cliente || 'pessoa_fisica',
        cpf_cnpj: cliente.cpf_cnpj || '',
        rg_ie: cliente.rg_ie || '',
        email: cliente.email || '',
        telefone: cliente.telefone || '',
        celular: cliente.celular || '',
        endereco: cliente.endereco || '',
        numero: cliente.numero || '',
        complemento: cliente.complemento || '',
        bairro: cliente.bairro || '',
        cidade: cliente.cidade || '',
        estado: cliente.estado || '',
        cep: cliente.cep || '',
        data_nascimento: cliente.data_nascimento || '',
        profissao: cliente.profissao || '',
        observacoes: cliente.observacoes || '',
        status: cliente.status || 'ativo',
        limite_credito: cliente.limite_credito || 0,
        pontos_fidelidade: cliente.pontos_fidelidade || 0
      });
    }
  }, [cliente]);

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));

    // Remove erro do campo quando o usuário começa a digitar
    if (errors[field]) {
      setErrors(prev => ({
        ...prev,
        [field]: null
      }));
    }
  };

  const handleDocumentoChange = (value) => {
    const documento = limparDocumento(value);
    handleInputChange('cpf_cnpj', documento);
  };

  const handleTelefoneChange = (field, value) => {
    const telefone = limparTelefone(value);
    handleInputChange(field, telefone);
  };

  const handleCepChange = (value) => {
    const cep = limparCEP(value);
    handleInputChange('cep', cep);
  };

  const validateForm = () => {
    const newErrors = {};

    // Nome é obrigatório
    if (!formData.nome.trim()) {
      newErrors.nome = 'Nome é obrigatório';
    }

    // Validação de CPF/CNPJ
    if (formData.cpf_cnpj) {
      if (formData.tipo_cliente === 'pessoa_fisica') {
        if (!validarCPF(formData.cpf_cnpj)) {
          newErrors.cpf_cnpj = 'CPF inválido';
        }
      } else {
        if (!validarCNPJ(formData.cpf_cnpj)) {
          newErrors.cpf_cnpj = 'CNPJ inválido';
        }
      }
    }

    // Validação de email
    if (formData.email && !validarEmail(formData.email)) {
      newErrors.email = 'Email inválido';
    }

    // Validação de CEP
    if (formData.cep && formData.cep.length !== 8) {
      newErrors.cep = 'CEP deve ter 8 dígitos';
    }

    // Validação de estado
    if (formData.estado && !ESTADOS_BRASIL.includes(formData.estado.toUpperCase())) {
      newErrors.estado = 'Estado inválido';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    try {
      // Prepara os dados para envio
      const dadosEnvio = {
        ...formData,
        limite_credito: parseInt(formData.limite_credito) || 0,
        pontos_fidelidade: parseInt(formData.pontos_fidelidade) || 0,
        estado: formData.estado.toUpperCase()
      };

      await onSubmit(dadosEnvio);
    } catch (error) {
      console.error('Erro ao salvar cliente:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const isEditing = !!cliente;

  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardHeader>
        <CardTitle>
          {isEditing ? 'Editar Cliente' : 'Novo Cliente'}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Dados Básicos */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="nome">Nome *</Label>
              <Input
                id="nome"
                value={formData.nome}
                onChange={(e) => handleInputChange('nome', e.target.value)}
                placeholder="Nome completo"
                className={errors.nome ? 'border-red-500' : ''}
              />
              {errors.nome && (
                <p className="text-sm text-red-500">{errors.nome}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="tipo_cliente">Tipo de Cliente</Label>
              <Select
                value={formData.tipo_cliente}
                onValueChange={(value) => handleInputChange('tipo_cliente', value)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="pessoa_fisica">Pessoa Física</SelectItem>
                  <SelectItem value="pessoa_juridica">Pessoa Jurídica</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Documentos */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="cpf_cnpj">
                {formData.tipo_cliente === 'pessoa_fisica' ? 'CPF' : 'CNPJ'}
              </Label>
              <Input
                id="cpf_cnpj"
                value={formatarCpfCnpj(formData.cpf_cnpj)}
                onChange={(e) => handleDocumentoChange(e.target.value)}
                placeholder={formData.tipo_cliente === 'pessoa_fisica' ? '000.000.000-00' : '00.000.000/0000-00'}
                className={errors.cpf_cnpj ? 'border-red-500' : ''}
              />
              {errors.cpf_cnpj && (
                <p className="text-sm text-red-500">{errors.cpf_cnpj}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="rg_ie">
                {formData.tipo_cliente === 'pessoa_fisica' ? 'RG' : 'Inscrição Estadual'}
              </Label>
              <Input
                id="rg_ie"
                value={formData.rg_ie}
                onChange={(e) => handleInputChange('rg_ie', e.target.value)}
                placeholder={formData.tipo_cliente === 'pessoa_fisica' ? 'RG' : 'Inscrição Estadual'}
              />
            </div>
          </div>

          {/* Contato */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => handleInputChange('email', e.target.value)}
                placeholder="email@exemplo.com"
                className={errors.email ? 'border-red-500' : ''}
              />
              {errors.email && (
                <p className="text-sm text-red-500">{errors.email}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="telefone">Telefone</Label>
              <Input
                id="telefone"
                value={formatarTelefone(formData.telefone)}
                onChange={(e) => handleTelefoneChange('telefone', e.target.value)}
                placeholder="(00) 0000-0000"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="celular">Celular</Label>
              <Input
                id="celular"
                value={formatarTelefone(formData.celular)}
                onChange={(e) => handleTelefoneChange('celular', e.target.value)}
                placeholder="(00) 00000-0000"
              />
            </div>
          </div>

          {/* Endereço */}
          <div className="space-y-4">
            <h3 className="text-lg font-medium">Endereço</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="md:col-span-2 space-y-2">
                <Label htmlFor="endereco">Logradouro</Label>
                <Input
                  id="endereco"
                  value={formData.endereco}
                  onChange={(e) => handleInputChange('endereco', e.target.value)}
                  placeholder="Rua, Avenida, etc."
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="numero">Número</Label>
                <Input
                  id="numero"
                  value={formData.numero}
                  onChange={(e) => handleInputChange('numero', e.target.value)}
                  placeholder="123"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="complemento">Complemento</Label>
                <Input
                  id="complemento"
                  value={formData.complemento}
                  onChange={(e) => handleInputChange('complemento', e.target.value)}
                  placeholder="Apto, Sala, etc."
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="space-y-2">
                <Label htmlFor="bairro">Bairro</Label>
                <Input
                  id="bairro"
                  value={formData.bairro}
                  onChange={(e) => handleInputChange('bairro', e.target.value)}
                  placeholder="Bairro"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="cidade">Cidade</Label>
                <Input
                  id="cidade"
                  value={formData.cidade}
                  onChange={(e) => handleInputChange('cidade', e.target.value)}
                  placeholder="Cidade"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="estado">Estado</Label>
                <Select
                  value={formData.estado}
                  onValueChange={(value) => handleInputChange('estado', value)}
                >
                  <SelectTrigger className={errors.estado ? 'border-red-500' : ''}>
                    <SelectValue placeholder="UF" />
                  </SelectTrigger>
                  <SelectContent>
                    {ESTADOS_BRASIL.map(estado => (
                      <SelectItem key={estado} value={estado}>
                        {estado}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                {errors.estado && (
                  <p className="text-sm text-red-500">{errors.estado}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="cep">CEP</Label>
                <Input
                  id="cep"
                  value={formatarCEP(formData.cep)}
                  onChange={(e) => handleCepChange(e.target.value)}
                  placeholder="00000-000"
                  className={errors.cep ? 'border-red-500' : ''}
                />
                {errors.cep && (
                  <p className="text-sm text-red-500">{errors.cep}</p>
                )}
              </div>
            </div>
          </div>

          {/* Dados Adicionais */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-2">
              <Label htmlFor="data_nascimento">Data de Nascimento</Label>
              <Input
                id="data_nascimento"
                type="date"
                value={formData.data_nascimento}
                onChange={(e) => handleInputChange('data_nascimento', e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="profissao">Profissão</Label>
              <Input
                id="profissao"
                value={formData.profissao}
                onChange={(e) => handleInputChange('profissao', e.target.value)}
                placeholder="Profissão"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="status">Status</Label>
              <Select
                value={formData.status}
                onValueChange={(value) => handleInputChange('status', value)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="ativo">Ativo</SelectItem>
                  <SelectItem value="inativo">Inativo</SelectItem>
                  <SelectItem value="bloqueado">Bloqueado</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Observações */}
          <div className="space-y-2">
            <Label htmlFor="observacoes">Observações</Label>
            <Textarea
              id="observacoes"
              value={formData.observacoes}
              onChange={(e) => handleInputChange('observacoes', e.target.value)}
              placeholder="Observações sobre o cliente..."
              rows={3}
            />
          </div>

          {/* Botões */}
          <div className="flex justify-end space-x-4">
            <Button
              type="button"
              variant="outline"
              onClick={onCancel}
              disabled={isSubmitting || loading}
            >
              <X className="w-4 h-4 mr-2" />
              Cancelar
            </Button>
            
            <Button
              type="submit"
              disabled={isSubmitting || loading}
            >
              {isSubmitting || loading ? (
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              ) : (
                <Save className="w-4 h-4 mr-2" />
              )}
              {isEditing ? 'Atualizar' : 'Salvar'}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
};

export default ClienteForm;

