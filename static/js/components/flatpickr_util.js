// Utilitário para inicialização do Flatpickr com configurações padrão do OMAUM
// Carrega Flatpickr e idioma português do Brasil

(function() {
    console.log('📅 [FLATPICKR-UTIL] Inicializando utilitário Flatpickr...');
    
    // Carrega CSS do Flatpickr via CDN
    const cssLink = document.createElement('link');
    cssLink.rel = 'stylesheet';
    cssLink.href = 'https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css';
    document.head.appendChild(cssLink);
    console.log('📅 [FLATPICKR-UTIL] CSS do Flatpickr carregado via CDN');
    
    // Verifica se Flatpickr está disponível
    if (typeof flatpickr === 'undefined') {
        console.warn('⚠️ [FLATPICKR-UTIL] Flatpickr não encontrado. Carregando via CDN...');
        
        // Carrega JS do Flatpickr
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/flatpickr';
        script.onload = function() {
            console.log('✅ [FLATPICKR-UTIL] Flatpickr carregado via CDN');
            loadPortuguese();
        };
        script.onerror = function() {
            console.error('❌ [FLATPICKR-UTIL] Erro ao carregar Flatpickr via CDN');
        };
        document.head.appendChild(script);
    } else {
        console.log('✅ [FLATPICKR-UTIL] Flatpickr já disponível');
        loadPortuguese();
    }
    
    function loadPortuguese() {
        // Carrega idioma português
        if (typeof flatpickr !== 'undefined' && !flatpickr.l10ns.pt) {
            const langScript = document.createElement('script');
            langScript.src = 'https://cdn.jsdelivr.net/npm/flatpickr/dist/l10n/pt.js';
            langScript.onload = function() {
                console.log('✅ [FLATPICKR-UTIL] Idioma português carregado');
                initializeDefaults();
            };
            document.head.appendChild(langScript);
        } else if (typeof flatpickr !== 'undefined') {
            initializeDefaults();
        }
    }
    
    function initializeDefaults() {
        // Configurações padrão para o OMAUM
        window.FlatpickrUtil = {
            defaultConfig: {
                locale: 'pt',
                dateFormat: 'd/m/Y',
                altFormat: 'd/m/Y',
                altInput: true,
                allowInput: true,
                clickOpens: true
            },
            
            // Inicializa múltiplas datas (para dias de atividades)
            initMultiple: function(selector, options) {
                const config = Object.assign({}, this.defaultConfig, {
                    mode: 'multiple',
                    conjunction: ', '
                }, options || {});
                
                return flatpickr(selector, config);
            },
            
            // Inicializa data única
            initSingle: function(selector, options) {
                const config = Object.assign({}, this.defaultConfig, options || {});
                return flatpickr(selector, config);
            }
        };
        
        console.log('✅ [FLATPICKR-UTIL] Configurações padrão definidas');
        
        // Dispara evento personalizado quando estiver pronto
        console.log('📅 [FLATPICKR-UTIL] 🔔 Despachando evento flatpickr-ready...');
        document.dispatchEvent(new CustomEvent('flatpickr-ready'));
        console.log('✅ [FLATPICKR-UTIL] 🎉 Evento flatpickr-ready despachado com sucesso!');
    }
})();
