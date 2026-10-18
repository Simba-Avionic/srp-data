"""Numerical/provenance checks independent of the browser."""
import importlib.util
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('charts', ROOT/'scripts/charts/generate.py')
charts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(charts)


class ChartsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.charts = charts.generate()

    def test_all_embeds_resolve_and_all_generated_charts_are_used(self):
        used = set()
        for page in (ROOT/'src').rglob('*.md'):
            for ref in re.findall(r'data-chart="([^"]+)"', page.read_text()):
                path = page.parent/ref
                self.assertTrue(path.is_file(), path)
                used.add(str(path.relative_to(ROOT/'src')).removesuffix('.plot.json'))
        self.assertEqual(used, set(self.charts))

    def test_finite_aligned_monotonic_measurements(self):
        for name, chart in self.charts.items():
            self.assertTrue((ROOT/chart['source']).is_file())
            json.dumps(chart, allow_nan=False)
            for trace in chart['data']:
                self.assertEqual(len(trace['x']), len(trace['y']), name)
                self.assertTrue(all(a <= b for a, b in zip(trace['x'], trace['x'][1:])), name)
                self.assertTrue(any(v is not None for v in trace['y']), name)

    def test_pressure_conversion_and_raw_oscillations(self):
        for date, offset in [('2026-03-21', 81), ('2026-04-10', 210.5)]:
            raw = charts.read_csv(f'data/R7/static/{date}/sw/start.csv', ';')
            expected = [(float(r['TIMESTAMP'])-float(raw[0]['TIMESTAMP']))/1000-offset for r in raw]
            first = next(i for i, t in enumerate(expected) if t > 0)
            result = self.charts[f'R7/tests/static/{date}/pressure_zoom']['data'][0]
            self.assertAlmostEqual(result['x'][0], expected[first])
            self.assertEqual(result['y'][0], float(raw[first]['TANK_PRESS'])/100)
            window = 20 if date == '2026-03-21' else 2
            smoothed = self.charts[f'R7/tests/static/{date}/pressure']['data'][0]
            self.assertAlmostEqual(smoothed['y'][0], sum(float(r['TANK_PRESS'])/100 for r in raw[first-window+1:first+1])/window)

    def test_thrust_preserves_export_and_impulse(self):
        for name, chart in self.charts.items():
            if not name.endswith('/thrust'):
                continue
            source = ROOT/chart['source']
            if source.suffix == '.eng':
                expected = [tuple(map(float, line.split())) for line in source.read_text().splitlines()[1:] if line.strip()]
            else:
                expected = [tuple(map(float, line.split(','))) for line in source.read_text().splitlines() if line.strip()]
            thrust, impulse = chart['data']
            self.assertEqual(list(zip(thrust['x'], thrust['y'])), expected)
            area = sum((b[0]-a[0])*(a[1]+b[1])/2 for a,b in zip(expected, expected[1:]))
            self.assertAlmostEqual(impulse['y'][-1], area)

    def test_step_compression_is_lossless(self):
        raw = charts.read_csv('data/R7/static/2026-10-15/sw/all.csv')
        for trace, convert in zip(self.charts['R7/tests/static/2026-10-15/pressure']['data'],
                                  [lambda r: float(r['OxidizerPressure']), lambda r: charts.chamber_bar(r['ChamberPress'])]):
            self.assertEqual(trace['line']['shape'], 'hv')
            self.assertEqual(trace['x'][-1], round(float(raw[-1]['TIMESTAMP']), 3))
            j = 0
            for row in raw:
                t = round(float(row['TIMESTAMP']), 3)
                while j+1 < len(trace['x']) and trace['x'][j+1] <= t:
                    j += 1
                self.assertEqual(trace['y'][j], convert(row))

    def test_launch_window_keeps_raw_samples(self):
        raw = charts.read_csv('data/R7/static/2026-10-15/sw/launch.csv')
        oxidizer, chamber = self.charts['R7/tests/static/2026-10-15/pressure_zoom']['data']
        self.assertEqual(oxidizer['x'][0], 0)
        self.assertEqual(oxidizer['y'], [float(r['OxidizerPressure']) for r in raw])
        self.assertEqual(len(chamber['y']), len(raw))

    def test_chamber_recalibration(self):
        # Logged: 100*(166.6667*V - 99); actual sensor 12: 41.66667*V - 23.98677, i.e. raw/400 + 0.7632.
        for raw in (-540, 0, 7032, 9476):
            self.assertAlmostEqual(charts.chamber_bar(raw), raw/400 + 0.7632, places=3)
        raw = charts.read_csv('data/R7/static/2026-10-15/sw/launch.csv')
        chamber = self.charts['R7/tests/static/2026-10-15/pressure_zoom']['data'][1]['y']
        self.assertTrue(all(c < float(r['OxidizerPressure']) for c, r in zip(chamber, raw) if c > 3))

    def test_recording_break_is_not_connected(self):
        for trace in self.charts['Liquid-Rurku/tests/static/2026_07_14/launch1']['data']:
            self.assertIn(None, trace['y'])
            for i in range(1, len(trace['x'])):
                if trace['x'][i] - trace['x'][i-1] > 5:
                    self.assertTrue(trace['y'][i] is None or trace['y'][i-1] is None)

    def test_liquid_does_not_recalibrate_csv(self):
        result = self.charts['Liquid-Rurku/tests/cold-flow/pressure']['data'][2]
        rows = charts.read_csv('data/Liquid-Rurku/cold-flow/2026_07_04/data.csv')
        origin = charts.datetime.strptime(rows[0]['timestamp'], '%H:%M:%S.%f')
        expected = [float(r['newpressurefeedpressevent']) for r in rows if 340 <= (charts.datetime.strptime(r['timestamp'], '%H:%M:%S.%f')-origin).total_seconds() <= 380]
        self.assertEqual(result['y'], expected)


if __name__ == '__main__':
    unittest.main()
