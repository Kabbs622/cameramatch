# C41 Cinema: Full Local AI Stack
Zero cloud subscriptions. Everything on your hardware. One interface (OpenClaw on Discord).

---

## THE STACK

### Brain (LLM / Code / Writing)
Ollama runs the models. OpenClaw is the interface. You talk to me on Discord, I route to the right model.

- **Qwen3-Coder-Next** — Daily driver. First local model people genuinely prefer over cloud. 256K context. Great at code, writing, reasoning, client work. Runs on 15GB VRAM + 30GB RAM.
- **Qwen3-235B-A22B** — Frontier reasoning. Competes with Claude Opus / GPT-5. For the hardest problems. Needs 70GB VRAM.
- **Qwen3-32B** — Fast mode. Quick tasks, summaries, emails. 24GB VRAM.
- **DeepSeek V3.1** — The absolute ceiling. 685B params. Needs 256GB+ VRAM. Only for the multi-GPU build.

### Eyes (Image Generation)
ComfyUI runs the pipeline. OpenClaw triggers it via custom skill.

The pro workflow (how practitioners actually work):
1. **Qwen-Image** — Composition and prompt adherence. Best text rendering. 13 sec/image with Nunchaku. (16-24GB)
2. **Wan 2.2 14B** (1-frame, low denoise) — Feed step 1 through this for photorealism. Skin, lighting, materials all improve dramatically. (16GB)
3. **SEEDVR2** — Upscale to 4K. (24-48GB)
4. **HiDream-E1.1** — Fix details with natural language. "Remove the watch. Change the background." (16-24GB)

For brand consistency: **Flux 2 Dev** — Feed up to 10 reference images. Maintains character/style without fine-tuning. (24GB at 4-bit)

### Motion (Video Generation)
ComfyUI runs Wan 2.2 workflows. OpenClaw triggers via custom skill.

- **Wan 2.2 14B** (i2v) — The model. Being used for real paid client work on single 4090s right now. 449-upvote Reddit post proving it. (24-48GB)
- **Wan 2.2 VACE** — Video editing: inpainting, outpainting, reference-based generation.
- **FramePack** — Long-form (1 min+). Constant VRAM regardless of length. (6GB minimum)
- **Speed-ups**: TeaCache (2x), Self-Forcing LoRAs, CFG-Zero*

### Talking (Lip-Synced Dialogue in Video)
This is the hard part you flagged. Here's what exists locally:

**Option 1: InfiniteTalk (Wan 2.2 + TTS)**
- 423-upvote workflow. ComfyUI pipeline: generate TTS audio, then use Wan 2.2 to animate a face speaking those words.
- Practitioner doing a full AI sci-fi film series with it (798-upvote post, "Stellarchive" on YouTube).
- Trade-off: About 1 in 10 generations has good enough lip sync. Cherry-picking required.
- Speed: ~33 seconds per 1 second of video on RTX 3090.

**Option 2: HuMo (ByteDance, 17B, just released)**
- 280-upvote post: "Looks way better than Wan S2V and InfiniteTalk, especially the facial emotion and actual lip movements fitting the speech."
- Open weights on HuggingFace. 68GB model.
- Kijai already building ComfyUI node.
- Best quality for the lip-sync problem specifically. Facial emotion matches speech.
- Trade-off: Very new, resource-heavy, currently limited to short clips (3-4 sec).

**Option 3: MultiTalk LoRA (for Wan 2.1/2.2)**
- 274-upvote production workflow: Full pipeline doing SeedVR2 upscale + VACE editing + Chatterbox TTS + MultiTalk LoRA. All in ComfyUI.
- The practitioner combined 7 different models in one pipeline and got convincing results.

**For the TTS voice itself** (making the dialogue sound human, not robotic):
- **IndexTTS2** — World-first emotion cloning. Provide a reference voice + an emotion reference. The most realistic local TTS.
- **Qwen3-TTS** — 97ms latency, OpenAI-compatible API, natural language voice direction ("say this nervously"). Easy to set up.
- **Chatterbox 2** — Lightweight, fast voice cloning from short samples. Good for quick turnaround.

**The realistic workflow:**
1. Write dialogue
2. Generate voice with IndexTTS2 or Qwen3-TTS (sounds human)
3. Generate/animate the talking head with HuMo or InfiniteTalk
4. Lip sync matches because the audio drives the animation
5. Composite into your video in post

### LoRA Training (The Commercial Moat)
- **musubi-tuner** — Train Wan 2.2 video LoRAs. 16GB VRAM, 3 hours for 250 images.
- **kohya-ss** — Train Flux/SDXL image LoRAs.
- **JoyCaption** — Auto-caption training images.

Train a client's brand character once, use it across ALL generation (image + video + talking head). No cloud service can do this.

---

## HOW OPENCLAW MANAGES IT

```
You (Discord)
    |
    v
OpenClaw (the brain)
    |
    +-- "Write me a proposal" --> Ollama (Qwen3-Coder-Next)
    +-- "Generate a product shot" --> ComfyUI (image pipeline)
    +-- "Make a 5-sec video of this" --> ComfyUI (Wan 2.2)
    +-- "Add dialogue to this clip" --> Qwen3-TTS + HuMo/InfiniteTalk
    +-- "Analyze this image" --> Ollama (Qwen2.5-VL)
    +-- Everything else --> Built-in tools (files, browser, web, etc.)
```

One chat. No switching apps. I route to the right tool.

**Already built into OpenClaw:**
- Ollama integration (auto-discovers models)
- TTS (points at local Qwen3-TTS server via OpenAI-compatible config)
- Discord, file management, browser, exec, web, cron, memory

**What I build as custom Skills:**
- ComfyUI image generation skill
- ComfyUI video generation skill
- ComfyUI lip-sync/dialogue skill

---

## HARDWARE

### The Pitch Build: $15-20K (No Compromises)

This is what the $17K Reddit build looks like (real, working, 950 upvotes):
- **8x RTX 3090 + 2x RTX 5090** = 256GB+ total VRAM
- Threadripper Pro 3995WX, 512GB DDR4
- Thermaltake Core W200 case
- Dual PSU (1600W + 1300W)
- Actual power draw under load: ~1,700W (each 3090 only pulls ~150W during inference)

What it runs:
- DeepSeek V3.1 at 25 tok/s
- Qwen3-235B at 31.5 tok/s
- Wan 2.2 video at full quality
- 4K upscaling
- Everything simultaneously

### Alternative: $6-10K (Production-Ready)

- **4x RTX 3090** (96GB total) — $3,200 for GPUs (used market)
- Threadripper, 256GB RAM
- Runs: Qwen3-235B (Q3), Wan 2.2 full quality, image pipeline, TTS
- Trade-off: Can't run DeepSeek V3.1 or do 4K upscaling at the same time as LLM

### Starter: $3-5K (Prove the Concept)

- **RTX 5090 32GB** or **RTX 4090 24GB**
- 64GB RAM
- Runs: Qwen3-Coder-Next, Wan 2.2 (GGUF), Qwen-Image, TTS
- Trade-off: One task at a time, model swapping

### The ROI Pitch

One-time hardware: $15-20K

Replaces monthly:
- Claude/ChatGPT Pro: $100-200/mo
- Runway Gen-4.5: $28-76/mo
- Midjourney: $10-60/mo
- ElevenLabs: $5-99/mo
- Suno: $10-30/mo
- Stock footage/images: $50-200/mo
- Total replaced: **$200-665/mo**

Break-even: **2-6 years** at low end, **8-14 months** at high end usage.

Plus capabilities cloud CAN'T offer:
- Custom LoRAs (brand consistency across campaigns)
- Unlimited generation (no credits, no rate limits)
- Client data never leaves your machine
- Full creative control over every parameter
- Train on client assets without uploading to third parties

---

## WHAT WE DO NOW

1. I write the pitch document for your father
2. I build the OpenClaw skills (ComfyUI integration, ready to deploy)
3. I design the ComfyUI workflow presets
4. When hardware arrives: plug in, install, go
