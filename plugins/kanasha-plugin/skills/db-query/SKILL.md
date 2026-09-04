---
name: db-query
description: Consulta bancos PostgreSQL autorizados por um broker local somente leitura, sem acesso a credenciais. Use para localizar ou verificar dados quando o broker estiver instalado.
user-invocable: true
argument-hint: "<o que deseja consultar>"
allowed-tools: Bash
---

# Consulta de banco via broker local

## Objetivo

Consultar somente aliases autorizados pelo broker PostgreSQL local. O agente não lê, procura, cria, edita ou imprime o YAML de conexões, nem aceita host, usuário, senha ou DSN em comandos.

## Fluxo

1. Execute `db-query list` para descobrir aliases e descrições não sensíveis.
2. Quando a relação não for conhecida, execute `db-query describe --db <alias> --relation <schema.relation>` somente para uma relação permitida.
3. Monte uma única `SELECT` PostgreSQL com colunas explícitas, relação qualificada, `LIMIT` literal dentro do teto do alias e valores em placeholders `$1`, `$2`, etc. Todo valor fora de `LIMIT` deve ser um placeholder; passe-os separadamente em `--params` como lista JSON.
4. Execute `db-query query --db <alias> --sql '<SQL>' --params '<lista-json>'`.
5. Apresente apenas os dados necessários e evite reproduzir dados pessoais sem necessidade.

O broker aceita apenas `SELECT` ou `WITH ... SELECT` em relações autorizadas. Ele limita linhas e tempo, rejeita escrita, DDL, CTE de escrita, `COPY`, múltiplas instruções, wildcard, funções não autorizadas e relações fora da allowlist.

## Limites operacionais

- Se `db-query list` indicar que o socket não está configurado ou indisponível, informe a falha sem procurar arquivos de configuração nem tentar conexão direta.
- Nunca execute SQL diretamente por Bash, nem use driver, ORM, psql ou variável de ambiente para contornar o broker.
- Não tente instalar, iniciar, recarregar ou administrar o serviço. A manutenção do YAML, systemd, conta Linux e permissões pertence ao administrador humano descrito em `docs/ADMINISTRATION.md`.
- O broker atual suporta apenas PostgreSQL.
