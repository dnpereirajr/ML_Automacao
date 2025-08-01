import React, { useState, useEffect } from 'react';
import { 
  Play, 
  Square, 
  Settings, 
  Mail, 
  MessageCircle, 
  Search, 
  Clock, 
  CheckCircle, 
  AlertCircle,
  ShoppingCart,
  Zap,
  Globe,
  User
} from 'lucide-react';

interface Product {
  title: string;
  originalPrice: number;
  currentPrice: number;
  discountPercentage: number;
  paymentOptions: string;
  shippingInfo: string;
  feedbackScore: string;
  productUrl: string;
  affiliateUrl: string;
  category: string;
  isPromotion: boolean;
}

interface SystemStatus {
  isRunning: boolean;
  lastExecution: string | null;
  productsFound: number;
  emailsSent: number;
  whatsappSent: number;
}

function App() {
  const [systemStatus, setSystemStatus] = useState<SystemStatus>({
    isRunning: false,
    lastExecution: null,
    productsFound: 0,
    emailsSent: 0,
    whatsappSent: 0
  });

  const [config, setConfig] = useState({
    mercadolivreEmail: '',
    mercadolivrePassword: '',
    gmailEmail: '',
    gmailPassword: '',
    whatsappPhone: '',
    affiliateId: 'ML_DEFAULT',
    intervalHours: 1
  });

  const [products, setProducts] = useState<Product[]>([]);
  const [logs, setLogs] = useState<string[]>([]);
  const [activeTab, setActiveTab] = useState('dashboard');

  const addLog = (message: string) => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs(prev => [`[${timestamp}] ${message}`, ...prev.slice(0, 49)]);
  };

  const startSystem = () => {
    setSystemStatus(prev => ({ ...prev, isRunning: true }));
    addLog('🚀 Sistema iniciado - Agendamento automático ativo');
    addLog('⏰ Próxima execução em 1 hora');
  };

  const stopSystem = () => {
    setSystemStatus(prev => ({ ...prev, isRunning: false }));
    addLog('🛑 Sistema parado');
  };

  const runSingleSearch = () => {
    addLog('🔍 Iniciando busca única...');
    addLog('🔐 Fazendo login no Mercado Livre...');
    
    // Simula busca de produtos
    setTimeout(() => {
      const mockProducts: Product[] = [
        {
          title: 'iPhone 13 128GB - Azul',
          originalPrice: 3999.00,
          currentPrice: 2999.00,
          discountPercentage: 25,
          paymentOptions: '12x de R$ 249,92 sem juros',
          shippingInfo: 'Frete grátis',
          feedbackScore: '⭐ 4.8',
          productUrl: 'https://mercadolivre.com.br/...',
          affiliateUrl: 'https://mercadolivre.com.br/...?affiliateId=ML_DEFAULT',
          category: 'eletrônicos',
          isPromotion: true
        },
        {
          title: 'Notebook Lenovo IdeaPad 3i',
          originalPrice: 2499.00,
          currentPrice: 1999.00,
          discountPercentage: 20,
          paymentOptions: '10x de R$ 199,90 sem juros',
          shippingInfo: 'Frete grátis',
          feedbackScore: '⭐ 4.6',
          productUrl: 'https://mercadolivre.com.br/...',
          affiliateUrl: 'https://mercadolivre.com.br/...?affiliateId=ML_DEFAULT',
          category: 'eletrônicos',
          isPromotion: true
        }
      ];

      setProducts(mockProducts);
      setSystemStatus(prev => ({
        ...prev,
        lastExecution: new Date().toLocaleString(),
        productsFound: mockProducts.length,
        emailsSent: 1,
        whatsappSent: mockProducts.length
      }));

      addLog(`✅ Encontrados ${mockProducts.length} produtos`);
      addLog('📧 Email enviado com sucesso');
      addLog('📱 Mensagens WhatsApp agendadas');
      addLog('🎉 Busca concluída com sucesso!');
    }, 3000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-lg border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-3">
              <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-3 rounded-xl">
                <ShoppingCart className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Sistema Mercado Livre</h1>
                <p className="text-gray-600">Automação Inteligente de Produtos</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className={`flex items-center space-x-2 px-4 py-2 rounded-full ${
                systemStatus.isRunning 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-red-100 text-red-800'
              }`}>
                <div className={`w-2 h-2 rounded-full ${
                  systemStatus.isRunning ? 'bg-green-500' : 'bg-red-500'
                }`}></div>
                <span className="font-medium">
                  {systemStatus.isRunning ? 'Ativo' : 'Parado'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Navigation Tabs */}
        <div className="bg-white rounded-xl shadow-sm mb-8">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-6">
              {[
                { id: 'dashboard', label: 'Dashboard', icon: Globe },
                { id: 'products', label: 'Produtos', icon: ShoppingCart },
                { id: 'config', label: 'Configurações', icon: Settings },
                { id: 'logs', label: 'Logs', icon: Clock }
              ].map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <tab.icon className="w-5 h-5" />
                  <span>{tab.label}</span>
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Dashboard Tab */}
        {activeTab === 'dashboard' && (
          <div className="space-y-8">
            {/* Control Panel */}
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Painel de Controle</h2>
              
              <div className="flex flex-wrap gap-4">
                <button
                  onClick={runSingleSearch}
                  className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
                >
                  <Search className="w-5 h-5" />
                  <span>Busca Única</span>
                </button>

                {!systemStatus.isRunning ? (
                  <button
                    onClick={startSystem}
                    className="flex items-center space-x-2 bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
                  >
                    <Play className="w-5 h-5" />
                    <span>Iniciar Automático</span>
                  </button>
                ) : (
                  <button
                    onClick={stopSystem}
                    className="flex items-center space-x-2 bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg font-medium transition-colors"
                  >
                    <Square className="w-5 h-5" />
                    <span>Parar Sistema</span>
                  </button>
                )}
              </div>
            </div>

            {/* Statistics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white rounded-xl shadow-sm p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Produtos Encontrados</p>
                    <p className="text-3xl font-bold text-gray-900">{systemStatus.productsFound}</p>
                  </div>
                  <div className="bg-blue-100 p-3 rounded-lg">
                    <ShoppingCart className="w-6 h-6 text-blue-600" />
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-xl shadow-sm p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Emails Enviados</p>
                    <p className="text-3xl font-bold text-gray-900">{systemStatus.emailsSent}</p>
                  </div>
                  <div className="bg-green-100 p-3 rounded-lg">
                    <Mail className="w-6 h-6 text-green-600" />
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-xl shadow-sm p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">WhatsApp Enviados</p>
                    <p className="text-3xl font-bold text-gray-900">{systemStatus.whatsappSent}</p>
                  </div>
                  <div className="bg-purple-100 p-3 rounded-lg">
                    <MessageCircle className="w-6 h-6 text-purple-600" />
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-xl shadow-sm p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Última Execução</p>
                    <p className="text-sm font-bold text-gray-900">
                      {systemStatus.lastExecution || 'Nunca'}
                    </p>
                  </div>
                  <div className="bg-orange-100 p-3 rounded-lg">
                    <Clock className="w-6 h-6 text-orange-600" />
                  </div>
                </div>
              </div>
            </div>

            {/* Setup Instructions */}
            <div className="bg-gradient-to-r from-yellow-50 to-orange-50 border border-yellow-200 rounded-xl p-6">
              <div className="flex items-start space-x-3">
                <AlertCircle className="w-6 h-6 text-yellow-600 mt-1" />
                <div>
                  <h3 className="text-lg font-semibold text-yellow-800 mb-2">Instruções de Configuração</h3>
                  <div className="space-y-3 text-yellow-700">
                    <div>
                      <h4 className="font-medium">1. ID de Afiliado (Opcional):</h4>
                      <p className="text-sm">Se você não tem um ID de afiliado do Mercado Livre, deixe como "ML_DEFAULT". Para obter um ID real, cadastre-se no programa de afiliados do Mercado Livre.</p>
                    </div>
                    
                    <div>
                      <h4 className="font-medium">2. Senha de App do Gmail:</h4>
                      <p className="text-sm">
                        • Acesse <a href="https://myaccount.google.com/security" target="_blank" className="text-blue-600 underline">Conta Google → Segurança</a><br/>
                        • Ative a "Verificação em duas etapas" primeiro<br/>
                        • Depois procure por "Senhas de app" na mesma página<br/>
                        • Gere uma senha para "Outro (nome personalizado)"<br/>
                        • Use essa senha de 16 caracteres no campo Gmail Password
                      </p>
                    </div>

                    <div>
                      <h4 className="font-medium">3. Problema do Terminal:</h4>
                      <p className="text-sm">
                        O terminal fecha rapidamente porque falta o arquivo .env ou há erro nas configurações. 
                        Use esta interface web ou adicione <code className="bg-yellow-200 px-1 rounded">input("Pressione Enter...")</code> no final do main.py para manter o terminal aberto.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Products Tab */}
        {activeTab === 'products' && (
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Produtos Encontrados</h2>
              
              {products.length === 0 ? (
                <div className="text-center py-12">
                  <ShoppingCart className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500">Nenhum produto encontrado ainda</p>
                  <p className="text-sm text-gray-400">Execute uma busca para ver os produtos aqui</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {products.map((product, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                      <div className="flex items-start justify-between mb-3">
                        <h3 className="font-semibold text-gray-900 text-lg">{product.title}</h3>
                        <span className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                          {product.category}
                        </span>
                      </div>
                      
                      <div className="space-y-2 mb-4">
                        <div className="flex items-center space-x-2">
                          <span className="text-gray-500 line-through">R$ {product.originalPrice.toFixed(2)}</span>
                          <span className="text-2xl font-bold text-red-600">R$ {product.currentPrice.toFixed(2)}</span>
                          <span className="bg-red-100 text-red-800 text-sm px-2 py-1 rounded">
                            -{product.discountPercentage}%
                          </span>
                        </div>
                        
                        <p className="text-sm text-gray-600">{product.paymentOptions}</p>
                        <p className="text-sm text-gray-600">{product.shippingInfo}</p>
                        <p className="text-sm text-gray-600">{product.feedbackScore}</p>
                      </div>
                      
                      <a
                        href={product.affiliateUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center space-x-2 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                      >
                        <span>📲 COMPRAR AGORA</span>
                      </a>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Configuration Tab */}
        {activeTab === 'config' && (
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Configurações do Sistema</h2>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Email Mercado Livre
                  </label>
                  <input
                    type="email"
                    value={config.mercadolivreEmail}
                    onChange={(e) => setConfig(prev => ({ ...prev, mercadolivreEmail: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="seu_email@gmail.com"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Senha Mercado Livre
                  </label>
                  <input
                    type="password"
                    value={config.mercadolivrePassword}
                    onChange={(e) => setConfig(prev => ({ ...prev, mercadolivrePassword: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="sua_senha"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Email Gmail
                  </label>
                  <input
                    type="email"
                    value={config.gmailEmail}
                    onChange={(e) => setConfig(prev => ({ ...prev, gmailEmail: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="seu_gmail@gmail.com"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Senha de App Gmail
                  </label>
                  <input
                    type="password"
                    value={config.gmailPassword}
                    onChange={(e) => setConfig(prev => ({ ...prev, gmailPassword: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="senha_app_16_caracteres"
                  />
                </div>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Telefone WhatsApp
                  </label>
                  <input
                    type="text"
                    value={config.whatsappPhone}
                    onChange={(e) => setConfig(prev => ({ ...prev, whatsappPhone: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="+5511999999999"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    ID de Afiliado (Opcional)
                  </label>
                  <input
                    type="text"
                    value={config.affiliateId}
                    onChange={(e) => setConfig(prev => ({ ...prev, affiliateId: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="ML_DEFAULT"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Intervalo (horas)
                  </label>
                  <input
                    type="number"
                    value={config.intervalHours}
                    onChange={(e) => setConfig(prev => ({ ...prev, intervalHours: parseInt(e.target.value) }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    min="1"
                    max="24"
                  />
                </div>

                <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg font-medium transition-colors">
                  Salvar Configurações
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Logs Tab */}
        {activeTab === 'logs' && (
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Logs do Sistema</h2>
            
            <div className="bg-gray-900 rounded-lg p-4 h-96 overflow-y-auto">
              {logs.length === 0 ? (
                <p className="text-gray-400">Nenhum log ainda...</p>
              ) : (
                <div className="space-y-1">
                  {logs.map((log, index) => (
                    <div key={index} className="text-green-400 font-mono text-sm">
                      {log}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;