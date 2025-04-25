// Redirecionamento para o módulo correto
console.warn('O arquivo dias-semana.js foi movido para /static/js/modules/. Por favor, atualize suas referências.');
import('/static/js/modules/dias-semana.js')
  .then(module => {
    window.DiasSemana = module.default || module;
  })
  .catch(error => {
    console.error('Erro ao carregar o módulo dias-semana.js:', error);
  });