import sys
import os
import torch

class FireDetection:
    def __init__(self, model_path):
        self.model_path = model_path
        self.device = torch.device('cpu')
        self.model = self.load_model()

    def load_model(self):
        # Add the directory containing the custom module to the Python path
        model_dir = os.path.dirname(self.model_path)
        if model_dir not in sys.path:
            sys.path.append(model_dir)
        model = torch.load(self.model_path, map_location=self.device)
        return model

    def predict(self, image_bytes):
        from torchvision import transforms
        from PIL import Image
        import io

        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        input_tensor = preprocess(image)
        input_batch = input_tensor.unsqueeze(0)  # Create a mini-batch as expected by the model

        with torch.no_grad():
            output = self.model(input_batch)
        
        return output.argmax().item()
