from typing import Dict, Sequence

import torch
import torchvision.transforms as transforms
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel


class OCR:
    def __init__(self, backbone: str = ""):
        self.backbone = backbone
        self.processor = TrOCRProcessor.from_pretrained(
            "microsoft/trocr-base-handwritten"
        )

        self.model = VisionEncoderDecoderModel.from_pretrained(
            "microsoft/trocr-base-handwritten"
        )
        self.transforms = transforms.Compose(
            [
                transforms.PILToTensor(),
                transforms.ConvertImageDtype(torch.float),
                transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
            ]
        )

    def preprocess(self, batch: Sequence[Image.Image]) -> Sequence[torch.Tensor]:
        return [
            self.processor(image, return_tensors="pt").pixel_values for image in batch
        ]

    def postprocess(self, outputs: torch.Tensor) -> Sequence[Dict]:
        self.processor.batch_decode(outputs.logits)["generated_text"]
        breakpoint()
        pass

    def __call__(self, batch: Sequence[Image.Image]) -> Sequence[Dict]:
        # tensors = self.preprocess(batch)
        generated_ids = self.model.generate(self.preprocess(batch)[0])
        self.processor.batch_decode(generated_ids, skip_special_tokens=True)
        breakpoint()
        pass


if __name__ == "__main__":
    model = OCR()
    img = Image.open("tests/assets/test.jpg")
    out = model([img])
    breakpoint()
    pass
