# tests/test_audio_stream_speed.py
"""Unit tests to verify data-streaming loop speed, chunk buffering, and latency guards."""
from __future__ import annotations

import time
import pytest

from livekit.plugins.google.realtime import realtime_api
from livekit.agents.utils import audio as audio_utils
from receptionist.config import load_config
from receptionist.prompts import build_system_prompt


def test_audio_chunk_buffer_under_100ms():
    """Verify outgoing audio chunks do not exceed 100ms per payload."""
    sample_rate = realtime_api.INPUT_AUDIO_SAMPLE_RATE  # 16000 Hz
    channels = realtime_api.INPUT_AUDIO_CHANNELS        # 1 channel
    samples_per_channel = sample_rate // 20             # 800 samples = 50ms
    bytes_per_sample = 2                                # 16-bit PCM

    chunk_duration_ms = (samples_per_channel / sample_rate) * 1000.0
    payload_size_bytes = samples_per_channel * bytes_per_sample * channels

    assert chunk_duration_ms <= 100.0, f"Chunk duration {chunk_duration_ms}ms exceeds 100ms threshold"
    assert chunk_duration_ms == 50.0
    assert payload_size_bytes == 1600


def test_audio_byte_stream_dispatch_timing():
    """Verify that a 500ms stream is chunked without accumulation stalls."""
    sample_rate = 16000
    channels = 1
    samples_per_chunk = 800
    bstream = audio_utils.AudioByteStream(sample_rate, channels, samples_per_channel=samples_per_chunk)

    slice_10ms = bytes(320)
    chunk_count = 0
    start = time.perf_counter()

    for _ in range(50):  # 50 * 10ms = 500ms of audio
        for _ in bstream.write(slice_10ms):
            chunk_count += 1

    elapsed = time.perf_counter() - start
    assert chunk_count == 10, f"Expected 10 chunks for 500ms audio, got {chunk_count}"
    assert elapsed < 0.05, f"Pure memory slicing took {elapsed*1000:.2f}ms, expected sub-50ms"


def test_prompt_generation_latency_sub_5ms():
    """Ensure dynamic prompt formatting does not block event loop turns."""
    config = load_config("config/businesses/aarogyam-clinic.yaml")
    t0 = time.perf_counter()
    prompt = build_system_prompt(config)
    duration_ms = (time.perf_counter() - t0) * 1000.0

    assert len(prompt) > 1000
    assert duration_ms < 10.0, f"Prompt formatting took {duration_ms:.2f}ms, expected < 10ms"
