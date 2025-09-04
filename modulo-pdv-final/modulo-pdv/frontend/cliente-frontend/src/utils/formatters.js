/**
 * Utilitários para formatação de dados
 */

/**
 * Formata CPF (000.000.000-00)
 */
export const formatarCPF = (cpf) => {
  if (!cpf) return '';
  const numeros = cpf.replace(/\D/g, '');
  return numeros.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
};

/**
 * Formata CNPJ (00.000.000/0000-00)
 */
export const formatarCNPJ = (cnpj) => {
  if (!cnpj) return '';
  const numeros = cnpj.replace(/\D/g, '');
  return numeros.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
};

/**
 * Formata CPF ou CNPJ automaticamente
 */
export const formatarCpfCnpj = (documento) => {
  if (!documento) return '';
  const numeros = documento.replace(/\D/g, '');
  
  if (numeros.length <= 11) {
    return formatarCPF(numeros);
  } else {
    return formatarCNPJ(numeros);
  }
};

/**
 * Formata telefone (00) 0000-0000 ou (00) 00000-0000
 */
export const formatarTelefone = (telefone) => {
  if (!telefone) return '';
  const numeros = telefone.replace(/\D/g, '');
  
  if (numeros.length <= 10) {
    return numeros.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
  } else {
    return numeros.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
  }
};

/**
 * Formata CEP (00000-000)
 */
export const formatarCEP = (cep) => {
  if (!cep) return '';
  const numeros = cep.replace(/\D/g, '');
  return numeros.replace(/(\d{5})(\d{3})/, '$1-$2');
};

/**
 * Formata data para exibição (DD/MM/AAAA)
 */
export const formatarData = (data) => {
  if (!data) return '';
  
  try {
    const date = new Date(data);
    return date.toLocaleDateString('pt-BR');
  } catch (error) {
    return data;
  }
};

/**
 * Formata data e hora para exibição (DD/MM/AAAA HH:mm)
 */
export const formatarDataHora = (dataHora) => {
  if (!dataHora) return '';
  
  try {
    const date = new Date(dataHora);
    return date.toLocaleString('pt-BR');
  } catch (error) {
    return dataHora;
  }
};

/**
 * Formata valor monetário (R$ 0,00)
 */
export const formatarMoeda = (valor) => {
  if (valor === null || valor === undefined) return 'R$ 0,00';
  
  // Converte centavos para reais
  const valorReais = valor / 100;
  
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(valorReais);
};

/**
 * Formata número de pontos
 */
export const formatarPontos = (pontos) => {
  if (pontos === null || pontos === undefined) return '0';
  
  return new Intl.NumberFormat('pt-BR').format(pontos);
};

/**
 * Capitaliza primeira letra de cada palavra
 */
export const capitalizarNome = (nome) => {
  if (!nome) return '';
  
  return nome
    .toLowerCase()
    .split(' ')
    .map(palavra => palavra.charAt(0).toUpperCase() + palavra.slice(1))
    .join(' ');
};

/**
 * Trunca texto com reticências
 */
export const truncarTexto = (texto, tamanho = 50) => {
  if (!texto) return '';
  
  if (texto.length <= tamanho) return texto;
  
  return texto.substring(0, tamanho) + '...';
};

/**
 * Formata status para exibição
 */
export const formatarStatus = (status) => {
  const statusMap = {
    'ativo': 'Ativo',
    'inativo': 'Inativo',
    'bloqueado': 'Bloqueado'
  };
  
  return statusMap[status] || status;
};

/**
 * Formata tipo de cliente para exibição
 */
export const formatarTipoCliente = (tipo) => {
  const tipoMap = {
    'pessoa_fisica': 'Pessoa Física',
    'pessoa_juridica': 'Pessoa Jurídica'
  };
  
  return tipoMap[tipo] || tipo;
};

/**
 * Remove formatação de documento (CPF/CNPJ)
 */
export const limparDocumento = (documento) => {
  if (!documento) return '';
  return documento.replace(/\D/g, '');
};

/**
 * Remove formatação de telefone
 */
export const limparTelefone = (telefone) => {
  if (!telefone) return '';
  return telefone.replace(/\D/g, '');
};

/**
 * Remove formatação de CEP
 */
export const limparCEP = (cep) => {
  if (!cep) return '';
  return cep.replace(/\D/g, '');
};

/**
 * Valida email
 */
export const validarEmail = (email) => {
  if (!email) return false;
  
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
};

/**
 * Valida CPF (algoritmo básico)
 */
export const validarCPF = (cpf) => {
  if (!cpf) return false;
  
  const numeros = cpf.replace(/\D/g, '');
  
  if (numeros.length !== 11) return false;
  
  // Verifica se todos os dígitos são iguais
  if (/^(\d)\1{10}$/.test(numeros)) return false;
  
  // Aqui poderia implementar a validação completa do CPF
  return true;
};

/**
 * Valida CNPJ (algoritmo básico)
 */
export const validarCNPJ = (cnpj) => {
  if (!cnpj) return false;
  
  const numeros = cnpj.replace(/\D/g, '');
  
  if (numeros.length !== 14) return false;
  
  // Verifica se todos os dígitos são iguais
  if (/^(\d)\1{13}$/.test(numeros)) return false;
  
  // Aqui poderia implementar a validação completa do CNPJ
  return true;
};

