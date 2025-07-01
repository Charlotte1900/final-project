import torch
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image
import os

def generate_anime_avatar_img2img(input_image_path, output_path):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # 使用绝对路径
    base_dir = os.path.abspath(os.path.dirname(__file__))
    model_path = os.path.join(base_dir, "models", "model.safetensors")
    config_path = os.path.join(base_dir, "models", "config.json")

    pipe = StableDiffusionImg2ImgPipeline.from_single_file(
        pretrained_model_link_or_path=model_path,
        original_config_file=config_path,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    ).to(device)

    # 加载图片
    init_image = Image.open(input_image_path).convert("RGB").resize((512, 512))

    prompt = "anime style, best quality, 1girl, upper body, facing viewer, masterpiece"
    result = pipe(prompt=prompt, image=init_image, strength=0.6, guidance_scale=7.5).images[0]

    result.save(output_path)
    print(f"动漫图保存成功：{output_path}")

generate_anime_avatar_img2img("your_face_crop.jpg", "anime_result.jpg")


