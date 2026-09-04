# Broker PostgreSQL read-only

Este diretório contém o cliente `db-query` e o broker local que isola as credenciais PostgreSQL do processo cliente. Ele é uma fonte portável: o host administrador escolhe caminhos, conta de serviço, grupo de socket e arquivo privado na instalação.

## Dependências e testes

Instale as dependências em ambiente isolado:

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
```

## Uso do cliente

A instalação expõe o socket por `DB_QUERY_SOCKET` ou pelo argumento `--socket`:

```bash
db-query list
db-query describe --db example_postgres --relation public.example_safe_view
db-query query --db example_postgres --sql 'SELECT id FROM public.example_safe_view WHERE application_id = $1 LIMIT 10' --params '["00000000-0000-0000-0000-000000000000"]'
```

O cliente não aceita arquivo de configuração, host, usuário ou senha. Consulte `docs/ADMINISTRATION.md` para instalação e manutenção administrativa.
