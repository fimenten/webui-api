# Dockerfile.Lite

# https://gitlab.com/nvidia/container-images/cuda/-/blob/master/dist/11.7.1/ubuntu2204/devel/cudnn8/Dockerfile
# FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu22.04
# https://gitlab.com/nvidia/container-images/cuda/-/blob/master/dist/11.7.1/ubuntu2204/base/Dockerfile
FROM nvidia/cuda:11.7.1-base-ubuntu22.04
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y libgl1 libglib2.0-0 wget git git-lfs python3-pip python-is-python3 && rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos '' user
RUN mkdir /content && chown -R user:user /content
WORKDIR /content
USER user

RUN pip3 install --upgrade pip
RUN pip install xformers==0.0.16 triton==2.0.0 -U
RUN pip install numexpr

RUN git clone -b v2.2 https://github.com/camenduru/stable-diffusion-webui
RUN cd stable-diffusion-webui && git reset --hard

RUN sed -i -e 's/    start()/    #start()/g' /content/stable-diffusion-webui/launch.py
# RUN sed -i 's/^\( \{4\}\)start\(\)/\1#start\(\)/g' /content/stable-diffusion-webui/launch.py
# RUN sed -i -e 's/    \bstart\(\)\b/    \#start\(\)\b/g' /content/stable-diffusion-webui/launch.py

RUN sed -i -e '/(txt2img_interface, \"txt2img\", \"txt2img\"),/d' /content/stable-diffusion-webui/modules/ui.py
RUN sed -i -e '/(img2img_interface, \"img2img\", \"img2img\"),/d' /content/stable-diffusion-webui/modules/ui.py
RUN sed -i -e '/(extras_interface, \"Extras\", \"extras\"),/d' /content/stable-diffusion-webui/modules/ui.py
RUN sed -i -e '/(pnginfo_interface, \"PNG Info\", \"pnginfo\"),/d' /content/stable-diffusion-webui/modules/ui.py
RUN sed -i -e '/(modelmerger_interface, \"Checkpoint Merger\", \"modelmerger\"),/d' /content/stable-diffusion-webui/modules/ui.py
RUN sed -i -e '/(train_interface, \"Train\", \"ti\"),/d' /content/stable-diffusion-webui/modules/ui.py
RUN sed -i -e '/extensions_interface, \"Extensions\", \"extensions\"/d' /content/stable-diffusion-webui/modules/ui.py
RUN sed -i -e '/settings_interface, \"Settings\", \"settings\"/d' /content/stable-diffusion-webui/modules/ui.py

RUN cd stable-diffusion-webui && python launch.py --no-half --use-cpu all --skip-torch-cuda-test

COPY --chown=user config.json /content/config.json
COPY --chown=user ui-config.json /content/ui-config.json

ADD --chown=user https://huggingface.co/ckpt/sd15/resolve/main/v1-5-pruned-emaonly.ckpt /content/stable-diffusion-webui/models/Stable-diffusion/v1-5-pruned-emaonly.ckpt
ADD --chown=user https://huggingface.co/ckpt/anything-v4.5-vae-swapped/resolve/main/anything-v4.5-vae-swapped.safetensors /content/stable-diffusion-webui/models/Stable-diffusion/anything-v4.5-vae-swapped.safetensors

# EXPOSE 7860

# CMD python -m http.server 7860
# /bin/sh: 1: Syntax error: "(" unexpected
# --api-auth={os.getenv('API_AUTH')} 
# --nowebui
CMD cd /content/stable-diffusion-webui && python webui.py --xformers --listen --enable-insecure-extension-access --gradio-queue --api --cors-allow-origins=* --ui-config-file /content/ui-config.json --ui-settings-file /content/config.json --api-auth=$API_AUTH