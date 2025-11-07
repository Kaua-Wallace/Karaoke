# Karaoke no terminal

# 🎤 Karaokê de Terminal

Um script em Python que transforma seu terminal em uma máquina de karaokê. Ele toca um arquivo `.mp3` enquanto exibe as letras de um arquivo `.lrc` em sincronia, destacando o verso atual.

O script usa `pygame` para tocar o áudio e `curses` para desenhar a interface no terminal.

## ✨ Funcionalidades

* Sincronização de letras (`.lrc`) com áudio (`.mp3`).
* Destaque do verso atual em tempo real.
* Interface limpa, rodando 100% no terminal.
* Cores de destaque e atributos (como negrito) personalizáveis.
* Compatível com Windows, macOS e Linux.

## 📁 Estrutura do Projeto

A estrutura de arquivos para o projeto funcionar é simples. Todos os arquivos devem estar na mesma pasta:
karaoke_de_terminal/ │ ├── 📄 script.py (O código principal do player em Python) ├── 🎵 musica.mp3 (O seu arquivo de áudio) └── 📄 musica.lrc (O seu arquivo de letras sincronizadas)]

## 🛠️ Instalação

Antes de rodar, você precisa instalar as bibliotecas necessárias.

1.  **Clone** este repositório ou baixe os arquivos para uma pasta.
2.  **Instale as dependências** via `pip`.

    ```bash
    # Instala a biblioteca de áudio
    pip install pygame
    ```

    **Atenção se estiver no Windows:** A biblioteca `curses` não vem com o Python no Windows. Você deve instalar o pacote `windows-curses` para que o script funcione:

    ```bash
    # Obrigatório apenas para usuários do Windows
    pip install windows-curses
    ```

## 🚀 Como Usar

1.  **Adicione seus arquivos**: Coloque seu arquivo de áudio (ex: `Alianca.mp3`) e seu arquivo de letra (ex: `Alianca.lrc`) na mesma pasta do `script.py`.

2.  **Edite o Script**: Abra o `script.py` e altere as duas últimas linhas para que apontem para os seus arquivos:

    ```python
    if __name__ == "__main__":
        MP3_FILE = "Alianca.mp3"  # <-- Mude aqui
        LRC_FILE = "Alianca.lrc"  # <-- E aqui
    ```

3.  **Execute**: Abra seu terminal, navegue até a pasta do projeto e execute o script:

    ```bash
    python script.py
    ```

4.  **Controles**: Pressione a tecla **`q`** a qualquer momento durante a música para fechar o programa.

## 🎨 Personalização de Cores

Você pode alterar facilmente a cor do verso destacado.

1.  Abra o `script.py` e procure pela função `main_terminal_ui`.
2.  Encontre a linha que começa com `curses.init_pair(1, ...)`
3.  O formato é `curses.init_pair(ID, COR_DA_LETRA, COR_DO_FUNDO)`.

**Exemplos:**

```python
# Padrão (Letra Preta, Fundo Branco)
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

# Estilo Karaokê Clássico (Letra Amarela, Fundo Padrão)
# (O -1 significa "usar o fundo padrão do terminal")
curses.init_pair(1, curses.COLOR_YELLOW, -1)

# Estilo "Hacker" (Letra Verde, Fundo Preto)
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

# Estilo (Letra Amarela, Fundo Azul)
curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLUE)
