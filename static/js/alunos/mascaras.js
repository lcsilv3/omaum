/**
 * Funções para aplicar máscaras e validações nos formulários de alunos
 */

$(document).ready(function() {
    // Máscaras para formulários
    function aplicarMascaras() {
        // CPF: 000.000.000-00
        $('input[name="cpf"]').mask('000.000.000-00', {
            reverse: true,
            onComplete: function(cpf) {
                // Remove a máscara para o valor que será enviado ao servidor
                $(this).data('rawValue', cpf.replace(/\D/g, ''));
            },
            onChange: function(cpf) {
                // Atualiza o valor raw enquanto digita
                $(this).data('rawValue', cpf.replace(/\D/g, ''));
            }
        });
        
        // CEP: 00000-000
        $('input[name="cep"]').mask('00000-000', {
            onComplete: function(cep) {
                $(this).data('rawValue', cep.replace(/\D/g, ''));
                // Opcionalmente, buscar endereço via API de CEP
                buscarEnderecoPorCep(cep.replace(/\D/g, ''));
            },
            onChange: function(cep) {
                $(this).data('rawValue', cep.replace(/\D/g, ''));
            }
        });
        
        // Celular: (00) 00000-0000
        $('input[name="celular_primeiro_contato"], input[name="celular_segundo_contato"]').mask('(00) 00000-0000', {
            onComplete: function(celular) {
                $(this).data('rawValue', celular.replace(/\D/g, ''));
            },
            onChange: function(celular) {
                $(this).data('rawValue', celular.replace(/\D/g, ''));
            }
        });
        
        // Tipo sanguíneo: A, B, AB, O
        $('input[name="tipo_sanguineo"]').on('input', function() {
            let valor = $(this).val().toUpperCase();
            // Permitir apenas A, B, AB ou O
            if (!/^(A|B|AB|O)?$/.test(valor)) {
                valor = valor.replace(/[^ABO]/g, '');
                if (valor.length > 2) valor = valor.substring(0, 2);
            }
            $(this).val(valor);
        });
    }
    
    // Função para buscar endereço por CEP usando a API ViaCEP
    function buscarEnderecoPorCep(cep) {
        if (cep.length !== 8) return;
        
        $.getJSON(`https://viacep.com.br/ws/${cep}/json/`, function(data) {
            if (!data.erro) {
                $('input[name="rua"]').val(data.logradouro);
                $('input[name="bairro"]').val(data.bairro);
                $('input[name="cidade"]').val(data.localidade);
                $('input[name="estado"]').val(data.uf);
                // Focar no campo número após preencher o endereço
                $('input[name="numero_imovel"]').focus();
            }
        });
    }
    
    // Aplicar máscaras nos campos
    aplicarMascaras();
    
    // IMPORTANTE: Interceptar o envio do formulário para remover as máscaras antes de enviar
    $('form').on('submit', function() {
        console.log("Formulário sendo enviado - removendo máscaras");
        
        // Para cada campo com máscara, substituir o valor pelo valor raw
        $('input[data-rawValue]').each(function() {
            var rawValue = $(this).data('rawValue');
            if (rawValue) {
                console.log(`Substituindo valor mascarado ${$(this).val()} por ${rawValue}`);
                $(this).val(rawValue);
            }
        });
        
        // Remover máscaras diretamente
        $('input[name="cpf"]').unmask();
        $('input[name="cep"]').unmask();
        $('input[name="celular_primeiro_contato"]').unmask();
        $('input[name="celular_segundo_contato"]').unmask();
        
        return true;
    });
    
    // Aplicar máscaras para exibição em páginas de detalhes
    function aplicarMascarasExibicao() {
        // CPF
        $('.cpf-mask').each(function(){
            var cpf = $(this).text().trim();
            if(cpf.length === 11) {
                $(this).text(cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, "$1.$2.$3-$4"));
            }
        });
        
        // CEP
        $('.cep-mask').each(function(){
            var cep = $(this).text().trim();
            if(cep.length === 8) {
                $(this).text(cep.replace(/(\d{5})(\d{3})/, "$1-$2"));
            }
        });
        
        // Celular
        $('.celular-mask').each(function(){
            var celular = $(this).text().trim();
            if(celular.length === 11) {
                $(this).text(celular.replace(/(\d{2})(\d{5})(\d{4})/, "($1) $2-$3"));
            } else if(celular.length === 10) {
                $(this).text(celular.replace(/(\d{2})(\d{4})(\d{4})/, "($1) $2-$3"));
            }
        });
    }
    
    // Aplicar máscaras de exibição
    aplicarMascarasExibicao();
});