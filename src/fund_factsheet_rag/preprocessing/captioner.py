from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

_processor = None
_model = None

def load_blip(model_name="Salesforce/blip-image-captioning-base"):
    global _processor, _model
    if _processor is None:
        _processor = BlipProcessor.from_pretrained(model_name)
        _model = BlipForConditionalGeneration.from_pretrained(model_name)
    return _processor, _model

def caption_image(image_path):
    processor, model = load_blip()
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption
