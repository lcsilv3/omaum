(function(window, document) {
  'use strict';

  if (window.FlatpickrUtil) return; // evitar redefinição

  function loadScriptOnce(id, src) {
    return new Promise((resolve, reject) => {
      if (document.getElementById(id)) {
        // já carregando/carregado
        const el = document.getElementById(id);
        if (el.getAttribute('data-loaded') === '1') return resolve();
        el.addEventListener('load', () => resolve());
        el.addEventListener('error', (e) => reject(e));
        return;
      }
      const s = document.createElement('script');
      s.id = id;
      s.src = src;
      s.async = true;
      s.addEventListener('load', () => { s.setAttribute('data-loaded', '1'); resolve(); });
      s.addEventListener('error', (e) => reject(e));
      document.head.appendChild(s);
    });
  }

  async function ensureLoaded() {
    if (typeof window.flatpickr === 'function') return;

    const base = window.FLATPICKR_BASE_URL || '/static/vendor/flatpickr';
    const STRICT_LOCAL = (window.FLATPICKR_STRICT_LOCAL !== false); // por padrão, só local; definir false para permitir fallback CDN
    // 1) Tenta local vendorizado
    try {
      await loadScriptOnce('flatpickr-local', base.replace(/\/$/, '') + '/flatpickr.min.js');
    } catch (localErr) {
      if (STRICT_LOCAL) {
        console.error('[FlatpickrUtil] Falha ao carregar Flatpickr local e modo estrito habilitado.');
        throw localErr;
      }
      // 2) CDN primário (apenas se modo estrito desabilitado)
      try {
        await loadScriptOnce('flatpickr-cdn', 'https://cdn.jsdelivr.net/npm/flatpickr@4.6.13/dist/flatpickr.min.js');
      } catch (cdnErr) {
        // 3) Fallback unpkg
        try {
          await loadScriptOnce('flatpickr-unpkg', 'https://unpkg.com/flatpickr@4.6.13/dist/flatpickr.min.js');
        } catch (err) {
          console.error('[FlatpickrUtil] Falha ao carregar Flatpickr (local/CDN).', err);
          throw err;
        }
      }
    }

    // Locale pt-BR
    try {
      await loadScriptOnce('flatpickr-l10n-pt', base.replace(/\/$/, '') + '/l10n/pt.js');
    } catch (localLocaleErr) {
      if (STRICT_LOCAL) {
        console.warn('[FlatpickrUtil] Falha ao carregar locale pt local e modo estrito habilitado. Prosseguindo com locale default.');
      } else {
        try {
          await loadScriptOnce('flatpickr-l10n-pt-cdn', 'https://cdn.jsdelivr.net/npm/flatpickr@4.6.13/dist/l10n/pt.js');
        } catch (cdnLocaleErr) {
          try {
            await loadScriptOnce('flatpickr-l10n-pt-unpkg', 'https://unpkg.com/flatpickr@4.6.13/dist/l10n/pt.js');
          } catch (err) {
            console.warn('[FlatpickrUtil] Locale pt não carregado; seguindo com default.', err);
          }
        }
      }
    }
  }

  function bindOpenHandlers(input, options) {
    const cfg = Object.assign({ openOnIcon: true, openOnInput: true, iconSelector: '.calendar-icon' }, options || {});
    // Ícone
    if (cfg.openOnIcon) {
      const icon = input.parentElement ? input.parentElement.querySelector(cfg.iconSelector) : null;
      if (icon) {
        icon.addEventListener('click', (e) => {
          e.preventDefault();
          if (input._flatpickr) input._flatpickr.open();
        });
      }
    }
    // Input
    if (cfg.openOnInput) {
      input.addEventListener('click', () => {
        if (input._flatpickr) input._flatpickr.open();
      });
    }
  }

  function initInput(input, options, bindOptions) {
    const base = Object.assign({
      mode: 'multiple',
      dateFormat: 'd',
      locale: (window.flatpickr && window.flatpickr.l10ns && window.flatpickr.l10ns.pt) ? window.flatpickr.l10ns.pt : 'pt'
    }, options || {});
    const instance = window.flatpickr(input, base);
    bindOpenHandlers(input, bindOptions);
    return instance;
  }

  async function withFlatpickr(callback) {
    try {
      await ensureLoaded();
      if (typeof callback === 'function') callback();
    } catch (e) {
      console.error('[FlatpickrUtil] withFlatpickr falhou:', e);
    }
  }

  window.FlatpickrUtil = {
    ensureLoaded,
    withFlatpickr,
    initInput,
    bindOpenOnIcon: (input) => bindOpenHandlers(input, { openOnIcon: true, openOnInput: false }),
    bindOpenHandlers
  };
})(window, document);
