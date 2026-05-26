-- Tabela de Perfis de Usuário (extensão do auth.users do Supabase)
CREATE TABLE profiles (
    id UUID REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
    nome_completo TEXT NOT NULL,
    email_institucional TEXT UNIQUE NOT NULL,
    matricula TEXT,
    role TEXT NOT NULL DEFAULT 'aluno' CHECK (role IN ('aluno', 'professor', 'admin')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de Cadeiras
CREATE TABLE cadeiras (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    descricao TEXT,
    professor_id UUID REFERENCES profiles(id) ON DELETE SET NULL,
    cor_quadro TEXT DEFAULT '#004d00', -- Hexadecimal da cor do quadro
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de Perguntas
CREATE TABLE perguntas (
    id SERIAL PRIMARY KEY,
    cadeira_id INTEGER REFERENCES cadeiras(id) ON DELETE CASCADE,
    enunciado TEXT NOT NULL,
    opcao_a TEXT NOT NULL,
    opcao_b TEXT NOT NULL,
    opcao_c TEXT NOT NULL,
    opcao_d TEXT NOT NULL,
    resposta_correta CHAR(1) NOT NULL CHECK (resposta_correta IN ('a', 'b', 'c', 'd')),
    ativa BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela de Partidas
CREATE TABLE partidas (
    id SERIAL PRIMARY KEY,
    usuario_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    cadeira_id INTEGER REFERENCES cadeiras(id) ON DELETE CASCADE,
    total_perguntas INTEGER NOT NULL,
    acertos INTEGER NOT NULL,
    tempo_segundos INTEGER NOT NULL,
    pontuacao_total INTEGER NOT NULL,
    data_partida TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE cadeiras ENABLE ROW LEVEL SECURITY;
ALTER TABLE perguntas ENABLE ROW LEVEL SECURITY;
ALTER TABLE partidas ENABLE ROW LEVEL SECURITY;

-- Políticas de segurança básicas (exemplos que serão refinados)
CREATE POLICY "Perfis visíveis para todos" ON profiles FOR SELECT USING (true);
CREATE POLICY "Usuários podem editar próprio perfil" ON profiles FOR UPDATE USING (auth.uid() = id);
