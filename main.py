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
        # Verifica se o arquivo .env existe
        if not os.path.exists('.env'):
            print("⚠️  ATENÇÃO: Arquivo .env não encontrado!")
            print("1. Copie o arquivo .env.example para .env")
            print("2. Preencha suas credenciais no arquivo .env")
            print("3. Execute o programa novamente")
            input("Pressione Enter para sair...")
            return
        
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