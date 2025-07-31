import os
import sys
from datetime import datetime
from colorama import init, Fore, Back, Style
import time

from .scheduler import AutomationScheduler
from .config import Config

# Inicializa colorama para cores no terminal
init(autoreset=True)

class TerminalInterface:
    def __init__(self):
        self.scheduler = AutomationScheduler()
        self.running = False
    
    def print_header(self):
        """Exibe cabeçalho estilizado"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"""{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════╗
║                  SISTEMA MERCADO LIVRE AUTOMÁTICO            ║
║                                                              ║
║  🤖 Busca automática de produtos                             ║
║  📧 Envio por email e WhatsApp                               ║
║  ⏰ Agendamento automático                                   ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """)
    
    def print_status(self):
        """Exibe status da configuração"""
        print(f"\n{Fore.YELLOW}📊 STATUS DA CONFIGURAÇÃO:{Style.RESET_ALL}")
        
        # Verifica configurações
        configs = [
            ("Email Mercado Livre", Config.MERCADOLIVRE_EMAIL),
            ("Senha Mercado Livre", "***" if Config.MERCADOLIVRE_PASSWORD else None),
            ("Email Gmail", Config.GMAIL_EMAIL),
            ("Senha Gmail", "***" if Config.GMAIL_PASSWORD else None),
            ("WhatsApp", Config.WHATSAPP_PHONE),
            ("ID Afiliado", Config.AFFILIATE_ID),
        ]
        
        for name, value in configs:
            status = f"{Fore.GREEN}✓ Configurado{Style.RESET_ALL}" if value else f"{Fore.RED}✗ Não configurado{Style.RESET_ALL}"
            print(f"  {name}: {status}")
        
        print(f"\n{Fore.BLUE}⚙️  CONFIGURAÇÕES:{Style.RESET_ALL}")
        print(f"  • Intervalo de envio: {Config.SEND_INTERVAL_HOURS} hora(s)")
        print(f"  • Máximo produtos por busca: {Config.MAX_PRODUCTS_PER_SEARCH}")
        print(f"  • Destinatários email: {len(Config.EMAIL_RECIPIENTS)}")
    
    def show_menu(self):
        """Exibe menu principal"""
        print(f"\n{Fore.MAGENTA}🔧 OPÇÕES DISPONÍVEIS:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}1.{Style.RESET_ALL} Executar busca única (teste)")
        print(f"  {Fore.GREEN}2.{Style.RESET_ALL} Iniciar agendamento automático")
        print(f"  {Fore.GREEN}3.{Style.RESET_ALL} Parar agendamento")
        print(f"  {Fore.GREEN}4.{Style.RESET_ALL} Ver configurações")
        print(f"  {Fore.GREEN}5.{Style.RESET_ALL} Ajuda")
        print(f"  {Fore.RED}0.{Style.RESET_ALL} Sair")
    
    def run_single_search(self):
        """Executa busca única"""
        print(f"\n{Fore.YELLOW}🔍 Executando busca única...{Style.RESET_ALL}")
        print("Isso pode levar alguns minutos...")
        
        try:
            self.scheduler.run_once()
            print(f"{Fore.GREEN}✓ Busca concluída com sucesso!{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}✗ Erro na busca: {e}{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Pressione Enter para continuar...{Style.RESET_ALL}")
    
    def start_scheduler(self):
        """Inicia agendamento automático"""
        if self.running:
            print(f"{Fore.YELLOW}⚠️  Agendador já está rodando!{Style.RESET_ALL}")
            input(f"\n{Fore.CYAN}Pressione Enter para continuar...{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.GREEN}🚀 Iniciando agendamento automático...{Style.RESET_ALL}")
        
        try:
            self.scheduler.start_scheduler()
            self.running = True
            print(f"{Fore.GREEN}✓ Agendador iniciado com sucesso!{Style.RESET_ALL}")
            print(f"Sistema rodando em background. Envios a cada {Config.SEND_INTERVAL_HOURS} hora(s).")
        except Exception as e:
            print(f"{Fore.RED}✗ Erro ao iniciar agendador: {e}{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Pressione Enter para continuar...{Style.RESET_ALL}")
    
    def stop_scheduler(self):
        """Para agendamento"""
        if not self.running:
            print(f"{Fore.YELLOW}⚠️  Agendador não está rodando!{Style.RESET_ALL}")
            input(f"\n{Fore.CYAN}Pressione Enter para continuar...{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.YELLOW}🛑 Parando agendador...{Style.RESET_ALL}")
        
        try:
            self.scheduler.stop_scheduler()
            self.running = False
            print(f"{Fore.GREEN}✓ Agendador parado com sucesso!{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}✗ Erro ao parar agendador: {e}{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Pressione Enter para continuar...{Style.RESET_ALL}")
    
    def show_help(self):
        """Exibe ajuda"""
        print(f"\n{Fore.CYAN}📖 AJUDA E INSTRUÇÕES:{Style.RESET_ALL}")
        print(f"""
{Fore.YELLOW}1. CONFIGURAÇÃO INICIAL:{Style.RESET_ALL}
   • Copie o arquivo .env.example para .env
   • Preencha suas credenciais no arquivo .env
   • Configure os destinatários de email no config.py

{Fore.YELLOW}2. CREDENCIAIS NECESSÁRIAS:{Style.RESET_ALL}
   • Email e senha do Mercado Livre
   • Gmail com senha de app (não a senha normal)
   • Número do WhatsApp (formato: +5511999999999)
   • ID de afiliado (opcional)

{Fore.YELLOW}3. FUNCIONAMENTO:{Style.RESET_ALL}
   • O sistema busca produtos em promoção e normais
   • Classifica automaticamente por categoria
   • Gera links de afiliado
   • Envia por email (todos produtos) e WhatsApp (top 5)

{Fore.YELLOW}4. AGENDAMENTO:{Style.RESET_ALL}
   • Executa automaticamente a cada hora
   • Roda em background
   • Pode ser parado a qualquer momento

{Fore.YELLOW}5. PROBLEMAS COMUNS:{Style.RESET_ALL}
   • Erro de login: Verifique credenciais
   • Selenium não funciona: Instale Chrome/Chromium
   • WhatsApp não envia: Certifique-se que o WhatsApp Web está logado
        """)
        
        input(f"\n{Fore.CYAN}Pressione Enter para continuar...{Style.RESET_ALL}")
    
    def run(self):
        """Loop principal da interface"""
        try:
            while True:
                self.print_header()
                self.print_status()
                self.show_menu()
                
                # Status do agendador
                if self.running:
                    print(f"\n{Fore.GREEN}🟢 AGENDADOR: ATIVO{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.RED}🔴 AGENDADOR: PARADO{Style.RESET_ALL}")
                
                print(f"\n{Fore.CYAN}Hora atual: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}{Style.RESET_ALL}")
                
                choice = input(f"\n{Fore.WHITE}Digite sua opção: {Style.RESET_ALL}").strip()
                
                if choice == '1':
                    self.run_single_search()
                elif choice == '2':
                    self.start_scheduler()
                elif choice == '3':
                    self.stop_scheduler()
                elif choice == '4':
                    self.print_header()
                    self.print_status()
                    input(f"\n{Fore.CYAN}Pressione Enter para continuar...{Style.RESET_ALL}")
                elif choice == '5':
                    self.show_help()
                elif choice == '0':
                    self.stop_scheduler()
                    print(f"\n{Fore.YELLOW}👋 Saindo do sistema...{Style.RESET_ALL}")
                    break
                else:
                    print(f"\n{Fore.RED}❌ Opção inválida! Tente novamente.{Style.RESET_ALL}")
                    time.sleep(2)
        
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}🛑 Interrompido pelo usuário{Style.RESET_ALL}")
            self.stop_scheduler()
        except Exception as e:
            print(f"\n{Fore.RED}💥 Erro inesperado: {e}{Style.RESET_ALL}")
        finally:
            print(f"{Fore.CYAN}Obrigado por usar o Sistema Mercado Livre Automático!{Style.RESET_ALL}")