import os  
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"  # <-- retira "Hello from the pygame community. https://www.pygame.org/contribute.html"
import curses
import pygame
import time
import re

def parse_lrc(lrc_path):
    """
    Analisa um arquivo .lrc e extrai os metadados e as letras cronometradas.
    Retorna um dicionário de metadados e uma lista de tuplas (segundos, letra).
    """
    metadata = {}
    lyrics = []
    
    # Regex para capturar tags de tempo [mm:ss.xx]
    time_regex = re.compile(r'\[(\d{2}):(\d{2})\.(\d{2})\]')
    # Regex para capturar tags de metadados [tag:valor]
    meta_regex = re.compile(r'\[(ti|ar|al):(.*?)\]')

    try:
        with open(lrc_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Tenta extrair metadados (Título, Artista, Álbum)
                meta_match = meta_regex.match(line)
                if meta_match:
                    tag, value = meta_match.groups()
                    metadata[tag] = value
                    continue
                
                # Tenta extrair tempo e letra
                time_match = time_regex.search(line)
                if time_match:
                    minutes, seconds, hundredths = map(int, time_match.groups())
                    total_seconds = (minutes * 60) + seconds + (hundredths / 100.0)
                    
                    # Pega a letra após o último timestamp
                    lyric_text = line[time_match.end():].strip()
                    
                    # Ignora linhas que são apenas timestamps sem letra
                    if lyric_text:
                        lyrics.append((total_seconds, lyric_text))

    except FileNotFoundError:
        return None, None
    
    # Garante que as letras estejam ordenadas pelo tempo
    lyrics.sort()
    return metadata, lyrics

def main_terminal_ui(stdscr, metadata, lyrics, mp3_path):
    """
    Função principal da UI do terminal, gerenciada pelo curses.wrapper.
    """
    # Inicializa o mixer do pygame
    pygame.mixer.init()
    try:
        pygame.mixer.music.load(mp3_path)
    except pygame.error:
        # Se o arquivo não for encontrado ou for formato inválido
        return "Erro: Não foi possível carregar o arquivo de áudio. Verifique o caminho e o formato."

    # Configurações do Curses
    curses.curs_set(0)  # Oculta o cursor
    stdscr.nodelay(True)  # Torna getch() não bloqueante
    
    # Configura um par de cores para o destaque (texto branco sobre fundo preto - reverso)
    curses.start_color()
    curses.use_default_colors() # Usa cores padrão do terminal
    # Cria o par de cores 1: Texto preto em fundo branco (para o destaque)
    # Letra AMARELA, fundo do terminal (padrão)
    curses.init_pair(1, curses.COLOR_YELLOW, -1)    
    # Toca a música
    pygame.mixer.music.play()
    
    current_line_index = -1
    
    # Loop principal: roda enquanto a música estiver tocando
    while pygame.mixer.music.get_busy():
        try:
            # 1. Obter o tempo atual da música
            # get_pos() retorna milissegundos, então convertemos para segundos
            current_time_sec = pygame.mixer.music.get_pos() / 1000.0
            
            # 2. Encontrar o índice da linha atual
            # Procura pela *última* letra cujo tempo já passou
            new_current_line_index = -1
            for i, (timestamp, line) in enumerate(lyrics):
                if current_time_sec >= timestamp:
                    new_current_line_index = i
                else:
                    # Como a lista está ordenada, podemos parar assim que
                    # encontrarmos um timestamp futuro.
                    break
            
            current_line_index = new_current_line_index

            # 3. Desenhar a UI
            stdscr.clear() # Limpa a tela
            
            # Pega o tamanho da janela
            max_y, max_x = stdscr.getmaxyx()

            # Desenha o Título e o Artista
            title = metadata.get('ti', 'Título Desconhecido')
            artist = metadata.get('ar', 'Artista Desconhecido')

            # Garante que o texto não ultrapasse a largura da tela
            
            title_line = title[:max_x - 2]   # -2 para margem
            artist_line = artist[:max_x - 2] # -2 para margem

            # Adiciona o artista no canto esquerdo (linha 0)
            stdscr.addstr(0, 1, artist_line, curses.A_BOLD) # Em negrito

            # Adiciona o título no canto esquerdo (linha 1)
            stdscr.addstr(1, 1, title_line, curses.A_BOLD) #em negrito

            # 4. Desenhar as Letras
            # Define o início da rolagem (para centralizar la linha atual)
            start_line = 0
            if current_line_index != -1:
                # Tenta centralizar a linha ativa na vertical
                start_line = max(0, current_line_index - (max_y // 3))

            # Itera e desenha apenas as linhas visíveis
            for i in range(start_line, len(lyrics)):
                # Calcula a posição Y na tela
                # +3 para pular o artista e o título 
                screen_y = (i - start_line) + 3

                # Para de desenhar se passar da borda da tela
                if screen_y >= max_y - 1: # -1 para deixar uma margem
                    break

                timestamp, line_text = lyrics[i]
                
                # Garante que o texto não ultrapasse a largura da tela
                line_text = line_text[:max_x - 2] # -2 para margem

                # Se for a linha atual, usa o destaque
                if i == current_line_index:
                    stdscr.addstr(screen_y, 1, line_text, curses.color_pair(1) | curses.A_BOLD)
                else:
                    stdscr.addstr(screen_y, 1, line_text)
            
            stdscr.refresh() # Atualiza a tela

            # 5. Lidar com entrada do usuário (para sair)
            key = stdscr.getch()
            if key == ord('q'):
                pygame.mixer.music.stop()
                break
                
            # 6. Pausa o loop para não usar 100% da CPU
            time.sleep(0.05) # Atualiza ~20x por segundo

        except curses.error:
            # Isso geralmente acontece se o usuário redimensionar a janela
            stdscr.clear()
            stdscr.addstr(0, 0, "Redimensionando... Por favor, aguarde.")
            stdscr.refresh()
            time.sleep(0.5)

    # A música terminou, espera por uma tecla antes de sair
    stdscr.nodelay(False) # Torna getch() bloqueante novamente
    stdscr.clear()
    stdscr.addstr(max_y // 2, (max_x - 8) // 2, "Fim. Pressione qualquer tecla para sair.")
    stdscr.refresh()
    stdscr.getch()
    
    return "Execução terminada com sucesso."

# --- Ponto de Entrada do Script ---
if __name__ == "__main__":
    MP3_FILE = "Assets/Musicas/intencao_marilia.mp3"
    LRC_FILE = "Assets/Musicas/intencao_marilia.lrc"
    
    # 1. Analisa o arquivo LRC
    metadata, lyrics = parse_lrc(LRC_FILE)
    
    if metadata is None or lyrics is None:
        print(f"Erro: Não foi possível encontrar ou ler o arquivo '{LRC_FILE}'.")
        print("Verifique se o nome do arquivo está correto e se ele está no mesmo diretório.")
    elif not lyrics:
         print(f"Erro: O arquivo '{LRC_FILE}' foi encontrado, mas não contém letras cronometradas válidas.")
    else:
        # 2. Inicia o pygame (apenas o módulo de áudio)
        pygame.init()
        pygame.mixer.init()

        # 3. Inicia o Curses
        # curses.wrapper cuida de inicializar e restaurar o terminal com segurança
        status_message = curses.wrapper(main_terminal_ui, metadata, lyrics, MP3_FILE)
        
        # 4. Encerra o pygame
        pygame.mixer.quit()
        pygame.quit()
        
        print(status_message)