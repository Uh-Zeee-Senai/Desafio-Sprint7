import flet as ft
import requests
import qrcode
from io import BytesIO
import base64
import uuid

API_CADASTRO = "http://localhost/Desafio_Sprint/php/api/cadastro.php"
API_LOGIN = "http://localhost/Desafio_Sprint/php/api/login.php"
API_EVENTOS = "http://localhost/Desafio_Sprint/php/api/listar_eventos.php"
API_COMPRAR = "http://localhost/Desafio_Sprint/php/api/comprar_ingresso.php"
API_MEUS_INGRESSOS = "http://localhost/Desafio_Sprint/php/api/meus_ingressos.php"

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
            global usuario_logado
            r = requests.post(API_LOGIN, json={
                "email": email.value,
                "senha": senha.value
            })
            dados = r.json()

            if dados["status"] == "success":
                usuario_logado = dados.get("user_id") or dados.get("id")

                print("USER LOGADO:", usuario_logado)

                tela_vitrine()
            else:
                msg.value = dados["message"]
                msg.color = "red"
                page.update()

        page.add(email, senha,
                 ft.ElevatedButton("Entrar", on_click=login),
                 msg)

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
                    padding=10,
                    border_radius=10,
                    content=ft.Column([
                        ft.Text(evento["nome_evento"], weight="bold"),
                        ft.Text(evento["descricao"], size=10),
                        ft.Text(f"R$ {evento['preco']}"),

                        ft.ElevatedButton(
                            "Ver Evento",
                            on_click=lambda e, ev=evento: tela_evento(ev)
                        )
                    ])
                )
            )

        page.add(grid)

    # -------- DETALHE EVENTO --------
    def tela_evento(evento):
        page.clean()
        app_bar(evento["nome_evento"])

        qtd = ft.TextField(value="1", width=60)

        def adicionar_carrinho(e):
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
            ft.Text(f"Preço: R$ {evento['preco']}"),

            ft.Row([
                ft.Text("Qtd: "),
                qtd
            ]),

            ft.ElevatedButton("Adicionar ao Carrinho", on_click=adicionar_carrinho),
            ft.TextButton("Voltar", on_click=lambda e: tela_vitrine())
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

            lista.controls.append(
                ft.Container(
                    bgcolor=ft.colors.GREY_900  ,
                    padding=10,
                    border_radius=10,
                    content=ft.Column([
                        ft.Text(ev["nome_evento"], weight="bold"),
                        ft.Text(f"Qtd: {qtd}"),
                        ft.Text(f"Subtotal: R$ {subtotal}")
                    ])
                )
            )

        page.add(
            lista,
            ft.Text(f"Total: R$ {total}", size=18, weight="bold"),
            ft.ElevatedButton("Finalizar Compra", on_click=lambda e: tela_pagamento(total))
        )

    # -------- PAGAMENTO --------
    def tela_pagamento(total):
        page.clean()
        app_bar("Pagamento")

        resultado = ft.Text()

        def pagar(tipo):
            try:
                codigos = []

                for item in carrinho:
                    for i in range(item["quantidade"]):
                        r = requests.post(API_COMPRAR, json={
                            "user_id": usuario_logado,
                            "evento_id": item["evento"]["id"],
                            "pagamento": tipo
                        })
                        print("USER LOGADO:", usuario_logado)

                        dados = r.json()
                        print("RESPOSTA API:", dados)
                        

                        if dados.get("status") == "success":
                            codigos.append(dados.get("codigo", "sem código"))
                        else:
                            codigos.append("erro")

                carrinho.clear()

                resultado.value = "Compra concluída!\nCódigos:\n" + "\n".join(codigos)
                resultado.color = "green"
                page.update()

            except Exception as erro:
                resultado.value = str(erro)
                resultado.color = "red"
                page.update()

        page.add(
            ft.Text(f"Total: R$ {total}", size=20),

            ft.ElevatedButton("💳 Cartão", on_click=lambda e: pagar("cartao")),
            ft.ElevatedButton("📱 Pix", on_click=lambda e: pagar("pix")),
            ft.ElevatedButton("📄 Boleto", on_click=lambda e: pagar("boleto")),
            ft.ElevatedButton("💵 Dinheiro", on_click=lambda e: pagar("dinheiro")),

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
                qr_texto = ing.get("qr_code", codigo)

                qr = gerar_qr(qr_texto)

                lista.controls.append(
                    ft.Container(
                        bgcolor=ft.colors.GREY_900,
                        padding=15,
                        border_radius=12,
                        content=ft.Column([
                            ft.Text(ing.get("titulo", "Evento"), weight="bold", size=16),
                            ft.Text(f"📅 {ing.get('data_evento','')}"),
                            ft.Text(f"💳 {ing.get('pagamento','')}"),
                            ft.Text(f"💰 R$ {ing.get('valor','')}"),
                            ft.Text(f"🎫 Código: {codigo}", size=10),
                            ft.Image(src_base64=qr, width=140)
                        ])
                    )
                )

        except Exception as erro:
            lista.controls.append(ft.Text(str(erro), color="red"))

        page.add(lista)

    tela_login()


ft.app(target=main)