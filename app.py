import streamlit as st
import os
import pickle
import google.auth.transport.requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configurações
st.set_page_config(
    page_title="Organizador de Transcrições Automático",
    page_icon="📁",
    layout="wide"
)

# Parâmetros de autenticação
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/documents'
]
TEMPLATE_DOC_ID = '1e942AWo1npx4nRDigYtrc4_jVcfTVzJ3eFen-Et7-0c'

# Autenticação via OAuth2
def autenticar():
    token_file = "token.pkl"

    if os.path.exists(token_file):
        with open(token_file, "rb") as token:
            creds = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_config(
            {
                "installed": {
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            },
            SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open(token_file, "wb") as token:
            pickle.dump(creds, token)

    return creds

# Inicia autenticação
try:
    creds = autenticar()
    drive_service = build('drive', 'v3', credentials=creds)
    docs_service = build('docs', 'v1', credentials=creds)
except Exception as e:
    st.error(f"❌ Falha na autenticação: {str(e)}")
    st.stop()

# Funções de manipulação
def criar_pasta(nome, pai_id=None):
    try:
        query = f"name='{nome}' and mimeType='application/vnd.google-apps.folder'"
        if pai_id:
            query += f" and '{pai_id}' in parents"

        pastas = drive_service.files().list(q=query).execute().get('files', [])
        return pastas[0]['id'] if pastas else drive_service.files().create(
            body={
                'name': nome,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [pai_id] if pai_id else []
            },
            fields='id'
        ).execute()['id']
    except HttpError as e:
        st.error(f"Erro ao criar pasta '{nome}': {str(e)}")
        return None

def criar_documento_seguro(titulo, conteudo, pasta_id):
    try:
        doc_copy = drive_service.files().copy(
            fileId=TEMPLATE_DOC_ID,
            body={
                'name': titulo,
                'parents': [pasta_id]
            },
            supportsAllDrives=True,
            fields='id'
        ).execute()
        document_id = doc_copy.get('id')

        docs_service.documents().batchUpdate(
            documentId=document_id,
            body={
                'requests': [{
                    'insertText': {
                        'text': conteudo,
                        'location': {'index': 1}
                    }
                }]
            }
        ).execute()

        return True
    except HttpError as e:
        st.error(f"Erro ao criar documento '{titulo}': {str(e)}")
        return False

def detectar_idioma(nome_arquivo):
    prefixos = {
        'ar': 'Árabe', 'de': 'Alemão', 'es': 'Espanhol', 'fr': 'Francês',
        'it': 'Italiano', 'ja': 'Japonês', 'ko': 'Coreano', 'nl': 'Holandês',
        'pl': 'Polonês', 'pt': 'Português', 'ru': 'Russo', 'tr': 'Turco',
        'en': 'Inglês', 'hi': 'Hindi', 'id': 'Indonésio', 'fil': 'Filipino'
    }
    nome = nome_arquivo.lower()
    return prefixos.get(nome[:3], prefixos.get(nome[:2], 'Outros'))

# Interface
st.title("📂 Organizador de Transcrições PASTAS ATHOS")

with st.container(border=True):
    st.subheader("1. Selecione os arquivos .SRT")
    arquivos = st.file_uploader(
        "Arraste ou selecione os arquivos",
        type=['srt'],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    if arquivos:
        st.success(f"✅ {len(arquivos)} arquivo(s) selecionado(s)")
        with st.expander("📝 Visualizar arquivos"):
            for arquivo in arquivos:
                st.write(f"- {arquivo.name} ({arquivo.size/1024:.2f} KB)")

with st.container(border=True):
    st.subheader("2. Digite o título do vídeo")
    nome_video = st.text_input(
        "Nome sem extensão",
        placeholder="Ex: Transformei Villagers em Água no Minecraft",
        label_visibility="collapsed"
    )

if st.button("🚀 Processar Transcrições", type="primary", use_container_width=True):
    if not arquivos:
        st.warning("Por favor, selecione pelo menos um arquivo .SRT")
        st.stop()

    if not nome_video:
        st.warning("Digite o título do vídeo")
        st.stop()

    with st.status("Processando...", expanded=True) as status:
        try:
            pasta_principal = criar_pasta("Transcricoes_Athos")
            if not pasta_principal:
                st.error("Falha ao criar pasta principal.")
                st.stop()

            st.write(f"✅ Pasta criada: [Abrir no Drive](https://drive.google.com/drive/folders/{pasta_principal})")

            for arquivo in arquivos:
                try:
                    st.write(f"\n📄 Processando: {arquivo.name}")
                    conteudo = arquivo.read().decode('utf-8')
                    idioma = detectar_idioma(arquivo.name)

                    st.write(f"📁 Criando pasta '{idioma}'...")
                    pasta_idioma = criar_pasta(idioma, pasta_principal)
                    if not pasta_idioma:
                        continue

                    st.write("✍️ Criando transcrição...")
                    if criar_documento_seguro(f"Transcrição - {arquivo.name}", conteudo, pasta_idioma):
                        st.write("✅ Transcrição criada")

                    st.write("🎬 Criando cópia nomeada...")
                    if criar_documento_seguro(nome_video, conteudo, pasta_idioma):
                        st.write("✅ Cópia criada")

                    st.success(f"✔️ {arquivo.name} processado com sucesso!")
                except Exception as e:
                    st.error(f"Erro no arquivo {arquivo.name}: {str(e)}")
                    continue

            status.update(label="✅ Processamento concluído!", state="complete")
            st.balloons()

        except Exception as e:
            status.update(label="❌ Falha no processamento", state="error")
            st.error(f"Erro geral: {str(e)}")
