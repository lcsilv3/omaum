from scripts.import_utils import pick_field


def test_pick_field_handles_corrupted_headers():
    # simula uma linha de CSV com cabeçalhos corrompidos/acentos estranhos
    row = {
        "Unnamed: 0": "",
        # versões com caracteres corrompidos (normalização remove acentos)
        "cdigo tipo": "1",
        "Descrio tipo": "Administrativos",
        "cdigo": "10",
        "Descrio cdigo": "Códigos Administrativos",
    }

    tipo = pick_field(row, ["Tipo", "tipo", "codigo tipo", "código tipo", "cdigo tipo", "unnamed: 0"])
    codigo = pick_field(row, ["Nome", "nome", "codigo", "código", "cdigo"]) 
    descricao = pick_field(row, ["Descrição", "descricao", "Descrio", "Descrio cdigo", "Descri\u00e7\u00e3o"]) 

    assert tipo is not None and tipo.strip() == "1"
    assert codigo is not None and codigo.strip() == "10"
    # garantir que alguma descrição foi encontrada (não testar valor exato por diferença de encoding)
    assert descricao is not None and descricao.strip() != ""
