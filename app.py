import streamlit as st
from pypdf import PdfWriter
import io

st.set_page_config(page_title="Nando PDF Tool", page_icon="📄")

st.title("📄 Mesclador de PDF")
st.markdown("---")

# 1. Upload dos arquivos
arquivos_pdf = st.file_uploader(
    "Escolha os arquivos PDF (múltipla seleção permitida). Máximo de 200 mb por arquivo", 
    type="pdf", 
    accept_multiple_files=True
)

if arquivos_pdf:
    # Criamos um dicionário para mapear o nome do arquivo ao objeto do arquivo
    mapa_arquivos = {pdf.name: pdf for pdf in arquivos_pdf}
    nomes_arquivos = list(mapa_arquivos.keys())

    st.subheader("Configuração da Ordem")
    
    # 2. Interface de Reordenação
    # O multiselect virá pré-preenchido com todos os arquivos
    ordem_final = st.multiselect(
        "Verifique ou altere a ordem de junção:",
        options=nomes_arquivos,
        default=nomes_arquivos
    )

    st.info("💡 O primeiro da lista será o topo do documento final.")

    # 3. Processamento
    if st.button("Unir e Gerar PDF"):
        if not ordem_final:
            st.warning("Por favor, selecione pelo menos um arquivo na lista de ordem.")
        else:
            merger = PdfWriter()
            
            with st.spinner('Processando PDFs...'):
                for nome in ordem_final:
                    arquivo_obj = mapa_arquivos[nome]
                    merger.append(arquivo_obj)
                
                output = io.BytesIO()
                merger.write(output)
                merger.close()
            
            st.success("✨ Tudo pronto!")
            
            # 4. Download
            st.download_button(
                label="📥 Baixar PDF Mesclado",
                data=output.getvalue(),
                file_name="pdf_final_combinado.pdf",
                mime="application/pdf"
            )