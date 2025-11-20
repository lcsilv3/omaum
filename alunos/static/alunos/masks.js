// Utilidades de máscaras e auto-preenchimento para o app Alunos
// Fase 1-2: CEP -> (rua,bairro,cidade,estado) e Estado -> Cidades (com cache simples)
// Expõe utilitário global para remover máscaras antes do submit
window.addSubmitMaskRemover = function(formId) {
  const form = document.getElementById(formId);
  if (!form) {
    return;
  }
  form.addEventListener('submit', () => {
    const limpar = campoId => {
      const campo = document.getElementById(campoId);
      if (campo && typeof campo.value === 'string') {
        campo.value = campo.value.replace(/\D/g, '');
      }
    };
    limpar('id_cpf');
    limpar('id_cep');
    limpar('id_celular_primeiro_contato');
    limpar('id_celular_segundo_contato');
  });
};

(function(){
  const cacheCidadesPorEstado = {}; // {estadoId: [{id,nome}, ...]}
  function maskCPF(v){return v.replace(/\D/g,'').replace(/(\d{3})(\d)/,'$1.$2').replace(/(\d{3})(\d)/,'$1.$2').replace(/(\d{3})(\d{1,2})$/,'$1-$2').substring(0,14);} 
  function maskCEP(v){
    // Novo formato: 00.000-000 (10 caracteres visuais) armazenando só dígitos
    const d = v.replace(/\D/g,'').substring(0,8); // max 8 dígitos
    if(d.length <= 2) return d; // 0-2
    if(d.length <= 5) return d.replace(/(\d{2})(\d+)/,'$1.$2'); // 3-5
    return d.replace(/(\d{2})(\d{3})(\d{0,3})/,'$1.$2-$3'); // 6-8
  } 
  function maskPhone(v){const n=v.replace(/\D/g,'').substring(0,11);if(n.length<=10){return n.replace(/(\d{2})(\d{4})(\d{0,4})/,'($1) $2-$3').replace(/-$/,'');}return n.replace(/(\d{2})(\d{5})(\d{0,4})/,'($1) $2-$3').replace(/-$/,'');}
  function cleanDigits(v){return v.replace(/\D/g,'');}
  function maskOrdemServico(v) {
    // Permite apenas números e barra, formato: 1234/2025
    let val = v.replace(/[^\d]/g, '');
    if (val.length > 8) val = val.substring(0, 8);
    if (val.length > 4) {
      return val.substring(0, 4) + '/' + val.substring(4, 8);
    }
    return val;
  }

  function attach(){
    const cpf=document.getElementById('id_cpf'); if(cpf){
      cpf.value = maskCPF(cpf.value);
      cpf.addEventListener('input',e=>e.target.value=maskCPF(e.target.value));
    }

    // Máscara Ordem de Serviço (____/9999)
    function applyOrdemServicoMaskTo(el) {
      if (!el) return;
      el.addEventListener('input', e => {
        e.target.value = maskOrdemServico(e.target.value);
      });
    }
    // IDs e names possíveis
    const ordemIds = [
      'id_ordem_servico',
      'ordem_servico',
    ];
    ordemIds.forEach(id => {
      const el = document.getElementById(id);
      if (el) applyOrdemServicoMaskTo(el);
    });
    // Formsets dinâmicos (historico-__prefix__-ordem_servico)
    function applyMaskToAllOrdemServico() {
      const historicoInputs = document.querySelectorAll('input[id^="id_historico-"][id$="-ordem_servico"]');
      historicoInputs.forEach(applyOrdemServicoMaskTo);
    }
    applyMaskToAllOrdemServico();

    // MutationObserver para campos adicionados dinamicamente
    const historicoFormList = document.getElementById('historico-form-list');
    if (historicoFormList && window.MutationObserver) {
      const observer = new MutationObserver((mutationsList) => {
        for (const mutation of mutationsList) {
          if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
            mutation.addedNodes.forEach(node => {
              if (node.nodeType === 1) {
                const input = node.querySelector('input[id^="id_historico-"][id$="-ordem_servico"]');
                if (input) applyOrdemServicoMaskTo(input);
              }
            });
          }
        }
      });
      observer.observe(historicoFormList, { childList: true, subtree: true });
    }
    const cep=document.getElementById('id_cep'); if(cep){
      cep.value = maskCEP(cep.value);
      cep.addEventListener('input',e=>e.target.value=maskCEP(e.target.value));
      cep.addEventListener('blur',()=>{
        const raw=cleanDigits(cep.value);
        if(raw.length===8){
          fetch('https://viacep.com.br/ws/'+raw+'/json/')
            .then(r=>r.json())
            .then(d=>{
              if(!d.erro){
                const map={rua:'logradouro',bairro:'bairro',cidade:'localidade',estado:'uf'};
                ['rua','bairro','cidade','estado'].forEach(k=>{
                  const el=document.getElementById('id_'+k);
                  if(!el) return;
                  const novoValor=d[map[k]]||'';
                  if(novoValor){
                    if(el.value!==novoValor){
                      el.value=novoValor;
                      el.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                  } else if(!el.value) {
                    el.value='';
                  }
                });
              }
            })
            .catch(()=>{});
        }
      });
    }
    ['celular_primeiro_contato','celular_segundo_contato'].forEach(id=>{const el=document.getElementById('id_'+id); if(el){
      el.value = maskPhone(el.value);
      el.addEventListener('input',e=>e.target.value=maskPhone(e.target.value));
    }});

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
})();
