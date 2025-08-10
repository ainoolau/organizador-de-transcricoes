\# 📂 Organizador de Transcrições Automático



\### Sobre o Projeto

Este projeto nasceu de uma necessidade pessoal e de um problema recorrente. Antes, meu processo de trabalho envolvia criar manualmente uma hierarquia de pastas no Google Drive para cada vídeo que eu precisava transcrever. Para cada idioma (Inglês, Alemão, Francês, etc.), eu precisava criar uma pasta específica e, só então, salvar a transcrição lá dentro. Era um trabalho repetitivo e demorado que consumia um tempo valioso.



Sabendo que a automação poderia resolver esse problema, decidi criar um aplicativo para simplificar e acelerar esse fluxo de trabalho.



\### A Solução

O \*\*Organizador de Transcrições Automático\*\* é um aplicativo web desenvolvido com Streamlit que automatiza toda a organização de transcrições de vídeos. Com ele, o processo manual de criação de pastas e organização de arquivos é substituído por um fluxo rápido e eficiente, me permitindo focar no que realmente importa.



\### Como Funciona

O fluxo de trabalho é intuitivo e eficiente:



1\.  \*\*Carregamento de Arquivos:\*\* Você carrega um ou mais arquivos de legenda (`.srt`) diretamente no aplicativo.

2\.  \*\*Nome do Vídeo:\*\* Você insere o título do vídeo ao qual as transcrições pertencem.

3\.  \*\*Criação de Pastas Inteligente:\*\* O app faz a mágica:

&nbsp;   \* Ele cria uma pasta principal chamada `Transcricoes\_Athos` no seu Google Drive (se ela ainda não existir).

&nbsp;   \* Dentro da pasta principal, ele cria uma subpasta com o nome do vídeo que você digitou.

&nbsp;   \* Para cada arquivo `.srt` carregado, ele detecta automaticamente o idioma (ex: `en` para Inglês, `de` para Alemão) e cria uma pasta correspondente (ex: "Inglês", "Alemão") dentro da pasta do vídeo.

4\.  \*\*Organização Automática:\*\* Finalmente, ele salva os documentos de transcrição formatados dentro de suas respectivas pastas de idioma.



\### Tecnologias Utilizadas

O projeto foi construído utilizando as seguintes tecnologias:



\* \*\*Python:\*\* Linguagem de programação principal.

\* \*\*Streamlit:\*\* Framework para a criação da interface de usuário simples e interativa.

\* \*\*Google Drive API:\*\* Para criar pastas e arquivos no Google Drive.

\* \*\*Google Docs API:\*\* Para criar e inserir o conteúdo dos documentos.

\* \*\*Google OAuth:\*\* Para o sistema de autenticação segura.



\### Como Usar

Para rodar este projeto localmente, siga estes passos:



1\.  1. \*\*Clone o Repositório:\*\*

&nbsp;   ```bash

&nbsp;   git clone \[https://github.com/ainoolau/organizador-de-transcricoes.git](https://github.com/ainoolau/organizador-de-transcricoes.git)

&nbsp;   cd organizador-de-transcricoes

&nbsp;   ```
2.  \*\*Instale as Dependências:\*\*

&nbsp;   ```bash

&nbsp;   pip install -r requirements.txt

&nbsp;   ```

3\.  \*\*Configurações da Google API:\*\*

&nbsp;   \* Siga o guia para \[configurar as credenciais da Google API](https://developers.google.com/workspace/guides/create-project). Certifique-se de baixar o arquivo JSON para "Aplicativo para computador" e salvá-lo como `secrets.json` na raiz do projeto.

4\.  \*\*Execute o Aplicativo:\*\*

&nbsp;   ```bash

&nbsp;   streamlit run app.py

&nbsp;   ```



Sinta-se à vontade para explorar e adaptar este projeto para suas próprias necessidades!



---

