from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime, timedelta
import json
import os
import pytz

# ================= CONFIGURAÇÃO =================

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "pastoral-acolhida-2026")

ESCALA_FILE = "escala.json"
EXTRAS_FILE = "extras.json"

USUARIO_ADMIN = "USUÁRIO"
SENHA_ADMIN = "SENHA"

# ================= DADOS FIXOS =================

dias_validos = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

horarios_por_dia_formatados = {
    "Segunda": ["20:00"],
    "Terça": ["7:30", "15:00"],
    "Quarta": ["7:30"],
    "Quinta": ["7:30", "15:00"],
    "Sexta": ["7:30", "20:00"],
    "Sábado": ["12:00", "17:00"],
    "Domingo": ["7:00", "9:00", "11:00", "18:00"]
}

escala_inicial = {
    f"{dia} {hora}": []
    for dia, horas in horarios_por_dia_formatados.items()
    for hora in horas
}

# ================= FUNÇÕES =================

def carregar_json(arq):
    if os.path.exists(arq):
        with open(arq, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_json(arq, dados):
    with open(arq, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def get_segunda_base():
    tz = pytz.timezone("America/Sao_Paulo")
    agora = datetime.now(tz)
    hoje = agora.date()
    segunda = hoje - timedelta(days=hoje.weekday())
    if hoje.weekday() == 6 and agora.hour >= 19:
        segunda += timedelta(days=7)
    return segunda

def saudacao():
    h = datetime.now(pytz.timezone("America/Sao_Paulo")).hour
    if 5 <= h < 12: return "Bom dia"
    if 12 <= h < 18: return "Boa tarde"
    if 18 <= h < 24: return "Boa noite"
    return "Boa madrugada"

todas_escalas = carregar_json(ESCALA_FILE)

# ================= SEMANAS =================

def gerar_informacoes_com_base(inicio):
    datas = [inicio + timedelta(days=i) for i in range(7)]
    chave = inicio.strftime("%Y-%m-%d")

    if chave not in todas_escalas:
        todas_escalas[chave] = {k: [] for k in escala_inicial}
        salvar_json(ESCALA_FILE, todas_escalas)

    extras = carregar_json(EXTRAS_FILE)
    extras_semana = extras.get(chave, {})

    horarios = {d: list(horarios_por_dia_formatados[d]) for d in dias_validos}

    for i, d in enumerate(dias_validos):
        if d == "Quarta" and datas[i].day == 28:
            horarios[d] = ["7:00", "10:00", "12:00", "15:00", "18:00", "20:00"]

    info = {
        d: {"data": datas[i].strftime("%d/%m"), "extra": extras_semana.get(d, [])}
        for i, d in enumerate(dias_validos)
    }

    titulo = f"{datas[0].strftime('%d/%m/%Y')} a {datas[6].strftime('%d/%m/%Y')}"
    curto = f"{datas[0].strftime('%d/%m')} a {datas[6].strftime('%d/%m')}"

    return info, titulo, horarios, chave, curto

# ================= ROTAS =================

@app.route("/")
def index():
    segunda = get_segunda_base()
    semanas = []

    for o in [0, 7, 14]:
        inicio = segunda + timedelta(days=o)
        info, titulo, horarios, chave, curto = gerar_informacoes_com_base(inicio)
        semanas.append({
            "titulo": titulo,
            "titulo_curto": curto,
            "dias": [{"nome": d, "data": info[d]["data"]} for d in dias_validos],
            "informacoes": info,
            "horarios": horarios,
            "escala": todas_escalas[chave]
        })

    return render_template("index.html", semanas=semanas, saudacao=saudacao())

@app.route("/adicionar/<int:s>", methods=["POST"])
def adicionar(s):
    nome = request.form.get("nome","").strip()
    dia = request.form.get("dia")
    hora = request.form.get("hora")

    if not nome:
        flash("Preencha o nome.", "warning")
        return redirect("/")

    inicio = get_segunda_base() + timedelta(days=s*7)
    chave = inicio.strftime("%Y-%m-%d")
    slot = f"{dia} {hora}"

    if nome not in todas_escalas[chave][slot]:
        todas_escalas[chave][slot].append(nome)
        salvar_json(ESCALA_FILE, todas_escalas)
        flash("Nome adicionado.", "success")

    return redirect("/")

@app.route("/remover/<int:s>", methods=["POST"])
def remover(s):
    nome = request.form.get("nome","").strip()
    dia = request.form.get("dia")
    hora = request.form.get("hora")

    inicio = get_segunda_base() + timedelta(days=s*7)
    chave = inicio.strftime("%Y-%m-%d")
    slot = f"{dia} {hora}"

    if nome in todas_escalas[chave][slot]:
        todas_escalas[chave][slot].remove(nome)
        salvar_json(ESCALA_FILE, todas_escalas)
        flash("Nome removido.", "info")

    return redirect("/")

# ===== LOGIN / ADMIN =====

@app.route("/login", methods=["POST"])
def login():
    if request.form.get("usuario") == USUARIO_ADMIN and request.form.get("senha") == SENHA_ADMIN:
        session["logado"] = True
        flash("Login realizado.", "success")
        return redirect("/admin")
    flash("Dados incorretos.", "danger")
    return redirect("/admin")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logout realizado.", "info")
    return redirect("/")

@app.route("/admin")
def admin():
    if not session.get("logado"):
        return render_template("login.html")

    segunda = get_segunda_base()
    semanas = []

    for o in [0,7,14]:
        inicio = segunda + timedelta(days=o)
        info, titulo, _, chave, _ = gerar_informacoes_com_base(inicio)
        semanas.append({"titulo": titulo, "chave": chave, "informacoes": info})

    return render_template("admin.html", semanas=semanas, dias_validos=dias_validos)

@app.route("/admin/aviso", methods=["POST"])
def admin_aviso():
    if not session.get("logado"):
        return redirect("/")

    chave = request.form["chave_semana"]
    dia = request.form["dia"]
    aviso = request.form.get("aviso","").strip()
    acao = request.form["acao"]

    extras = carregar_json(EXTRAS_FILE)
    extras.setdefault(chave, {})

    if acao == "salvar":
        extras[chave][dia] = [aviso] if aviso else []
        flash("Aviso salvo.", "success")
    else:
        extras[chave][dia] = []
        flash("Aviso removido.", "info")

    salvar_json(EXTRAS_FILE, extras)
    return redirect("/admin")

if __name__ == "__main__":
    app.run(debug=False)

