"""
send_email.py  -  the GitHub Actions job emails the rendered report itself, so no Claude session has to carry the body
(added 20 Nov 2026 after a 145 KB weekend body proved too large to pass through the Gmail connector in one call).

    python3 send_email.py <run_id> [--dry-run]

Reads   reports/manifests/<run_id>.json                         window, completion status
        reports/<mode>/<date>/email_<date>_<mode>.html          the body, sent exactly as rendered by render_email.py
        reports/<mode>/<date>/combined_<date>.pdf               attached when it exists
        reports/chatgpt_review/chatgpt_review_<date>_<mode>.md  attached when it exists
Writes  reports/email_log/<run_id>.json                         what was sent, when, to whom (committed with the run)
        reports/email_log/<run_id>.eml  (--dry-run only)        the full message instead of sending it

Subject   Football V4.1 <mode>: <Sat d Mon> to <Sun d Mon>      the manifest window with the years removed
Transport Gmail SMTP over SSL (smtp.gmail.com:465) with a Google app password. Environment (repository secrets):
        GMAIL_USER            the Gmail address that sends
        GMAIL_APP_PASSWORD    a 16-character app password for that account (Google account > Security > 2-Step > App passwords)
        MAIL_TO               recipient, default robin@facestagram.co.uk

If the model step failed (completion.status is not ok) or the body is missing, a short failure notice is sent instead, so a
bad run is never silent. The body is never rewritten: the only thing ever added is that notice, and only when there is no body.
Exit code is 0 on a sent message and 1 otherwise; ci/run.sh records the exit but does not fail the job on it.
"""
import sys, os, re, json, smtplib, datetime as dt, mimetypes
from email.message import EmailMessage
from email.utils import make_msgid, formatdate

ACTIONS = "https://github.com/RobinChoppaBrooks/football-intelligence-v4/actions"
DEFAULT_TO = "robin@facestagram.co.uk"


def subject_for(mode, window):
    short = re.sub(r"\s+\d{4}\b", "", window or "").strip()           # "Sat 21 Nov 2026 to Sun 22 Nov 2026" -> "Sat 21 Nov to Sun 22 Nov"
    return f"Football V4.1 {mode}: {short}" if short else f"Football V4.1 {mode}"


def attach(msg, path):
    if not os.path.exists(path):
        return None
    ctype, _ = mimetypes.guess_type(path)
    ctype = ctype or ("text/markdown" if path.endswith(".md") else "application/octet-stream")
    main, sub = ctype.split("/", 1)
    with open(path, "rb") as f:
        msg.add_attachment(f.read(), maintype=main, subtype=sub, filename=os.path.basename(path))
    return path


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    run_id = sys.argv[1]; dry = "--dry-run" in sys.argv
    mode = run_id.split("_")[0]; st = run_id.split("_")[1]; date = f"{st[:4]}-{st[4:6]}-{st[6:8]}"
    outdir = f"reports/{'range' if mode == 'range' else mode}/{date}"

    man_path = f"reports/manifests/{run_id}.json"
    man = json.load(open(man_path, encoding="utf-8")) if os.path.exists(man_path) else {}
    window = man.get("fixture_window", {}).get("text", "")
    completion = man.get("completion", {})
    status = completion.get("status", "missing")
    body_path = f"{outdir}/email_{date}_{mode}.html"

    sender = os.environ.get("GMAIL_USER", "").strip()
    password = os.environ.get("GMAIL_APP_PASSWORD", "").strip()
    to = os.environ.get("MAIL_TO", DEFAULT_TO).strip() or DEFAULT_TO
    if not dry and (not sender or not password):
        print("send_email: GMAIL_USER / GMAIL_APP_PASSWORD not set; nothing sent"); sys.exit(1)

    msg = EmailMessage()
    msg["From"] = sender or "football-v4-bot@example.invalid"
    msg["To"] = to
    msg["Date"] = formatdate(localtime=False)
    msg["Message-ID"] = make_msgid(domain="football-intelligence-v4")
    subject = subject_for(mode, window)
    attached = []
    if status == "ok" and os.path.exists(body_path):
        html_body = open(body_path, encoding="utf-8").read()
        msg["Subject"] = subject
        msg.set_content("This report is HTML. Open it in a mail client that shows HTML, or see the attached files.")
        msg.add_alternative(html_body, subtype="html")
        for p in (f"{outdir}/combined_{date}.pdf", f"reports/chatgpt_review/chatgpt_review_{date}_{mode}.md"):
            if attach(msg, p): attached.append(p)
        kind = "report"
    else:
        reason = completion.get("message", "") if status != "ok" else f"body missing: {body_path}"
        msg["Subject"] = f"{subject} FAILED"
        text = (f"The GitHub Actions {mode} run {run_id} did not produce a report.\n"
                f"Completion status: {status}. {reason}\n\nCheck the run log: {ACTIONS}\n")
        msg.set_content(text)
        msg.add_alternative(
            f'<p style="color:#d00000;font-weight:bold;font-family:Arial,Helvetica,sans-serif">The GitHub Actions {mode} run {run_id} did not produce a report.</p>'
            f'<p style="font-family:Arial,Helvetica,sans-serif">Completion status: {status}. {reason}</p>'
            f'<p style="font-family:Arial,Helvetica,sans-serif">Check the run log: <a href="{ACTIONS}">{ACTIONS}</a></p>', subtype="html")
        kind = "failure notice"

    os.makedirs("reports/email_log", exist_ok=True)
    log = dict(run_id=run_id, mode=mode, kind=kind, subject=str(msg["Subject"]), to=to, sent_utc=None,
               body=body_path if kind == "report" else None, body_bytes=os.path.getsize(body_path) if os.path.exists(body_path) else 0,
               attachments=attached, message_id=str(msg["Message-ID"]), dry_run=dry, error=None)
    try:
        if dry:
            open(f"reports/email_log/{run_id}.eml", "wb").write(bytes(msg))
        else:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=60) as s:
                s.login(sender, password)
                s.send_message(msg)
        log["sent_utc"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:                      # noqa: BLE001  (the log must always be written)
        log["error"] = f"{type(e).__name__}: {e}"
    json.dump(log, open(f"reports/email_log/{run_id}.json", "w", encoding="utf-8"), indent=1)
    print(f"send_email: {kind} '{log['subject']}' to {to}, {log['body_bytes']} bytes, {len(attached)} attachments, "
          f"{'dry run' if dry else ('sent ' + log['sent_utc'] if log['sent_utc'] else 'FAILED ' + str(log['error']))}")
    sys.exit(0 if log["sent_utc"] else 1)


if __name__ == "__main__":
    main()
