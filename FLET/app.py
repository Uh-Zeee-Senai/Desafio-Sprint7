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
API_VALIDAR = "http://localhost/Desafio_Sprint/php/api/validar_ingresso.php"

usuario_logado = None
usuario_admin = False


def main(page: ft.Page):
    global usuario_logado, usuario_admin

    page.title = "Loja de Eventos"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO

    # -------- APP BAR --------
    def app_bar(titulo):
        page.appbar = ft.AppBar(
            title=ft.Text(titulo, weight="bold"),
            center_title=True,
            bgcolor=ft.colors.BLUE_700,
            actions=[
                ft.IconButton(
                    icon=ft.icons.LOGOUT,
                    on_click=lambda e: tela_login()
                )
            ]
        )

    # -------- QR --------
    def gerar_qr_base64(texto):
        qr = qrcode.make(texto)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()

    # -------- LOGIN --------
    def tela_login():
        page.clean()
        app_bar("Login")

        email = ft.TextField(label="Email")
        senha = ft.TextField(label="Senha", password=True)
        mensagem = ft.Text()

        def login(e):
            global usuario_logado, usuario_admin
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

        page.add(
            ft.Column([
                email,
                senha,
                ft.ElevatedButton("Entrar", on_click=login),
                ft.TextButton("Criar Conta", on_click=lambda e: tela_cadastro()),
                mensagem
            ])
        )

    # -------- CADASTRO --------
    def tela_cadastro():
        page.clean()
        app_bar("Cadastro")

        nome = ft.TextField(label="Nome")
        email = ft.TextField(label="Email")
        senha = ft.TextField(label="Senha", password=True)
        mensagem = ft.Text()

        def cadastrar(e):
            r = requests.post(API_CADASTRO, json={
                "nome": nome.value,
                "email": email.value,
                "senha": senha.value
            })
            dados = r.json()

            mensagem.value = dados["message"]
            mensagem.color = "green" if dados["status"] == "success" else "red"
            page.update()

        page.add(nome, email, senha,
                 ft.ElevatedButton("Cadastrar", on_click=cadastrar),
                 ft.TextButton("Voltar", on_click=lambda e: tela_login()),
                 mensagem)

    # -------- CRIAR EVENTO --------
    def tela_criar_evento():
        if not usuario_admin:
            return

        page.clean()
        app_bar("Criar Evento")

        nome = ft.TextField(label="Nome")
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

        page.add(nome, descricao, data, preco,
                 ft.ElevatedButton("Criar", on_click=criar))

    # -------- VALIDAR --------
    def tela_validar():
        page.clean()
        app_bar("Validar Ingresso")

        campo = ft.TextField(label="QR (INGRESSO:ID)")
        resultado = ft.Text()

        def validar(e):
            r = requests.post(API_VALIDAR, data={
                "qr_code": campo.value
            })
            dados = r.json()

            resultado.value = dados["message"]
            resultado.color = "green" if dados["status"] == "success" else "red"
            page.update()

        page.add(
            campo,
            ft.ElevatedButton("Validar", on_click=validar),
            resultado,
            ft.TextButton("Voltar", on_click=lambda e: tela_vitrine())
        )

    # -------- PAGAMENTO --------
    def escolher_pagamento(evento_id):
        def pagar(tipo):
            r = requests.post(API_COMPRAR, data={
                "user_id": usuario_logado,
                "evento_id": evento_id,
                "pagamento": tipo
            })
            page.snack_bar = ft.SnackBar(ft.Text(r.json()["message"]))
            page.snack_bar.open = True
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Pagamento"),
            content=ft.Column([
                ft.ElevatedButton("Cartão", on_click=lambda e: pagar("cartao")),
                ft.ElevatedButton("Pix", on_click=lambda e: pagar("pix")),
                ft.ElevatedButton("Dinheiro", on_click=lambda e: pagar("dinheiro")),
            ])
        )

        page.dialog = dialog
        dialog.open = True
        page.update()

    # -------- VITRINE --------
    def tela_vitrine():
        page.clean()
        app_bar("Eventos")

        grid = ft.GridView(expand=True, max_extent=200)

        r = requests.get(API_EVENTOS)
        dados = r.json()

        for evento in dados["dados"]:
            grid.controls.append(
                ft.Container(
                    bgcolor=ft.colors.GREY_900,
                    border_radius=10,
                    padding=10,
                    content=ft.Column([
                        ft.Text(evento["nome_evento"], weight="bold"),
                        ft.Text(evento["descricao"], size=10),
                        ft.Text(f"R$ {evento['preco']}"),

                        ft.ElevatedButton(
                            "Comprar",
                            on_click=lambda e, id=evento["id"]: escolher_pagamento(id)
                        )
                    ])
                )
            )

        botoes = [
            ft.ElevatedButton("Minha Wallet", on_click=lambda e: tela_wallet())
        ]

        if usuario_admin:
            botoes.append(ft.ElevatedButton("Criar Evento", on_click=lambda e: tela_criar_evento()))
            botoes.append(ft.ElevatedButton("Validar", on_click=lambda e: tela_validar()))

        page.add(grid, ft.Row(botoes))

    # -------- WALLET --------
    def tela_wallet():
        page.clean()
        app_bar("Wallet")

        lista = ft.Column()

        r = requests.get(f"{API_MEUS_INGRESSOS}?user_id={usuario_logado}")
        dados = r.json()

        for ingresso in dados["dados"]:
            qr_texto = ingresso["qr_code"]
            img = gerar_qr_base64(qr_texto)

            lista.controls.append(
                ft.Container(
                    bgcolor=ft.colors.GREY_900,
                    padding=15,
                    border_radius=10,
                    content=ft.Column([
                        ft.Text(ingresso["titulo"], weight="bold"),
                        ft.Text(ingresso["data_evento"]),
                        ft.Image(src_base64=img, width=150),
                        ft.Text(qr_texto, size=10)
                    ])
                )
            )

        page.add(lista, ft.TextButton("Voltar", on_click=lambda e: tela_vitrine()))

    tela_login()


ft.app(target=main)