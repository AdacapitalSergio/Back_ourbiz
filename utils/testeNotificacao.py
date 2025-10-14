import google.generativeai as genai

# Configura a API Key (nunca exponha publicamente)
genai.configure(api_key="AIzaSyCYfHeJAJqyi2qrBpygTQn0XxTfg4K83po")

# Inicializa o modelo
model = genai.GenerativeModel("gemini-2.5-flash")


# Faz uma pergunta
response = model.generate_content("Explique o que é aprendizado de máquina em termos simples.")

# Mostra a resposta
print(response.text)
