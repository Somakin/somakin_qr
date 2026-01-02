import frappe

@frappe.whitelist()
def make_qr_attachment(doctype: str, docname: str, payload: str, attach_field: str = "qr_image"):
    """
    Erzeugt aus payload ein QR-PNG und hängt es als File an das Dokument.
    attach_field: Custom Attach Image Feldname (z.B. "custom_qr_image")
    """
    # Import hier drin, damit Import-Fehler sauber sichtbar sind
    import qrcode
    from io import BytesIO

    if not (doctype and docname and payload):
        frappe.throw("doctype, docname und payload sind Pflicht.")

    doc = frappe.get_doc(doctype, docname)

    img = qrcode.make(payload)
    buf = BytesIO()
    img.save(buf, format="PNG")
    content = buf.getvalue()

    filename = f"qr_{doctype}_{docname}.png".replace(" ", "_")
    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": filename,
        "attached_to_doctype": doctype,
        "attached_to_name": docname,
        "is_private": 1,
        "content": content,
    })
    file_doc.insert(ignore_permissions=True)

    # Feld setzen (Attach Image / Attach)
    if attach_field:
        doc.set(attach_field, file_doc.file_url)
        doc.save(ignore_permissions=True)

    return {"file_url": file_doc.file_url, "file_name": file_doc.file_name}