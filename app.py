import os
from subprocess import getoutput

gpu_info = getoutput('nvidia-smi')
if("A10G" in gpu_info):
    os.system(f"pip install -q https://github.com/camenduru/stable-diffusion-webui-colab/releases/download/0.0.15/xformers-0.0.15.dev0+4c06c79.d20221205-cp38-cp38-linux_x86_64.whl")
elif("T4" in gpu_info):
    os.system(f"pip install -q https://github.com/camenduru/stable-diffusion-webui-colab/releases/download/0.0.15/xformers-0.0.15.dev0+1515f77.d20221130-cp38-cp38-linux_x86_64.whl")

os.system(f"git clone -b v1.5 https://github.com/camenduru/stable-diffusion-webui /home/user/app/stable-diffusion-webui")
os.chdir("/home/user/app/stable-diffusion-webui")

# ------------------------------------------------------------------v1.5-----------------------------------------------------------------------------
os.system(f'''sed -i -e "s/document.getElementsByTagName('gradio-app')\[0\].shadowRoot/!!document.getElementsByTagName('gradio-app')[0].shadowRoot ? document.getElementsByTagName('gradio-app')[0].shadowRoot : document/g" /home/user/app/stable-diffusion-webui/script.js''')
os.system(f"sed -i -e 's/                show_progress=False,/                show_progress=True,/g' /home/user/app/stable-diffusion-webui/modules/ui.py")
os.system(f"sed -i -e 's/shared.demo.launch/shared.demo.queue().launch/g' /home/user/app/stable-diffusion-webui/webui.py")
os.system(f"sed -i -e 's/ outputs=\[/queue=False, &/g' /home/user/app/stable-diffusion-webui/modules/ui.py")
os.system(f"sed -i -e 's/               queue=False,  /                /g' /home/user/app/stable-diffusion-webui/modules/ui.py")
os.system(f'''sed -i -e "s/allow_methods=\['\*'\]/allow_methods=['*'], allow_credentials=True, allow_headers=['*']/g" /home/user/app/stable-diffusion-webui/webui.py''')
# ---------------------------------------------------------------------------------------------------------------------------------------------------

os.system(f"sed -i -e '/(txt2img_interface, \"txt2img\", \"txt2img\"),/d' /home/user/app/stable-diffusion-webui/modules/ui.py")
os.system(f"sed -i -e '/(img2img_interface, \"img2img\", \"img2img\"),/d' /home/user/app/stable-diffusion-webui/modules/ui.py")
os.system(f"sed -i -e '/(extras_interface, \"Extras\", \"extras\"),/d' /home/user/app/stable-diffusion-webui/modules/ui.py")
os.system(f"sed -i -e '/(pnginfo_interface, \"PNG Info\", \"pnginfo\"),/d' /home/user/app/stable-diffusion-webui/modules/ui.py")
os.system(f"sed -i -e '/(modelmerger_interface, \"Checkpoint Merger\", \"modelmerger\"),/d' /home/user/app/stable-diffusion-webui/modules/ui.py")
os.system(f"sed -i -e '/(train_interface, \"Train\", \"ti\"),/d' /home/user/app/stable-diffusion-webui/modules/ui.py")
os.system(f"sed -i -e '/extensions_interface, \"Extensions\", \"extensions\"/d' /home/user/app/stable-diffusion-webui/modules/ui.py")
os.system(f"sed -i -e '/settings_interface, \"Settings\", \"settings\"/d' /home/user/app/stable-diffusion-webui/modules/ui.py")

os.system(f"wget -q {os.getenv('MODEL_LINK')} -O /home/user/app/stable-diffusion-webui/models/Stable-diffusion/{os.getenv('MODEL_NAME')}")
os.system(f"wget -q {os.getenv('VAE_LINK')} -O /home/user/app/stable-diffusion-webui/models/Stable-diffusion/{os.getenv('VAE_NAME')}")
os.system(f"wget -q {os.getenv('YAML_LINK')} -O /home/user/app/stable-diffusion-webui/models/Stable-diffusion/{os.getenv('YAML_NAME')}")

#CPU
#os.system(f"python launch.py --disable-console-progressbars --enable-console-prompts --ui-config-file /home/user/app/ui-config.json --ui-settings-file /home/user/app/config.json --no-progressbar-hiding --api --cors-allow-origins=* --api-auth={os.getenv('API_AUTH')} --use-cpu all --precision full --no-half --skip-torch-cuda-test")

#GPU
os.system(f"python launch.py --force-enable-xformers --disable-console-progressbars --enable-console-prompts --ui-config-file /home/user/app/ui-config.json --ui-settings-file /home/user/app/config.json --no-progressbar-hiding --api --cors-allow-origins=* --api-auth={os.getenv('API_AUTH')}")
