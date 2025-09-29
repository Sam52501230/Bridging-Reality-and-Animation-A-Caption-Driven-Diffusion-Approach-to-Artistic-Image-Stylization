from atelier_generator import AtelierGenerator # type: ignore
import importlib.resources as resources
import google.generativeai as genai
from PIL import Image
import json
import os
import inspect
import shutil

# ------------------ FixedAtelierGenerator ------------------
original_preset_path = "data.py"

class FixedAtelierGenerator(AtelierGenerator):
    def __init__(self, *args, **kwargs):
        self._AtelierGenerator__load_preset = self._fixed_load_preset
        super().__init__(*args, **kwargs)

    def _fixed_load_preset(self, preset_path=original_preset_path):
        try:
            module_name = 'atelier_generator'
            try:
                with resources.files(module_name).joinpath(preset_path).open('r', encoding="utf-8") as f:
                    __atr_preset = json.load(f)
            except (TypeError, FileNotFoundError, AttributeError):
                try:
                    with resources.path(module_name, preset_path) as path_obj:
                        with open(path_obj, 'r', encoding="utf-8") as f:
                            __atr_preset = json.load(f)
                except (FileNotFoundError, AttributeError):
                    module_path = os.path.dirname(inspect.getfile(AtelierGenerator))
                    file_path = os.path.join(module_path, preset_path)
                    if os.path.exists(file_path):
                        with open(file_path, 'r', encoding="utf-8") as f:
                            __atr_preset = json.load(f)
                    else:
                        raise FileNotFoundError(f"Could not find preset file: {preset_path}")

            self._AtelierGenerator__atr_generate = __atr_preset["adr"]["generate"]
            self._AtelierGenerator__atr_prompt = __atr_preset["adr"]["prompt"]
            self._AtelierGenerator__atr_bgremove = __atr_preset["adr"]["bgremove"]
            self._AtelierGenerator__atr_upscale = __atr_preset["adr"]["upscale"]
            self._AtelierGenerator__atr_remix = __atr_preset["adr"]["remix"]
            self._AtelierGenerator__atr_enhance = __atr_preset["adr"]["enhance"]
            self._AtelierGenerator__atr_eraser = __atr_preset["adr"]["eraser"]
            self._AtelierGenerator__atr_inpaint = __atr_preset["adr"]["inpaint"]
            self._AtelierGenerator__atr_realtime = __atr_preset["adr"]["realtime"]
            self._AtelierGenerator__atr_canvas = __atr_preset["adr"]["canvas"]
            self._AtelierGenerator__atr_outpaint = __atr_preset["adr"]["outpaint"]
            self._AtelierGenerator__atr_caption = __atr_preset["adr"]["caption"]
            self._AtelierGenerator__atr_codeformer = __atr_preset["adr"]["codeformer"]
            self._AtelierGenerator__atr_transparent = __atr_preset["adr"]["transparent"]
            self._AtelierGenerator__atr_g_variation = __atr_preset["guide_range"]["variation"]
            self._AtelierGenerator__atr_g_structure = __atr_preset["guide_range"]["structure"]
            self._AtelierGenerator__atr_g_facial = __atr_preset["guide_range"]["facial"]
            self._AtelierGenerator__atr_g_style = __atr_preset["guide_range"]["style"]
            self._AtelierGenerator__atr_controlnets = __atr_preset["controlnets"]
            self._AtelierGenerator__atr_models_sdxl = __atr_preset["models_sdxl"]
            self._AtelierGenerator__atr_models_flux = __atr_preset["models_flux"]
            self._AtelierGenerator__atr_models_svi = __atr_preset["models_svi"]
            self._AtelierGenerator__atr_lora_flux = __atr_preset["lora_flux"]
            self._AtelierGenerator__atr_loc = __atr_preset["locale"][0]
            self._AtelierGenerator__atr_ime = __atr_preset["locale"][1]
            self._AtelierGenerator__atr_inf = __atr_preset["locale"][2]
            self._AtelierGenerator__atr_arc = __atr_preset["locale"][3]
            self._AtelierGenerator__atr_error = __atr_preset["error"][0]
            self._AtelierGenerator__atr_lora_svi = __atr_preset["lora_svi"]
            self._AtelierGenerator__atr_lora_rt = __atr_preset["lora_rt"]
            self._AtelierGenerator__atr_test = __atr_preset["test"][0]
            self._AtelierGenerator__atr_styles = __atr_preset["styles"]
            self._AtelierGenerator__atr_gfpgan = __atr_preset["gfpgan"]
            self._AtelierGenerator__atr_remix_model = __atr_preset["remix"]
            self._AtelierGenerator__atr_size = __atr_preset["size"]
            self._AtelierGenerator__atr_models = {**self._AtelierGenerator__atr_models_flux,
                                                  **self._AtelierGenerator__atr_models_svi,
                                                  **self._AtelierGenerator__atr_models_sdxl}
            self._AtelierGenerator__atr_models_guide = {**self._AtelierGenerator__atr_models_flux,
                                                        **self._AtelierGenerator__atr_models_svi}
        except Exception as e:
            self.logger.error(f"Error in fixed_load_atr_preset: {e}")
            print(f"Error loading preset: {e}")
            self._initialize_default_values()

    def _initialize_default_values(self):
        pass  # Can be customized

# ------------------ Image Processing + Poem Generator ------------------

# Google API for Gemini
google_api_key = ".."
genai.configure(api_key=google_api_key)

def generate_multilingual_poem(image_path, selected_languages, length, style):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        img = Image.open(image_path)

        poems = {}
        for lang in selected_languages:
            prompt = f"Write a {length.lower()} {style.lower()} poem in {lang} inspired by the uploaded image. Be creative and poetic."
            print(f"\nGenerating poem in {lang}...")
            response = model.generate_content([img, prompt])
            poems[lang] = response.text.strip()

        return poems
    except Exception as e:
        print(f"Error generating poem: {e}")
        return {}

def process_image(input_path, output_path, style_key, client):
    try:
        print("Processing image...")

        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input image not found: {input_path}")

        size, _, _ = client.size_checker(input_path)
        print(f"Image size: {size}")

        prompt = client.image_caption(input_path)
        if not prompt:
            prompt = "A beautiful artistic image"
        print(f"Generated caption: {prompt}")
        

        lora_styles = {
            '1': ('VeerAvi/studio-ghibli', 'studio-ghibli'),
            '2': ('VeerAvi/anime-plus', 'anime-plus'),
            '3': ('VeerAvi/softserve-anime', 'softserve-anime')
        }

        selected_style = lora_styles.get(style_key)
        if not selected_style:
            raise ValueError("Invalid style key selected")

        style_name = selected_style[1]

        result_path = client.image_variation(
            input_path,
            prompt,
            image_size=size,
            strength=0.99,
            lora_flux=style_name
        )

        if result_path and os.path.exists(result_path):
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            output_file_path = os.path.join(output_path, os.path.basename(result_path))
            shutil.copy(result_path, output_file_path)
            print(f"Image processed successfully! Saved to: {output_file_path}")
            return output_file_path
        else:
            print("Error: image_variation did not return a valid image path.")
            return None

    except Exception as e:
        print(f"Error in process_image: {e}")
        return None

# ------------------ Run Everything ------------------

if __name__ == "__main__":
    try:
        client = FixedAtelierGenerator(wm_text="Ghiblify! by VeerAvi")

        # ==== USER DEFINED INPUTS ====
        input_image_path = ""
        output_image_dir = ""
        style_key = '3'  # Options: '1', '2', '3'
        selected_languages = ["English"]
        poem_length = "Short"
        poem_style = "Free Verse"

        # ==== Step 1: Generate Stylized Image ====
        generated_image_path = process_image(input_image_path, output_image_dir, style_key, client)

        if generated_image_path:
            # ==== Step 2: Generate Poem from Stylized Image ====
            print("\nGenerating multilingual poems from stylized image...")
            poems = generate_multilingual_poem(generated_image_path, selected_languages, poem_length, poem_style)

            for lang, poem in poems.items():
                print(f"\n--- {lang} Poem ---\n{poem}\n")
        else:
            print("❌ Failed to generate image variation.")

    except Exception as e:
        print(f"Fatal error: {e}")
