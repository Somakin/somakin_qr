import frappe

@frappe.whitelist()
def make_qr_attachment(
    doctype: str,
    docname: str,
    payload: str,
    attach_field: str = "qr_image",
    is_private: int = 1,
    overwrite: int = 1,
    box_size: int = 10,
    border: int = 4,
):
    import qrcode
    from io import BytesIO

    if not (doctype and docname and payload):
        frappe.throw("doctype, docname und payload sind Pflicht.")

    # Optional: alte Datei löschen, wenn Feld schon gesetzt ist
    if overwrite and attach_field:
        old_url = frappe.db.get_value(doctype, docname, attach_field)
        if old_url:
            old_file = frappe.db.get_value("File", {"file_url": old_url}, "name")
            if old_file:
                frappe.delete_doc("File", old_file, ignore_permissions=True, force=True)

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=int(box_size),
        border=int(border),
    )
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buf = BytesIO()
    img.save(buf, format="PNG")
    content = buf.getvalue()

    filename = f"qr_{doctype}_{docname}.png".replace(" ", "_")

    file_doc = frappe.get_doc({
        "doctype": "File",
        "file_name": filename,
        "attached_to_doctype": doctype,
        "attached_to_name": docname,
        "is_private": 1 if int(is_private) else 0,
        "content": content,
    })
    file_doc.insert(ignore_permissions=True)

    if attach_field:
        # db_set statt doc.save()
        frappe.db.set_value(doctype, docname, attach_field, file_doc.file_url)

    return {"file_url": file_doc.file_url, "file_name": file_doc.file_name}