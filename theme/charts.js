/* Progressive enhancement: original images survive JavaScript/network failures. */
(() => {
  'use strict';
  if (location.pathname.endsWith('/print.html')) return;
  const printState = new Map();
  function preparePrint() {
    document.querySelectorAll('.chart-fallback').forEach(details => {
      if (!printState.has(details)) printState.set(details, details.open);
      details.open = true;
    });
  }
  function restorePrint() {
    printState.forEach((open, details) => { details.open = open; });
    printState.clear();
  }
  window.addEventListener('beforeprint', preparePrint);
  window.addEventListener('afterprint', restorePrint);
  matchMedia('print').addEventListener('change', event => event.matches ? preparePrint() : restorePrint());
  const scriptURL = document.currentScript.src;
  let library;
  function loadPlotly() {
    if (!library) library = new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = new URL('../vendor/plotly-basic-3.7.0.min.js', scriptURL).href;
      script.onload = () => resolve(window.Plotly);
      script.onerror = () => reject(new Error('Nie udało się załadować biblioteki wykresów.'));
      document.head.append(script);
    });
    return library;
  }
  function button(text, action) {
    const node = document.createElement('button');
    node.type = 'button'; node.textContent = text;
    node.addEventListener('click', action);
    return node;
  }
  async function activate(host) {
    const status = document.createElement('p');
    status.setAttribute('role', 'status');
    status.textContent = 'Ładowanie wykresu…';
    host.prepend(status);
    const plot = document.createElement('div');
    plot.className = 'chart-canvas';
    plot.setAttribute('role', 'img');
    plot.setAttribute('aria-label', host.dataset.title || 'Interaktywny wykres pomiarów');
    try {
      const [Plotly, response] = await Promise.all([loadPlotly(), fetch(host.dataset.chart)]);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const spec = await response.json();
      host.insertBefore(plot, status);
      const layout = {...structuredClone(spec.layout), autosize: true,
        margin: {t: 25, b: 110, l: 65, r: spec.layout.yaxis2 ? 70 : 25},
        showlegend: true, legend: {orientation: 'h', y: -0.25},
        hovermode: 'x unified', dragmode: 'zoom',
        paper_bgcolor: '#fff', plot_bgcolor: '#fff', font: {color: '#222'},
        colorway: ['#0072B2', '#D55E00', '#009E73', '#CC79A7', '#8c6300']};
      await Plotly.newPlot(plot, spec.data, layout, {
        responsive: true, scrollZoom: true, displaylogo: false,
        displayModeBar: true, showTips: false, modeBarButtonsToRemove: ['select2d', 'lasso2d'],
        toImageButtonOptions: {format: 'png', filename: 'wykres', scale: 2}
      });
      const controls = document.createElement('div'); controls.className = 'chart-controls';
      controls.append(button('Resetuj widok', () => {
        const update = {'yaxis.autorange': true};
        if (spec.layout.xaxis.range) update['xaxis.range'] = spec.layout.xaxis.range.slice();
        else update['xaxis.autorange'] = true;
        if (spec.layout.yaxis2) update['yaxis2.autorange'] = true;
        Plotly.relayout(plot, update);
      }), button('Pokaż wszystkie linie', () => Plotly.restyle(plot, {visible: true})),
      button('Powiększ / zmniejsz', () => {
        host.classList.toggle('chart-expanded'); Plotly.Plots.resize(plot);
      }));
      // Keyboard-accessible trace toggles supplement Plotly's SVG legend.
      spec.data.forEach((trace, index) => {
        const label = document.createElement('label'), input = document.createElement('input');
        input.type = 'checkbox'; input.checked = true;
        input.addEventListener('change', () => Plotly.restyle(plot, {visible: input.checked ? true : 'legendonly'}, [index]));
        label.append(input, document.createTextNode(trace.name)); controls.append(label);
        plot.on('plotly_restyle', () => { input.checked = plot.data[index].visible !== 'legendonly' && plot.data[index].visible !== false; });
      });
      host.insertBefore(controls, plot);
      status.textContent = 'Zaznacz obszar, aby przybliżyć; kółko myszy zmienia skalę. Przesuwanie: narzędzie Pan. Kliknij legendę, aby ukryć linię; dwuklik izoluje serię.';
      const provenance = document.createElement('p'); provenance.className = 'chart-source';
      provenance.textContent = `${spec.note} Źródło: ${spec.source}`;
      host.append(provenance);
      const fallback = host.querySelector('.chart-fallback');
      if (fallback) fallback.open = false;
      const observer = new ResizeObserver(() => {
        if (plot.offsetWidth && plot.offsetHeight && !matchMedia('print').matches) {
          Plotly.Plots.resize(plot).catch(() => { /* The print dialog can hide a pending resize. */ });
        }
      });
      observer.observe(host);
      host.dataset.loaded = 'true';
    } catch (error) {
      plot.remove(); status.textContent = 'Nie udało się wczytać wykresu. Dostępny jest obraz archiwalny. ' + error.message;
      const fallback = host.querySelector('.chart-fallback');
      if (fallback) fallback.open = true;
    }
  }
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) if (entry.isIntersecting) {
      observer.unobserve(entry.target); activate(entry.target);
    }
  }, {rootMargin: '300px'});
  document.querySelectorAll('[data-chart]').forEach(host => observer.observe(host));
})();
