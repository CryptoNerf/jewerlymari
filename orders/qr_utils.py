import qrcode
from io import BytesIO
import base64

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=2,
        border=4,
    )
    qr.add_data(data)  # Добавление данных для QR-кода
    qr.make(fit=True)

    buffer = BytesIO()  # Буфер для сохранения QR-кода
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img.save(buffer, format="PNG")

    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')  # Кодирование в base64
    return img_base64