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
                ft.IconButton(icon=ft.icons.LOGOUT, on_click=lambda e: tela_login())
            ]
        )

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
            try:
                r = requests.post(API_LOGIN, data={
                    "email": email.value,
                    "senha": senha.value
                })
                dados = r.json()

                if dados["status"] == "success":
                    usuario_logado = dados.get("user_id")
                    usuario_admin = dados.get("is_admin") == 1

                    tela_vitrine()
                else:
                    msg.value = dados["message"]
                    msg.color = "red"
                    page.update()

            except Exception as erro:
                msg.value = str(erro)
                msg.color = "red"
                page.update()

        page.add(email, senha,
                 ft.ElevatedButton("Entrar", on_click=login),
                 msg)

    # -------- VITRINE --------
    def tela_vitrine():
        page.clean()
        app_bar("Eventos")

        grid = ft.GridView(expand=True, max_extent=250)

        try:
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

        except Exception as erro:
            grid.controls.append(ft.Text(str(erro), color="red"))

        botoes = []

        if usuario_admin:
            botoes.append(
                ft.ElevatedButton("🎫 Validar Ingresso", on_click=lambda e: tela_validar())
            )

        page.add(grid, ft.Row(botoes))

    # -------- DETALHE EVENTO --------
    def tela_evento(evento):
        page.clean()
        app_bar(evento["nome_evento"])

        qtd = ft.TextField(value="1", width=60)

        def adicionar_carrinho(e):
            if not qtd.value.isdigit() or int(qtd.value) <= 0:
                page.snack_bar = ft.SnackBar(ft.Text("Quantidade inválida"))
                page.snack_bar.open = True
                page.update()
                return

            carrinho.append({
                "evento": evento,
                "quantidade": int(qtd.value)
            })

            page.snack_bar = ft.SnackBar(ft.Text("Adicionado ao carrinho"))
            page.snack_bar.open = True
            page.update()

        page.add(
            ft.Text(evento["nome_evento"], size=22, weight="bold"),
            ft.Text(evento["descricao"]),
            ft.Text(f"Data: {evento['data_evento']}"),
            ft.Text(f"Preço: R$ {float(evento['preco']):.2f}"),

            ft.Row([ft.Text("Qtd:"), qtd]),

            ft.ElevatedButton("Adicionar ao Carrinho", on_click=adicionar_carrinho),
            ft.TextButton("Voltar", on_click=lambda e: tela_vitrine())
        )

    # -------- CARRINHO --------
    def tela_carrinho():
        page.clean()
        app_bar("Carrinho")

        if not carrinho:
            page.add(
                ft.Text("🛒 Carrinho vazio", size=20),
                ft.TextButton("Voltar", on_click=lambda e: tela_vitrine())
            )
            return

        lista = ft.Column()
        total = 0

        def remover_item(index):
            carrinho.pop(index)
            tela_carrinho()

        for i, item in enumerate(carrinho):
            ev = item["evento"]
            qtd = item["quantidade"]
            subtotal = float(ev["preco"]) * qtd
            total += subtotal

            lista.controls.append(
                ft.Container(
                    bgcolor=ft.colors.GREY_900,
                    padding=10,
                    border_radius=10,
                    content=ft.Column([
                        ft.Text(ev["nome_evento"], weight="bold"),
                        ft.Text(f"Qtd: {qtd}"),
                        ft.Text(f"Subtotal: R$ {subtotal:.2f}"),
                        ft.TextButton("❌ Remover", on_click=lambda e, idx=i: remover_item(idx))
                    ])
                )
            )

        page.add(
            lista,
            ft.Text(f"Total: R$ {total:.2f}", size=18, weight="bold"),
            ft.ElevatedButton("Finalizar Compra", on_click=lambda e: tela_pagamento(total))
        )

    # -------- PAGAMENTO --------
    def tela_pagamento(total):
        page.clean()
        app_bar("Pagamento")

        metodo = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="cartao", label="💳 Cartão"),
                ft.Radio(value="pix", label="📱 Pix"),
                ft.Radio(value="boleto", label="📄 Boleto"),
                ft.Radio(value="dinheiro", label="💵 Dinheiro"),
            ])
        )

        resultado = ft.Text()

        def pagar(e):
            if not metodo.value:
                resultado.value = "Escolha um método de pagamento"
                resultado.color = "red"
                page.update()
                return

            codigos = []

            for item in carrinho:
                for _ in range(item["quantidade"]):
                    try:
                        r = requests.post(API_COMPRAR, data={
                            "user_id": str(usuario_logado),
                            "evento_id": str(item["evento"]["id"]),
                            "pagamento": metodo.value
                        })

                        dados = r.json()
                        print("RESPOSTA API:", dados)

                        if dados.get("status") == "success":
                            codigos.append(dados.get("codigo", "sem código"))
                        else:
                            codigos.append("erro")

                    except:
                        codigos.append("erro")

            carrinho.clear()

            page.snack_bar = ft.SnackBar(ft.Text("Compra realizada com sucesso! 🎉"))
            page.snack_bar.open = True

            resultado.value = "Códigos:\n" + "\n".join(codigos)
            resultado.color = "green"
            page.update()

        page.add(
            ft.Text(f"Total: R$ {total:.2f}", size=22, weight="bold"),
            ft.Divider(),
            ft.Text("Selecione o pagamento:"),
            metodo,
            ft.ElevatedButton("Finalizar Pagamento", on_click=pagar),
            ft.Divider(),
            resultado,
            ft.ElevatedButton("Ver Ingressos", on_click=lambda e: tela_wallet())
        )

    # -------- WALLET --------
    def tela_wallet():
        page.clean()
        app_bar("Meus Ingressos")

        lista = ft.Column()

        try:
            r = requests.get(f"{API_MEUS_INGRESSOS}?user_id={usuario_logado}")
            dados = r.json()

            for ing in dados["dados"]:
                codigo = ing.get("codigo_compra", "N/A")
                qr = gerar_qr(ing.get("qr_code", codigo))

                lista.controls.append(
                    ft.Card(
                        content=ft.Container(
                            padding=15,
                            content=ft.Column([
                                ft.Text(ing.get("titulo"), weight="bold"),
                                ft.Text(f"📅 {ing.get('data_evento')}"),
                                ft.Text(f"💳 {ing.get('pagamento')}"),
                                ft.Text(f"💰 R$ {ing.get('valor')}"),
                                ft.Text(f"🎫 Código: {codigo}", size=10),
                                ft.Image(src_base64=qr, width=140)
                            ], horizontal_alignment="center")
                        )
                    )
                )

        except Exception as erro:
            lista.controls.append(ft.Text(str(erro), color="red"))

        page.add(lista)

    # -------- VALIDAR --------
    def tela_validar():
        page.clean()
        app_bar("Check-in")

        campo = ft.TextField(label="QR Code", autofocus=True)
        resultado = ft.Text()

        def validar(e):
            try:
                r = requests.post(API_VALIDAR, data={
                    "qr_code": campo.value
                })

                dados = r.json()

                resultado.value = dados["message"]
                resultado.color = "green" if dados["status"] == "success" else "red"

                campo.value = ""
                page.update()

            except Exception as erro:
                resultado.value = str(erro)
                resultado.color = "red"
                page.update()

        campo.on_submit = validar

        page.add(
            ft.Text("🎫 Validador de Ingressos", size=20),
            campo,
            resultado,
            ft.TextButton("Voltar", on_click=lambda e: tela_vitrine())
        )

    tela_login()

ft.app(target=main)