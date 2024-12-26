import streamlit as st
import requests

# Configuração do webhook do n8n
WEBHOOK_URL = "https://devn8n.4blue.com.br/webhook/1ff18ee9-06ef-442e-9789-663d2a9cedc7/chat"

# Função para exibir o chatbot como um widget expansível
def chatbot_widget():
    # Inicializar o histórico de mensagens
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Widget expansível para o chatbot
    with st.expander("Abrir Chatbot 🤖"):
        # Exibir mensagens do histórico
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Entrada do usuário
        user_input = st.chat_input("Digite sua mensagem...")

        # Lógica para enviar mensagem e receber resposta
        if user_input:
            # Adicionar a mensagem do usuário ao histórico
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            # Enviar a mensagem ao webhook do n8n
            try:
                response = requests.post(WEBHOOK_URL, json={"message": user_input})
                response_data = response.json()
                bot_response = response_data.get("message", "Sem resposta do servidor.")

                # Adicionar a resposta do bot ao histórico
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                with st.chat_message("assistant"):
                    st.markdown(bot_response)

            except Exception as e:
                error_message = "Erro ao conectar com o servidor."
                st.session_state.messages.append({"role": "assistant", "content": error_message})
                with st.chat_message("assistant"):
                    st.markdown(error_message)

# Título da página principal
st.title("Minha Aplicação com Chatbot")

# Chamando o widget do chatbot
chatbot_widget()
