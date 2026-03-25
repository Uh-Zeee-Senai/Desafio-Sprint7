import flet as ft
import requests
import qrcode
from io import BytesIO
import base64
import webbrowser

API_CADASTRO = "http://localhost/Desafio_Sprint/php/api/cadastro.php"
API_LOGIN = "http://localhost/Desafio_Sprint/php/api/login.php"
API_EVENTOS = "http://localhost/Desafio_Sprint/php/api/listar_eventos.php"
API_COMPRAR = "http://localhost/Desafio_Sprint/php/api/comprar_ingresso.php"
API_MEUS_INGRESSOS = "http://localhost/Desafio_Sprint/php/api/meus_ingressos.php"
API_VALIDAR = "http://localhost/Desafio_Sprint/php/api/validar_ingresso.php"
API_CRIAR_EVENTO = "http://localhost/Desafio_Sprint/php/api/criar_evento.php"
API_DELETAR_EVENTO = "http://localhost/Desafio_Sprint/php/api/deletar_evento.php"

usuario_logado = None
usuario_admin = False
carrinho = []

def main(page: ft.Page):
    global usuario_logado, usuario_admin, carrinho

    page.title = "Sistema de Eventos"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO

    page.bgcolor = "#0f172a"

    # -------- APP BAR --------
    def app_bar(titulo):
        page.appbar = ft.AppBar(
            title=ft.Text(titulo, size=20, weight="bold"),
            bgcolor=ft.colors.BLUE_700,
            center_title=True,
            actions=[
                ft.IconButton(icon=ft.icons.SHOPPING_CART, icon_size=28, on_click=lambda e: tela_carrinho()),
                ft.IconButton(icon=ft.icons.CONFIRMATION_NUMBER, icon_size=28, on_click=lambda e: tela_wallet()),
                ft.IconButton(icon=ft.icons.LOGOUT, icon_size=28, on_click=lambda e: logout())
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

        email = ft.TextField(label="Email", width=320)
        senha = ft.TextField(label="Senha", password=True, width=320)
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
                usuario_admin = str(dados.get("is_admin")) == "1"
                tela_vitrine()
            else:
                msg.value = dados["message"]
                msg.color = "red"
                page.update()

        page.add(
            ft.Column([
                email,
                senha,
                ft.ElevatedButton("Entrar", width=220, on_click=login),
                ft.TextButton("Criar conta", on_click=lambda e: tela_cadastro()),
                msg
            ], horizontal_alignment="center", alignment="center")
        )

    # -------- CADASTRO --------
    def tela_cadastro():
        page.clean()
        app_bar("Cadastro")

        nome = ft.TextField(label="Nome", width=320)
        email = ft.TextField(label="Email", width=320)
        senha = ft.TextField(label="Senha", password=True, width=320)
        msg = ft.Text()

        def cadastrar(e):
            r = requests.post(API_CADASTRO, json={
                "nome": nome.value,
                "email": email.value,
                "senha": senha.value
            })

            dados = r.json()

            msg.value = dados["message"]
            msg.color = "green" if dados["status"] == "success" else "red"
            page.update()

        page.add(
            ft.Column([
                nome,
                email,
                senha,
                ft.ElevatedButton("Cadastrar", width=220, on_click=cadastrar),
                ft.TextButton("Voltar", on_click=lambda e: tela_login()),
                msg
            ], horizontal_alignment="center")
        )

    # -------- VITRINE --------
    def tela_vitrine():
        page.clean()
        app_bar("Eventos")

        grid = ft.GridView(
            expand=True,
            max_extent=420,  # 🔥 MAIOR
            spacing=20,
            run_spacing=20
        )

        r = requests.get(API_EVENTOS)
        dados = r.json()

        for evento in dados["dados"]:
            grid.controls.append(
                ft.Container(
                    width=380,
                    padding=20,
                    border_radius=20,
                    bgcolor="#1e293b",
                    content=ft.Column([
                        ft.Image(src=evento.get("imagem", ""), height=180, fit=ft.ImageFit.COVER),
                        ft.Text(evento["nome_evento"], size=20, weight="bold"),
                        ft.Text(evento["descricao"], size=14),
                        ft.Text(f"R$ {float(evento['preco']):.2f}", size=18),

                        ft.Row([
                            ft.ElevatedButton(
                                "Ver Evento",
                                width=180,
                                height=45,
                                on_click=lambda e, ev=evento: tela_evento(ev)
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                visible=usuario_admin,
                                icon_size=28,
                                on_click=lambda e, ev=evento: excluir_evento(ev["id"])
                            )
                        ], alignment="spaceBetween")
                    ])
                )
            )

        if usuario_admin:
            page.add(
                ft.Container(
                    content=ft.Column([
                        ft.Text("🔧 Painel Admin", size=22, weight="bold"),
                        ft.Row([
                            ft.ElevatedButton("➕ Criar Evento", on_click=lambda e: tela_criar_evento()),
                            ft.ElevatedButton("🎫 Validar Ingresso", on_click=lambda e: tela_validar())
                        ], alignment="center")
                    ]),
                    bgcolor=ft.colors.GREY_800,
                    padding=15,
                    border_radius=15
                )
            )

        page.add(grid)

    # -------- CRIAR EVENTO --------
    def tela_criar_evento():
        page.clean()
        app_bar("Criar Evento")

        nome = ft.TextField(label="Nome", width=320)
        descricao = ft.TextField(label="Descrição", width=320)
        data = ft.TextField(label="Data", width=320)
        preco = ft.TextField(label="Preço", width=320)
        imagem = ft.TextField(label="URL da Imagem", width=320)
        msg = ft.Text()

        def criar(e):
            r = requests.post(API_CRIAR_EVENTO, json={
                "user_id": usuario_logado,
                "nome_evento": nome.value,
                "descricao": descricao.value,
                "data_evento": data.value,
                "preco": preco.value,
                "imagem": imagem.value
            })

            dados = r.json()
            msg.value = dados.get("message", "")
            msg.color = "green" if dados["status"] == "success" else "red"
            page.update()

        page.add(
            ft.Column([
                nome, descricao, data, preco, imagem,
                ft.ElevatedButton("Criar", width=220, on_click=criar),
                msg,
                ft.TextButton("Voltar", on_click=lambda e: tela_vitrine())
            ], horizontal_alignment="center")
        )

    # -------- EXCLUIR EVENTO --------
    def excluir_evento(evento_id):

        def fechar(e):
            page.dialog.open = False
            page.update()

        def confirmar(e):
            requests.post(API_DELETAR_EVENTO, json={
                "id": evento_id,
                "user_id": usuario_logado
            })
            page.dialog.open = False
            tela_vitrine()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar"),
            content=ft.Text("Deseja excluir este evento?"),
            actions=[
                ft.TextButton("Cancelar", on_click=fechar),
                ft.TextButton("Excluir", on_click=confirmar)
            ]
        )

        page.dialog.open = True
        page.update()

    # -------- EVENTO --------
    def tela_evento(evento):
        page.clean()
        app_bar(evento["nome_evento"])

        qtd = ft.TextField(value="1", width=80)

        def add(e):
            carrinho.append({
                "evento": evento,
                "quantidade": int(qtd.value)
            })

            page.snack_bar = ft.SnackBar(ft.Text("Adicionado ao carrinho"))
            page.snack_bar.open = True
            page.update()

        page.add(
            ft.Container(
                padding=20,
                content=ft.Column([
                    ft.Image(
                        src=evento.get("imagem") if evento.get("imagem") else "https://via.placeholder.com/400x250",
                        height=250,
                        fit=ft.ImageFit.COVER
                    ),

                    ft.Text(evento["nome_evento"], size=26, weight="bold"),

                    ft.Text(evento["descricao"], size=14),

                    ft.Text(f"Preço: R$ {evento['preco']}", size=18, color="#22c55e"),

                    ft.Row([
                        ft.Text("Quantidade:"),
                        qtd
                    ]),

                    ft.ElevatedButton(
                        "Adicionar ao Carrinho",
                        height=45,
                        on_click=add
                    ),

                    ft.TextButton("Voltar", on_click=lambda e: tela_vitrine())
                ])
            )
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
            ft.ElevatedButton("Finalizar", on_click=lambda e: tela_pagamento(total)),
            ft.TextButton("Voltar", on_click=lambda e: tela_vitrine())
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
                    r = requests.post(API_COMPRAR, json={
                        "user_id": usuario_logado,
                        "evento_id": item["evento"]["id"],
                        "pagamento": metodo.value
                    })

                    dados = r.json()

                    if dados.get("status") == "success":
                        codigos.append(dados.get("codigo", "sem código"))
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
            resultado,
            ft.ElevatedButton("Ver Ingressos", on_click=lambda e: tela_wallet())
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

            usado = ing.get("usado", 0)

            status = "✅ Usado" if usado == 1 else "❌ Não usado"

            lista.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=15,
                        content=ft.Column([
                            ft.Text(ing["titulo"], weight="bold"),
                            ft.Text(f"Código: {ing['codigo_compra']}"),
                            ft.Text(status),
                            ft.Image(src_base64=qr, width=120)
                        ])
                    )
                )
            )

        page.add(lista)

    # -------- VALIDAR --------
    def tela_validar():
        page.clean()
        app_bar("Validar")

        campo = ft.TextField(label="QR Code")
        resultado = ft.Text()

        def validar(e):
            r = requests.post(API_VALIDAR, json={
                "qr_code": campo.value
            })

            dados = r.json()

            resultado.value = dados["message"]
            resultado.color = "green" if dados["status"] == "success" else "red"
            page.update()

        def abrir_camera(e):
            webbrowser.open("http://localhost/Desafio_Sprint/PHP/assets/scanner.html")

        page.add(
            campo,
            ft.Row([
                ft.ElevatedButton("Validar", on_click=validar),
                ft.ElevatedButton("📷 Câmera", on_click=abrir_camera)
            ]), 
            resultado
        )

    tela_login()


ft.app(target=main)