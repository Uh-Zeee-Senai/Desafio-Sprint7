import flet as ft
import requests
import qrcode
from io import BytesIO
import base64

API_CADASTRO = "http://localhost/Desafio_Sprint/php/api/cadastro.php"
API_LOGIN = "http://localhost/Desafio_Sprint/php/api/login.php"
API_EVENTOS = "http://localhost/Desafio_Sprint/php/api/listar_eventos.php"
API_COMPRAR = "http://localhost/Desafio_Sprint/php/api/comprar_ingresso.php"
API_MEUS_INGRESSOS = "http://localhost/Desafio_Sprint/php/api/meus_ingressos.php"
API_CRIAR_EVENTO = "http://localhost/Desafio_Sprint/php/api/criar_evento.php"

usuario_logado = None
usuario_admin = False


def main(page: ft.Page):
    global usuario_logado, usuario_admin

    page.title = "Loja de Eventos"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 700
    page.padding = 10

    def app_bar(titulo):
        page.appbar = ft.AppBar(
            title=ft.Text(titulo, weight="bold"),
            center_title=True,
            bgcolor=ft.colors.BLUE_700
        )

    def gerar_qr_base64(texto):
        qr = qrcode.make(texto)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()

    # ---------------- LOGIN ----------------
    def tela_login():
        page.clean()
        app_bar("Login")

        email = ft.TextField(label="Email", border_radius=10)
        senha = ft.TextField(label="Senha", password=True, border_radius=10)
        mensagem = ft.Text()

        def login(e):
            global usuario_logado, usuario_admin
            try:
                r = requests.post(API_LOGIN, json={
                    "email": email.value,
                    "senha": senha.value
                })
                dados = r.json()

                if dados["status"] == "success":
                    usuario_logado = dados["user_id"]
                    usuario_admin = dados.get("is_admin", 0) == 1
                    tela_vitrine()
                else:
                    mensagem.value = dados["message"]
                    mensagem.color = "red"
                    page.update()

            except Exception as erro:
                mensagem.value = str(erro)
                page.update()

        page.add(
            ft.Column([
                email,
                senha,
                ft.ElevatedButton("Entrar", on_click=login, width=200),
                ft.TextButton("Criar Conta", on_click=lambda e: tela_cadastro()),
                mensagem
            ], horizontal_alignment="center")
        )

    # ---------------- CADASTRO ----------------
    def tela_cadastro():
        page.clean()
        app_bar("Criar Conta")

        nome = ft.TextField(label="Nome", border_radius=10)
        email = ft.TextField(label="Email", border_radius=10)
        senha = ft.TextField(label="Senha", password=True, border_radius=10)
        mensagem = ft.Text()

        def cadastrar(e):
            try:
                r = requests.post(API_CADASTRO, json={
                    "nome": nome.value,
                    "email": email.value,
                    "senha": senha.value
                })
                dados = r.json()

                mensagem.value = dados.get("message", "")
                mensagem.color = "green" if dados["status"] == "success" else "red"
                page.update()

            except Exception as erro:
                mensagem.value = str(erro)
                page.update()

        page.add(
            ft.Column([
                nome,
                email,
                senha,
                ft.ElevatedButton("Cadastrar", on_click=cadastrar),
                ft.TextButton("Voltar", on_click=lambda e: tela_login()),
                mensagem
            ])
        )

    # ---------------- CRIAR EVENTO ----------------
    def tela_criar_evento():
        if not usuario_admin:
            page.snack_bar = ft.SnackBar(ft.Text("Apenas administradores"))
            page.snack_bar.open = True
            page.update()
            return

        page.clean()
        app_bar("Criar Evento")

        nome = ft.TextField(label="Nome do Evento")
        descricao = ft.TextField(label="Descrição")
        data = ft.TextField(label="Data")
        preco = ft.TextField(label="Preço")

        def criar(e):
            requests.post(API_CRIAR_EVENTO, data={
                "nome_evento": nome.value,
                "descricao": descricao.value,
                "data_evento": data.value,
                "preco": preco.value
            })
            tela_vitrine()

        page.add(
            nome, descricao, data, preco,
            ft.ElevatedButton("Criar Evento", on_click=criar),
            ft.TextButton("Voltar", on_click=lambda e: tela_vitrine())
        )

    # ---------------- PAGAMENTO ----------------
    def escolher_pagamento(evento_id):
        def pagar(tipo):
            comprar_evento(evento_id, tipo)

        dialog = ft.AlertDialog(
            title=ft.Text("Pagamento"),
            content=ft.Column([
                ft.ElevatedButton("💳 Cartão", on_click=lambda e: pagar("cartao")),
                ft.ElevatedButton("📱 Pix", on_click=lambda e: pagar("pix")),
                ft.ElevatedButton("💵 Dinheiro", on_click=lambda e: pagar("dinheiro")),
            ])
        )

        page.dialog = dialog
        dialog.open = True
        page.update()

    def comprar_evento(evento_id, pagamento):
        r = requests.post(API_COMPRAR, data={
            "user_id": usuario_logado,
            "evento_id": evento_id,
            "pagamento": pagamento
        })
        dados = r.json()

        page.snack_bar = ft.SnackBar(ft.Text(dados["message"]))
        page.snack_bar.open = True
        page.update()

    # ---------------- VITRINE (MELHORADA) ----------------
    def tela_vitrine():
        page.clean()
        app_bar("Eventos")

        lista = ft.Column(scroll="auto")

        try:
            r = requests.get(API_EVENTOS)
            dados = r.json()

            for evento in dados["dados"]:
                card = ft.Container(
                    margin=10,
                    border_radius=15,
                    bgcolor=ft.colors.GREY_900,
                    content=ft.Column([

                        ft.Image(
                            src=evento.get("imagem", "https://via.placeholder.com/300x150"),
                            height=150,
                            fit=ft.ImageFit.COVER
                        ),

                        ft.Container(
                            padding=10,
                            content=ft.Column([
                                ft.Text(evento["nome_evento"], size=18, weight="bold"),
                                ft.Text(evento["descricao"], size=12),
                                ft.Text(f"📅 {evento['data_evento']}"),
                                ft.Text(f"💰 R$ {evento['preco']}"),

                                ft.ElevatedButton(
                                    "Comprar ingresso",
                                    bgcolor=ft.colors.GREEN_600,
                                    color="white",
                                    on_click=lambda e, id=evento["id"]: escolher_pagamento(id)
                                )
                            ])
                        )
                    ])
                )

                lista.controls.append(card)

        except Exception as erro:
            lista.controls.append(ft.Text(str(erro)))

        botoes = [
            ft.ElevatedButton("Minha Wallet", on_click=lambda e: tela_wallet()),
        ]

        if usuario_admin:
            botoes.append(
                ft.ElevatedButton("Criar Evento", on_click=lambda e: tela_criar_evento())
            )

        botoes.append(ft.TextButton("Sair", on_click=lambda e: tela_login()))

        page.add(lista, *botoes)

    # ---------------- WALLET ----------------
    def tela_wallet():
        page.clean()
        app_bar("Minha Wallet")

        lista = ft.Column(scroll="auto")

        r = requests.get(f"{API_MEUS_INGRESSOS}?user_id={usuario_logado}")
        dados = r.json()

        for ingresso in dados["dados"]:
            img = gerar_qr_base64(ingresso["titulo"])

            lista.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=15,
                        content=ft.Column([
                            ft.Text(ingresso["titulo"], weight="bold"),
                            ft.Text(f"📅 {ingresso['data_evento']}"),
                            ft.Image(src_base64=img, width=150)
                        ], horizontal_alignment="center")
                    )
                )
            )

        page.add(
            lista,
            ft.TextButton("Voltar", on_click=lambda e: tela_vitrine())
        )

    tela_login()


ft.app(target=main)