from Modules.cmds import help, info, start

def handle_message(sender_id, text, send_func):
    text = (text or "").strip().lower()

    if text in ["hi", "hello", "hey"]:
        start.run(sender_id, send_func)
    elif text == "help":
        help.run(sender_id, send_func)
    elif text == "info":
        info.run(sender_id, send_func)
    else:
        send_func(sender_id, f"🤖 Tumi likhecho: {text}")
