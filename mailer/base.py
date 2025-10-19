
class BaseSender:
    def send_email(self, to_address, subject, body):
        raise NotImplementedError("Subclasses must implement this method.")
    
    def send_email_with_attachment(self, to_address, subject, body, attachment_path):
        raise NotImplementedError("Subclasses must implement this method.")
