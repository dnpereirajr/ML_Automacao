# Sistema Automatizado Mercado Livre

Sistema completo em Python para automação de busca, classificação e envio de produtos do Mercado Livre via email e WhatsApp.

## 🚀 Funcionalidades

- **🔐 Login Automático**: Login seguro no Mercado Livre
- **🔍 Busca Inteligente**: Produtos em promoção e normais
- **📊 Classificação Automática**: Categorização por tipo (eletrônicos, roupas, casa, etc.)
- **💰 Links de Afiliado**: Geração automática de links com seu ID
- **📧 Email Elegante**: Template HTML moderno e responsivo
- **📱 WhatsApp Individual**: Mensagem separada por produto
- **⏰ Agendamento**: Envios automáticos a cada hora
- **🖥️ Interface Terminal**: Controle completo via linha de comando

## 📋 Pré-requisitos

- Python 3.8+
- Google Chrome ou Chromium instalado
- Conta Gmail com senha de app configurada
- WhatsApp Web ativo no navegador
- Conta no Mercado Livre

## 🛠️ Instalação

1. **Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd mercadolivre-automation
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente:**
```bash
cp .env.example .env
```

4. **Edite o arquivo `.env` com suas credenciais:**
```env
MERCADOLIVRE_EMAIL=seu_email@gmail.com
MERCADOLIVRE_PASSWORD=sua_senha
GMAIL_EMAIL=seu_gmail@gmail.com
GMAIL_PASSWORD=sua_senha_app_gmail
WHATSAPP_PHONE=+5511999999999
AFFILIATE_ID=seu_id_afiliado
```

## 🎯 Como Usar

### Execução Simples
```bash
python main.py
```

### Menu Principal
O sistema oferece as seguintes opções:

1. **Executar busca única** - Teste o sistema uma vez
2. **Iniciar agendamento automático** - Ativação do modo automático
3. **Parar agendamento** - Desativa o modo automático
4. **Ver configurações** - Mostra status da configuração
5. **Ajuda** - Instruções detalhadas

## 📧 Configuração do Gmail

Para usar o Gmail, você precisa de uma **senha de app**:

1. Acesse sua conta Google
2. Vá em **Segurança** → **Verificação em duas etapas**
3. Role até **Senhas de app**
4. Gere uma nova senha para "Outro (nome personalizado)"
5. Use essa senha no arquivo `.env`

## 📱 Configuração do WhatsApp

1. Certifique-se que o WhatsApp Web está ativo no seu navegador
2. O número deve estar no formato internacional: `+5511999999999`
3. Mantenha o WhatsApp Web aberto durante o uso

## ⚙️ Configurações Avançadas

### Categorias de Produtos
Edite `src/config.py` para personalizar as categorias:

```python
CATEGORIES = {
    'eletrônicos': ['smartphone', 'notebook', 'tablet'],
    'roupas': ['camiseta', 'calça', 'vestido'],
    'casa': ['sofá', 'mesa', 'cadeira'],
    # Adicione suas categorias
}
```

### Destinatários de Email
Configure os destinatários em `src/config.py`:

```python
EMAIL_RECIPIENTS = [
    'destinatario1@gmail.com',
    'destinatario2@gmail.com'
]
```

### Intervalo de Envio
Altere o intervalo em `src/config.py`:

```python
SEND_INTERVAL_HOURS = 1  # Enviar a cada 1 hora
```

## 📊 Estrutura do Projeto

```
mercadolivre-automation/
├── src/
│   ├── config.py              # Configurações
│   ├── models.py              # Modelos de dados
│   ├── scraper.py             # Web scraping
│   ├── notification_manager.py # Envio de notificações
│   ├── scheduler.py           # Agendamento
│   └── terminal_interface.py  # Interface do usuário
├── main.py                    # Arquivo principal
├── requirements.txt           # Dependências
├── .env.example              # Exemplo de configuração
└── README.md                 # Documentação
```

## 🎨 Template de Mensagem

### Email
- Design moderno e responsivo
- Cards individuais por produto
- Informações completas de preço e desconto
- Links diretos para compra

### WhatsApp
```
🔥 *OFERTA ESPECIAL* 📱

*iPhone 13 128GB*

💰 ~De R$ 3.999,00~
💸 *Por R$ 2.999,00*
🏷️ *Desconto de 25%*

💳 12x de R$ 249,92 sem juros
🚚 Frete grátis
⭐ 4.8

📲 *LINK DE COMPRA* ⬇️
https://mercadolivre.com.br/...

_Oferta por tempo limitado!_ ⏰
```

## 🔒 Segurança

- **Nunca** compartilhe suas credenciais
- Use senhas de app para Gmail
- Mantenha o arquivo `.env` privado
- Respeite os termos de uso do Mercado Livre

## ⚠️ Limitações e Avisos

- **Termos de Uso**: Certifique-se de respeitar os termos do Mercado Livre
- **Rate Limiting**: O sistema inclui pausas entre requisições
- **Selenium**: Requer Chrome/Chromium instalado
- **WhatsApp**: Depende do WhatsApp Web estar ativo

## 🐛 Resolução de Problemas

### Erro de Login
- Verifique credenciais no arquivo `.env`
- Certifique-se que não há verificação 2FA pendente

### Selenium não funciona
- Instale Google Chrome ou Chromium
- Verifique se o ChromeDriver está atualizado

### WhatsApp não envia
- Mantenha WhatsApp Web aberto
- Verifique o formato do número de telefone

### Gmail não autentica
- Use senha de app, não a senha normal
- Verifique se a verificação em duas etapas está ativa

## 📝 Logs

O sistema gera logs detalhados no terminal, incluindo:
- Status de login
- Produtos encontrados
- Envios realizados
- Erros e avisos

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto é para fins educacionais e de demonstração. Use com responsabilidade e respeite os termos de serviço das plataformas utilizadas.

## 📞 Suporte

Para dúvidas ou problemas:
- Consulte a seção de ajuda no menu do programa
- Verifique os logs de erro
- Revise as configurações do arquivo `.env`

---

**⚡ Sistema Automatizado Mercado Livre - Automatize suas vendas com inteligência!**