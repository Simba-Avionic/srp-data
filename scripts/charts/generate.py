#!/usr/bin/env python3
"""Reproducible chart data; standard library only. Run from any directory."""
import argparse
import csv
import json
import math
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read_csv(path, delimiter=','):
    with (ROOT / path).open(newline='') as stream:
        reader = csv.DictReader(stream, delimiter=delimiter)
        return [row for row in reader if list(row.values()) != reader.fieldnames]


def number(value):
    if value in ('', None):
        return None
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f'Non-finite measurement: {value}')
    return result


def rolling(values, window):
    return [sum(values[i-window+1:i+1]) / window if i >= window-1 else None
            for i in range(len(values))]


def trace(name, x, y, **extra):
    assert len(x) == len(y) and x
    assert all(a <= b for a, b in zip(x, x[1:])), 'Time goes backwards'
    return dict(name=name, x=x, y=y, type='scatter', mode='lines',
                connectgaps=False, **extra)


def chart(traces, ylabel, source, note, xrange=None, xlabel='Czas [s]', **layout):
    return dict(data=traces, layout=dict(xaxis=dict(title=dict(text=xlabel), **(
        {'range': xrange} if xrange else {})), yaxis=dict(title=dict(text=ylabel)), **layout),
        source=source, note=note)


def generate():
    charts = {}
    for date, offset, window, duration in [('2026-03-21', 81, 20, 15), ('2026-04-10', 210.5, 2, 12)]:
        source = f'data/R7/static/{date}/sw/start.csv'
        rows = read_csv(source, ';')
        t = [(float(r['TIMESTAMP']) - float(rows[0]['TIMESTAMP'])) / 1000 for r in rows]
        # Preserve the notebook's rolling window BEFORE cutting the time interval.
        for zoom in (False, True):
            indices = [i for i, v in enumerate(t) if offset < v <= offset + duration]
            traces = []
            for col, label in [('TANK_PRESS', 'Zbiornik'), ('TANK_D_PRESS', 'Komora')]:
                y = [float(r[col])/100 for r in rows]
                if not zoom:
                    y = rolling(y, window)
                traces.append(trace(label, [t[i]-offset for i in indices], [y[i] for i in indices]))
            charts[f'R7/tests/static/{date}/pressure{"_zoom" if zoom else ""}'] = chart(
                traces, 'Ciśnienie [bar]', source,
                f'Oś czasu względem {offset} s logu. ' + ('Dane bez wygładzania.' if zoom else f'Średnia krocząca: {window} próbek, zgodnie z notebookiem.'),
                [1 if date == '2026-03-21' else .5, 6 if date == '2026-03-21' else 5.5] if zoom else [0, duration])
    source = 'data/R7/static/2026-02-21/sw/dane_wykres_artur.csv'
    rows = read_csv(source)
    t = [float(r['Timestamp'])-float(rows[0]['Timestamp']) for r in rows]
    series = []
    for token, label, window in [('Tank Pressure', 'Zbiornik', 15), ('Tank D Pressure', 'Komora', 1)]:
        values, last = [], None
        for row in rows:
            match = re.search(r'Receive new '+token+r':\s*([-\d.]+) Bar', row['Payload'])
            if match:
                last = float(match[1])
            values.append(last)
        # Forward fill follows the notebook; retain unavailable leading samples as gaps.
        y = [sum(values[i-window+1:i+1])/window if i >= window-1 and None not in values[i-window+1:i+1] else None for i in range(len(values))]
        ids = [i for i, v in enumerate(t) if 1740 <= v <= 1755]
        series.append(trace(label, [t[i] for i in ids], [y[i] for i in ids]))
    charts['R7/tests/static/2026-02-21/pressure'] = chart(series, 'Ciśnienie [bar]', source,
        'Przeliczenia z notebooka: podtrzymanie ostatniego pomiaru; zbiornik — średnia 15 próbek. Oba czujniki logują bar.', [1743, 1752])
    for path in sorted((ROOT/'data/R7').rglob('*.eng')):
        pairs = [list(map(float, line.split())) for line in path.read_text().splitlines()[1:] if line.strip()]
        x, y = map(list, zip(*pairs))
        impulse = [0.0]
        for i in range(1, len(x)):
            impulse.append(impulse[-1]+(x[i]-x[i-1])*(y[i]+y[i-1])/2)
        kind, date = path.relative_to(ROOT/'data/R7').parts[:2]
        charts[f'R7/tests/{kind}/{date}/thrust'] = chart([
            trace('Ciąg — filtr Savitzky–Golay', x, y),
            trace('Impuls', x, impulse, yaxis='y2')], 'Ciąg [N]', str(path.relative_to(ROOT)),
            'Zapisana krzywa .eng (filtr SG 21/3), bez ponownej kalibracji. Impuls: całkowanie trapezami; czas od pierwszej próbki.',
            yaxis2=dict(title=dict(text='Impuls [N·s]'), overlaying='y', side='right'))
    source = 'data/Liquid-Rurku/cold-flow/2026_07_04/data.csv'
    rows = read_csv(source)
    times = [datetime.strptime(r['timestamp'], '%H:%M:%S.%f') for r in rows]
    t = [(v-times[0]).total_seconds() for v in times]
    ids = [i for i, v in enumerate(t) if 340 <= v <= 380]
    series = [trace(label, [t[i]-340 for i in ids], [number(rows[i][col]) for i in ids]) for col, label in [
        ('newchamberpressevent1', 'Komora'), ('newoxidizerpressevent', 'Utleniacz'), ('newpressurefeedpressevent', 'Pressure feed')]]
    charts['Liquid-Rurku/tests/cold-flow/pressure'] = chart(series, 'Ciśnienie [wartość z CSV]', source,
        'Zakres 340–380 s według notebooka. CSV zawiera już korektę pressure feed — nie stosujemy jej drugi raz. Jednostka nie została potwierdzona w notebooku.', [0, 40])
    # No saved recipe ties the July PNG to a particular window. Publish both logs explicitly.
    for run in (1, 2):
        source = f'data/Liquid-Rurku/static/2026_07_14/launch{run}_app.csv'
        rows = read_csv(source)
        times = [datetime.fromisoformat(r['timestamp']) for r in rows]
        x = [(v-times[0]).total_seconds() for v in times]
        series = [trace(label, x, [number(r[col]) for r in rows]) for col, label in [
            ('envapp_newoxidizerpressevent', 'Utleniacz'), ('envapp_newpressurefeedpressevent', 'Pressure feed'),
            ('envapp_newchamberpressevent1', 'Komora 1'), ('secenvapp_newethanolpressevent', 'Etanol'),
            ('secenvapp_newchamberpressevent3', 'Komora 3')]]
        # The app log has a 44-minute recording break; do not draw a false connecting line.
        for line in series:
            for i in reversed(range(1, len(x))):
                if x[i] - x[i-1] > 5:
                    line['x'] = line['x'][:i] + [(x[i]+x[i-1])/2] + line['x'][i:]
                    line['y'].insert(i, None)
        charts[f'Liquid-Rurku/tests/static/2026_07_14/launch{run}'] = chart(series, 'Ciśnienie [bar]', source,
            f'Pełny log aplikacji launch{run}; czas od pierwszej próbki. Przerwy rejestracji >5 s są przerwami linii. Archiwalny PNG nie ma zapisanej receptury wyboru zakresu.')
    return charts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if committed chart data is stale')
    args = parser.parse_args()
    for name, spec in generate().items():
        path = ROOT/'src'/f'{name}.plot.json'
        content = json.dumps(spec, ensure_ascii=False, allow_nan=False, separators=(',', ':'))+'\n'
        if args.check:
            if not path.exists() or path.read_text() != content:
                raise SystemExit(f'Stale chart: {path}; run python3 scripts/charts/generate.py')
        else:
            path.write_text(content)
        print(name)


if __name__ == '__main__':
    main()
