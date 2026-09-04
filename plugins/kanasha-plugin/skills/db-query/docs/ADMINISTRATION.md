# Administração do broker PostgreSQL

## Limite de responsabilidade

O cliente `db-query` nunca recebe o YAML, credenciais, host, porta ou DSN. Somente o processo do broker, executado pela conta de serviço dedicada, lê a configuração privada. O cliente só conhece o caminho do socket definido pela instalação.

Os caminhos, usuário Linux, grupo de socket e nome do serviço são parâmetros da instalação. Preencha os marcadores do template systemd para o host alvo; não acrescente caminhos de usuário, aliases reais ou segredos ao código-fonte.

## Instalação administrativa

1. Crie uma conta Linux de sistema sem shell para o broker e um grupo separado para os clientes autorizados.
2. Instale este diretório em uma localização somente leitura para a conta cliente e instale as dependências de `requirements.txt` em um ambiente Python pertencente ao administrador.
3. Crie um diretório de configuração acessível somente pelo administrador e pela conta do broker. Instale ali uma cópia editada de `databases.yaml.example`, nunca o arquivo de exemplo no repositório.
4. Gere a unidade systemd a partir de `systemd/kanasha-db-query-broker.service.template`, substituindo todos os marcadores `@...@`. O diretório de runtime deve permitir travessia para o grupo cliente, mas não listagem; o socket deve ser criado com modo `0660` e o grupo de clientes.
5. Habilite e inicie o serviço somente após uma revisão humana dos caminhos, permissões e da conta PostgreSQL read-only.

Não use regras `NOPASSWD` para manutenção da configuração. O Codex não deve receber `sudo`, acesso à conta do broker ou permissão para ler o diretório privado.

## Criar, alterar ou desativar uma conexão

Em uma sessão administrativa interativa, fora de qualquer execução do Codex:

1. Abra o YAML privado com `sudoedit`.
2. Inclua, altere ou remova um alias com `enabled: true`, `type: postgresql`, relações completas (`schema.relation`) e apenas as funções necessárias. Para desativar temporariamente um alias sem removê-lo, defina `enabled: false`; ele deixa de aparecer e não pode receber consultas.
3. Execute `db_query_broker.py --config <caminho-privado> --validate-config` como a conta do broker. Esse comando não exibe valores de conexão.
4. Envie `SIGHUP` pelo `systemctl reload <nome-do-serviço>`. O broker só troca sua configuração quando a nova versão é válida; em erro, mantém a anterior.
5. Use `db-query list` e uma consulta mínima permitida para verificar o novo alias. Nenhuma saída deve mostrar a configuração.

## Regras para cada banco PostgreSQL

- Use uma conta dedicada de leitura, sem privilégios administrativos, escrita ou DDL.
- Conceda somente `CONNECT`, `USAGE` no schema necessário e `SELECT` nas views ou relações autorizadas.
- Prefira views com projeção mínima e filtro de tenant a tabelas completas, especialmente para dados pessoais.
- Mantenha o limite de linhas e timeout conservadores. O broker aceita no máximo 1.000 linhas por alias.
- Trate o log do serviço como metadado operacional: ele registra solicitante Unix, alias, resumo sem valores, duração e contagem de linhas; nunca credenciais, parâmetros ou resultados.

## Validação de integração opcional

O teste `tests/test_postgresql_integration.py` permanece ignorado até que uma fixture PostgreSQL isolada seja disponibilizada. Defina explicitamente o socket, alias e relação dessa fixture nas variáveis indicadas pelo teste. Não aponte essas variáveis para banco local compartilhado, homologação ou produção.
