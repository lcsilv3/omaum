// Utilidades de máscaras e auto-preenchimento para o app Alunos
// Fase 1-2: CEP -> (rua,bairro,cidade,estado) e Estado -> Cidades (com cache simples)
(function(){
  const cacheCidadesPorEstado = {}; // {estadoId: [{id,nome}, ...]}
  
  // Máscara de CPF: aceita entrada com ou sem formatação, aplica formato 999.999.999-99
  function maskCPF(v){
    const digits = v.replace(/\D/g,''); // Remove tudo que não é dígito
    if (digits.length === 0) return '';
    if (digits.length <= 3) return digits;
    if (digits.length <= 6) return digits.replace(/(\d{3})(\d{1,3})/,'$1.$2');
    if (digits.length <= 9) return digits.replace(/(\d{3})(\d{3})(\d{1,3})/,'$1.$2.$3');
    return digits.substring(0,11).replace(/(\d{3})(\d{3})(\d{3})(\d{1,2})/,'$1.$2.$3-$4');
  }
  
  // MÁSCARA ROBUSTA CEP: Suporta dois formatos via Shift
  // Formato 1 (padrão): _____-___ (ex: 20250-450)
  // Formato 2 (Shift): __.___ -___ (ex: 20.250-450)
  function createCEPMask(input) {
    let useShortFormat = false; // false = _____-___, true = __.___ -___
    let currentDigits = [];
    const MAX_DIGITS = 8;

    function getTemplate() {
      return useShortFormat ? '__.___-___' : '_____-___';
    }

    function getDigitPositions() {
      return useShortFormat ? [0, 1, 3, 4, 5, 7, 8, 9] : [0, 1, 2, 3, 4, 6, 7, 8];
    }

    function applyMask() {
      const template = getTemplate();
      const positions = getDigitPositions();
      const chars = template.split('');
      currentDigits.forEach((digit, i) => {
        if (i < positions.length) {
          chars[positions[i]] = digit;
        }
      });
      return chars.join('');
    }

    function updateValue() {
      input.value = applyMask();
    }

    function setCursorPosition() {
      const positions = getDigitPositions();
      const pos = currentDigits.length < positions.length 
        ? positions[currentDigits.length] 
        : getTemplate().length;
      setTimeout(() => {
        input.setSelectionRange(pos, pos);
      }, 0);
    }

    function handleKeyDown(e) {
      // Alternar formato com Shift+C
      if (e.shiftKey && e.key.toLowerCase() === 'c') {
        e.preventDefault();
        useShortFormat = !useShortFormat;
        updateValue();
        setCursorPosition();
        console.log('🔄 Formato CEP alternado para:', useShortFormat ? '__.___-___' : '_____-___');
        return;
      }

      if (['Tab', 'Shift', 'Control', 'Alt', 'Meta'].includes(e.key)) {
        return;
      }

      if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'].includes(e.key)) {
        e.preventDefault();
        return;
      }

      if (e.key === 'Backspace') {
        e.preventDefault();
        if (currentDigits.length > 0) {
          currentDigits.pop();
          updateValue();
          setCursorPosition();
        }
        return;
      }

      if (e.key === 'Delete') {
        e.preventDefault();
        currentDigits = [];
        updateValue();
        setCursorPosition();
        return;
      }

      if (!/^\d$/.test(e.key)) {
        e.preventDefault();
        return;
      }

      if (currentDigits.length >= MAX_DIGITS) {
        e.preventDefault();
        return;
      }

      e.preventDefault();
      currentDigits.push(e.key);
      updateValue();
      setCursorPosition();
    }

    function handleInput(e) {
      e.preventDefault();
      updateValue();
      setCursorPosition();
    }

    function handlePaste(e) {
      e.preventDefault();
      const text = (e.clipboardData || window.clipboardData).getData('text');
      const digits = text.replace(/\D/g,'').substring(0, MAX_DIGITS);
      currentDigits = digits.split('');
      updateValue();
      setCursorPosition();
    }

    function handleFocus() {
      if (!input.value || input.value.length !== getTemplate().length) {
        updateValue();
      }
      setCursorPosition();
    }

    function handleBlur() {
      if (currentDigits.length === 0) {
        input.value = '';
      }
    }

    function initialize() {
      const existingValue = input.value.replace(/\D/g,'').substring(0, MAX_DIGITS);
      if (existingValue) {
        currentDigits = existingValue.split('');
      }
      updateValue();
      
      input.addEventListener('keydown', handleKeyDown);
      input.addEventListener('input', handleInput);
      input.addEventListener('paste', handlePaste);
      input.addEventListener('focus', handleFocus);
      input.addEventListener('blur', handleBlur);
    }

    initialize();
  } 
  // MÁSCARA ROBUSTA HORA: HH:MM
  function createHoraMask(input) {
    const TEMPLATE = 'HH:MM';
    const DIGIT_POSITIONS = [0, 1, 3, 4];
    const MAX_DIGITS = 4;
    let currentDigits = [];

    function applyMask() {
      const chars = TEMPLATE.split('');
      currentDigits.forEach((digit, i) => {
        if (i < DIGIT_POSITIONS.length) {
          chars[DIGIT_POSITIONS[i]] = digit;
        }
      });
      return chars.join('');
    }

    function updateValue() {
      input.value = applyMask();
    }

    function setCursorPosition() {
      const pos = currentDigits.length < DIGIT_POSITIONS.length 
        ? DIGIT_POSITIONS[currentDigits.length] 
        : TEMPLATE.length;
      setTimeout(() => {
        input.setSelectionRange(pos, pos);
      }, 0);
    }

    function handleKeyDown(e) {
      if (['Tab', 'Shift', 'Control', 'Alt', 'Meta'].includes(e.key)) {
        return;
      }

      if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'].includes(e.key)) {
        e.preventDefault();
        return;
      }

      if (e.key === 'Backspace') {
        e.preventDefault();
        if (currentDigits.length > 0) {
          currentDigits.pop();
          updateValue();
          setCursorPosition();
        }
        return;
      }

      if (e.key === 'Delete') {
        e.preventDefault();
        currentDigits = [];
        updateValue();
        setCursorPosition();
        return;
      }

      if (!/^\d$/.test(e.key)) {
        e.preventDefault();
        return;
      }

      // Validação de hora (HH <= 23, MM <= 59)
      if (currentDigits.length === 0 && parseInt(e.key) > 2) {
        e.preventDefault();
        return;
      }
      if (currentDigits.length === 1 && parseInt(currentDigits[0]) === 2 && parseInt(e.key) > 3) {
        e.preventDefault();
        return;
      }
      if (currentDigits.length === 2 && parseInt(e.key) > 5) {
        e.preventDefault();
        return;
      }

      if (currentDigits.length >= MAX_DIGITS) {
        e.preventDefault();
        return;
      }

      e.preventDefault();
      currentDigits.push(e.key);
      updateValue();
      setCursorPosition();
    }

    function handleInput(e) {
      e.preventDefault();
      updateValue();
      setCursorPosition();
    }

    function handlePaste(e) {
      e.preventDefault();
      const text = (e.clipboardData || window.clipboardData).getData('text');
      const digits = text.replace(/\D/g,'').substring(0, MAX_DIGITS);
      currentDigits = digits.split('');
      updateValue();
      setCursorPosition();
    }

    function handleFocus() {
      if (!input.value || input.value.length !== TEMPLATE.length) {
        updateValue();
      }
      setCursorPosition();
    }

    function handleBlur() {
      if (currentDigits.length === 0) {
        input.value = '';
      }
    }

    function initialize() {
      const existingValue = input.value.replace(/\D/g,'').substring(0, MAX_DIGITS);
      if (existingValue) {
        currentDigits = existingValue.split('');
      }
      updateValue();
      
      input.addEventListener('keydown', handleKeyDown);
      input.addEventListener('input', handleInput);
      input.addEventListener('paste', handlePaste);
      input.addEventListener('focus', handleFocus);
      input.addEventListener('blur', handleBlur);
    }

    initialize();
  }

  // MÁSCARA ROBUSTA CELULAR: (__) _____-____
  function createCelularMask(input) {
    const TEMPLATE = '(__) _____-____';
    const DIGIT_POSITIONS = [1, 2, 5, 6, 7, 8, 9, 11, 12, 13, 14];
    const MAX_DIGITS = 11;
    let currentDigits = [];

    function applyMask() {
      const chars = TEMPLATE.split('');
      currentDigits.forEach((digit, i) => {
        if (i < DIGIT_POSITIONS.length) {
          chars[DIGIT_POSITIONS[i]] = digit;
        }
      });
      return chars.join('');
    }

    function updateValue() {
      input.value = applyMask();
    }

    function setCursorPosition() {
      const pos = currentDigits.length < DIGIT_POSITIONS.length 
        ? DIGIT_POSITIONS[currentDigits.length] 
        : TEMPLATE.length;
      setTimeout(() => {
        input.setSelectionRange(pos, pos);
      }, 0);
    }

    function handleKeyDown(e) {
      if (['Tab', 'Shift', 'Control', 'Alt', 'Meta'].includes(e.key)) {
        return;
      }

      if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'].includes(e.key)) {
        e.preventDefault();
        return;
      }

      if (e.key === 'Backspace') {
        e.preventDefault();
        if (currentDigits.length > 0) {
          currentDigits.pop();
          updateValue();
          setCursorPosition();
        }
        return;
      }

      if (e.key === 'Delete') {
        e.preventDefault();
        currentDigits = [];
        updateValue();
        setCursorPosition();
        return;
      }

      if (!/^\d$/.test(e.key)) {
        e.preventDefault();
        return;
      }

      if (currentDigits.length >= MAX_DIGITS) {
        e.preventDefault();
        return;
      }

      e.preventDefault();
      currentDigits.push(e.key);
      updateValue();
      setCursorPosition();
    }

    function handleInput(e) {
      e.preventDefault();
      updateValue();
      setCursorPosition();
    }

    function handlePaste(e) {
      e.preventDefault();
      const text = (e.clipboardData || window.clipboardData).getData('text');
      const digits = text.replace(/\D/g,'').substring(0, MAX_DIGITS);
      currentDigits = digits.split('');
      updateValue();
      setCursorPosition();
    }

    function handleFocus() {
      if (!input.value || input.value.length !== TEMPLATE.length) {
        updateValue();
      }
      setCursorPosition();
    }

    function handleBlur() {
      if (currentDigits.length === 0) {
        input.value = '';
      }
    }

    function initialize() {
      const existingValue = input.value.replace(/\D/g,'').substring(0, MAX_DIGITS);
      if (existingValue) {
        currentDigits = existingValue.split('');
      }
      updateValue();
      
      input.addEventListener('keydown', handleKeyDown);
      input.addEventListener('input', handleInput);
      input.addEventListener('paste', handlePaste);
      input.addEventListener('focus', handleFocus);
      input.addEventListener('blur', handleBlur);
    }

    initialize();
  }

  // MÁSCARA ROBUSTA TELEFONE: (__) ____-____
  function createTelefoneMask(input) {
    const TEMPLATE = '(__) ____-____';
    const DIGIT_POSITIONS = [1, 2, 5, 6, 7, 8, 10, 11, 12, 13];
    const MAX_DIGITS = 10;
    let currentDigits = [];

    function applyMask() {
      const chars = TEMPLATE.split('');
      currentDigits.forEach((digit, i) => {
        if (i < DIGIT_POSITIONS.length) {
          chars[DIGIT_POSITIONS[i]] = digit;
        }
      });
      return chars.join('');
    }

    function updateValue() {
      input.value = applyMask();
    }

    function setCursorPosition() {
      const pos = currentDigits.length < DIGIT_POSITIONS.length 
        ? DIGIT_POSITIONS[currentDigits.length] 
        : TEMPLATE.length;
      setTimeout(() => {
        input.setSelectionRange(pos, pos);
      }, 0);
    }

    function handleKeyDown(e) {
      if (['Tab', 'Shift', 'Control', 'Alt', 'Meta'].includes(e.key)) {
        return;
      }

      if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'].includes(e.key)) {
        e.preventDefault();
        return;
      }

      if (e.key === 'Backspace') {
        e.preventDefault();
        if (currentDigits.length > 0) {
          currentDigits.pop();
          updateValue();
          setCursorPosition();
        }
        return;
      }

      if (e.key === 'Delete') {
        e.preventDefault();
        currentDigits = [];
        updateValue();
        setCursorPosition();
        return;
      }

      if (!/^\d$/.test(e.key)) {
        e.preventDefault();
        return;
      }

      if (currentDigits.length >= MAX_DIGITS) {
        e.preventDefault();
        return;
      }

      e.preventDefault();
      currentDigits.push(e.key);
      updateValue();
      setCursorPosition();
    }

    function handleInput(e) {
      e.preventDefault();
      updateValue();
      setCursorPosition();
    }

    function handlePaste(e) {
      e.preventDefault();
      const text = (e.clipboardData || window.clipboardData).getData('text');
      const digits = text.replace(/\D/g,'').substring(0, MAX_DIGITS);
      currentDigits = digits.split('');
      updateValue();
      setCursorPosition();
    }

    function handleFocus() {
      if (!input.value || input.value.length !== TEMPLATE.length) {
        updateValue();
      }
      setCursorPosition();
    }

    function handleBlur() {
      if (currentDigits.length === 0) {
        input.value = '';
      }
    }

    function initialize() {
      const existingValue = input.value.replace(/\D/g,'').substring(0, MAX_DIGITS);
      if (existingValue) {
        currentDigits = existingValue.split('');
      }
      updateValue();
      
      input.addEventListener('keydown', handleKeyDown);
      input.addEventListener('input', handleInput);
      input.addEventListener('paste', handlePaste);
      input.addEventListener('focus', handleFocus);
      input.addEventListener('blur', handleBlur);
    }

    initialize();
  }
  function cleanDigits(v){return v.replace(/\D/g,'');}
  /**
   * Máscara robusta para Ordem de Serviço: ____/____ (formato NNNN/AAAA)
   * Mantém template visível e permite apenas 8 dígitos
   */
  function createOrdemServicoMask(input) {
    const TEMPLATE = '____/____';
    const DIGIT_POSITIONS = [0, 1, 2, 3, 5, 6, 7, 8];
    const MAX_DIGITS = 8;
    let currentDigits = [];

    function applyMask() {
      const chars = TEMPLATE.split('');
      currentDigits.forEach((digit, i) => {
        if (i < DIGIT_POSITIONS.length) {
          chars[DIGIT_POSITIONS[i]] = digit;
        }
      });
      return chars.join('');
    }

    function updateValue() {
      input.value = applyMask();
    }

    function setCursorPosition() {
      const pos = currentDigits.length < DIGIT_POSITIONS.length 
        ? DIGIT_POSITIONS[currentDigits.length] 
        : TEMPLATE.length;
      setTimeout(() => {
        input.setSelectionRange(pos, pos);
      }, 0);
    }

    function handleKeyDown(e) {
      console.log('🔑 keydown Ordem Serviço:', e.key, 'Dígitos atuais:', currentDigits.length);
      
      if (['Tab', 'Shift', 'Control', 'Alt', 'Meta'].includes(e.key)) {
        return;
      }

      if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'].includes(e.key)) {
        e.preventDefault();
        return;
      }

      if (e.key === 'Backspace') {
        e.preventDefault();
        if (currentDigits.length > 0) {
          currentDigits.pop();
          updateValue();
          setCursorPosition();
          // Limpar validação visual ao editar
          input.style.borderColor = '';
          input.style.backgroundColor = '';
        }
        return;
      }

      if (e.key === 'Delete') {
        e.preventDefault();
        if (currentDigits.length > 0) {
          currentDigits.pop();
          updateValue();
          setCursorPosition();
          input.style.borderColor = '';
          input.style.backgroundColor = '';
        }
        return;
      }

      if (!/^\d$/.test(e.key)) {
        e.preventDefault();
        return;
      }

      if (currentDigits.length >= MAX_DIGITS) {
        e.preventDefault();
        return;
      }

      e.preventDefault();
      currentDigits.push(e.key);
      updateValue();
      setCursorPosition();
      
      // Validar ano quando completar 8 dígitos (NNNN/AAAA)
      if (currentDigits.length === MAX_DIGITS) {
        const ano = parseInt(currentDigits.slice(4, 8).join(''));
        if (ano < 1900 || ano > 2099) {
          input.style.borderColor = '#dc3545';
          input.style.backgroundColor = '#fff5f5';
          setTimeout(() => {
            input.style.borderColor = '';
            input.style.backgroundColor = '';
          }, 2000);
          console.warn('⚠️ Ano fora do intervalo válido (1900-2099):', ano);
        } else {
          input.style.borderColor = '#28a745';
          setTimeout(() => {
            input.style.borderColor = '';
          }, 1000);
        }
      }
    }

    function handleInput(e) {
      e.preventDefault();
      updateValue();
      setCursorPosition();
    }

    function handlePaste(e) {
      e.preventDefault();
    }

    function handleFocus() {
      if (!input.value || input.value.length !== TEMPLATE.length) {
        updateValue();
      }
      setCursorPosition();
    }

    function handleBlur() {
      if (currentDigits.length === 0) {
        input.value = '';
      }
    }

    function initialize() {
      const initialValue = input.value || '';
      if (initialValue) {
        const digits = initialValue.replace(/\D/g, '').slice(0, MAX_DIGITS).split('');
        currentDigits = digits;
      }
      updateValue();
    }

    initialize();

    input.addEventListener('keydown', handleKeyDown);
    input.addEventListener('input', handleInput);
    input.addEventListener('paste', handlePaste);
    input.addEventListener('focus', handleFocus);
    input.addEventListener('blur', handleBlur);
  }

  function applyPhoneMasks(){
    const phoneIds=['celular_primeiro_contato','celular_segundo_contato','telefone','celular'];
    phoneIds.forEach(id=>{const el=document.getElementById('id_'+id); if(el){el.value=maskPhone(el.value||'');}});
    document.querySelectorAll('[data-mask-phone]').forEach(el=>{
      el.value=maskPhone(el.value||'');
    });
  }

  // Máscaras para exibição (spans) no modo de detalhe
  function applyDisplayMasks(){
    const formatText=(selector, formatter)=>{
      document.querySelectorAll(selector).forEach(el=>{
        const raw=(el.textContent||'').trim();
        if(!raw) return;
        const formatted=formatter(raw);
        if(formatted) el.textContent=formatted;
      });
    };

    formatText('.cpf-mask', maskCPF);
    formatText('.cep-mask', maskCEP);
    formatText('.celular-mask', maskPhone);
    formatText('.telefone-mask', maskPhone);
  }
  window.applyDisplayMasks = applyDisplayMasks;

  function attach(){
    // Máscara CPF (mantém legado por compatibilidade com forms.py)
    const cpf=document.getElementById('id_cpf'); if(cpf){cpf.addEventListener('input',e=>e.target.value=maskCPF(e.target.value)); cpf.value=maskCPF(cpf.value||'');}

    // Aplicar máscaras robustas nos campos principais
    // CEP com integração ViaCEP
    const cepEl = document.getElementById('id_cep');
    if (cepEl && !cepEl.dataset.maskApplied) {
      createCEPMask(cepEl);
      cepEl.dataset.maskApplied = 'true';
      
      // Integração ViaCEP ao perder foco
      cepEl.addEventListener('blur', () => {
        const raw = cleanDigits(cepEl.value);
        if (raw.length === 8) {
          fetch('https://viacep.com.br/ws/' + raw + '/json/')
            .then(r => r.json())
            .then(d => {
              if (!d.erro) {
                const map = {rua: 'logradouro', bairro_ref: 'bairro', cidade_ref: 'localidade', estado: 'uf'};
                Object.keys(map).forEach(k => {
                  const el = document.getElementById('id_' + k);
                  if (el && !el.value) el.value = d[map[k]] || '';
                });
              }
            })
            .catch(() => {});
        }
      });
    }

    const horaEl = document.getElementById('id_hora_nascimento');
    if (horaEl && !horaEl.dataset.maskApplied) {
      createHoraMask(horaEl);
      horaEl.dataset.maskApplied = 'true';
    }

    // Celulares
    ['celular', 'celular_primeiro_contato', 'celular_segundo_contato'].forEach(id => {
      const el = document.getElementById('id_' + id);
      if (el && !el.dataset.maskApplied) {
        createCelularMask(el);
        el.dataset.maskApplied = 'true';
      }
    });

    // Telefone
    const telefoneEl = document.getElementById('id_telefone');
    if (telefoneEl && !telefoneEl.dataset.maskApplied) {
      createTelefoneMask(telefoneEl);
      telefoneEl.dataset.maskApplied = 'true';
    }

    // Máscara Ordem de Serviço (____/____)
    function applyMaskToAllOrdemServico() {
      // EXCLUIR template __prefix__ do querySelector
      const historicoInputs = document.querySelectorAll('input[id^="id_historico-"][id$="-ordem_servico"]:not([id*="__prefix__"])');
      console.log('🔍 Aplicando máscara Ordem de Serviço. Campos encontrados (exceto templates):', historicoInputs.length);
      historicoInputs.forEach(input => {
        if (input && !input.dataset.maskApplied) {
          console.log('✅ Aplicando máscara em:', input.id);
          createOrdemServicoMask(input);
          input.dataset.maskApplied = 'true';
        } else if (input) {
          console.log('⚠️ Máscara já aplicada em:', input.id);
        }
      });
      
      // Também aplicar em campos individuais (fora do formset)
      const ordemIds = ['id_ordem_servico', 'ordem_servico'];
      ordemIds.forEach(id => {
        const el = document.getElementById(id);
        if (el && !el.dataset.maskApplied) {
          console.log('✅ Aplicando máscara em campo individual:', id);
          createOrdemServicoMask(el);
          el.dataset.maskApplied = 'true';
        }
      });
    }
    
    // Executar imediatamente
    applyMaskToAllOrdemServico();

    // MutationObserver para campos adicionados dinamicamente (substitui o setInterval)
    const historicoFormList = document.getElementById('historico-form-list');
    if (historicoFormList && window.MutationObserver) {
      console.log('🔎 MutationObserver ativo em historico-form-list');
      const observer = new MutationObserver((mutationsList) => {
        console.log('🔄 MutationObserver detectou', mutationsList.length, 'mutações');
        for (const mutation of mutationsList) {
          if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
            console.log('  📦 childList com', mutation.addedNodes.length, 'nós adicionados');
            mutation.addedNodes.forEach(node => {
              if (node.nodeType === 1) {
                console.log('  🆕 Nó element:', node.tagName, node.id || node.className);
                // Excluir __prefix__ do querySelector
                const input = node.querySelector('input[id^="id_historico-"][id$="-ordem_servico"]:not([id*="__prefix__"])');
                if (input && !input.dataset.maskApplied) {
                  console.log('  ✅ Aplicando máscara via MutationObserver em:', input.id);
                  createOrdemServicoMask(input);
                  input.dataset.maskApplied = 'true';
                } else if (input) {
                  console.log('  ⚠️ Máscara já aplicada em:', input.id);
                }
              }
            });
          }
        }
      });
      observer.observe(historicoFormList, { childList: true, subtree: true });
    } else {
      console.warn('⚠️ historico-form-list não encontrado ou MutationObserver não disponível');
    }

    // Fallback genérico: qualquer campo com data-mask-phone recebe a máscara mesmo se o id mudar
    document.querySelectorAll('[data-mask-phone]').forEach(el=>{
      if (!el.dataset.maskApplied) {
        // Se for celular (11 dígitos), usar createCelularMask, senão createTelefoneMask
        const digits = el.value.replace(/\D/g,'');
        if (digits.length > 10 || el.id.includes('celular')) {
          createCelularMask(el);
        } else {
          createTelefoneMask(el);
        }
        el.dataset.maskApplied = 'true';
      }
    });

    // Carregamento dinâmico de cidades baseado no estado (se houver endpoint disponível)
    const estadoField=document.getElementById('id_estado');
    let cidadeField=document.getElementById('id_cidade');
    if(estadoField && cidadeField){
      // Anotar data-id nas <option> do estado se só tivermos o mapping serializado
      const rawMap=estadoField.getAttribute('data-mapping-json');
      let estadoMap=null;
      if(rawMap){
        try{ const parsed=JSON.parse(rawMap.replace(/'/g,'"')); if(parsed && typeof parsed==='object') estadoMap=parsed; }catch(e){ estadoMap=null; }
      }
      if(estadoMap){
        for(const opt of estadoField.options){
          const val=opt.value; if(val && estadoMap[val] && !opt.getAttribute('data-id')){ opt.setAttribute('data-id', estadoMap[val]); }
        }
      }
      const turnCityIntoSelect=(lista)=>{
        if(cidadeField.tagName!=='SELECT'){
          const select=document.createElement('select');
          select.name=cidadeField.name; select.id=cidadeField.id; select.className='form-select';
          cidadeField.replaceWith(select); cidadeField=select;
        }
        cidadeField.innerHTML='<option value="">Selecione</option>'+lista.map(c=>`<option value="${c.nome}" data-id="${c.id}">${c.nome}</option>`).join('');
      };
      estadoField.addEventListener('change',()=>{
        const opt=estadoField.selectedOptions&&estadoField.selectedOptions[0];
        let estadoId=opt?opt.getAttribute('data-id'):null;
        if(!estadoId && estadoMap){
          const uf=estadoField.value; if(uf && estadoMap[uf]) estadoId=estadoMap[uf];
        }
        if(!estadoId) return;
        // Cache primeiro
        if(cacheCidadesPorEstado[estadoId]){
          turnCityIntoSelect(cacheCidadesPorEstado[estadoId]);
          return;
        }
        fetch(`/alunos/api/cidades/estado/${estadoId}/`)
          .then(r=>r.ok?r.json():[])
          .then(lista=>{if(Array.isArray(lista)&&lista.length){cacheCidadesPorEstado[estadoId]=lista;turnCityIntoSelect(lista);} })
          .catch(()=>{});
      });
      // Encadeamento cidade -> bairros (se campos presentes)
      let bairroField=document.getElementById('id_bairro');
      const bindBairros=(cidadeId)=>{
        if(!bairroField) return;
        // Endpoint pode não existir em alguns ambientes; fallback silencioso
        fetch(`/alunos/api/bairros/cidade/${cidadeId}/`)
          .then(r=>r.ok?r.json():[])
          .then(lista=>{
            if(!Array.isArray(lista)) return;
            if(bairroField.tagName!=='SELECT'){
              const select=document.createElement('select');
              select.name=bairroField.name; select.id=bairroField.id; select.className='form-select';
              bairroField.replaceWith(select); bairroField=select;
            }
            bairroField.innerHTML='<option value="">Selecione</option>'+lista.map(b=>`<option value="${b.nome}" data-id="${b.id}">${b.nome}</option>`).join('');
          })
          .catch(()=>{});
      };
      if(cidadeField){
        cidadeField.addEventListener('change',()=>{
          const CidadeSelect = document.getElementById('id_cidade');
          const selectedOption = CidadeSelect && CidadeSelect.options[CidadeSelect.selectedIndex];
          const cidadeId = selectedOption ? selectedOption.getAttribute('data-id') : null;
          if(cidadeId){ bindBairros(cidadeId); }
        });
      }
    }
  }
  document.addEventListener('DOMContentLoaded', attach);
  document.addEventListener('DOMContentLoaded', applyDisplayMasks);
  window.addEventListener('load', applyPhoneMasks);
})();
