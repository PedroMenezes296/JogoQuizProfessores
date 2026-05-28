import os
from supabase import create_client

SUPABASE_URL = "https://alonggxaumhxpcaqjaig.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFsb25nZ3hhdW1oeHBjYXFqYWlnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk1MzA0MzMsImV4cCI6MjA5NTEwNjQzM30.3p0sJ-piGBy_-FenU-Vvw3gSdcLeHiCX5LvAlOcPW44"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFsb25nZ3hhdW1oeHBjYXFqYWlnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3OTUzMDQzMywiZXhwIjoyMDk1MTA2NDMzfQ.QnDR9a0z8ILV0XyiFFH-GVJ0kIuwTJClhJkAfPesMUQ"

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    print("Erro: SUPABASE_URL e SUPABASE_SERVICE_KEY devem estar definidas.")
    exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def seed():
    # 1. Cadeiras iniciais
    cadeiras = [
        {"nome": "Redes de Computadores", "descricao": "Fundamentos de redes, protocolos e topologias.", "cor_quadro": "#004d00"},
        {"nome": "Engenharia de Software", "descricao": "Processos, requisitos e modelagem de sistemas.", "cor_quadro": "#000080"}
    ]

    for c in cadeiras:
        exists = supabase.table("cadeiras").select("id").eq("nome", c["nome"]).execute()
        if not exists.data:
            supabase.table("cadeiras").insert(c).execute()
            print(f"Cadeira '{c['nome']}' inserida.")
        else:
            print(f"Cadeira '{c['nome']}' já existe.")

    # 2. Obter IDs das cadeiras
    redes_res = supabase.table("cadeiras").select("id").eq("nome", "Redes de Computadores").execute()
    eng_res = supabase.table("cadeiras").select("id").eq("nome", "Engenharia de Software").execute()

    if not redes_res.data or not eng_res.data:
        print("Erro: cadeiras não encontradas após inserção.")
        return

    redes_id = redes_res.data[0]["id"]
    eng_id = eng_res.data[0]["id"]

    # 3. Perguntas — Redes de Computadores
    redes_perguntas = [
        {
            "enunciado": "Qual protocolo da camada de transporte garante entrega confiável e ordenada de dados?",
            "opcao_a": "UDP", "opcao_b": "TCP", "opcao_c": "IP", "opcao_d": "ICMP",
            "resposta_correta": "b"
        },
        {
            "enunciado": "O modelo OSI é dividido em quantas camadas?",
            "opcao_a": "4", "opcao_b": "5", "opcao_c": "6", "opcao_d": "7",
            "resposta_correta": "d"
        },
        {
            "enunciado": "Qual é a função principal de um roteador em uma rede?",
            "opcao_a": "Amplificar o sinal Wi-Fi",
            "opcao_b": "Conectar dispositivos em uma mesma LAN",
            "opcao_c": "Interligar redes diferentes e encaminhar pacotes",
            "opcao_d": "Converter sinais digitais em analógicos",
            "resposta_correta": "c"
        },
        {
            "enunciado": "O que significa a sigla DHCP?",
            "opcao_a": "Dynamic Host Configuration Protocol",
            "opcao_b": "Data Host Control Protocol",
            "opcao_c": "Direct Hardware Communication Protocol",
            "opcao_d": "Domain Host Configuration Process",
            "resposta_correta": "a"
        },
        {
            "enunciado": "Qual porta padrão é utilizada pelo protocolo HTTPS?",
            "opcao_a": "80", "opcao_b": "21", "opcao_c": "443", "opcao_d": "8080",
            "resposta_correta": "c"
        },
        {
            "enunciado": "Em que camada do modelo OSI opera o protocolo IP?",
            "opcao_a": "Camada de Enlace",
            "opcao_b": "Camada de Rede",
            "opcao_c": "Camada de Transporte",
            "opcao_d": "Camada de Aplicação",
            "resposta_correta": "b"
        },
        {
            "enunciado": "O que é NAT (Network Address Translation)?",
            "opcao_a": "Um protocolo de roteamento dinâmico",
            "opcao_b": "Uma técnica que traduz endereços IP privados para públicos",
            "opcao_c": "Um tipo de cabo de rede",
            "opcao_d": "Um algoritmo de criptografia simétrica",
            "resposta_correta": "b"
        },
        {
            "enunciado": "Qual é a principal diferença entre TCP e UDP?",
            "opcao_a": "TCP é mais rápido que UDP",
            "opcao_b": "UDP garante entrega dos pacotes, TCP não",
            "opcao_c": "TCP verifica entrega e ordem dos dados, UDP não",
            "opcao_d": "Não há diferença significativa entre os dois",
            "resposta_correta": "c"
        },
        {
            "enunciado": "O que é um endereço MAC?",
            "opcao_a": "Um endereço IP versão 6",
            "opcao_b": "Um identificador único de 48 bits atribuído a interfaces de rede",
            "opcao_c": "Um protocolo de roteamento",
            "opcao_d": "Um tipo de topologia de rede",
            "resposta_correta": "b"
        },
        {
            "enunciado": "O protocolo DNS tem como função principal:",
            "opcao_a": "Enviar e-mails pela rede",
            "opcao_b": "Traduzir nomes de domínio em endereços IP",
            "opcao_c": "Estabelecer conexões VPN seguras",
            "opcao_d": "Gerenciar arquivos em servidores FTP",
            "resposta_correta": "b"
        },
        {
            "enunciado": "Qual topologia de rede conecta todos os dispositivos a um único cabo central?",
            "opcao_a": "Estrela", "opcao_b": "Anel", "opcao_c": "Barramento", "opcao_d": "Malha",
            "resposta_correta": "c"
        },
        {
            "enunciado": "O que é uma VPN (Virtual Private Network)?",
            "opcao_a": "Uma rede local sem fio de alta velocidade",
            "opcao_b": "Uma rede virtual que cria um túnel criptografado pela internet",
            "opcao_c": "Um protocolo de transferência de arquivos",
            "opcao_d": "Um tipo de switch gerenciável",
            "resposta_correta": "b"
        },
        {
            "enunciado": "Qual protocolo é responsável pelo envio de e-mails?",
            "opcao_a": "POP3", "opcao_b": "IMAP", "opcao_c": "SMTP", "opcao_d": "FTP",
            "resposta_correta": "c"
        },
        {
            "enunciado": "O que é o protocolo ARP?",
            "opcao_a": "Protocolo de roteamento automático entre redes",
            "opcao_b": "Protocolo que resolve endereços IP em endereços MAC",
            "opcao_c": "Protocolo de transferência de arquivos seguro",
            "opcao_d": "Protocolo de autenticação em redes sem fio",
            "resposta_correta": "b"
        },
        {
            "enunciado": "Em uma máscara de sub-rede /24, quantos hosts são endereçáveis?",
            "opcao_a": "256", "opcao_b": "254", "opcao_c": "512", "opcao_d": "128",
            "resposta_correta": "b"
        },
    ]

    # 4. Perguntas — Engenharia de Software
    eng_perguntas = [
        {
            "enunciado": "O que é o Scrum?",
            "opcao_a": "Uma linguagem de programação orientada a objetos",
            "opcao_b": "Um framework ágil iterativo com sprints e reuniões diárias",
            "opcao_c": "Um banco de dados relacional open-source",
            "opcao_d": "Um protocolo de comunicação entre microsserviços",
            "resposta_correta": "b"
        },
        {
            "enunciado": "O que significa TDD (Test-Driven Development)?",
            "opcao_a": "Prática de desenvolver testes após o código estar pronto",
            "opcao_b": "Prática de escrever testes antes do código de produção",
            "opcao_c": "Técnica de documentação automática de software",
            "opcao_d": "Método de integração entre sistemas legados",
            "resposta_correta": "b"
        },
        {
            "enunciado": "O que significa a sigla UML?",
            "opcao_a": "Unified Modeling Language",
            "opcao_b": "Universal Machine Language",
            "opcao_c": "Unified Module Library",
            "opcao_d": "User Memory Language",
            "resposta_correta": "a"
        },
        {
            "enunciado": "O que é refatoração de código?",
            "opcao_a": "Reescrever o sistema do zero com nova tecnologia",
            "opcao_b": "Melhorar a estrutura interna do código sem alterar seu comportamento externo",
            "opcao_c": "Adicionar novas funcionalidades ao sistema existente",
            "opcao_d": "Criar documentação técnica completa do código",
            "resposta_correta": "b"
        },
        {
            "enunciado": "O que é integração contínua (CI)?",
            "opcao_a": "Integrar o banco de dados com a camada de aplicação",
            "opcao_b": "Prática de mesclar código frequentemente com build e testes automáticos",
            "opcao_c": "Conectar diferentes APIs externas em um sistema",
            "opcao_d": "Realizar deploy manual na última sexta-feira do mês",
            "resposta_correta": "b"
        },
        {
            "enunciado": "No modelo Cascata (Waterfall), como as fases são organizadas?",
            "opcao_a": "As fases se sobrepõem e ocorrem em paralelo",
            "opcao_b": "Cada fase deve ser totalmente concluída antes de iniciar a próxima",
            "opcao_c": "As fases são executadas em iterações curtas de 2 semanas",
            "opcao_d": "Não existe uma ordem definida entre as fases",
            "resposta_correta": "b"
        },
        {
            "enunciado": "O que é um diagrama de casos de uso em UML?",
            "opcao_a": "Representa a arquitetura de banco de dados do sistema",
            "opcao_b": "Mostra as interações entre atores externos e as funcionalidades do sistema",
            "opcao_c": "Detalha o fluxo de execução de um algoritmo específico",
            "opcao_d": "Exibe a topologia de rede da infraestrutura do sistema",
            "resposta_correta": "b"
        },
        {
            "enunciado": "No princípio SOLID, o que significa a letra 'O'?",
            "opcao_a": "Object-Oriented — o código deve ser orientado a objetos",
            "opcao_b": "Open/Closed — classes abertas para extensão, fechadas para modificação",
            "opcao_c": "Overriding — toda classe deve sobrescrever métodos da superclasse",
            "opcao_d": "Optional — dependências opcionais devem ser injetadas",
            "resposta_correta": "b"
        },
        {
            "enunciado": "O que é um padrão de design (Design Pattern)?",
            "opcao_a": "Um framework de desenvolvimento web full-stack",
            "opcao_b": "Uma solução reutilizável para problemas comuns de design de software",
            "opcao_c": "Um tipo de banco de dados orientado a documentos",
            "opcao_d": "Uma linguagem de programação funcional moderna",
            "resposta_correta": "b"
        },
        {
            "enunciado": "Para que serve o Git?",
            "opcao_a": "Banco de dados relacional open-source",
            "opcao_b": "Sistema de controle de versão distribuído para rastrear mudanças no código",
            "opcao_c": "Linguagem de programação back-end baseada em Python",
            "opcao_d": "Servidor de aplicações para deploy em nuvem",
            "resposta_correta": "b"
        },
        {
            "enunciado": "O que é um MVP (Minimum Viable Product) no contexto ágil?",
            "opcao_a": "Um produto com todas as funcionalidades planejadas desenvolvidas",
            "opcao_b": "A versão mais simples de um produto com funcionalidades suficientes para validar o conceito",
            "opcao_c": "Um tipo de teste de aceitação do usuário",
            "opcao_d": "Um documento de especificação técnica completa de requisitos",
            "resposta_correta": "b"
        },
        {
            "enunciado": "O que é débito técnico?",
            "opcao_a": "O custo financeiro de aquisição de licenças de software",
            "opcao_b": "O custo futuro de manutenção causado por atalhos e soluções subótimas no código",
            "opcao_c": "O tempo investido na criação de documentação técnica",
            "opcao_d": "O número total de bugs encontrados em produção",
            "resposta_correta": "b"
        },
        {
            "enunciado": "O que é o padrão arquitetural MVC (Model-View-Controller)?",
            "opcao_a": "Um protocolo de rede para comunicação entre microsserviços",
            "opcao_b": "Um padrão que separa a aplicação em dados, interface e lógica de controle",
            "opcao_c": "Um algoritmo de ordenação eficiente para grandes volumes de dados",
            "opcao_d": "Um tipo de banco de dados NoSQL orientado a grafos",
            "resposta_correta": "b"
        },
        {
            "enunciado": "O que significa 'deploy' no desenvolvimento de software?",
            "opcao_a": "Processo de escrever testes unitários para o código",
            "opcao_b": "Disponibilizar uma aplicação em um ambiente de execução (produção, homologação)",
            "opcao_c": "Criar diagramas de arquitetura do sistema",
            "opcao_d": "Realizar backup completo do banco de dados",
            "resposta_correta": "b"
        },
        {
            "enunciado": "O que é um diagrama de sequência em UML?",
            "opcao_a": "Mostra a estrutura hierárquica de classes do sistema",
            "opcao_b": "Representa a interação entre objetos ao longo do tempo em uma sequência de mensagens",
            "opcao_c": "Detalha o modelo entidade-relacionamento do banco de dados",
            "opcao_d": "Exibe a implantação física dos componentes do sistema",
            "resposta_correta": "b"
        },
    ]

    def inserir_perguntas(perguntas, cadeira_id, nome_cadeira):
        print(f"\nInserindo perguntas — {nome_cadeira}:")
        for p in perguntas:
            p_com_id = dict(p, cadeira_id=cadeira_id, ativa=True)
            exists = supabase.table("perguntas").select("id").eq("enunciado", p["enunciado"]).execute()
            if not exists.data:
                supabase.table("perguntas").insert(p_com_id).execute()
                print(f"  [+] {p['enunciado'][:60]}...")
            else:
                print(f"  [=] Já existe: {p['enunciado'][:60]}...")

    inserir_perguntas(redes_perguntas, redes_id, "Redes de Computadores")
    print(f"\nInserindo perguntas — Engenharia de Software:")
    inserir_perguntas(eng_perguntas, eng_id, "Engenharia de Software")
    print("\nSeed concluído!")


if __name__ == "__main__":
    seed()
