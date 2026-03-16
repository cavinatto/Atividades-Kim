import csv
import statistics
from collections import Counter, defaultdict
from pathlib import Path

CSV_FILE = Path('air_quality_with_target .csv')
REPORT_FILE = Path('analise_qualidade_ar.md')
CHART_FILE = Path('grafico_target.svg')


def load_data(path: Path):
    co_values = []
    nox_values = []
    target_counts = Counter()
    by_target = defaultdict(lambda: {'co': [], 'nox': []})

    with path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            target = row['Target']
            target_counts[target] += 1

            co = float(row['CO(GT)'])
            nox = float(row['NOx(GT)'])

            if co != -200:
                co_values.append(co)
                by_target[target]['co'].append(co)
            if nox != -200:
                nox_values.append(nox)
                by_target[target]['nox'].append(nox)

    return co_values, nox_values, target_counts, by_target


def summarize(values):
    freq = Counter(values)
    max_freq = max(freq.values())
    modes = sorted(v for v, n in freq.items() if n == max_freq)

    return {
        'n': len(values),
        'mean': sum(values) / len(values),
        'median': statistics.median(values),
        'mode': modes,
        'mode_freq': max_freq,
        'variance': statistics.variance(values),
        'std': statistics.stdev(values),
        'min': min(values),
        'max': max(values),
    }


def save_svg_target_chart(target_counts: Counter, out_file: Path):
    width, height = 700, 420
    margin_left, margin_bottom, margin_top = 70, 70, 40
    chart_w = width - margin_left - 40
    chart_h = height - margin_bottom - margin_top

    items = sorted(target_counts.items(), key=lambda kv: kv[0])
    max_count = max(target_counts.values())
    bar_w = chart_w / (len(items) * 1.8)
    gap = bar_w * 0.8

    colors = {
        'Low': '#4CAF50',
        'Moderate': '#FFC107',
        'High': '#F44336',
    }

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<style>text{font-family:Arial,sans-serif;fill:#222}.title{font-size:20px;font-weight:bold}.axis{font-size:12px}.label{font-size:13px}.value{font-size:12px;font-weight:bold}</style>',
        f'<text class="title" x="{width/2}" y="28" text-anchor="middle">Distribuição por Target</text>',
        f'<line x1="{margin_left}" y1="{height-margin_bottom}" x2="{width-20}" y2="{height-margin_bottom}" stroke="#333"/>',
        f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{height-margin_bottom}" stroke="#333"/>',
    ]

    for i in range(0, max_count + 1, 50):
        y = margin_top + chart_h - (i / max_count) * chart_h
        svg.append(f'<line x1="{margin_left-5}" y1="{y:.1f}" x2="{margin_left}" y2="{y:.1f}" stroke="#333"/>')
        svg.append(f'<text class="axis" x="{margin_left-10}" y="{y+4:.1f}" text-anchor="end">{i}</text>')

    x = margin_left + gap
    for name, value in items:
        bar_h = (value / max_count) * chart_h
        y = margin_top + chart_h - bar_h
        color = colors.get(name, '#2196F3')

        svg.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{bar_h:.1f}" fill="{color}"/>')
        svg.append(f'<text class="value" x="{x + bar_w/2:.1f}" y="{y-8:.1f}" text-anchor="middle">{value}</text>')
        svg.append(f'<text class="label" x="{x + bar_w/2:.1f}" y="{height-margin_bottom+20}" text-anchor="middle">{name}</text>')
        x += bar_w + gap

    svg.append(f'<text class="axis" x="20" y="{height/2}" transform="rotate(-90 20,{height/2})">Contagem</text>')
    svg.append('</svg>')

    out_file.write_text('\n'.join(svg), encoding='utf-8')


def create_report(co_stats, nox_stats, target_counts, by_target):
    total = sum(target_counts.values())

    def f4(n):
        return f'{n:.4f}'

    linhas_target = []
    for k, v in sorted(target_counts.items(), key=lambda kv: kv[1], reverse=True):
        pct = (v / total) * 100
        linhas_target.append(f'- **{k}**: {v} registros ({pct:.1f}%).')

    rows_by_target = []
    for g in ['Low', 'Moderate', 'High']:
        if g in by_target:
            co_mean = sum(by_target[g]['co']) / len(by_target[g]['co']) if by_target[g]['co'] else float('nan')
            nox_mean = sum(by_target[g]['nox']) / len(by_target[g]['nox']) if by_target[g]['nox'] else float('nan')
            rows_by_target.append(f'| {g} | {len(by_target[g]["co"])} | {len(by_target[g]["nox"])} | {co_mean:.3f} | {nox_mean:.3f} |')

    report = f"""# Análise estatística da qualidade do ar (CO e NOx)

## 1) Medidas de tendência central e variação

### CO (CO(GT))
- Amostras válidas: **{co_stats['n']}** (valores `-200` tratados como ausentes).
- Média: **{f4(co_stats['mean'])}**
- Mediana: **{f4(co_stats['median'])}**
- Moda: **{', '.join(str(m) for m in co_stats['mode'])}** (frequência: {co_stats['mode_freq']})
- Variância amostral: **{f4(co_stats['variance'])}**
- Desvio padrão: **{f4(co_stats['std'])}**
- Intervalo observado: **{co_stats['min']} a {co_stats['max']}**

### NOx (NOx(GT))
- Amostras válidas: **{nox_stats['n']}** (valores `-200` tratados como ausentes).
- Média: **{f4(nox_stats['mean'])}**
- Mediana: **{f4(nox_stats['median'])}**
- Moda: **{', '.join(str(m) for m in nox_stats['mode'])}** (frequência: {nox_stats['mode_freq']})
- Variância amostral: **{f4(nox_stats['variance'])}**
- Desvio padrão: **{f4(nox_stats['std'])}**
- Intervalo observado: **{nox_stats['min']} a {nox_stats['max']}**

## 2) Quantidade por grupo no Target

{chr(10).join(linhas_target)}

![Distribuição de registros por Target](grafico_target.svg)

## 3) Leitura estatística

- A mediana de **CO** é 0.5, próxima da moda (0.5), indicando concentração no menor patamar observado.
- Para **NOx**, mediana e moda em 150 sugerem concentração no patamar superior disponível, apesar da média ficar menor (125.46) pela presença de valores em 100.
- A variabilidade relativa do NOx é maior em termos absolutos (desvio padrão ≈ 25) do que a do CO (≈ 0.249), mostrando maior oscilação entre os dois níveis observados de NOx.

### Médias por grupo de risco (Target)

| Target | n válido CO | n válido NOx | Média CO | Média NOx |
|---|---:|---:|---:|---:|
{chr(10).join(rows_by_target)}

Interpretação rápida:
- O grupo **Moderate** tem a maior média de CO.
- O grupo **Low** tem a maior média de NOx nesta amostra.
- As diferenças são pequenas, o que indica que outras variáveis ambientais também podem influenciar o Target.

## 4) Storytelling (contexto em linguagem natural)

Imagine uma cidade em que, ao amanhecer, o tráfego começa a crescer e os corredores urbanos passam a concentrar emissões. Mesmo com parte das medições em níveis baixos de CO, o NOx frequentemente aparece em patamares altos. Isso sinaliza um ambiente onde o ar pode parecer "normal" para quem observa apenas um indicador, mas continua agressivo para vias respiratórias sensíveis.

Com o passar dos dias, a população mais vulnerável — crianças, idosos e pessoas com asma — sente primeiro: tosse persistente, irritação e piora de crises respiratórias. Os serviços de saúde percebem aumento de atendimentos em períodos de maior acúmulo de poluentes. O retrato estatístico do dataset reforça esse enredo: a presença recorrente de níveis elevados de NOx é um alerta para políticas públicas preventivas.

## 5) Ações recomendadas para autoridades sanitárias

1. **Sistema de alerta por qualidade do ar** em tempo real (apps, SMS e rádio), com recomendações específicas para grupos de risco.
2. **Protocolos sazonais de saúde respiratória** (reforço de equipes, insumos e triagem) em dias com pior dispersão atmosférica.
3. **Integração com mobilidade urbana**: restrição de emissões em horários críticos, incentivo a transporte limpo e zonas de baixa emissão.
4. **Vigilância epidemiológica ambiental**: correlacionar poluentes com internações por bairro para ações direcionadas.
5. **Intervenções em escolas e unidades de saúde**: monitoramento de ar interno, filtragem adequada e orientação à comunidade.
6. **Campanhas de prevenção**: reduzir exposição em horários de pico, uso correto de medicação de controle em asmáticos e ampliação de vacinação respiratória.

---
Relatório gerado automaticamente por `analise_qualidade_ar.py`.
"""

    REPORT_FILE.write_text(report, encoding='utf-8')


def main():
    co, nox, target_counts, by_target = load_data(CSV_FILE)
    co_stats = summarize(co)
    nox_stats = summarize(nox)
    save_svg_target_chart(target_counts, CHART_FILE)
    create_report(co_stats, nox_stats, target_counts, by_target)
    print('Relatório e gráfico gerados com sucesso.')


if __name__ == '__main__':
    main()
