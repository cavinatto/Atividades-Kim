# Análise de Qualidade do Ar (CO e NOx)

Este projeto realiza uma análise estatística do arquivo `air_quality_with_target .csv`, com foco nas variáveis:

- `CO(GT)`
- `NOx(GT)`
- `Target`

A análise calcula medidas de tendência central e variação, conta os grupos do target, gera visualização e produz um texto interpretativo com recomendações de saúde pública.

---

## 📌 Objetivo

Atender ao estudo solicitado sobre qualidade do ar, contemplando:

1. **Medidas de tendência central**: média, mediana e moda.
2. **Medidas de variação**: variância e desvio padrão.
3. **Contagem dos grupos no `Target`**.
4. **Geração de gráfico**.
5. **Análise estatística interpretativa**.
6. **Storytelling** sobre impactos respiratórios.
7. **Ações para autoridades sanitárias**.

---

## 📂 Estrutura dos arquivos

- `air_quality_with_target .csv` → base de dados de entrada.
- `analise_qualidade_ar.py` → script principal de análise.
- `analise_qualidade_ar.md` → relatório gerado automaticamente.
- `grafico_target.svg` → gráfico de barras com a distribuição por `Target`.

---

## ▶️ Como executar

No diretório do projeto, rode:

```bash
python analise_qualidade_ar.py
```

Ao final da execução, serão (re)gerados:

- `analise_qualidade_ar.md`
- `grafico_target.svg`

---

## 🧪 O que o script faz

O script:

- Lê o CSV com `csv.DictReader`.
- Trata o valor `-200` como ausente para `CO(GT)` e `NOx(GT)`.
- Calcula, para cada coluna-alvo:
  - média
  - mediana
  - moda (com frequência)
  - variância amostral
  - desvio padrão
  - mínimo e máximo
- Conta registros por classe de `Target` (`Low`, `Moderate`, `High`).
- Gera um gráfico em SVG com a distribuição das classes.
- Escreve um relatório em Markdown com:
  - análise estatística
  - tabela por grupo de risco
  - storytelling
  - recomendações de ação pública

---

## 📊 Resumo dos principais resultados (dataset atual)

### CO (CO(GT))
- Amostras válidas: **676**
- Média: **0.7234**
- Mediana: **0.5000**
- Moda: **0.5**
- Variância: **0.0619**
- Desvio padrão: **0.2488**

### NOx (NOx(GT))
- Amostras válidas: **656**
- Média: **125.4573**
- Mediana: **150.0000**
- Moda: **150.0**
- Variância: **625.7447**
- Desvio padrão: **25.0149**

### Target (contagem)
- **Low**: 367
- **High**: 325
- **Moderate**: 308

> Observação: os valores acima refletem a versão atual do arquivo CSV. Se o dataset mudar, os resultados serão recalculados automaticamente.

---

## 🩺 Recomendações para autoridades sanitárias

Com base na análise, recomenda-se:

1. Monitoramento e alertas públicos em tempo real.
2. Protocolos de resposta em dias de pior qualidade do ar.
3. Integração com políticas de mobilidade e redução de emissões.
4. Vigilância epidemiológica correlacionando poluição e internações.
5. Ações focadas em grupos vulneráveis (crianças, idosos, asmáticos).

Essas ações ajudam a reduzir exposição populacional e a incidência de problemas respiratórios.
