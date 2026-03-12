import base64
from io import BytesIO

import qrcode


def _generate_qr_image(child_id: int):
    url = f"/checkin/{child_id}"
    qr = qrcode.QRCode(version=1, box_size=8, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img


def generate_child_qr_base64(child_id: int) -> str:
    """
    Generate a QR code pointing to the check-in URL for the child and return it as a base64 string.
    """
    img = _generate_qr_image(child_id)

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return base64.b64encode(buffer.read()).decode("utf-8")


def generate_child_qr_bytes(child_id: int) -> bytes:
    """
    Generate a QR code PNG bytes for download.
    """
    img = _generate_qr_image(child_id)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.read()

