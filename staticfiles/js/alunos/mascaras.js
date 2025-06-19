/**
 * Funções para aplicar máscaras e validações nos formulários de alunos
 */

$(document).ready(function() {
    // Aplicar máscaras
    $('#id_cpf').mask('000.000.000-00');
    $('#id_cep').mask('00000-000');
    $('#id_celular_primeiro_contato').mask('(00) 00000-0000');
    $('#id_celular_segundo_contato').mask('(00) 00000-0000');
    
    // Remover máscaras antes do envio do formulário
    $('form').on('submit', function() {
        console.log("Formulário sendo enviado - removendo máscaras");
        
        // Remover máscaras dos campos
        var cpf = $('#id_cpf').val().replace(/\D/g, '');
        var cep = $('#id_cep').val().replace(/\D/g, '');
        var celular1 = $('#id_celular_primeiro_contato').val().replace(/\D/g, '');
        var celular2 = $('#id_celular_segundo_contato').val().replace(/\D/g, '');
        
        // Atualizar os campos com valores sem máscara
        $('#id_cpf').val(cpf);
        $('#id_cep').val(cep);
        $('#id_celular_primeiro_contato').val(celular1);
        $('#id_celular_segundo_contato').val(celular2);
        
        // Não usar preventDefault() para permitir o envio normal do formulário
        return true;
    });
});