"""
频域图像水印工具 v2 —— DCT 版
==========================
用 DCT（离散余弦变换）替代 FFT，避免相位问题和吉布斯振荡。

原理：
  嵌入：宿主图分块 DCT → 中频系数嵌入水印(±alpha) → IDCT
  提取：原图与含水印图分块 DCT 相减 → 判断正负 → 恢复水印

特点：
  - 无可见波纹/环状噪声
  - 水印提取清晰可辨
  - 支持中英文任意文本

依赖：pip install numpy pillow matplotlib scipy
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from scipy.fft import dct, idct

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# ============================================================
# 全局默认参数
# ============================================================

DEFAULT_BLOCK_SIZE = 8      # DCT 块大小（越小水印越清晰，2=256²网格；鲁棒需抗压缩可改为 4/8）
DEFAULT_ALPHA = 16.0        # 嵌入强度（越大越鲁棒但也越可见，推荐 8~20）
DEFAULT_WATERMARK_TEXT = "仅限董超用作\n更换经纪人"


# ============================================================
# 1. DCT 工具
# ============================================================

def dct2(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')


def idct2(block):
    return idct(idct(block.T, norm='ortho').T, norm='ortho')


# ============================================================
# 2. 文本 → 二值水印图
# ============================================================

def text_to_watermark(text, size=(512, 512), font_size=48):
    """将文本渲染为二值图 (0/1)；自动放大字号使文字填满约 85% 宽度，
    以便在低分辨率块网格下仍清晰可辨。"""
    fpath = None
    for fname in ["C:/Windows/Fonts/msyh.ttc",
                  "C:/Windows/Fonts/simhei.ttf",
                  "C:/Windows/Fonts/simsun.ttc"]:
        if os.path.exists(fname):
            fpath = fname
            break

    def _load(fs):
        return ImageFont.truetype(fpath, fs) if fpath else ImageFont.load_default()

    img = Image.new("L", size, 0)
    draw = ImageDraw.Draw(img)

    # 自动适配字号：让文字宽度接近画布 85%
    font = _load(font_size)
    if fpath:
        target_w = size[0] * 0.85
        fs = font_size
        for _ in range(20):
            bbox = draw.textbbox((0, 0), text, font=_load(fs))
            tw = bbox[2] - bbox[0]
            if tw >= target_w or fs >= size[1] // 2:
                break
            fs += 4
        font = _load(fs)

    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size[0] - tw) // 2 - bbox[0]
    y = (size[1] - th) // 2 - bbox[1]
    draw.text((x, y), text, fill=255, font=font)

    return np.array(img, dtype=np.float64) / 255.0


# ============================================================
# 3. 分块 DCT 嵌入 + 提取
# ============================================================

# 嵌入用的多个中频系数位置（随块大小自适应，避开 DC/低频与最高频）。
# 用多个系数同时编码并在提取时平均，可大幅提升信噪比、抑制单系数周期纹理。
def _embed_coeffs(bs):
    if bs >= 8:
        return [(2, 3), (3, 2), (3, 3), (4, 2), (2, 4)]
    if bs == 4:
        return [(1, 2), (2, 1), (2, 2), (1, 3), (3, 1)]
    c = max(1, bs // 2)
    return [(c, c)]


def _watermark_to_grid(watermark, grid_shape):
    """
    将任意分辨率的二值水印降采样到“块网格”分辨率 (Hb, Wb)。
    每个网格像素对应一个 DCT 块，1:1 编码，避免细笔画在块内被淹没。
    """
    Hb, Wb = grid_shape
    img = Image.fromarray((np.clip(watermark, 0, 1) * 255).astype(np.uint8))
    # 用 LANCZOS 下采样保留笔画灰度，再阈值二值化
    img = img.resize((Wb, Hb), Image.LANCZOS)
    grid = np.array(img, dtype=np.float64) / 255.0
    return (grid > 0.35).astype(np.float64)


def embed_watermark(host, watermark, alpha=DEFAULT_ALPHA, block_size=DEFAULT_BLOCK_SIZE):
    """
    分块 DCT 嵌入：水印与块网格 1:1 对齐，仅在“白块”叠加 +alpha。
    block_size 越小网格分辨率越高（文字越清晰、边缘越平滑），推荐 2。
    若需抗 JPEG 压缩等强鲁棒性，可改用 4 或 8。
    host:     [0,255] 灰度图
    alpha:    越大越鲁棒但也越可见（推荐 8~20）
    返回:     [0,255] uint8 含水印图
    """
    host = host.astype(np.float64)
    H, W = host.shape
    bs = block_size
    Hb, Wb = H // bs, W // bs
    coeffs = _embed_coeffs(bs)

    wm_grid = _watermark_to_grid(watermark, (Hb, Wb))

    out = host.copy()
    for bi in range(Hb):
        for bj in range(Wb):
            if wm_grid[bi, bj] <= 0.5:
                continue  # 黑块不动 → 差值图只在文字处出现，真正“隐形”
            i, j = bi * bs, bj * bs
            dct_block = dct2(host[i:i+bs, j:j+bs])
            for u, v in coeffs:
                dct_block[u, v] += alpha
            out[i:i+bs, j:j+bs] = idct2(dct_block)

    return np.clip(out, 0, 255).astype(np.uint8)


def extract_watermark(original, watermarked, block_size=DEFAULT_BLOCK_SIZE, alpha=DEFAULT_ALPHA):
    """
    分块 DCT 提取水印（非盲，需要原图辅助）。
    对多个中频系数差值取平均后阈值判断，输出与原图同尺寸的二值图。
    """
    orig = original.astype(np.float64)
    wmed = watermarked.astype(np.float64)
    H, W = orig.shape
    bs = block_size
    Hb, Wb = H // bs, W // bs
    coeffs = _embed_coeffs(bs)
    n = len(coeffs)
    thresh = alpha * 0.5

    grid = np.zeros((Hb, Wb), dtype=np.float64)
    for bi in range(Hb):
        for bj in range(Wb):
            i, j = bi * bs, bj * bs
            do = dct2(orig[i:i+bs, j:j+bs])
            dw = dct2(wmed[i:i+bs, j:j+bs])
            diff = sum(dw[u, v] - do[u, v] for u, v in coeffs) / n
            grid[bi, bj] = 1.0 if diff > thresh else 0.0

    # 网格放大回原尺寸（最近邻 → 边缘锐利、无糊化）
    full = np.array(
        Image.fromarray((grid * 255).astype(np.uint8)).resize((W, H), Image.NEAREST)
    )
    return full.astype(np.uint8)


# ============================================================
# 4. RGB 支持（嵌入到 Y 通道）
# ============================================================

def embed_watermark_rgb(host_rgb, text, alpha=DEFAULT_ALPHA, block_size=DEFAULT_BLOCK_SIZE, font_size=None):
    """RGB 图亮度通道嵌入水印"""
    host_rgb = _ensure_uint8(host_rgb)
    H, W = host_rgb.shape[:2]
    fs = font_size or max(28, min(W, H) // 10)

    wm = text_to_watermark(text, size=(max(W, 128), max(H, 128)), font_size=fs)
    wm = np.array(Image.fromarray((wm * 255).astype(np.uint8)).resize((W, H))) / 255.0

    ycbcr = rgb2ycbcr(host_rgb)
    Y = ycbcr[:, :, 0].astype(np.float64)
    Y_emb = embed_watermark(Y, wm, alpha=alpha, block_size=block_size)

    ycbcr[:, :, 0] = Y_emb
    return np.clip(ycbcr2rgb(ycbcr), 0, 255).astype(np.uint8)


def extract_watermark_rgb(original_rgb, watermarked_rgb, block_size=DEFAULT_BLOCK_SIZE, alpha=DEFAULT_ALPHA):
    """从 RGB 图提取水印"""
    orig_yc = rgb2ycbcr(_ensure_uint8(original_rgb)).astype(np.float64)
    wmed_yc = rgb2ycbcr(_ensure_uint8(watermarked_rgb)).astype(np.float64)

    return extract_watermark(orig_yc[:, :, 0], wmed_yc[:, :, 0],
                             block_size=block_size, alpha=alpha)


# ============================================================
# 5. 颜色空间转换
# ============================================================

def rgb2ycbcr(rgb):
    rgb = rgb.astype(np.float64)
    Y  =  0.299  * rgb[:, :, 0] + 0.587  * rgb[:, :, 1] + 0.114  * rgb[:, :, 2]
    Cb = -0.1687 * rgb[:, :, 0] - 0.3313 * rgb[:, :, 1] + 0.5    * rgb[:, :, 2] + 128
    Cr =  0.5    * rgb[:, :, 0] - 0.4187 * rgb[:, :, 1] - 0.0813 * rgb[:, :, 2] + 128
    return np.stack([Y, Cb, Cr], axis=-1).astype(np.uint8)


def ycbcr2rgb(ycbcr):
    y = ycbcr[:, :, 0].astype(np.float64)
    cb = ycbcr[:, :, 1].astype(np.float64) - 128
    cr = ycbcr[:, :, 2].astype(np.float64) - 128
    R = y + 1.402 * cr
    G = y - 0.34414 * cb - 0.71414 * cr
    B = y + 1.772 * cb
    return np.stack([R, G, B], axis=-1)


def _ensure_uint8(img):
    return np.clip(img, 0, 255).astype(np.uint8)


# ============================================================
# 6. 演示
# ============================================================

def demo(host_path=None, wm_text=DEFAULT_WATERMARK_TEXT, alpha=DEFAULT_ALPHA):
    print("=" * 60)
    print("  频域图像水印工具 v2  (DCT 版)")
    print("=" * 60)
    print(f"  水印: '{wm_text}'   强度: {alpha}")
    print()

    # 加载或生成宿主图
    if host_path and os.path.exists(host_path):
        host = np.array(Image.open(host_path).convert("RGB"))
    else:
        print("  (使用 512×512 测试图)")
        size = 512
        host = np.zeros((size, size, 3), dtype=np.uint8)
        host[:, :, 0] = np.linspace(0, 200, size).reshape(1, -1)
        host[:, :, 1] = np.linspace(200, 0, size).reshape(-1, 1)
        host[:, :, 2] = 180

    H, W = host.shape[:2]
    print(f"  图像尺寸: {W}×{H}")

    # 水印缩略图（展示用）
    wm_display = text_to_watermark(wm_text, size=(W, H), font_size=max(28, min(W, H) // 10))

    # 嵌入
    print("  嵌入水印中...")
    watermarked = embed_watermark_rgb(host, wm_text, alpha=alpha)

    # 提取
    print("  提取水印中...")
    extracted = extract_watermark_rgb(host, watermarked, alpha=alpha)

    # 准确率（与降采样后的真值网格比对）
    bs = DEFAULT_BLOCK_SIZE
    wm_grid = _watermark_to_grid(wm_display, (H // bs, W // bs))
    ext_grid = _watermark_to_grid(extracted / 255.0, (H // bs, W // bs))
    acc = (wm_grid == ext_grid).mean() * 100
    print(f"  提取准确率: {acc:.1f}%")

    # 可视化
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))

    axes[0, 0].set_title("宿主图")
    axes[0, 0].imshow(host)
    axes[0, 0].axis("off")

    axes[0, 1].set_title("原始水印")
    axes[0, 1].imshow(wm_display, cmap="gray")
    axes[0, 1].axis("off")

    axes[0, 2].set_title("含水印图 (不可见)")
    axes[0, 2].imshow(watermarked)
    axes[0, 2].axis("off")

    axes[1, 0].set_title("提取的水印")
    axes[1, 0].imshow(extracted, cmap="gray")
    axes[1, 0].axis("off")

    # 差值（放大 5×）
    diff = np.abs(host.astype(np.float64) - watermarked.astype(np.float64)).mean(axis=2)
    diff = np.clip(diff * 5, 0, 255)
    axes[1, 1].set_title("差值 (×5 放大)")
    axes[1, 1].imshow(diff, cmap="hot")
    axes[1, 1].axis("off")

    # 直方图
    axes[1, 2].set_title("像素差值分布")
    for ch, col in enumerate(["red", "green", "blue"]):
        ch_diff = np.abs(host[:, :, ch].astype(np.float64) - watermarked[:, :, ch].astype(np.float64)).ravel()
        axes[1, 2].hist(ch_diff, bins=50, color=col, alpha=0.4, label=f"{'RGB'[ch]}")
    axes[1, 2].legend(fontsize=8)
    axes[1, 2].set_xlabel("像素差值")

    fig.suptitle(f"DCT 频域水印  alpha={alpha}", fontsize=16)
    plt.tight_layout()
    plt.show()

    # 保存
    out_dir = os.path.dirname(os.path.abspath(__file__))
    save_image(watermarked, os.path.join(out_dir, "watermarked_v2.png"))
    save_image(extracted, os.path.join(out_dir, "extracted_v2.png"))
    print(f"\n  已保存: watermarked_v2.png, extracted_v2.png")
    print("=" * 60)


def save_image(arr, path):
    Image.fromarray(_ensure_uint8(arr)).save(path)

def run_interactive():
    """命令行交互模式"""
    import sys

    print("=" * 60)
    print("  频域图像水印工具 — 交互模式")
    print("=" * 60)

    path = input("宿主图路径 (回车=生成测试图): ").strip().strip('"')
    if path and not os.path.exists(path):
        print(f"文件不存在: {path}"); sys.exit(1)
    path = path if path else None

    text = input(f"水印文字 (回车='{DEFAULT_WATERMARK_TEXT}'): ").strip()
    if not text:
        text = DEFAULT_WATERMARK_TEXT

    alpha_str = input(f"嵌入强度 alpha (回车={DEFAULT_ALPHA:.0f}): ").strip()
    alpha = float(alpha_str) if alpha_str else DEFAULT_ALPHA

    demo(host_path=path, wm_text=text, alpha=alpha)


# ============================================================
# main
# ============================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == "demo":
            img = sys.argv[2] if len(sys.argv) > 2 else None
            txt = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_WATERMARK_TEXT
            a = float(sys.argv[4]) if len(sys.argv) > 4 else DEFAULT_ALPHA
            demo(host_path=img, wm_text=txt, alpha=a)
        elif arg == "interactive":
            run_interactive()
        else:
            print("用法: python frequency_watermark_v2.py demo [图片] [水印文字] [强度]")
    else:
        demo()
