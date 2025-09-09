# nmap_tester

 Passo a Passo para Configurar e Executar a Ferramenta em Linux Mint e Windows
O  script npm_tester_gui.py (a ferramenta de varredura de portas com interface gráfica) em Linux e Windows. 

### Passo a Passo Simples para Usar o Projeto nmap_tester_gui.py no Linux
 Baixe o arquivo do GitHub:

Acesse o repositório no GitHub no navegador.
Clique em "Code" > "Download ZIP" para baixar o repositório completo como um arquivo ZIP.
O arquivo será salvo no seu diretório de downloads (ex.: ~/Downloads/nome_do_repositorio.zip).

Descompacte o arquivo ZIP:

Abra o terminal (Ctrl + Alt + T).
Navegue até o diretório de downloads:
 cd ~/Downloads

 unzip nmap_tester.zip

Navegue até a pasta do projeto:

No terminal, entre na pasta descompactada:

  cd caminnho da pasta/nmap_tester_main

  nstale as dependências (se necessário):

Verifique o Python 3:
 python3 --version

Se não estiver instalado:
 sudo apt update
 sudo apt install python3

 Instale o Tkinter para a GUI:
  sudo apt install python3-tk


Execute o script:

 No terminal, rode o script:
 python3 nmap_tester_gui.py

Para varreduras UDP mais precisas (opcional, requer senha de sudo):
 sudo python3 nmap_tester_gui.py

Use a aplicação:

A janela gráfica abrirá.
Preencha os campos: Host(s) (ex.: 127.0.0.1), Portas (ex.: 1-100,443), Tipo (TCP/UDP/Ambos), Threads (ex.: 10).
Clique em "Iniciar Varredura" para ver os resultados.
Use os botões para limpar ou salvar os resultados.

Dicas: Se houver erros, verifique o firewall (sudo ufw disable temporariamente) ou teste com portas locais ativas (ex.: 22 para SSH).

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


 ### Configuração e Execução no Windows
 Pré-requisitos:

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
python --version

Se não funcionar, reinstale e confirme o PATH.


## Salve o script:

Abra um editor de texto (ex.: VS Code, Notepad++, ou Bloco de Notas).
Cole o código completo do script em um arquivo chamado nmap_tester_gui.py.
Salve em um diretório acessível (ex.: C:\Users\SeuUsuario\Documents\nmap_tester_gui.py).
Certifique-se de salvar com codificação UTF-8 e quebras de linha Unix (se usando VS Code, configure em "LF" no canto inferior direito).


## Abra o Prompt de Comando ou PowerShell:

Pressione Win + R, digite cmd ou powershell, e pressione Enter.
Navegue até o diretório do script:
cd C:\Users\SeuUsuario\Documents



## Execute o script:

Para execução normal (TCP funciona bem; UDP pode ser menos preciso sem privilégios):
  python nmap_tester_gui.py

Para varreduras UDP mais precisas (requer privilégios de administrador):

Clique com o botão direito no Prompt de Comando ou PowerShell e selecione "Executar como administrador".
Execute:
  python nmap_tester_gui.py



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
  netsh advfirewall set allprofiles state off
Reative com:
  netsh advfirewall set allprofiles state on

Teste com portas comuns (ex.: 80 para um servidor web local, se ativo) para validar.
