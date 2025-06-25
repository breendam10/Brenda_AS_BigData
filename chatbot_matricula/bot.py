from botbuilder.core import TurnContext, ActivityHandler
from botbuilder.schema import (
    Activity,
    ActivityTypes,
    HeroCard,
    CardAction,
    ActionTypes,
    Attachment,
)
import requests
from config import FAQ, BACKEND_URL

user_states = {}

class ChatBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        user_id = turn_context.activity.from_property.id
        text = turn_context.activity.text.strip().lower()

        if user_id not in user_states:
            user_states[user_id] = {"step": None, "nome": "", "email": "", "curso": ""}

        state = user_states[user_id]

        # Exibir menu com botões
        if text in ["menu", "início", "opções", "ajuda"]:
            await self.enviar_menu(turn_context)
            return

        # Perguntas frequentes
        if text in FAQ:
            await turn_context.send_activity(FAQ[text])
            await turn_context.send_activity("Digite 'menu' para ver mais opções.")
            return

        # Informações gerais sobre o Ibmec
        elif text in ["informações", "informações gerais", "sobre o ibmec"]:
            await turn_context.send_activity(
                "**📚 Sobre o Ibmec:**\n\n"
                "- 🎓 Instituição de ensino superior reconhecida pela excelência acadêmica.\n"
                "- 📍 Presente em várias capitais do Brasil: São Paulo, Rio de Janeiro, Belo Horizonte, Brasília e mais.\n"
                "- 💼 Oferece cursos de Graduação, Pós, MBA e Extensão em diversas áreas (Direito, Administração, Economia, Engenharias, etc.).\n\n"
                "**📞 Contato Geral:** (21) 4503-4000\n"
                "**🌐 Site Oficial:** https://ibmec.br\n"
                "**✉️ E-mail da Secretaria:** secretaria@ibmec.edu.br"
            )
            await turn_context.send_activity("Digite 'menu' para voltar às opções.")
            return

        # Listar matrículas
        elif text in ["listar matrículas", "ver matrículas", "matrículas registradas"]:
            try:
                resp = requests.get(BACKEND_URL)
                if resp.status_code == 200:
                    lista = resp.json()
                    if not lista:
                        await turn_context.send_activity("Nenhuma matrícula registrada.")
                    else:
                        msg = "\n\n".join(
                            [f"📘 {m['nome']} ({m['curso']}) - Matrícula #{m['matricula']}" for m in lista]
                        )
                        await turn_context.send_activity(f"Lista de matrículas:\n{msg}")
                else:
                    await turn_context.send_activity("Erro ao buscar as matrículas.")
            except Exception as e:
                await turn_context.send_activity(f"Erro de conexão: {str(e)}")
            return

        # Início do fluxo de matrícula
        elif "matricula" in text or "matrícula" in text:
            state["step"] = "nome"
            await turn_context.send_activity("Vamos começar sua matrícula. Qual seu nome completo?")
            return

        elif state["step"] == "nome":
            state["nome"] = turn_context.activity.text.strip()
            state["step"] = "email"
            await turn_context.send_activity("Agora, informe seu e-mail:")
            return

        elif state["step"] == "email":
            state["email"] = turn_context.activity.text.strip()
            state["step"] = "curso"
            await turn_context.send_activity("Por fim, qual curso deseja se matricular?")
            return

        elif state["step"] == "curso":
            state["curso"] = turn_context.activity.text.strip()
            state["step"] = None

            try:
                response = requests.post(BACKEND_URL, json={
                    "nome": state["nome"],
                    "email": state["email"],
                    "curso": state["curso"]
                })

                if response.status_code == 200:
                    dados = response.json()
                    matricula_id = dados.get("matricula")
                    await turn_context.send_activity(
                        f"✅ Matrícula realizada com sucesso!\nNúmero da matrícula: **{matricula_id}**"
                    )
                else:
                    await turn_context.send_activity("❌ Erro ao registrar matrícula. Verifique os dados ou tente novamente.")
            except Exception as e:
                await turn_context.send_activity(f"❌ Erro ao conectar com o servidor: {str(e)}")

            user_states[user_id] = {"step": None, "nome": "", "email": "", "curso": ""}
            await turn_context.send_activity("Digite 'menu' para retornar às opções.")
            return

        # Caso não reconheça
        else:
            await turn_context.send_activity(
                "Desculpe, não entendi. Você pode digitar 'menu' para ver as opções ou 'matrícula' para iniciar o processo."
            )

    # Método para mostrar o menu com Hero Card
    async def enviar_menu(self, turn_context: TurnContext):
        card = HeroCard(
            title="👋 Bem-vindo! O que você deseja fazer?",
            buttons=[
                CardAction(
                    type=ActionTypes.im_back,
                    title="📝 Realizar matrícula",
                    value="matrícula"
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title="📨 Secretaria",
                    value="secretaria"
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title="ℹ️ Informações gerais",
                    value="informações"
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title="📋 Listar matrículas",
                    value="listar matrículas"
                )
            ]
        )

        attachment = Attachment(
            content_type="application/vnd.microsoft.card.hero",
            content=card
        )

        activity = Activity(
            type=ActivityTypes.message,
            attachments=[attachment]
        )

        try:
            await turn_context.send_activity(activity)
        except Exception as e:
            print("Erro ao enviar HeroCard:", str(e))
            await turn_context.send_activity("❌ Erro ao exibir o menu.")
