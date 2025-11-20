
from pathlib import Path
import argparse
import json
import math
import random
import tempfile
import shutil

import numpy as np
import pandas as pd
import cv2

# optional: ultralytics may not be present in every env; import when used
from ultralytics import YOLO

# -------------------- Utilities --------------------

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def set_seed(seed: int = 23):
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
    except Exception:
        pass


# robustness config & samplers 
# Compact, parameterized priors for augmentation sampling
ROBUST_PRIORS = {
    "noise_sigma": ("lognormal", {"mu": math.log(2.0), "sigma": 0.6}),
    "motion_length": ("lognormal", {"mu": math.log(3.0), "sigma": 0.6}),
    "gauss_k": ("discrete_uniform_odd", {"low": 1, "high": 11}),
    "jpeg_q": ("beta_scaled", {"a": 2.0, "b": 5.0, "low": 10, "high": 95}),
    "brightness_shift": ("normal", {"loc": 0.0, "scale": 20.0}),
    "contrast_scale": ("lognormal", {"mu": math.log(1.0), "sigma": 0.15}),
    "occl_rel_size": ("beta_scaled", {"a": 1.5, "b": 3.0, "low": 0.02, "high": 0.25}),
    "affine_angle": ("normal", {"loc": 0.0, "scale": 2.0}),
    "affine_scale": ("normal", {"loc": 1.0, "scale": 0.03}),
}


def level_multiplier(level: float) -> float:
    # mapping level [0..1] to variance multiplier
    return 1.0 + 3.0 * float(np.clip(level, 0.0, 1.0))


def sample_from_prior(name: str, level: float):
    dist, params = ROBUST_PRIORS[name]
    mult = level_multiplier(level)
    if dist == "lognormal":
        mu, sigma = params["mu"], params["sigma"] * math.sqrt(mult)
        return float(np.random.lognormal(mean=mu, sigma=sigma))
    if dist == "normal":
        loc, scale = params["loc"], params["scale"] * math.sqrt(mult)
        return float(np.random.normal(loc, scale))
    if dist == "discrete_uniform_odd":
        low, high = params["low"], params["high"]
        val = int(np.random.randint(low, high + 1))
        if val % 2 == 0:
            val += 1
        return max(1, val)
    if dist == "beta_scaled":
        a, b, low, high = params["a"], params["b"], params["low"], params["high"]
        a2 = a * (1.0 + level)
        b2 = b
        s = np.random.beta(a2, b2)
        return float(low + s * (high - low))
    # fallback
    return float(np.random.rand())


# - Basic image ops --

def motion_blur(img: np.ndarray, length: float, angle: float) -> np.ndarray:
    k = max(1, int(round(length)))
    k = k if k % 2 == 1 else k + 1
    kernel = np.zeros((k, k), dtype=np.float32)
    center = k // 2
    sin_a = math.sin(math.radians(angle))
    cos_a = math.cos(math.radians(angle))
    for i in range(k):
        offset = i - center
        x = int(center + offset * cos_a)
        y = int(center + offset * sin_a)
        if 0 <= x < k and 0 <= y < k:
            kernel[y, x] = 1.0
    s = kernel.sum()
    if s != 0:
        kernel /= s
    return cv2.filter2D(img, -1, kernel)



def apply_distortions_v2(img: np.ndarray, level: float = 0.0, record: dict = None) -> (np.ndarray, dict):
    """Apply a sequence of sampled distortions controlled by level in [0,1].
    Returns (out_img, record_of_params).
    """
    if record is None:
        record = {}
    out = img.copy()
    h, w = out.shape[:2]

    # probability modifiers for operations (simple mapping)
    def p(base):
        lam = 1.0 + 2.5 * level
        pval = 1.0 - math.exp(-base * lam)
        return float(np.clip(pval * np.random.uniform(0.95, 1.05), 0.0, 1.0))

    # gaussian noise
    if np.random.rand() < p(0.6):
        sigma = sample_from_prior("noise_sigma", level)
        record["gauss_sigma"] = float(sigma)
        noise = np.random.normal(0, sigma, out.shape).astype(np.float32)
        out = np.clip(out.astype(np.float32) + noise, 0, 255).astype(np.uint8)

    # gaussian blur
    if np.random.rand() < p(0.5):
        k = int(sample_from_prior("gauss_k", level))
        if k % 2 == 0:
            k += 1
        record["gauss_k"] = int(k)
        out = cv2.GaussianBlur(out, (k, k), 0)

    # motion blur
    if np.random.rand() < p(0.35):
        length = sample_from_prior("motion_length", level)
        angle = sample_from_prior("affine_angle", level)
        record["motion_length"] = float(length)
        record["motion_angle"] = float(angle)
        out = motion_blur(out, length, angle)

    # jpeg compression
    if np.random.rand() < p(0.3):
        q = int(sample_from_prior("jpeg_q", level))
        q = max(1, min(100, q))
        record["jpeg_q"] = int(q)
        _, enc = cv2.imencode('.jpg', out, [int(cv2.IMWRITE_JPEG_QUALITY), q])
        out = cv2.imdecode(enc, cv2.IMREAD_COLOR)

    # brightness & contrast
    if np.random.rand() < p(0.75):
        alpha = float(sample_from_prior("contrast_scale", level))
        beta = float(sample_from_prior("brightness_shift", level))
        record["alpha"] = alpha
        record["beta"] = beta
        out = cv2.convertScaleAbs(out, alpha=alpha, beta=beta)

    # occlusion
    if np.random.rand() < p(0.5):
        n_boxes = np.random.randint(1, 1 + max(1, int(round(level * 4))))
        record["n_occl"] = int(n_boxes)
        for _ in range(n_boxes):
            rel = sample_from_prior("occl_rel_size", level)
            bw = int(rel * w)
            bh = int(rel * h)
            if bw < 1 or bh < 1:
                continue
            x1 = np.random.randint(0, max(1, w - bw + 1))
            y1 = np.random.randint(0, max(1, h - bh + 1))
            if np.random.rand() < 0.5:
                cv2.rectangle(out, (x1, y1), (x1 + bw, y1 + bh), (0, 0, 0), -1)
            else:
                sx = np.random.randint(0, max(1, w - bw + 1))
                sy = np.random.randint(0, max(1, h - bh + 1))
                patch = out[sy:sy+bh, sx:sx+bw].copy()
                if patch.shape[0] != bh or patch.shape[1] != bw:
                    patch = cv2.resize(patch, (bw, bh))
                out[y1:y1+bh, x1:x1+bw] = patch

    # small affine
    if np.random.rand() < p(0.4):
        angle = float(sample_from_prior("affine_angle", level))
        scale = float(sample_from_prior("affine_scale", level))
        record["affine_angle"] = angle
        record["affine_scale"] = scale
        M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, scale)
        out = cv2.warpAffine(out, M, (w, h), borderMode=cv2.BORDER_REFLECT)

    return out, record


# File-system helpers

def transform_folder_with_distortions(src_dir: Path, dst_dir: Path, level: float):
    ensure_dir(dst_dir)
    exts = {".jpg", ".jpeg", ".png", ".bmp"}
    for p in src_dir.iterdir():
        if not p.is_file() or p.suffix.lower() not in exts:
            continue
        img = cv2.imread(str(p))
        if img is None:
            continue
        out, _ = apply_distortions_v2(img, level=level)
        cv2.imwrite(str(dst_dir / p.name), out)


# Commands

def command_train(args):
    set_seed(args.seed)
    model = YOLO(args.model)
    exp_name = args.name or f"agropest_{Path(args.model).stem}"

    print(f"Training -> project={args.project}, name={exp_name}, data={args.data}")

    model.train(
        data=args.data,
        imgsz=args.imgsz,
        epochs=args.epochs,
        batch=args.batch,
        name=exp_name,
        project=args.project,
        device=args.device,
        lr0=args.lr0,
        patience=args.patience,
        augment=True,
        mosaic=args.mosaic,
        mixup=args.mixup,
        hsv_h=args.hsv_h,
        hsv_s=args.hsv_s,
        hsv_v=args.hsv_v,
        degrees=args.degrees,
        translate=args.translate,
        scale=args.scale,
        shear=args.shear,
        fliplr=args.fliplr,
        flipud=args.flipud,
        workers=args.workers,
    )

    best_path = Path(args.project) / (args.name or exp_name) / 'weights' / 'best.pt'
    print(f"[OK] Training finished. Best weights expected at: {best_path}")

    cfg_path = Path(args.project) / (args.name or exp_name) / 'train_config.json'
    ensure_dir(cfg_path.parent)
    # Filter out non-serializable objects (like function 'func')
    config_dict = {k: v for k, v in vars(args).items() if not callable(v)}
    cfg_path.write_text(json.dumps(config_dict, indent=2))
    print(f"[OK] config saved to {cfg_path}")


def command_val(args):
    model = YOLO(args.weights)
    res = model.val(data=args.data, split=args.split, save_json=True, project=args.project, name=args.name)
    d = dict(res.results_dict)
    out_dir = Path(args.out_directory)
    ensure_dir(out_dir)
    (out_dir / f"{args.name or 'val'}.json").write_text(json.dumps(d, indent=2))
    pd.DataFrame([d]).to_csv(out_dir / f"{args.name or 'val'}.csv", index=False)
    print(f"[OK] val results saved to {out_dir}")


def command_predict(args):
    model = YOLO(args.weights)
    model.predict(source=args.source, imgsz=args.imgsz, conf=args.conf, save=True, project=args.project, name=args.name, device=args.device)
    print(f"[OK] predictions saved under {Path(args.project)/args.name}")


def command_summarize(args):
    p = Path(args.metrics_dir)
    files = list(p.glob('*.json'))
    box = []
    for f in files:
        try:
            d = json.loads(f.read_text(encoding='utf-8'))
            d['run'] = f.stem
            box.append(d)
        except Exception as e:
            print(f"skip {f}: {e}")
    if not box:
        print("[WARN] no metrics found")
        return
    df = pd.DataFrame(box)
    cols = ['run'] + [c for c in df.columns if any(k in c.lower() for k in ['map', 'precision', 'recall', 'f1'])]
    df[cols].to_csv(args.out, index=False)
    print(f"[OK] summary written to {args.out}")


def command_robust(args):
    model = YOLO(args.weights)
    base_yaml = Path(args.data).read_text(encoding='utf-8')

    # load YAML lazily to avoid adding PyYAML dependency here; ultralytics expects path or dict
    import yaml
    base = yaml.safe_load(base_yaml)
    test_path = base.get('test')
    if not test_path:
        raise ValueError('data.yaml must contain `test` key pointing to image directory')

    root = Path(base.get('path') or '.').resolve()
    test_dir = Path(test_path) if Path(test_path).is_absolute() else (root / test_path).resolve()
    ensure_dir(Path(args.out_directory))

    records = []
    for level in args.levels:
        with tempfile.TemporaryDirectory() as td:
            dst = Path(td) / 'images'
            transform_folder_with_distortions(test_dir, dst, level=float(level))

            tmp_yaml = dict(base)
            tmp_yaml['test'] = str(dst)
            tmp_yaml_path = Path(td) / 'tmp_data.yaml'
            tmp_yaml_path.write_text(yaml.safe_dump(tmp_yaml))

            res = model.val(data=str(tmp_yaml_path), split='test', save_json=False, project=args.project, name=f'robust_{level}', imgsz=args.imgsz)
            d = dict(res.results_dict)
            d.update({'level': float(level)})
            records.append(d)
            key = next((k for k in d.keys() if 'map' in k.lower()), None)
            if key:
                print(f"[robust] level={level} {key}={d.get(key):.4f}")
            else:
                print(f"[robust] level={level} -> {d}")

    df = pd.DataFrame(records)
    out_csv = Path(args.out_directory) / 'robustness_summary.csv'
    df.to_csv(out_csv, index=False)
    print(f"[OK] robustness summary: {out_csv}")



def build_parser():
    p = argparse.ArgumentParser(description='YOLOv8 pipeline (精简版)')
    sub = p.add_subparsers(dest='cmd', required=True)

    # train
    t = sub.add_parser('train')
    t.add_argument('--data', required=True)
    t.add_argument('--model', default='./yolov8n.pt')
    t.add_argument('--imgsz', type=int, default=640)
    t.add_argument('--epochs', type=int, default=150)
    t.add_argument('--batch', type=int, default=16)
    t.add_argument('--name', default=None)
    t.add_argument('--project', default='runs')
    t.add_argument('--device', default=None)
    t.add_argument('--lr0', type=float, default=0.01)
    t.add_argument('--patience', type=int, default=30)
    t.add_argument('--seed', type=int, default=23)
    t.add_argument('--mosaic', type=float, default=1.0)
    t.add_argument('--mixup', type=float, default=0.0)
    t.add_argument('--hsv_h', type=float, default=0.015)
    t.add_argument('--hsv_s', type=float, default=0.7)
    t.add_argument('--hsv_v', type=float, default=0.4)
    t.add_argument('--degrees', type=float, default=0.0)
    t.add_argument('--translate', type=float, default=0.1)
    t.add_argument('--scale', type=float, default=0.5)
    t.add_argument('--shear', type=float, default=0.0)
    t.add_argument('--fliplr', type=float, default=0.5)
    t.add_argument('--flipud', type=float, default=0.0)
    t.add_argument('--workers', type=int, default=4, help='Number of dataloader workers (reduce if memory error)')
    t.set_defaults(func=command_train)

    # val
    v = sub.add_parser('val')
    v.add_argument('--weights', required=True)
    v.add_argument('--data', required=True)
    v.add_argument('--split', default='val', choices=['val', 'test'])
    v.add_argument('--project', default='runs')
    v.add_argument('--name', default='val')
    v.add_argument('--out_directory', default='runs/model_result')
    v.set_defaults(func=command_val)

    # predict
    pr = sub.add_parser('predict')
    pr.add_argument('--weights', required=True)
    pr.add_argument('--source', required=True)
    pr.add_argument('--imgsz', type=int, default=640)
    pr.add_argument('--conf', type=float, default=0.25)
    pr.add_argument('--device', default=None)
    pr.add_argument('--project', default='runs')
    pr.add_argument('--name', default='predict')
    pr.set_defaults(func=command_predict)

    # summarize
    s = sub.add_parser('summarize')
    s.add_argument('--metrics-dir', default='runs/model_result')
    s.add_argument('--out', default='runs/metrics_summary.csv')
    s.set_defaults(func=command_summarize)

    # robust
    r = sub.add_parser('robust')
    r.add_argument('--weights', required=True)
    r.add_argument('--data', required=True)
    r.add_argument('--imgsz', type=int, default=640)
    r.add_argument('--project', default='runs')
    r.add_argument('--out_directory', default='runs')
    r.add_argument('--levels', nargs='+', type=float, default=[0.0, 0.3, 0.6])
    r.set_defaults(func=command_robust)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
