from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()
_processor = None
_model = None

def load_trocr():
    """Loads TrOCR model."""
    global _processor, _model
    if _processor is None:
        model_name = os.getenv("OCR_MODEL", "microsoft/trocr-base-printed")
        _processor = TrOCRProcessor.from_pretrained(model_name)
        _model = VisionEncoderDecoderModel.from_pretrained(model_name)
    return _processor, _model

def ocr_image(image_path: str) -> str:
    processor, model = load_trocr()
    image = Image.open(image_path).convert("RGB")
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return text.strip()
