from fastapi import APIRouter
from fastapi import UploadFile, File
from PIL import Image, ImageOps
from io import BytesIO
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.post("/picture/invert")
def invert_image(img: UploadFile = File(...)):
    original_image = Image.open(img.file)
    original_image = ImageOps.invert(original_image)
    filtered_image = BytesIO()
    original_image.save(filtered_image, "JPEG")
    filtered_image.seek(0)
    return StreamingResponse(filtered_image, media_type = "image/jpeg")