document.addEventListener('DOMContentLoaded', function() {
    // Função para mostrar/ocultar campos de pagamento
    function toggleCamposPagamento() {
        const statusSelect = document.getElementById('id_status');
        const camposPagamento = document.getElementById('campos-pagamento');
        
        if (statusSelect && camposPagamento) {
            if (statusSelect.value === 'PAGO') {
                camposPagamento.style.display = 'flex';
                
                // Preencher data de pagamento se estiver vazia
                const dataPagamentoField = document.getElementById('id_data_pagamento');
                if (dataPagamentoField && !dataPagamentoField.value) {
                    const hoje = new Date();
                    const ano = hoje.getFullYear();
                    const mes = String(hoje.getMonth() + 1).padStart(2, '0');
                    const dia = String(hoje.getDate()).padStart(2, '0');
                    dataPagamentoField.value = `${ano}-${mes}-${dia}`;
                }
                
                // Preencher valor pago se estiver vazio
                const valorPagoField = document.getElementById('id_valor_pago');
                const valorField = document.getElementById('id_valor');
                if (valorPagoField && valorField && !valorPagoField.value) {
                    valorPagoField.value = valorField.value;
                }
            } else {
                camposPagamento.style.display = 'none';
            }
        }
    }
    
    // Executar na inicialização
    toggleCamposPagamento();
    
    // Adicionar evento de mudança ao select de status
    const statusSelect = document.getElementById('id_status');
    if (statusSelect) {
        statusSelect.addEventListener('change', toggleCamposPagamento);
    }
    
    // Validação do formulário
    const form = document.getElementById('pagamento-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            let formValido = true;
            
            // Validar aluno
            const alunoSelect = document.getElementById('id_aluno');
            if (alunoSelect && !alunoSelect.value) {
                e.preventDefault();
                alert('Selecione um aluno.');
                alunoSelect.focus();
                formValido = false;
            }
            
            // Validar valor
            const valorField = document.getElementById('id_valor');
            if (valorField && (!valorField.value || parseFloat(valorField.value) <= 0)) {
                e.preventDefault();
                alert('O valor deve ser maior que zero.');
                valorField.focus();
                formValido = false;
            }
            
            // Validar data de vencimento
            const dataVencimentoField = document.getElementById('id_data_vencimento');
            if (dataVencimentoField && !dataVencimentoField.value) {
                e.preventDefault();
                alert('A data de vencimento é obrigatória.');
                dataVencimentoField.focus();
                formValido = false;
            }
            
            // Validar campos adicionais quando o status for PAGO
            const statusSelect = document.getElementById('id_status');
            if (statusSelect && statusSelect.value === 'PAGO') {
                const dataPagamentoField = document.getElementById('id_data_pagamento');
                if (dataPagamentoField && !dataPagamentoField.value) {
                    e.preventDefault();
                    alert('A data de pagamento é obrigatória quando o status é Pago.');
                    dataPagamentoField.focus();
                    formValido = false;
                }
                
                const valorPagoField = document.getElementById('id_valor_pago');
                if (valorPagoField && (!valorPagoField.value || parseFloat(valorPagoField.value) <= 0)) {
                    e.preventDefault();
                    alert('O valor pago deve ser maior que zero quando o status é Pago.');
                    valorPagoField.focus();
                    formValido = false;
                }
            }
            
            return formValido;
        });
    }
});