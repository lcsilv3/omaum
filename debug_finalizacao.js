/**
 * debug_finalizacao.js
 * 
 * INSTRUÇÕES DE USO:
 * 1. Abra a página de "Registrar Presença / Dias das Atividades".
 * 2. Realize o processo de seleção de dias e marcação de presenças.
 * 3. ANTES de clicar em "Finalizar Registro Completo", abra o console do navegador (F12).
 * 4. Copie e cole TODO o conteúdo deste arquivo no console e pressione Enter.
 * 5. Uma análise detalhada do estado atual dos dados será exibida.
 * 6. Se houver problemas, a análise indicará as possíveis causas e soluções.
 * 7. Envie o resultado do diagnóstico para o desenvolvedor para análise.
 */

(function() {
    if (typeof window.PresencaManager === 'undefined') {
        console.error("❌ PresencaManager não foi encontrado. O script principal de presenças não foi carregado corretamente.");
        return;
    }

    console.log("✅ PresencaManager encontrado. Iniciando diagnóstico...");

    const { presencasRegistradas, diasSelecionados, convocadosIndividuais, alunosData } = window.PresencaManager;

    console.log("======================================================");
    console.log("🕵️ DIAGNÓSTICO DE FINALIZAÇÃO DE REGISTRO DE PRESENÇA 🕵️");
    console.log("======================================================");

    // --- 1. Análise dos Alunos ---
    console.log("\n--- 1. ANÁLISE DE ALUNOS ---");
    if (alunosData && alunosData.length > 0) {
        console.log(`✅ Encontrados ${alunosData.length} alunos para esta turma.`);
    } else {
        console.error("❌ NENHUM ALUNO CARREGADO. Isso é um erro crítico. A página não pode funcionar sem alunos.");
    }

    // --- 2. Análise dos Dias Selecionados ---
    console.log("\n--- 2. ANÁLISE DOS DIAS SELECIONADOS (CALENDÁRIO) ---");
    const atividadesComDias = Object.keys(diasSelecionados);
    if (atividadesComDias.length > 0) {
        console.log(`✅ Dias selecionados em ${atividadesComDias.length} atividade(s).`);
        atividadesComDias.forEach(id => {
            console.log(`   - Atividade ID ${id}: Dias [${diasSelecionados[id].join(', ')}]`);
        });
    } else {
        console.warn("⚠️ NENHUM DIA FOI SELECIONADO NOS CALENDÁRIOS. Você precisa selecionar os dias de cada atividade.");
    }

    // --- 3. Análise das Presenças Registradas ---
    console.log("\n--- 3. ANÁLISE DAS PRESENÇAS REGISTRADAS (MODAL) ---");
    const atividadesComPresenca = Object.keys(presencasRegistradas);
    if (atividadesComPresenca.length > 0) {
        console.log(`✅ Presenças registradas para ${atividadesComPresenca.length} atividade(s).`);
        atividadesComPresenca.forEach(id => {
            const diasComPresenca = Object.keys(presencasRegistradas[id]);
            console.log(`   - Atividade ID ${id}: Presenças nos dias [${diasComPresenca.join(', ')}]`);
        });
    } else {
        console.warn("⚠️ NENHUMA PRESENÇA FOI REGISTRADA. Depois de selecionar os dias no calendário, você precisa clicar em cada dia azul para abrir o modal e salvar as presenças.");
    }

    // --- 4. Verificação Cruzada: Dias Selecionados vs. Presenças Registradas ---
    console.log("\n--- 4. VERIFICAÇÃO CRUZADA (DIAS SELECIONADOS vs. PRESENÇAS) ---");
    let diasPendentes = 0;
    let diasOk = 0;
    let diasSemSelecao = 0;

    const todasAtividades = new Set([...atividadesComDias, ...atividadesComPresenca]);

    todasAtividades.forEach(id => {
        const diasSel = diasSelecionados[id] || [];
        const diasPres = Object.keys(presencasRegistradas[id] || {});

        diasSel.forEach(dia => {
            if (diasPres.includes(String(dia))) {
                console.log(`   [OK] Atividade ${id}, Dia ${dia}: Selecionado e com presença registrada.`);
                diasOk++;
            } else {
                console.error(`   [PENDENTE] Atividade ${id}, Dia ${dia}: Selecionado, mas SEM presença registrada. CLIQUE NELE PARA ABRIR O MODAL.`);
                diasPendentes++;
            }
        });

        diasPres.forEach(dia => {
            if (!diasSel.includes(Number(dia))) {
                console.warn(`   [AVISO] Atividade ${id}, Dia ${dia}: Tem presença registrada, mas não está na lista de dias selecionados. Isso pode ser um erro interno.`);
                diasSemSelecao++;
            }
        });
    });

    // --- 5. Análise das Convocações Individuais ---
    console.log("\n--- 5. ANÁLISE DE CONVOCAÇÕES ---");
    const alunosComConvocacaoManual = Object.keys(convocadosIndividuais);
    if (alunosComConvocacaoManual.length > 0) {
        console.log(`✅ ${alunosComConvocacaoManual.length} aluno(s) tiveram o status de 'Convocado' alterado manualmente.`);
        alunosComConvocacaoManual.forEach(cpf => {
            console.log(`   - Aluno CPF ${cpf}: Convocado = ${convocadosIndividuais[cpf]}`);
        });
    } else {
        console.log("ℹ️ Nenhuma alteração manual no status de 'Convocado'. Todos seguirão o padrão da atividade.");
    }

    // --- 6. Resumo e Diagnóstico Final ---
    console.log("\n======================================================");
    console.log("🏁 DIAGNÓSTICO FINAL 🏁");
    console.log("======================================================");

    if (diasPendentes > 0) {
        console.error(`❌ PROBLEMA PRINCIPAL: Existem ${diasPendentes} dia(s) que foram selecionados no calendário, mas para os quais as presenças não foram salvas no modal.`);
        console.error("   COMO RESOLVER: Para cada dia marcado como [PENDENTE] acima, clique no dia (azul) no calendário, marque as presenças no modal e clique em 'Salvar Presenças'.");
    } else if (atividadesComDias.length === 0) {
        console.error("❌ PROBLEMA PRINCIPAL: Nenhum dia foi selecionado nos calendários.");
        console.error("   COMO RESOLVER: Clique nos campos de cada atividade para abrir os calendários e selecionar os dias em que ocorreram.");
    } else if (diasOk > 0 && diasPendentes === 0) {
        console.log("✅ TUDO CERTO! Todos os dias selecionados têm presenças registradas. Você pode clicar em 'Finalizar Registro Completo'.");
    } else {
        console.warn("⚠️ SITUAÇÃO INESPERADA. Não há dias pendentes, mas também não há dias com presenças registradas. Verifique se você selecionou os dias e salvou as presenças.");
    }

    if (diasSemSelecao > 0) {
        console.warn(`   AVISO ADICIONAL: ${diasSemSelecao} dia(s) com presença registrada não constam como selecionados. Isso pode indicar um bug. Informe o desenvolvedor.`);
    }

    console.log("\nFim do diagnóstico.");
})();
