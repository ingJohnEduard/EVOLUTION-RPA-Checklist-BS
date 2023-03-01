from .email_service import set_email_format, send_email


def send_message(path_pdf: str):
    """
    Sends an e-mail message with the recipients arguments and EMAIL_RECIPIENTS as recipients and inserting the file specified by filename as attachment.
    """
    file = [path_pdf]
    message = set_email_format(files_to_attach=file)
    send_email(message)
