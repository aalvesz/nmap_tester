# nmap_tester

Passo a Passo para Configurar e Executar a Ferramenta em Linux Mint e Windows
O  script port_scanner_gui.py (a ferramenta de varredura de portas com interface gráfica) em Linux e Windows. 

1. Configuração e Execução no Linux 
Pré-requisitos:

Python 3 instalado (geralmente já vem pré-instalado no Linux Mint).
 - Tkinter para a interface gráfica.
 - Acesso ao terminal.

 Passos para configurar e executar:

 Verifique o Python e instale dependências:

 Abra o terminal (Ctrl + Alt + T).
 Verifique a versão do Python com o comando:
   textpython3 --version

 Se não estiver instalado ou for uma versão antiga, instale:
 textsudo apt update
 sudo apt install python3



 Instale o Tkinter (necessário para a GUI):
 textsudo apt install python3-tk



 Salve o script:

 Crie ou edite o arquivo port_scanner_gui.py no diretório desejado (ex.: use nano para editar):
 textnano port_scanner_gui.py

 Cole o código completo do script (incluindo as funções de varredura e a GUI aprimorada).
 Salve com Ctrl + O, Enter, e saia com Ctrl + X.


Dê permissão de execução (opcional, mas recomendado):
 textchmod +x port_scanner_gui.py

Execute o script:

Para execução normal (TCP funciona bem; UDP pode ser menos preciso sem privilégios):
textpython3 port_scanner_gui.py

Para varreduras UDP mais precisas (requer privilégios para capturar respostas ICMP):
textsudo python3 port_scanner_gui.py



Uso na GUI:

A janela "Port Scanner" abrirá.
Preencha os campos:

Host(s): Ex.: 127.0.0.1 ou 127.0.0.1,192.168.1.1 (para múltiplos).
Portas: Ex.: 1-100,443,8080.
Tipo de varredura: Selecione TCP, UDP ou Ambos.
Threads: Ex.: 10 (valor padrão).


Clique em "Iniciar Varredura" e observe a barra de progresso.
Use "Limpar Resultados" para resetar a área de texto.
Use "Salvar Resultados" para exportar para scan_results.txt.



Dicas de solução de problemas:

Se a GUI não abrir, confirme o Tkinter com python3 -c "import tkinter".
Desative o firewall temporariamente para testes: sudo ufw disable (reative com sudo ufw enable).
Teste com portas comuns (ex.: 22 para SSH, se ativo) para validar.

 Configuração e Execução no Windows
 # Pré-requisitos:

 Python 3 instalado (baixe do site oficial se necessário).
 Tkinter (vem incluído na instalação padrão do Python). 
 Acesso ao Prompt de Comando ou PowerShell.

Passos para configurar e executar:

Instale o Python:

Baixe o instalador do Python 3 do site oficial.
Durante a instalação:

Marque "Add Python to PATH".
Marque "Install Tcl/Tk and IDLE" (para garantir o Tkinter).


Verifique a instalação no Prompt de Comando (Win + R, digite cmd, Enter):
textpython --version

Se não funcionar, reinstale e confirme o PATH.




## Salve o script:

Abra um editor de texto (ex.: VS Code, Notepad++, ou Bloco de Notas).
Cole o código completo do script em um arquivo chamado port_scanner_gui.py.
Salve em um diretório acessível (ex.: C:\Users\SeuUsuario\Documents\port_scanner_gui.py).
Certifique-se de salvar com codificação UTF-8 e quebras de linha Unix (se usando VS Code, configure em "LF" no canto inferior direito).


## Abra o Prompt de Comando ou PowerShell:

Pressione Win + R, digite cmd ou powershell, e pressione Enter.
Navegue até o diretório do script:
textcd C:\Users\SeuUsuario\Documents



## Execute o script:

Para execução normal (TCP funciona bem; UDP pode ser menos preciso sem privilégios):
textpython port_scanner_gui.py

Para varreduras UDP mais precisas (requer privilégios de administrador):

Clique com o botão direito no Prompt de Comando ou PowerShell e selecione "Executar como administrador".
Execute:
textpython port_scanner_gui.py



## Uso na GUI:

A janela "Port Scanner" abrirá.
Preencha os campos:

Host(s): Ex.: 127.0.0.1 ou 127.0.0.1,192.168.1.1 (para múltiplos).
Portas: Ex.: 1-100,443,8080.
Tipo de varredura: Selecione TCP, UDP ou Ambos.
Threads: Ex.: 10 (valor padrão).


Clique em "Iniciar Varredura" e observe a barra de progresso.
Use "Limpar Resultados" para resetar a área de texto.
Use "Salvar Resultados" para exportar para scan_results.txt.



## Dicas de solução de problemas:

Se a GUI não abrir, confirme o Tkinter com python -c "import tkinter".
Desative o firewall temporariamente para testes: Abra o Prompt como administrador e execute:
textnetsh advfirewall set allprofiles state off
Reative com:
textnetsh advfirewall set allprofiles state on

Teste com portas comuns (ex.: 80 para um servidor web local, se ativo) para validar.
