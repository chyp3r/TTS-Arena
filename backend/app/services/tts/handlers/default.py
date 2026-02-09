import torch
import inspect
from transformers import (
    AutoModelForTextToWaveform,
    AutoModelForTextToSpectrogram,
    AutoModel,
    AutoProcessor,
    AutoTokenizer,
)
from services.tts.handlers.base import BaseHandler


class AutoTTSHandler(BaseHandler):
    def load_model(self, model_id: str, device: str):
        last_error = None

        for cls in (
            AutoModelForTextToWaveform,
            AutoModelForTextToSpectrogram,
            AutoModel,
        ):
            try:
                model = cls.from_pretrained(model_id)
                model.to(device)
                model.eval()
                return model
            except Exception as e:
                last_error = e

        raise RuntimeError(
            f"Model yuklenemedi: {model_id}\nSon hata: {last_error}"
        )

    def load_processor(self, model_id: str):
        try:
            return AutoProcessor.from_pretrained(model_id)
        except Exception:
            pass

        try:
            return AutoTokenizer.from_pretrained(model_id)
        except Exception:
            return None

    def infer(self, model, inputs=None, text=None, **kwargs):
        device = next(model.parameters()).device

        model_inputs = self._prepare_inputs(
            model=model,
            inputs=inputs,
            text=text,
            device=device,
            **kwargs,
        )

        with torch.no_grad():
            output = self._call_model(model, model_inputs, **kwargs)

        audio = self._extract_audio(output)

        if audio is None:
            raise RuntimeError("Model output'undan audio cikartilamadi")

        if isinstance(audio, torch.Tensor):
            audio = audio.detach().cpu().numpy().squeeze()

        sample_rate = self._get_sample_rate(model)
        return audio, sample_rate

    def _prepare_inputs(self, model, inputs, text, device, **kwargs):
        if isinstance(inputs, dict):
            model_inputs = {
                k: v.to(device) if isinstance(v, torch.Tensor) else v
                for k, v in inputs.items()
            }
        elif text is not None:
            processor = kwargs.get("processor")
            if processor:
                processed = processor(text, return_tensors="pt")
                model_inputs = {
                    k: v.to(device) if isinstance(v, torch.Tensor) else v
                    for k, v in processed.items()
                }
            else:
                if isinstance(text, torch.Tensor):
                    model_inputs = {"input_ids": text.to(device)}
                else:
                    model_inputs = {"text": text}
        else:
            raise ValueError("infer icin girdi yok")

        if (
            "attention_mask" in inspect.signature(model.forward).parameters
            and "attention_mask" not in model_inputs
            and "input_ids" in model_inputs
        ):
            model_inputs["attention_mask"] = torch.ones_like(
                model_inputs["input_ids"]
            )

        return model_inputs

    def _call_model(self, model, model_inputs, **kwargs):
        if hasattr(model, "generate"):
            try:
                sig = inspect.signature(model.generate)
                valid_kwargs = {
                    k: v for k, v in kwargs.items() if k in sig.parameters
                }
                return model.generate(**model_inputs, **valid_kwargs)
            except Exception:
                pass

        sig = inspect.signature(model.forward)
        valid_kwargs = {
            k: v for k, v in kwargs.items() if k in sig.parameters
        }
        return model(**model_inputs, **valid_kwargs)

    def _extract_audio(self, output):
        for attr in (
            "waveform",
            "audio",
            "audio_values",
            "audios",
            "logits",
        ):
            if hasattr(output, attr):
                return getattr(output, attr)

        if isinstance(output, dict):
            for key in (
                "waveform",
                "audio",
                "audio_values",
                "audios",
            ):
                if key in output:
                    return output[key]

        if isinstance(output, (tuple, list)) and len(output) > 0:
            return output[0]

        if isinstance(output, torch.Tensor):
            return output

        return None

    def _get_sample_rate(self, model):
        config = getattr(model, "config", None)
        if config:
            for key in ("sampling_rate", "sample_rate"):
                if hasattr(config, key):
                    return getattr(config, key)

        for key in ("sampling_rate", "sample_rate"):
            if hasattr(model, key):
                return getattr(model, key)

        return 24000
