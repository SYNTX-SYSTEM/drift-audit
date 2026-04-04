from typing import Optional

# ── FALLBACK TRANSLATIONS (DB ist primär) ─────────────────────
TRANSLATIONS = {
    "EN": {
        "pending_subject": "Drift Audit – Request Received",
        "pending_body": """Your request has been received.

Submission ID: {submission_id}

We are analyzing your content and will get back to you once your audit is ready.
You will then receive a payment link, followed by your results.

— SYNTX System""",
        "ready_subject": "Drift Audit – Your Audit is Ready",
        "ready_body": """Your audit is ready.

Pay now to receive your results:

→ {paypal_link}

After payment you will automatically receive:
  1. The link to your audit document
  2. The password in a separate email

— SYNTX System""",
        "delivery_link_subject": "Drift Audit – Your Results",
        "delivery_link_body": """Your audit is available.

→ {proton_link}

You will receive the password in a separate email.

— SYNTX System""",
        "delivery_password_subject": "Drift Audit – Your Access Password",
        "delivery_password_body": """Your password for the audit document:

{password}

— SYNTX System""",
    },
    "DE": {
        "pending_subject": "Drift Audit – Eingang bestätigt",
        "pending_body": """Deine Anfrage ist eingegangen.

Submission-ID: {submission_id}

Wir analysieren deinen Content und melden uns sobald dein Audit fertig ist.
Du erhältst dann einen Link zur Zahlung und danach dein Ergebnis.

— SYNTX System""",
        "ready_subject": "Drift Audit – Dein Audit ist fertig",
        "ready_body": """Dein Audit ist fertig.

Jetzt bezahlen und dein Ergebnis erhalten:

→ {paypal_link}

Nach der Zahlung erhältst du automatisch:
  1. Den Link zu deinem Audit-Dokument
  2. Das Passwort in einer separaten Mail

— SYNTX System""",
        "delivery_link_subject": "Drift Audit – Dein Ergebnis",
        "delivery_link_body": """Dein Audit ist verfügbar.

→ {proton_link}

Das Passwort erhältst du in einer separaten Mail.

— SYNTX System""",
        "delivery_password_subject": "Drift Audit – Dein Zugangspasswort",
        "delivery_password_body": """Dein Passwort für das Audit-Dokument:

{password}

— SYNTX System""",
    },
    "ZH": {
        "pending_subject": "Drift Audit – 已收到请求",
        "pending_body": """您的请求已收到。

提交编号: {submission_id}

我们正在分析您的内容，审计完成后将与您联系。
届时您将收到付款链接，随后收到您的结果。

— SYNTX System""",
        "ready_subject": "Drift Audit – 您的审计已完成",
        "ready_body": """您的审计已完成。

立即付款以获取结果：

→ {paypal_link}

付款后您将自动收到：
  1. 审计文档链接
  2. 单独邮件中的密码

— SYNTX System""",
        "delivery_link_subject": "Drift Audit – 您的结果",
        "delivery_link_body": """您的审计文档已可获取。

→ {proton_link}

密码将在单独邮件中发送。

— SYNTX System""",
        "delivery_password_subject": "Drift Audit – 您的访问密码",
        "delivery_password_body": """您的审计文档密码：

{password}

— SYNTX System""",
    },
    "ES": {
        "pending_subject": "Drift Audit – Solicitud recibida",
        "pending_body": """Tu solicitud ha sido recibida.

ID de envío: {submission_id}

Estamos analizando tu contenido y nos pondremos en contacto cuando tu auditoría esté lista.
Recibirás un enlace de pago y luego tus resultados.

— SYNTX System""",
        "ready_subject": "Drift Audit – Tu auditoría está lista",
        "ready_body": """Tu auditoría está lista.

Paga ahora para recibir tus resultados:

→ {paypal_link}

Después del pago recibirás automáticamente:
  1. El enlace a tu documento de auditoría
  2. La contraseña en un correo separado

— SYNTX System""",
        "delivery_link_subject": "Drift Audit – Tus resultados",
        "delivery_link_body": """Tu auditoría está disponible.

→ {proton_link}

Recibirás la contraseña en un correo separado.

— SYNTX System""",
        "delivery_password_subject": "Drift Audit – Tu contraseña de acceso",
        "delivery_password_body": """Tu contraseña para el documento de auditoría:

{password}

— SYNTX System""",
    },
    "HI": {
        "pending_subject": "Drift Audit – अनुरोध प्राप्त हुआ",
        "pending_body": """आपका अनुरोध प्राप्त हो गया है।

सबमिशन ID: {submission_id}

हम आपकी सामग्री का विश्लेषण कर रहे हैं और ऑडिट तैयार होने पर संपर्क करेंगे।
आपको भुगतान लिंक और फिर परिणाम मिलेंगे।

— SYNTX System""",
        "ready_subject": "Drift Audit – आपका ऑडिट तैयार है",
        "ready_body": """आपका ऑडिट तैयार है।

परिणाम प्राप्त करने के लिए अभी भुगतान करें:

→ {paypal_link}

भुगतान के बाद आपको स्वचालित रूप से मिलेगा:
  1. आपके ऑडिट दस्तावेज़ का लिंक
  2. अलग ईमेल में पासवर्ड

— SYNTX System""",
        "delivery_link_subject": "Drift Audit – आपके परिणाम",
        "delivery_link_body": """आपका ऑडिट उपलब्ध है।

→ {proton_link}

पासवर्ड अलग ईमेल में भेजा जाएगा।

— SYNTX System""",
        "delivery_password_subject": "Drift Audit – आपका एक्सेस पासवर्ड",
        "delivery_password_body": """ऑडिट दस्तावेज़ के लिए आपका पासवर्ड:

{password}

— SYNTX System""",
    },
    "AR": {
        "pending_subject": "Drift Audit – تم استلام طلبك",
        "pending_body": """تم استلام طلبك.

معرف الإرسال: {submission_id}

نحن نحلل محتواك وسنتواصل معك عند اكتمال التدقيق.
ستتلقى رابط الدفع ثم نتائجك.

— SYNTX System""",
        "ready_subject": "Drift Audit – تدقيقك جاهز",
        "ready_body": """تدقيقك جاهز.

ادفع الآن لتلقي نتائجك:

→ {paypal_link}

بعد الدفع ستتلقى تلقائياً:
  1. رابط وثيقة التدقيق
  2. كلمة المرور في بريد إلكتروني منفصل

— SYNTX System""",
        "delivery_link_subject": "Drift Audit – نتائجك",
        "delivery_link_body": """تدقيقك متاح.

→ {proton_link}

ستتلقى كلمة المرور في بريد إلكتروني منفصل.

— SYNTX System""",
        "delivery_password_subject": "Drift Audit – كلمة مرور الوصول",
        "delivery_password_body": """كلمة مرورك لوثيقة التدقيق:

{password}

— SYNTX System""",
    },
    "PT": {
        "pending_subject": "Drift Audit – Pedido recebido",
        "pending_body": """O seu pedido foi recebido.

ID de submissão: {submission_id}

Estamos a analisar o seu conteúdo e entraremos em contacto quando a sua auditoria estiver pronta.
Receberá um link de pagamento e depois os seus resultados.

— SYNTX System""",
        "ready_subject": "Drift Audit – A sua auditoria está pronta",
        "ready_body": """A sua auditoria está pronta.

Pague agora para receber os seus resultados:

→ {paypal_link}

Após o pagamento receberá automaticamente:
  1. O link para o seu documento de auditoria
  2. A senha num email separado

— SYNTX System""",
        "delivery_link_subject": "Drift Audit – Os seus resultados",
        "delivery_link_body": """A sua auditoria está disponível.

→ {proton_link}

Receberá a senha num email separado.

— SYNTX System""",
        "delivery_password_subject": "Drift Audit – A sua senha de acesso",
        "delivery_password_body": """A sua senha para o documento de auditoria:

{password}

— SYNTX System""",
    },
    "BN": {
        "pending_subject": "Drift Audit – অনুরোধ পাওয়া গেছে",
        "pending_body": """আপনার অনুরোধ পাওয়া গেছে।

সাবমিশন ID: {submission_id}

আমরা আপনার কন্টেন্ট বিশ্লেষণ করছি এবং অডিট প্রস্তুত হলে যোগাযোগ করব।
আপনি পেমেন্ট লিংক এবং তারপর আপনার ফলাফল পাবেন।

— SYNTX System""",
        "ready_subject": "Drift Audit – আপনার অডিট প্রস্তুত",
        "ready_body": """আপনার অডিট প্রস্তুত।

ফলাফল পেতে এখনই পেমেন্ট করুন:

→ {paypal_link}

পেমেন্টের পরে আপনি স্বয়ংক্রিয়ভাবে পাবেন:
  1. আপনার অডিট ডকুমেন্টের লিংক
  2. আলাদা ইমেইলে পাসওয়ার্ড

— SYNTX System""",
        "delivery_link_subject": "Drift Audit – আপনার ফলাফল",
        "delivery_link_body": """আপনার অডিট উপলব্ধ।

→ {proton_link}

পাসওয়ার্ড আলাদা ইমেইলে পাঠানো হবে।

— SYNTX System""",
        "delivery_password_subject": "Drift Audit – আপনার অ্যাক্সেস পাসওয়ার্ড",
        "delivery_password_body": """অডিট ডকুমেন্টের জন্য আপনার পাসওয়ার্ড:

{password}

— SYNTX System""",
    },
    "RU": {
        "pending_subject": "Drift Audit – Запрос получен",
        "pending_body": """Ваш запрос получен.

ID заявки: {submission_id}

Мы анализируем ваш контент и свяжемся с вами, когда аудит будет готов.
Вы получите ссылку для оплаты, а затем результаты.

— SYNTX System""",
        "ready_subject": "Drift Audit – Ваш аудит готов",
        "ready_body": """Ваш аудит готов.

Оплатите сейчас, чтобы получить результаты:

→ {paypal_link}

После оплаты вы автоматически получите:
  1. Ссылку на документ аудита
  2. Пароль в отдельном письме

— SYNTX System""",
        "delivery_link_subject": "Drift Audit – Ваши результаты",
        "delivery_link_body": """Ваш аудит доступен.

→ {proton_link}

Пароль будет отправлен в отдельном письме.

— SYNTX System""",
        "delivery_password_subject": "Drift Audit – Ваш пароль доступа",
        "delivery_password_body": """Ваш пароль для документа аудита:

{password}

— SYNTX System""",
    },
    "JA": {
        "pending_subject": "Drift Audit – リクエストを受け付けました",
        "pending_body": """リクエストを受け付けました。

送信ID: {submission_id}

コンテンツを分析中です。監査が完了次第ご連絡します。
支払いリンクをお送りし、その後結果をお届けします。

— SYNTX System""",
        "ready_subject": "Drift Audit – 監査が完了しました",
        "ready_body": """監査が完了しました。

結果を受け取るには今すぐお支払いください：

→ {paypal_link}

お支払い後、自動的に受け取ります：
  1. 監査ドキュメントへのリンク
  2. 別メールでパスワード

— SYNTX System""",
        "delivery_link_subject": "Drift Audit – 結果のお届け",
        "delivery_link_body": """監査ドキュメントが利用可能になりました。

→ {proton_link}

パスワードは別メールでお送りします。

— SYNTX System""",
        "delivery_password_subject": "Drift Audit – アクセスパスワード",
        "delivery_password_body": """監査ドキュメントのパスワード：

{password}

— SYNTX System""",
    },
}


def get_translation(language: str, key: str, db=None, **kwargs) -> str:
    lang = (language or "EN").upper()
    if lang not in TRANSLATIONS:
        lang = "EN"

    # ── DB FIRST ──────────────────────────────────────────────
    if db is not None:
        try:
            from app.models.structure import MailTemplate
            template = db.query(MailTemplate).filter_by(
                language=lang, key=key
            ).first()
            if template:
                text = template.content
                return text.format(**kwargs) if kwargs else text
        except Exception:
            pass

    # ── FALLBACK: translations.py ──────────────────────────────
    text = TRANSLATIONS[lang].get(key, TRANSLATIONS["EN"].get(key, ""))
    return text.format(**kwargs) if kwargs else text
