"""
IMAP email reader — works with Gmail, Outlook, Yahoo, and any standard IMAP server.

Gmail setup:
  1. Google Account → Security → 2-Step Verification → App Passwords
  2. Generate a 16-char App Password for "Mail"
  3. Use imap.gmail.com : 993 with that App Password

Outlook/Hotmail: imap-mail.outlook.com : 993
Yahoo:           imap.mail.yahoo.com   : 993
"""
import imaplib
import email
import re
from email.header import decode_header
from email.utils import parsedate_to_datetime

URL_RE = re.compile(
    r'https?://(?:[a-zA-Z0-9\-._~:/?#\[\]@!$&\'()*+,;=%])+',
    re.IGNORECASE
)

JUNK_EXTENSIONS = {'.css', '.js', '.woff', '.woff2', '.ttf', '.eot', '.ico', '.svg'}

COMMON_IMAP_HOSTS = {
    'gmail.com':     ('imap.gmail.com', 993),
    'googlemail.com':('imap.gmail.com', 993),
    'outlook.com':   ('imap-mail.outlook.com', 993),
    'hotmail.com':   ('imap-mail.outlook.com', 993),
    'live.com':      ('imap-mail.outlook.com', 993),
    'yahoo.com':     ('imap.mail.yahoo.com',   993),
    'ymail.com':     ('imap.mail.yahoo.com',   993),
}


def guess_host(email_addr: str):
    domain = email_addr.split('@')[-1].lower()
    return COMMON_IMAP_HOSTS.get(domain, ('imap.' + domain, 993))


def _decode(s):
    if not s:
        return ''
    parts = decode_header(s)
    result = ''
    for chunk, enc in parts:
        if isinstance(chunk, bytes):
            result += chunk.decode(enc or 'utf-8', errors='replace')
        else:
            result += str(chunk)
    return result.strip()


def _clean_urls(urls):
    """Remove tracking pixels, font URLs, and other noise."""
    cleaned = []
    seen = set()
    for u in urls:
        # strip trailing punctuation that regex may grab
        u = u.rstrip('.,;:)')
        if u in seen:
            continue
        seen.add(u)
        ext = '.' + u.split('?')[0].rsplit('.', 1)[-1].lower() if '.' in u else ''
        if ext in JUNK_EXTENSIONS:
            continue
        cleaned.append(u)
    return cleaned


def test_connection(host, port, email_addr, password):
    try:
        m = imaplib.IMAP4_SSL(host, int(port))
        m.login(email_addr, password)
        folders_ok = m.list()[0] == 'OK'
        m.logout()
        return True, None
    except imaplib.IMAP4.error as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)


def list_folders(host, port, email_addr, password):
    try:
        m = imaplib.IMAP4_SSL(host, int(port))
        m.login(email_addr, password)
        _, folder_list = m.list()
        m.logout()
        folders = []
        for item in folder_list:
            if item:
                parts = item.decode().split('"."')
                name = parts[-1].strip().strip('"')
                folders.append(name)
        return folders
    except Exception:
        return ['INBOX']


def fetch_emails(host, port, email_addr, password, folder='INBOX', limit=30, unread_only=False):
    try:
        m = imaplib.IMAP4_SSL(host, int(port))
        m.login(email_addr, password)
        m.select(f'"{folder}"')

        search_criteria = 'UNSEEN' if unread_only else 'ALL'
        _, data = m.search(None, search_criteria)
        ids = data[0].split()

        # Take the latest 'limit' emails
        ids = ids[-limit:]
        ids = list(reversed(ids))

        results = []
        for mid in ids:
            try:
                _, msg_data = m.fetch(mid, '(RFC822)')
                raw = msg_data[0][1]
                msg = email.message_from_bytes(raw)

                msg_id    = _decode(msg.get('Message-ID', '')) or f'__uid_{mid.decode()}__'
                subject   = _decode(msg.get('Subject', '(no subject)'))
                sender    = _decode(msg.get('From', ''))
                date_raw  = msg.get('Date', '')

                # Parse date nicely
                try:
                    dt = parsedate_to_datetime(date_raw)
                    date_str = dt.strftime('%d %b %Y, %H:%M')
                except Exception:
                    date_str = date_raw

                # Walk MIME parts
                body_plain = ''
                body_html  = ''
                attachments = []

                for part in msg.walk():
                    ct  = part.get_content_type()
                    cd  = str(part.get('Content-Disposition', ''))
                    fn  = part.get_filename()

                    if fn and 'attachment' in cd:
                        attachments.append(_decode(fn))
                        continue

                    payload = part.get_payload(decode=True)
                    if payload is None:
                        continue

                    text = payload.decode('utf-8', errors='replace')
                    if ct == 'text/plain':
                        body_plain += text
                    elif ct == 'text/html':
                        body_html += text

                # Prefer plain text; fall back to HTML for URL extraction
                body = body_plain or body_html
                urls = _clean_urls(URL_RE.findall(body))

                results.append({
                    'msg_id':       msg_id,
                    'subject':      subject,
                    'sender':       sender,
                    'date':         date_str,
                    'urls':         urls,
                    'url_count':    len(urls),
                    'attachments':  attachments,
                    'body_preview': (body_plain or body_html)[:400].replace('\n', ' ').strip(),
                })
            except Exception:
                continue

        m.logout()
        return results

    except Exception as e:
        return []
