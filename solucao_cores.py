import matplotlib.pyplot as plt
import math
import colorsys
import os

# paleta base (12 cores do círculo cromático)
COLOR_WHEEL = {
    "vermelho": (1.0, 0.0, 0.0),
    "vermelho-laranja": (1.0, 0.25, 0.0),
    "laranja": (1.0, 0.5, 0.0),
    "amarelo-laranja": (1.0, 0.75, 0.0),
    "amarelo": (1.0, 1.0, 0.0),
    "amarelo-verde": (0.5, 1.0, 0.0),
    "verde": (0.0, 1.0, 0.0),
    "azul-verde": (0.0, 1.0, 0.5),
    "azul": (0.0, 0.0, 1.0),
    "azul-violeta": (0.25, 0.0, 1.0),
    "violeta": (0.5, 0.0, 1.0),
    "vermelho-violeta": (0.75, 0.0, 1.0),
}
COLOR_NAMES = list(COLOR_WHEEL.keys())

def get_harmonies(base_color_name: str) -> dict:
    """gera algumas paletas harmônicas a partir de uma cor"""
    if base_color_name not in COLOR_NAMES:
        return None

    base_index = COLOR_NAMES.index(base_color_name)
    num_colors = len(COLOR_NAMES)

    harmonies = {}

    # complementar (oposta no círculo)
    complementary_index = (base_index + num_colors // 2) % num_colors
    harmonies['complementar'] = [base_color_name, COLOR_NAMES[complementary_index]]

    # análogas (lado a lado)
    analogous_indices = [(base_index - 1 + num_colors) % num_colors, base_index, (base_index + 1) % num_colors]
    harmonies['analoga'] = [COLOR_NAMES[i] for i in analogous_indices]

    # triádica (3 cores igualmente espaçadas)
    triadic_indices = [base_index, (base_index + num_colors // 3) % num_colors, (base_index + 2 * num_colors // 3) % num_colors]
    harmonies['triadica'] = [COLOR_NAMES[i] for i in triadic_indices]

    # dividida complementar (base + vizinhas da oposta)
    split_comp_indices = [base_index, (complementary_index - 1 + num_colors) % num_colors, (complementary_index + 1) % num_colors]
    harmonies['dividida_complementar'] = [COLOR_NAMES[i] for i in split_comp_indices]

    # tétrade (2 pares de complementares)
    tetradic_indices = [base_index, (base_index + 2) % num_colors, complementary_index, (complementary_index + 2) % num_colors]
    harmonies['tetrade'] = [COLOR_NAMES[i] for i in tetradic_indices]

    # monocromática (mesma cor variando luz/saturação)
    base_rgb = COLOR_WHEEL[base_color_name]
    h, l, s = colorsys.rgb_to_hls(*base_rgb)
    harmonies['monocromatica'] = [
        colorsys.hls_to_rgb(h, max(0, l * 0.5), s),
        base_rgb,
        colorsys.hls_to_rgb(h, min(1, l * 1.5), s)
    ]

    return harmonies

def visualize_palette(title: str, colors: list, color_map: dict):
    """gera uma imagem da paleta e salva em uma pasta 'imagens_paletas'"""
    
    output_dir = "imagens_paletas"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    rgb_colors, labels = [], []
    for color in colors:
        if isinstance(color, str):
            rgb_colors.append(color_map.get(color, (0,0,0)))
            labels.append(color)
        else:
            rgb_colors.append(color)
            labels.append(f"({color[0]:.2f}, {color[1]:.2f}, {color[2]:.2f})")

    fig, ax = plt.subplots(1, len(rgb_colors), figsize=(len(rgb_colors) * 2, 2))
    plt.suptitle(title, fontsize=16)
    
    if len(rgb_colors) == 1:
        ax = [ax]
        
    for i, (color_rgb, label) in enumerate(zip(rgb_colors, labels)):
        ax[i].add_patch(plt.Rectangle((0, 0), 1, 1, color=color_rgb))
        ax[i].set_title(label, pad=10)
        ax[i].axis('off')
    
    plt.tight_layout(rect=[0, 0, 1, 0.9])
    
    safe_title = title.replace(' ', '_').replace(':', '').replace('(', '').replace(')', '').lower()
    
    filepath = os.path.join(output_dir, f"{safe_title}.png")
    plt.savefig(filepath)
    plt.close(fig)
    
def ryb_to_rgb(r: float, y: float, b: float) -> tuple:
    """converte de RYB (pintura) pra RGB (digital)"""
    white = min(r, y, b)
    r -= white; y -= white; b -= white
    red = r + y - min(y, b)
    green = y + min(y, b)
    blue = b + min(y, b)
    red += white; green += white; blue += white
    return (max(0, min(1, red)), max(0, min(1, green)), max(0, min(1, blue)))

def rgb_to_hsl(r: float, g: float, b: float) -> tuple:
    """RGB → HSL (hue, saturation, lightness)"""
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h, s, l

def hex_to_rgb_normalized(hex_code: str) -> tuple:
    """#hex → (r,g,b) normalizado (0–1)"""
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def find_closest_color(target_rgb: tuple, color_wheel: dict) -> str:
    """acha a cor mais próxima no círculo (distância euclidiana RGB)"""
    min_distance = float('inf')
    closest_color_name = None
    for name, rgb in color_wheel.items():
        distance = math.sqrt(sum([(c1 - c2) ** 2 for c1, c2 in zip(target_rgb, rgb)]))
        if distance < min_distance:
            min_distance = distance
            closest_color_name = name
    return closest_color_name

# ==================== "execução" ====================

def executar_exercicio1():
    print("--- EXERCÍCIO 1 ---")
    base_color = "azul"
    print(f"Paletas da cor: '{base_color}'")
    palettes = get_harmonies(base_color)
    for name, colors in palettes.items():
        title = f"Paleta {name.replace('_', ' ').capitalize()} (Base: {base_color})"
        visualize_palette(title, colors, COLOR_WHEEL)
    print("ok!")

def executar_exercicio2():
    print("\n--- EXERCÍCIO 2 ---")
    print("RYB → RGB:")
    ryb_colors = {
        "Vermelho (RYB)": (1, 0, 0),
        "Amarelo (RYB)": (0, 1, 0),
        "Azul (RYB)": (0, 0, 1),
        "Verde (RYB)": (0, 1, 1),
        "Laranja (RYB)": (1, 1, 0),
    }
    for name, ryb_val in ryb_colors.items():
        rgb_val = ryb_to_rgb(*ryb_val)
        print(f"  - {name}: {ryb_val} -> RGB: ({rgb_val[0]:.2f}, {rgb_val[1]:.2f}, {rgb_val[2]:.2f})")
        visualize_palette(f"{name} em RGB", [rgb_val], {})

    print("\nRGB → HSL:")
    rgb_magenta = (1.0, 0.0, 1.0)
    hsl_magenta = rgb_to_hsl(*rgb_magenta)
    print(f"  - Magenta: {rgb_magenta} -> HSL: (H:{hsl_magenta[0]:.2f}, S:{hsl_magenta[1]:.2f}, L:{hsl_magenta[2]:.2f})")

def executar_exercicio3():
    print("\n--- EXERCÍCIO 3 ---")
    color_name = "Mocha Mousse"
    hex_code = "#967444"
    print(f"Cor base: {color_name} ({hex_code})")
    target_rgb = hex_to_rgb_normalized(hex_code)
    closest_color = find_closest_color(target_rgb, COLOR_WHEEL)
    print(f"Mais próxima no círculo: '{closest_color}'")
    palettes = get_harmonies(closest_color)
    temp_color_map = COLOR_WHEEL.copy()
    temp_color_map[color_name] = target_rgb
    for name, colors in palettes.items():
        display_colors = [color_name] + colors
        title = f"Paleta {name.replace('_', ' ').capitalize()} (Base: {color_name})"
        visualize_palette(title, display_colors, temp_color_map)
    print("ok!")

if __name__ == "__main__":
    print("\n\n\nIniciando...\n\n")
    executar_exercicio1()
    print("\n\n")
    executar_exercicio2()
    print("\n\n")
    executar_exercicio3()
    print("\n\nTodos finalizados.\n\n\n")