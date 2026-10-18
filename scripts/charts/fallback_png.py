#!/usr/bin/env python3
"""Render a static PNG fallback from *.plot.json for reports without an archival image."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

COLORS = ['#0072B2', '#D55E00', '#009E73', '#CC79A7', '#8c6300']


def render(path):
    spec = json.loads(Path(path).read_text())
    layout = spec['layout']
    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
    ax2 = ax.twinx() if 'yaxis2' in layout else None
    for color, trace in zip(COLORS, spec['data']):
        axis = ax2 if trace.get('yaxis') == 'y2' else ax
        y = [float('nan') if v is None else v for v in trace['y']]
        style = 'steps-post' if trace.get('line', {}).get('shape') == 'hv' else 'default'
        axis.plot(trace['x'], y, color=color, label=trace['name'], linewidth=.8, drawstyle=style)
    ax.set_xlabel(layout['xaxis']['title']['text'])
    ax.set_ylabel(layout['yaxis']['title']['text'])
    if 'range' in layout['xaxis']:
        ax.set_xlim(layout['xaxis']['range'])
    if ax2:
        ax2.set_ylabel(layout['yaxis2']['title']['text'])
    handles = [h for a in (ax, ax2) if a for h in a.get_legend_handles_labels()[0]]
    ax.legend(handles, [h.get_label() for h in handles], loc='upper right')
    ax.grid(alpha=.3)
    fig.tight_layout()
    out = Path(path).with_name(Path(path).name.removesuffix('.plot.json') + '.png')
    fig.savefig(out)
    print(out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('charts', nargs='+', help='*.plot.json files')
    for chart in parser.parse_args().charts:
        render(chart)
