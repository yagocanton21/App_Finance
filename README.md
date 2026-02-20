# Sistema de Finanças Pessoais

Sistema simples para controle de finanças pessoais desenvolvido em Flask com arquitetura MVC.

## Funcionalidades

- Cadastro de categorias
- Registro de transações (receitas e despesas)
- Visualização de transações com filtros e paginação
- Interface web responsiva
- Integração com PostgreSQL

## Tecnologias

- **Backend**: Flask (Python)
- **Banco de dados**: PostgreSQL
- **Frontend**: HTML, CSS, Bootstrap
- **Containerização**: Docker & Docker Compose

## Como executar

### Deploy no Vercel (Produção)

1. Crie uma conta no [Vercel](https://vercel.com)

2. Instale o Vercel CLI:
```bash
npm i -g vercel
```

3. Configure um banco PostgreSQL (recomendado: [Neon](https://neon.tech), [Supabase](https://supabase.com) ou [Railway](https://railway.app))

4. No diretório do projeto, execute:
```bash
vercel
```

5. Configure as variáveis de ambiente no painel do Vercel:
   - `DB_HOST`
   - `DB_PORT`
   - `DB_NAME`
   - `DB_USER`
   - `DB_PASSWORD`
   - `SECRET_KEY`

6. Faça o deploy:
```bash
vercel --prod
```

### Com Docker (Recomendado para desenvolvimento)

1. Certifique-se de ter Docker e Docker Compose instalados.

2. Clone o repositório e navegue até a pasta do projeto.

3. Copie o arquivo de exemplo de variáveis de ambiente:
```bash
cp .env.example .env
```

4. Execute a aplicação:
```bash
docker-compose up --build
```

5. Acesse: http://localhost:5000

### Sem Docker (Desenvolvimento local)

1. Instale PostgreSQL e crie um banco de dados.

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente no arquivo `.env` (baseado em `.env.example`).

4. Execute o script de inicialização do banco:
```bash
python scripts/init_db.py
```

5. Execute a aplicação:
```bash
python -c "from app import create_app; app = create_app(); app.run(host='0.0.0.0', port=5000)"
```

6. Acesse: http://127.0.0.1:5000

## Estrutura do projeto (MVC)

```
├── api/
│   └── index.py             # Ponto de entrada Vercel
├── app/
│   ├── __init__.py          # Configuração da aplicação Flask
│   ├── controllers/         # Controladores (lógica de rotas)
│   ├── models/              # Modelos (lógica de dados)
│   └── views/               # Templates HTML (não mostrado)
├── static/                  # Arquivos estáticos (CSS, JS)
├── templates/               # Templates HTML
├── Dockerfile               # Configuração Docker
├── docker-compose.yml       # Orquestração de containers
├── vercel.json              # Configuração Vercel
├── requirements.txt         # Dependências Python
└── README.md
```

## Variáveis de ambiente

Configure no arquivo `.env` (local) ou no painel do Vercel (produção):

- `DB_HOST`: Host do PostgreSQL
- `DB_PORT`: Porta do PostgreSQL
- `DB_NAME`: Nome do banco
- `DB_USER`: Usuário do banco
- `DB_PASSWORD`: Senha do banco
- `SECRET_KEY`: Chave secreta do Flask

## Desenvolvimento

Para contribuir:
1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto é open source. Sinta-se à vontade para usar e modificar.
