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

    imagem_base64 = {"data": None}
    def tratar_imagem(img):
        if not img:
            return "https://via.placeholder.com/400x250", None

        # 🔥 URL
        if img.startswith("http"):
            return img, None

        # 🔥 BASE64 (verifica tamanho mínimo)
        if len(img) > 100:
            return None, img

        # 🔥 NOME DE ARQUIVO (tipo "Skillet.jpg")
        return "https://via.placeholder.com/400x250", None

    # 🔥 FILE PICKER CORRIGIDO
    def file_result(e: ft.FilePickerResultEvent):
        if e.files:
            file = e.files[0]
            with open(file.path, "rb") as f:
                imagem_base64["data"] = base64.b64encode(f.read()).decode()

    arquivo = ft.FilePicker(on_result=file_result)
    page.overlay.append(arquivo)

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

        email = ft.TextField(label="Email", width=300)
        senha = ft.TextField(label="Senha", password=True, width=300)
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
            ft.Container(
                alignment=ft.alignment.center,
                content=ft.Column(
                    [email, senha, ft.ElevatedButton("Entrar", on_click=login),
                     ft.TextButton("Criar conta", on_click=lambda e: tela_cadastro()), msg],
                    horizontal_alignment="center"
                )
            )
        )

    # -------- CADASTRO --------
    def tela_cadastro():
        page.clean()
        app_bar("Cadastro")

        nome = ft.TextField(label="Nome")
        email = ft.TextField(label="Email")
        senha = ft.TextField(label="Senha", password=True)
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

        page.add(nome, email, senha,
                 ft.ElevatedButton("Cadastrar", on_click=cadastrar),
                 ft.TextButton("Voltar", on_click=lambda e: tela_login()),
                 msg)

# -------- VITRINE --------
    def tela_vitrine():
        page.clean()
        app_bar("Eventos")

        grid = ft.GridView(
            expand=True,
            max_extent=420,
            spacing=20,
            run_spacing=20
        )

        r = requests.get(API_EVENTOS)
        dados = r.json()

        for evento in dados["dados"]:
            src, b64 = tratar_imagem(evento.get("imagem"))

            grid.controls.append(
                ft.Container(
                    width=380,
                    padding=15,
                    bgcolor="#1e293b",
                    border_radius=15,
                    content=ft.Column([
                        ft.Image(
                            src=src,
                            src_base64=b64,
                            height=200,
                            width=360,
                            fit=ft.ImageFit.COVER,
                            border_radius=10
                        ),
                        ft.Text(evento["nome_evento"], weight="bold", size=18),
                        ft.Text(evento["descricao"], size=13),
                        ft.Text(f"R$ {evento['preco']}", size=16),

                        ft.Row([
                            ft.ElevatedButton(
                                "Ver Evento",
                                on_click=lambda e, ev=evento: tela_evento(ev)
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                visible=usuario_admin,
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
                        ft.Text("🔧 Painel Admin", size=20, weight="bold"),
                        ft.Row([
                            ft.ElevatedButton("➕ Criar Evento", on_click=lambda e: tela_criar_evento()),
                            ft.ElevatedButton("🎫 Validar Ingresso", on_click=lambda e: tela_validar())
                        ])
                    ]),
                    bgcolor="#1e293b",
                    padding=10,
                    border_radius=10
                )
            )

        page.add(grid)


    # -------- CRIAR EVENTO --------
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
                "user_id": usuario_logado,
                "nome_evento": nome.value,
                "descricao": descricao.value,
                "data_evento": data.value,
                "preco": preco.value,
                "imagem": imagem_base64["data"]
            })

            dados = r.json()
            msg.value = dados.get("message", "")
            msg.color = "green" if dados["status"] == "success" else "red"
            page.update()

        page.add(
            nome, descricao, data, preco,
            ft.ElevatedButton("Selecionar Imagem", on_click=lambda e: arquivo.pick_files()),
            ft.ElevatedButton("Criar", on_click=criar),
            msg,
            ft.TextButton("Voltar", on_click=lambda e: tela_vitrine())
        )


    # -------- EXCLUIR EVENTO --------
    def excluir_evento(evento_id):

        def fechar(e):
            page.dialog.open = False
            page.update()

        def confirmar(e):
            requests.post(API_DELETAR_EVENTO, json={"id": evento_id})
            page.dialog.open = False
            page.update()
            tela_vitrine()

        page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar"),
            content=ft.Text("Excluir evento?"),
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

        src, b64 = tratar_imagem(evento.get("imagem"))

        def add(e):
            quantidade = int(qtd.value) if qtd.value.isdigit() else 1

            carrinho.append({
                "evento": evento,
                "quantidade": quantidade
            })

            page.snack_bar = ft.SnackBar(ft.Text("Adicionado"))
            page.snack_bar.open = True
            page.update()

        page.add(
            ft.Image(
                src=src,
                src_base64=b64,
                height=250,
                fit=ft.ImageFit.COVER
            ),
            ft.Text(evento["nome_evento"], size=22, weight="bold"),
            ft.Text(evento["descricao"]),
            ft.Text(f"R$ {evento['preco']}"),
            ft.Row([ft.Text("Qtd"), qtd]),
            ft.ElevatedButton("Adicionar", on_click=add),
            ft.TextButton("Voltar", on_click=lambda e: tela_vitrine())
        )


    # -------- CARRINHO --------
    def tela_carrinho():
        page.clean()
        app_bar("Carrinho")

        lista = ft.Column()
        total = 0

        for i, item in enumerate(carrinho):
            ev = item["evento"]
            qtd = item["quantidade"]
            subtotal = float(ev["preco"]) * qtd
            total += subtotal

            def remover(e, index=i):
                carrinho.pop(index)
                tela_carrinho()

            lista.controls.append(
                ft.Row([
                    ft.Text(f"{ev['nome_evento']} x{qtd}"),
                    ft.IconButton(icon=ft.icons.DELETE, on_click=remover)
                ])
            )

        page.add(
            lista,
            ft.Text(f"Total: R$ {total:.2f}"),
            ft.ElevatedButton("Finalizar", on_click=lambda e: tela_pagamento(total)),
            ft.TextButton("Voltar", on_click=lambda e: tela_vitrine())
        )

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
            if not metodo.value:
                resultado.value = "Selecione um método de pagamento"
                resultado.color = "red"
                page.update()
                return

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
            ft.TextButton("Voltar", on_click=lambda e: tela_carrinho()),
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