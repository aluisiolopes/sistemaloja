import React, { useState } from 'react';
import ProdutoList from './components/ProdutoList';
import ProdutoForm from './components/ProdutoForm';
import ProdutoDetails from './components/ProdutoDetails';

function App() {
    const [currentView, setCurrentView] = useState('list'); // 'list', 'form', 'details'
    const [selectedProduto, setSelectedProduto] = useState(null);

    const handleNewProduto = () => {
        setSelectedProduto(null);
        setCurrentView('form');
    };

    const handleEditProduto = (produto) => {
        setSelectedProduto(produto);
        setCurrentView('form');
    };

    const handleViewProduto = (produto) => {
        setSelectedProduto(produto);
        setCurrentView('details');
    };

    const handleSaveProduto = () => {
        setCurrentView('list');
    };

    const handleCancelForm = () => {
        setCurrentView('list');
    };

    const handleBackToList = () => {
        setCurrentView('list');
    };

    return (
        <div className="min-h-screen bg-gray-100 p-4">
            <header className="bg-white shadow p-4 mb-4 rounded-lg flex justify-between items-center">
                <h1 className="text-3xl font-bold text-gray-800">Gestão de Produtos</h1>
                {currentView === 'list' && (
                    <button
                        onClick={handleNewProduto}
                        className="px-4 py-2 bg-blue-600 text-white rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    >
                        Adicionar Novo Produto
                    </button>
                )}
            </header>

            <main>
                {currentView === 'list' && (
                    <ProdutoList onEdit={handleEditProduto} onSelectProduto={handleViewProduto} />
                )}
                {currentView === 'form' && (
                    <ProdutoForm produto={selectedProduto} onSave={handleSaveProduto} onCancel={handleCancelForm} />
                )}
                {currentView === 'details' && (
                    <ProdutoDetails produto={selectedProduto} onBack={handleBackToList} />
                )}
            </main>
        </div>
    );
}

export default App;


