#!/usr/bin/env python3
"""
Sistema Automatizado Mercado Livre
================================

Sistema completo para busca, classificação e envio automático de produtos
do Mercado Livre via email e WhatsApp.

Características:
- Login automático no Mercado Livre
- Busca produtos em promoção e normais
- Classificação automática por categorias
- Geração de links de afiliado
- Envio por email com HTML elegante
- Envio individual por WhatsApp
- Agendamento automático
- Interface terminal interativa

Autor: Sistema Automatizado
Data: 2025
"""

import sys
import os

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.terminal_interface import TerminalInterface

def main():
    """Função principal"""
    try:
        # Verifica o diretório atual
        current_dir = os.getcwd()
        env_path = os.path.join(current_dir, '.env')
        
        # Verifica se o arquivo .env existe
        if not os.path.exists(env_path):
            print(f"⚠️  ATENÇÃO: Arquivo .env não encontrado em: {env_path}")
            print("Criando arquivo .env com configurações padrão...")
            
            # Cria arquivo .env com configurações padrão
            default_env = """MERCADOLIVRE_EMAIL=seu_email@gmail.com
MERCADOLIVRE_PASSWORD=sua_senha
GMAIL_EMAIL=seu_gmail@gmail.com
GMAIL_PASSWORD=sua_senha_app_gmail
WHATSAPP_PHONE=+5511999999999
AFFILIATE_ID=ML_DEFAULT
ENABLE_EMAIL=false
ENABLE_WHATSAPP=true
"""
            with open(env_path, 'w', encoding='utf-8') as f:
                f.write(default_env)
            
            print("✅ Arquivo .env criado com sucesso!")
            print("📝 Agora edite o arquivo .env com suas credenciais:")
            print("   - MERCADOLIVRE_EMAIL: seu email do Mercado Livre")
            print("   - MERCADOLIVRE_PASSWORD: sua senha do Mercado Livre")
            print("   - WHATSAPP_PHONE: seu número no formato +5511999999999")
            print("   - Para apenas WhatsApp, deixe ENABLE_EMAIL=false")
            input("Pressione Enter para sair...")
            return
        else:
            print(f"✅ Arquivo .env encontrado em: {env_path}")
        
        # Inicia a interface terminal
        interface = TerminalInterface()
        interface.run()
        
    except Exception as e:
        print(f"Erro fatal: {e}")
        input("Pressione Enter para sair...")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())