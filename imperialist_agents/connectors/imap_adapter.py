from __future__ import annotations
import imaplib, email
from email.header import decode_header
from typing import List, Dict, Any

class IMAPEmail:
    """Thin IMAP adapter (read-only for safety)."""
    def __init__(self, host: str, username: str, password: str):
        self.host = host
        self.username = username
        self.password = password

    def _connect(self):
        m = imaplib.IMAP4_SSL(self.host)
        m.login(self.username, self.password)
        return m

    def list_subjects(self, mailbox: str = "INBOX", limit: int = 10) -> List[Dict[str, Any]]:
        m = self._connect()
        try:
            m.select(mailbox)
            status, data = m.search(None, "ALL")
            if status != "OK":
                return []
            ids = data[0].split()[-limit:]
            out = []
            for i in ids:
                _, msg_data = m.fetch(i, "(RFC822)")
                msg = email.message_from_bytes(msg_data[0][1])
                sub, enc = decode_header(msg.get("Subject", ""))[0]
                if isinstance(sub, bytes):
                    sub = sub.decode(enc or "utf-8", errors="ignore")
                out.append({"id": i.decode(), "subject": sub})
            return out
        finally:
            m.logout()