#!/usr/bin/env python
"""
Analisar o HTML salvo
"""


def analyze_saved_html():
    """Analisa o HTML salvo"""
    try:
        with open("html_dump_formset_get.html", "r", encoding="utf-8") as f:
            html = f.read()

        # Contar TOTAL_FORMS
        count = html.count('name="historico-TOTAL_FORMS"')
        print(f"📊 Contagem no HTML salvo: {count}")

        # Encontrar todas as posições
        pos = 0
        positions = []
        while True:
            pos = html.find('name="historico-TOTAL_FORMS"', pos)
            if pos == -1:
                break
            positions.append(pos)
            pos += 1

        print(f"📍 Posições: {positions}")

        # Mostrar contexto de cada posição
        for i, pos in enumerate(positions):
            start = max(0, pos - 150)
            end = min(len(html), pos + 150)
            context = html[start:end]
            print(f"\n--- CONTEXTO {i+1} (pos {pos}) ---")
            print(repr(context))  # usar repr para ver caracteres especiais
            print("--- FIM CONTEXTO ---")

    except FileNotFoundError:
        print("❌ Arquivo não encontrado")


if __name__ == "__main__":
    analyze_saved_html()
