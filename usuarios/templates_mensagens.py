def template_cadastro(nome, email, telefone):
    return (
        f"🟢 <b>Novo cadastro no site</b>\n\n"
        f"👤 <b>Nome:</b> {nome}\n"
        f"📧 <b>Email:</b> {email}\n"
        f"📞 <b>Telefone:</b> {telefone}"
    )


def template_erro(error_message):
    return (
        f"🔴 <b>Erro no site!</b>\n\n"
        f"⚠️ {error_message}"
    )


def template_pagamento(nome, valor):
    return (
        f"💰 <b>Novo pagamento recebido</b>\n\n"
        f"👤 <b>Usuário:</b> {nome}\n"
        f"💵 <b>Valor:</b> R$ {valor:.2f}"
    )
