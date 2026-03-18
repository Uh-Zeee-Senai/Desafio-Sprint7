import flet as ft
import requests
import qrcode
from io import BytesIO
import base64

API_CADASTRO = "http://localhost/Desafio_Sprint/php/api/cadastro.php"
API_LOGIN = "http://localhost/Desafio_Sprint/php/api/login.php"
API_EVENTOS = "http://localhost/Desafio_Sprint/php/api/eventos.php"
API_COMPRAR = "http://localhost/Desafio_Sprint/php/api/comprar.php"
API_MEUS_INGRESSOS = "http://localhost/Desafio_Sprint/php/api/meus_ingressos.php"

usuario_logado = None


def main(page: ft.Page):
    global usuario_logado

    page.title = "Loja de Eventos"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 700
    page.padding = 20

    def app_bar(titulo):
        page.appbar = ft.AppBar(
            title=ft.Text(titulo, weight="bold"),
            center_title=True,
            bgcolor=ft.Colors.BLUE_700
        )

    # ---------------- GERAR QR ----------------
    def gerar_qr_base64(texto):
        qr = qrcode.make(texto)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()

    # ---------------- CADASTRO ----------------
    def tela_cadastro():
        page.clean()
        app_bar("Criar Conta")

        nome = ft.TextField(label="Nome", border_radius=10)
        email = ft.TextField(label="Email", border_radius=10)
        senha = ft.TextField(label="Senha", password=True, border_radius=10)
        mensagem = ft.Text(color="red")

        def cadastrar(e):
            try:
                resposta = requests.post(API_CADASTRO, json={
                    "nome": nome.value,
                    "email": email.value,
                    "senha": senha.value
                })

                print("STATUS:", resposta.status_code)
                print("RESPOSTA BRUTA:", resposta.text)

                dados = resposta.json()

                if dados["status"] == "success":
                    mensagem.value = "Conta criada com sucesso!"
                    mensagem.color = "green"
                else:
                    mensagem.value = dados["message"]

                page.update()

            except Exception as erro:
                mensagem.value = f"Erro: {erro}"
                page.update()

        page.add(
            ft.Column(
                [
                    nome,
                    email,
                    senha,
                    ft.ElevatedButton(
                        "Cadastrar",
                        width=350,
                        height=50,
                        on_click=cadastrar
                    ),
                    ft.TextButton("Voltar para Login", on_click=lambda e: tela_login()),
                    mensagem
                ],
                spacing=15
            )
        )

    # ---------------- LOGIN ----------------
    def tela_login():
        page.clean()
        app_bar("Login")

        email = ft.TextField(label="Email", border_radius=10)
        senha = ft.TextField(label="Senha", password=True, border_radius=10)
        mensagem = ft.Text(color="red")

        def fazer_login(e):
            global usuario_logado
            try:
                resposta = requests.post(API_LOGIN, json={
                    "email": email.value,
                    "senha": senha.value
                })

                print("STATUS:", resposta.status_code)
                print("RESPOSTA BRUTA:", resposta.text)

                dados = resposta.json()

                if dados["status"] == "success":
                    usuario_logado = dados["user_id"]
                    tela_vitrine()
                else:
                    mensagem.value = dados["message"]
                    page.update()

            except Exception as erro:
                mensagem.value = f"Erro: {erro}"
                page.update()

        page.add(
            ft.Column(
                [
                    email,
                    senha,
                    ft.ElevatedButton(
                        "Entrar",
                        width=350,
                        height=50,
                        on_click=fazer_login
                    ),
                    ft.TextButton("Criar Conta", on_click=lambda e: tela_cadastro()),
                    mensagem
                ],
                spacing=15
            )
        )

    # ---------------- COMPRAR ----------------
    def comprar_evento(evento_id):
        try:
            resposta = requests.post(API_COMPRAR, json={
                "user_id": usuario_logado,
                "evento_id": evento_id
            })

            print("STATUS:", resposta.status_code)
            print("RESPOSTA BRUTA:", resposta.text)

            dados = resposta.json()

            page.snack_bar = ft.SnackBar(
                ft.Text("Compra realizada com sucesso!"),
                bgcolor=ft.Colors.GREEN
            )
            page.snack_bar.open = True
            page.update()

        except Exception as erro:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {erro}"))
            page.snack_bar.open = True
            page.update()

    # ---------------- VITRINE ----------------
    def tela_vitrine():
        page.clean()
        app_bar("Eventos Disponíveis")

        lista_eventos = ft.Column(scroll="auto")

        resposta = requests.get(API_EVENTOS)
        print("STATUS:", resposta.status_code)
        print("RESPOSTA BRUTA:", resposta.text)

        dados = resposta.json()

        dados = resposta.json()

        if dados["status"] == "success":
            for evento in dados["dados"]:
                card = ft.Card(
                    elevation=8,
                    content=ft.Container(
                        padding=15,
                        border_radius=15,
                        content=ft.Column([
                            ft.Text(evento["titulo"], size=18, weight="bold"),
                            ft.Text(evento["descricao"], size=13),
                            ft.Text(f"📅 {evento['data_evento']}"),
                            ft.Text(f"💰 R$ {evento['preco']}", weight="bold"),
                            ft.ElevatedButton(
                                "Comprar",
                                bgcolor=ft.Colors.BLUE_700,
                                color="white",
                                width=200,
                                on_click=lambda e, id=evento["id_evento"]: comprar_evento(id)
                            )
                        ], spacing=8)
                    )
                )
                lista_eventos.controls.append(card)

        page.add(
            lista_eventos,
            ft.ElevatedButton("Minha Wallet", width=350, on_click=lambda e: tela_wallet()),
            ft.TextButton("Sair", on_click=lambda e: tela_login())
        )

    # ---------------- WALLET ----------------
    def tela_wallet():
        page.clean()
        app_bar("Minha Wallet")

        lista = ft.Column(scroll="auto")

        resposta = requests.get(f"{API_MEUS_INGRESSOS}?user_id={usuario_logado}")
        print("STATUS:", resposta.status_code)
        print("RESPOSTA BRUTA:", resposta.text)

        dados = resposta.json()

        if dados["status"] == "success":
            for ingresso in dados["dados"]:
                img_base64 = gerar_qr_base64(ingresso["qr_code"])

                lista.controls.append(
                    ft.Card(
                        elevation=6,
                        content=ft.Container(
                            padding=15,
                            border_radius=15,
                            content=ft.Column([
                                ft.Text(ingresso["titulo"], weight="bold"),
                                ft.Text(f"📅 {ingresso['data_evento']}"),
                                ft.Image(src_base64=img_base64, width=200)
                            ])
                        )
                    )
                )

        page.add(
            lista,
            ft.TextButton("Voltar", on_click=lambda e: tela_vitrine())
        )

    tela_login() 


ft.app(target=main)