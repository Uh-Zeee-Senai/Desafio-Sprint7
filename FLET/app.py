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
API_VALIDAR = "http://localhost/Desafio_Sprint/php/api/validar_ingresso.php"
API_CRIAR_EVENTO = "http://localhost/Desafio_Sprint/php/api/criar_evento.php"

usuario_logado = None
usuario_admin = False
carrinho = []

def main(page: ft.Page):
    global usuario_logado, usuario_admin, carrinho

    page.title = "Sistema de Eventos"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO

    # -------- APP BAR --------
    def app_bar(titulo):
        page.appbar = ft.AppBar(
            title=ft.Text(titulo),
            bgcolor=ft.colors.BLUE_700,
            actions=[
                ft.IconButton(icon=ft.icons.SHOPPING_CART, on_click=lambda e: tela_carrinho()),
                ft.IconButton(icon=ft.icons.CONFIRMATION_NUMBER, on_click=lambda e: tela_wallet()),
                ft.IconButton(icon=ft.icons.LOGOUT, on_click=lambda e: logout())
            ]
        )

    def logout():
        global usuario_logado, usuario_admin, carrinho
        usuario_logado = None
        usuario_admin = False
        carrinho.clear()
        tela_login()

    # -------- QR --------
    def gerar_qr(texto):
        qr = qrcode.make(texto)
        buffer = BytesIO()
        qr.save(buffer)
        return base64.b64encode(buffer.getvalue()).decode()

    # -------- LOGIN --------
    def tela_login():
        page.clean()
        app_bar("Login")

        email = ft.TextField(label="Email")
        senha = ft.TextField(label="Senha", password=True)
        msg = ft.Text()

        def login(e):
            global usuario_logado, usuario_admin

            r = requests.post(API_LOGIN, json={
                "email": email.value,
                "senha": senha.value
            })

            dados = r.json()

            if dados["status"] == "success":
                usuario_logado = int(dados["user_id"])
                usuario_admin = dados.get("is_admin") == 1

                tela_vitrine()
            else:
                msg.value = dados["message"]
                msg.color = "red"
                page.update()

        page.add(
            email,
            senha,
            ft.ElevatedButton("Entrar", on_click=login),
            ft.TextButton("Criar conta", on_click=lambda e: tela_cadastro()),
            msg
        )

    # -------- CADASTRO --------
    def tela_cadastro():
        page.clean()
        app_bar("Cadastro")

        email = ft.TextField(label="Email")
        senha = ft.TextField(label="Senha", password=True)
        msg = ft.Text()

        def cadastrar(e):
            r = requests.post(API_CADASTRO, json={
                "email": email.value,
                "senha": senha.value
            })

            dados = r.json()

            msg.value = dados["message"]
            msg.color = "green" if dados["status"] == "success" else "red"
            page.update()

        page.add(
            email,
            senha,
            ft.ElevatedButton("Cadastrar", on_click=cadastrar),
            ft.TextButton("Voltar", on_click=lambda e: tela_login()),
            msg
        )

    # -------- VITRINE --------
    def tela_vitrine():
        page.clean()
        app_bar("Eventos")

        grid = ft.GridView(expand=True, max_extent=250)

        r = requests.get(API_EVENTOS)
        dados = r.json()

        for evento in dados["dados"]:
            grid.controls.append(
                ft.Container(
                    bgcolor=ft.colors.GREY_900,
                    padding=10,
                    border_radius=10,
                    content=ft.Column([
                        ft.Text(evento["nome_evento"], weight="bold"),
                        ft.Text(evento["descricao"], size=10),
                        ft.Text(f"R$ {float(evento['preco']):.2f}"),

                        ft.ElevatedButton(
                            "Ver Evento",
                            on_click=lambda e, ev=evento: tela_evento(ev)
                        )
                    ])
                )
            )

        botoes_admin = []

        if usuario_admin:
            botoes_admin.append(
                ft.ElevatedButton("➕ Criar Evento", on_click=lambda e: tela_criar_evento())
            )
            botoes_admin.append(
                ft.ElevatedButton("🎫 Validar Ingresso", on_click=lambda e: tela_validar())
            )

        page.add(grid, ft.Row(botoes_admin))

    # -------- CRIAR EVENTO (ADMIN) --------
    def tela_criar_evento():
        page.clean()
        app_bar("Criar Evento")

        nome = ft.TextField(label="Nome")
        descricao = ft.TextField(label="Descrição")
        data = ft.TextField(label="Data")
        preco = ft.TextField(label="Preço")
        msg = ft.Text()

        def criar(e):
            r = requests.post(API_CRIAR_EVENTO, json={
                "nome_evento": nome.value,
                "descricao": descricao.value,
                "data_evento": data.value,
                "preco": preco.value
            })

            dados = r.json()
            msg.value = dados["message"]
            page.update()

        page.add(nome, descricao, data, preco,
                 ft.ElevatedButton("Criar", on_click=criar),
                 msg)

    # -------- EVENTO --------
    def tela_evento(evento):
        page.clean()
        app_bar(evento["nome_evento"])

        qtd = ft.TextField(value="1", width=60)

        def add(e):
            carrinho.append({
                "evento": evento,
                "quantidade": int(qtd.value)
            })
            page.snack_bar = ft.SnackBar(ft.Text("Adicionado ao carrinho"))
            page.snack_bar.open = True
            page.update()

        page.add(
            ft.Text(evento["nome_evento"], size=22),
            ft.Text(evento["descricao"]),
            ft.Text(f"Preço: R$ {evento['preco']}"),
            ft.Row([ft.Text("Qtd"), qtd]),
            ft.ElevatedButton("Adicionar ao Carrinho", on_click=add)
        )

    # -------- CARRINHO --------
    def tela_carrinho():
        page.clean()
        app_bar("Carrinho")

        lista = ft.Column()
        total = 0

        for item in carrinho:
            ev = item["evento"]
            qtd = item["quantidade"]
            subtotal = float(ev["preco"]) * qtd
            total += subtotal

            lista.controls.append(ft.Text(f"{ev['nome_evento']} x{qtd}"))

        page.add(
            lista,
            ft.Text(f"Total: R$ {total:.2f}"),
            ft.ElevatedButton("Finalizar", on_click=lambda e: tela_pagamento(total))
        )

    # -------- PAGAMENTO --------
    def tela_pagamento(total):
        page.clean()
        app_bar("Pagamento")

        metodo = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="cartao", label="Cartão"),
                ft.Radio(value="pix", label="Pix"),
                ft.Radio(value="boleto", label="Boleto"),
                ft.Radio(value="dinheiro", label="Dinheiro"),
            ])
        )

        resultado = ft.Text()

        def pagar(e):
            codigos = []

            for item in carrinho:
                for _ in range(item["quantidade"]):

                    r = requests.post(API_COMPRAR, data={
                        "user_id": str(usuario_logado),
                        "evento_id": str(item["evento"]["id"]),
                        "pagamento": metodo.value
                    })

                    dados = r.json()

                    if dados["status"] == "success":
                        codigos.append(dados["codigo"])
                    else:
                        codigos.append("erro")

            carrinho.clear()

            resultado.value = "Compra concluída:\n" + "\n".join(codigos)
            resultado.color = "green"
            page.update()

        page.add(
            ft.Text(f"Total: R$ {total:.2f}"),
            metodo,
            ft.ElevatedButton("Pagar", on_click=pagar),
            resultado
        )

    # -------- WALLET --------
    def tela_wallet():
        page.clean()
        app_bar("Ingressos")

        lista = ft.Column()

        r = requests.get(f"{API_MEUS_INGRESSOS}?user_id={usuario_logado}")
        dados = r.json()

        for ing in dados["dados"]:
            qr = gerar_qr(ing["qr_code"])

            lista.controls.append(
                ft.Column([
                    ft.Text(ing["titulo"]),
                    ft.Text(ing["codigo_compra"]),
                    ft.Image(src_base64=qr, width=120)
                ])
            )

        page.add(lista)

    # -------- VALIDAR --------
    def tela_validar():
        page.clean()
        app_bar("Validar")

        campo = ft.TextField(label="QR")
        resultado = ft.Text()

        def validar(e):
            r = requests.post(API_VALIDAR, data={"qr_code": campo.value})
            dados = r.json()

            resultado.value = dados["message"]
            resultado.color = "green" if dados["status"] == "success" else "red"
            page.update()

        page.add(campo, ft.ElevatedButton("Validar", on_click=validar), resultado)

    tela_login()

ft.app(target=main)