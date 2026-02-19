# Estudo de Caso: CRON para Controle de Frutas na Fruteira

Este documento explica, com pseudocodigo, como criar um processo automatico (`CRON`) para controlar o ciclo de vida das frutas no estoque.

## Objetivo

Automatizar diariamente:
- Registro de chegada da fruta
- Entrada em promocao
- Inicio de apodrecimento
- Descarte

Exemplo real:
- Banana prata chegou em `16/02/2026`
- Em `20/02/2026` entra em promocao (4 dias depois)
- Comeca a apodrecer 4 dias apos a chegada
- Descarte 3 dias apos o inicio do apodrecimento

## Conceitos Rapidos

- `CRON`: agendador de tarefas no Linux/Unix.
- `cron expression`: regra de horario para executar o job.
- `job`: script que roda sozinho no horario configurado.

Exemplo de cron diario as 02:00:

```cron
0 2 * * * /usr/bin/python /app/jobs/atualizar_frutas.py
```

## Modelo de Dados (sugestao)

Tabela `frutas_estoque`:

- `id`
- `nome` (ex: banana prata)
- `data_chegada`
- `status` (`disponivel`, `promocao`, `apodrecendo`, `descartada`)
- `data_promocao`
- `data_inicio_apodrecimento`
- `data_descarte`
- `preco_normal`
- `preco_promocional`

## Regras de Negocio (caso base)

Para cada fruta:
- `data_promocao = data_chegada + 4 dias`
- `data_inicio_apodrecimento = data_chegada + 4 dias`
- `data_descarte = data_inicio_apodrecimento + 3 dias`

Observacao:
- No seu exemplo, promocao e inicio de apodrecimento acontecem no mesmo dia.
- Se quiser, depois voce pode separar esses tempos por tipo de fruta.

## Pseudocodigo Principal (job diario)

```text
ALGORITMO atualizar_status_frutas(data_hoje):
    frutas = buscar_frutas_nao_descartadas()

    PARA CADA fruta EM frutas:
        SE fruta.data_promocao estiver vazia:
            fruta.data_promocao = fruta.data_chegada + 4 dias

        SE fruta.data_inicio_apodrecimento estiver vazia:
            fruta.data_inicio_apodrecimento = fruta.data_chegada + 4 dias

        SE fruta.data_descarte estiver vazia:
            fruta.data_descarte = fruta.data_inicio_apodrecimento + 3 dias

        SE data_hoje >= fruta.data_descarte:
            fruta.status = "descartada"

        SENAO SE data_hoje >= fruta.data_inicio_apodrecimento:
            fruta.status = "apodrecendo"

        SENAO SE data_hoje >= fruta.data_promocao:
            fruta.status = "promocao"
            fruta.preco_atual = fruta.preco_promocional

        SENAO:
            fruta.status = "disponivel"
            fruta.preco_atual = fruta.preco_normal

        salvar(fruta)

    gerar_log("job executado com sucesso", data_hoje)
```

## Simulacao da Banana Prata

Entrada:
- `nome = banana prata`
- `data_chegada = 16/02/2026`

Calculo automatico:
- `data_promocao = 20/02/2026`
- `data_inicio_apodrecimento = 20/02/2026`
- `data_descarte = 23/02/2026`

Linha do tempo:
- `16/02 ate 19/02`: disponivel
- `20/02 ate 22/02`: promocao + apodrecendo
- `23/02 em diante`: descartada

## Versao 2 (melhor): regras por tipo de fruta

Crie tabela `regras_fruta`:
- `nome_fruta`
- `dias_para_promocao`
- `dias_para_apodrecer`
- `dias_ate_descarte_apos_apodrecer`

Pseudocodigo:

```text
ALGORITMO calcular_datas(fruta, regra):
    fruta.data_promocao = fruta.data_chegada + regra.dias_para_promocao
    fruta.data_inicio_apodrecimento = fruta.data_chegada + regra.dias_para_apodrecer
    fruta.data_descarte = fruta.data_inicio_apodrecimento + regra.dias_ate_descarte_apos_apodrecer
```

Exemplo de configuracao:
- Banana prata: `4, 4, 3`
- Morango: `2, 2, 1`
- Mamao: `3, 4, 2`

## Como aplicar amanha (passo a passo rapido)

1. Criar tabela de frutas no banco.
2. Cadastrar frutas com `data_chegada`.
3. Criar script `atualizar_frutas.py` com o pseudocodigo acima.
4. Rodar manualmente o script e validar datas/status.
5. Configurar o `cron` para rodar todo dia.
6. Ver logs diariamente.

## Exemplo de CRON no servidor

Editar crontab:

```bash
crontab -e
```

Adicionar:

```cron
0 2 * * * /usr/bin/python /app/jobs/atualizar_frutas.py >> /app/logs/cron_frutas.log 2>&1
```

## Checklist de validacao

- [ ] Data de promocao calculada corretamente
- [ ] Data de apodrecimento calculada corretamente
- [ ] Data de descarte calculada corretamente
- [ ] Status muda sozinho por data
- [ ] Fruta descartada nao volta para estoque
- [ ] Log do job gerado diariamente

## Dica Final

Voce pode comecar com esse modelo simples e, depois, evoluir para:
- alerta por WhatsApp/Email quando entrar em promocao
- dashboard de perdas
- previsao de compra por historico de descarte
