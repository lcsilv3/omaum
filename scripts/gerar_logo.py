#!/usr/bin/env python3
"""
Script para gerar logo do sistema Om-Aum
Cria um PNG simples com o símbolo Om (ॐ) em dourado sobre fundo transparente
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Configurações
WIDTH = 200
HEIGHT = 200
BACKGROUND_COLOR = (0, 0, 0, 0)  # Transparente
TEXT_COLOR = (255, 215, 0, 255)  # Dourado (gold)
SYMBOL = "ॐ"  # Símbolo Om em Devanagari

# Criar imagem com fundo transparente
img = Image.new('RGBA', (WIDTH, HEIGHT), BACKGROUND_COLOR)
draw = ImageDraw.Draw(img)

# Tentar usar uma fonte que suporte Devanagari
font_size = 120
try:
    # Tentar fontes comuns que suportam Devanagari
    font_paths = [
        "C:/Windows/Fonts/mangal.ttf",  # Windows
        "C:/Windows/Fonts/NotoSansDevanagari-Regular.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf",  # Linux
    ]
    
    font = None
    for font_path in font_paths:
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size)
            break
    
    if font is None:
        print("⚠️  Fonte Devanagari não encontrada, usando fonte padrão")
        font = ImageFont.load_default()
        # Usar texto alternativo se não houver suporte
        SYMBOL = "OM"
        font_size = 60
        font = ImageFont.truetype("arial.ttf", font_size) if os.path.exists("C:/Windows/Fonts/arial.ttf") else font
        
except Exception as e:
    print(f"Erro ao carregar fonte: {e}")
    font = ImageFont.load_default()
    SYMBOL = "OM"

# Calcular posição centralizada do texto
bbox = draw.textbbox((0, 0), SYMBOL, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
position = ((WIDTH - text_width) // 2, (HEIGHT - text_height) // 2)

# Desenhar o símbolo
draw.text(position, SYMBOL, font=font, fill=TEXT_COLOR)

# Salvar
output_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'img', 'logo.png')
img.save(output_path)
print(f"✅ Logo criado com sucesso: {output_path}")
print(f"   Tamanho: {WIDTH}x{HEIGHT}px")
print(f"   Símbolo: {SYMBOL}")
