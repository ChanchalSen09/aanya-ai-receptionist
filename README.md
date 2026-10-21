# Aanya — Multimodal AI Phone Receptionist & Voice Agent

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![LiveKit Agents](https://img.shields.io/badge/LiveKit-Agents%20SDK%201.8-FF6B35?style=flat-square&logo=webrtc&logoColor=white)](https://livekit.io/)
[![Google Gemini Live](https://img.shields.io/badge/Google%20Gemini-Live%20Multimodal%20API-4285F4?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev/)
[![OpenAI Realtime](https://img.shields.io/badge/OpenAI-Realtime%20API-412991?style=flat-square&logo=openai&logoColor=white)](https://platform.openai.com/)
[![Pydantic v2](https://img.shields.io/badge/Validation-Pydantic%20v2-E92063?style=flat-square&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Tests](https://img.shields.io/badge/Tests-672%20Passing-2EA44F?style=flat-square&logo=pytest&logoColor=white)](tests/)

**Aanya** is an enterprise-grade, real-time voice AI receptionist built for **customer desks, healthcare clinics, barbershops, and service businesses**. Operating directly over telephone networks (SIP/PSTN) and WebRTC, Aanya provides lifelike, low-latency (<500ms) speech-to-speech conversations with native multilingual code-switching (**Hindi, Indian English, and Hinglish**).

Powered by **Google Gemini Live Multimodal API** (`gemini-2.5-flash-native-audio`) and **OpenAI Realtime API** (`gpt-realtime-2.1`), she manages appointments, answers pricing and service questions, conducts structured caller intakes, and transfers calls to human staff.

---

## 🌟 Key Features

- **Dual Multimodal LLM Backends:** Built-in provider factory supporting both **Google Gemini Live API** (free-tier friendly, voice: `Aoede`) and **OpenAI Realtime API** (voice: `marin`), with automatic failover and rate-limit recovery.
- **Dynamic Multilingual Code-Switching:** Automatically detects and immediately adapts to the caller's spoken language in real-time. If the caller speaks Hindi or conversational Hinglish, Aanya immediately responds in fluent Hindi; if they switch to English, she responds in English.
- **Domain ASR Adaptation (`adaptation_phrases`):** Calibrates Google's speech recognition engine (`AudioTranscriptionConfigMode.SMART` with `hi-IN` and `en-IN` language codes) with business-specific vocabulary (doctor names, haircut styles, local landmarks) to eliminate phonetic mishearings.
- **Telephony & SIP Integration:** Answers standard mobile and landline calls via SIP trunks (Twilio / Telnyx) with background noise cancellation (`BVCTelephony`), DTMF keypad input, and SIP REFER transfers.
- **Calendar & Appointment Booking:** Real-time slot checking and booking via Google Calendar (localized to `Asia/Kolkata` IST), with race-condition prevention and email invites.
- **Smart FAQ Retrieval:** Bidirectional substring and token-overlap matcher that eliminates hallucinations by grounding answers strictly in configured business facts.
- **Multi-Tenant YAML Architecture:** Switch between completely different business verticals (clinics, salons, dental offices) simply by changing a single YAML configuration or room metadata tag.
- **670+ Automated Tests:** Comprehensive Pytest suite covering session lifecycles, silence-timeout watchdogs, recovery handlers, and tool contracts.

---

## 🏢 Pre-Configured Business Profiles

| Business Profile                  | File                                                                               | Vertical               | Key Capabilities                                                                                                                                       |
| --------------------------------- | ---------------------------------------------------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Aarogyam Clinic & Diagnostics** | [`config/businesses/aarogyam-clinic.yaml`](config/businesses/aarogyam-clinic.yaml) | Healthcare Clinic      | Doctor consultation timings (4 specialists), ₹500/₹800 consultation fees, diagnostic lab tests, fasting instructions, and free home sample collection. |
| **The Man Salon & Barbershop**    | [`config/businesses/man-salon.yaml`](config/businesses/man-salon.yaml)             | Men's Salon & Grooming | Haircuts (Classic ₹350, Fade ₹500), Royal Shaves (₹400), beard shaping, charcoal detan facials, head massages, and stylist bookings (Rahul, Imran).    |
| **Acme Dental**                   | [`config/businesses/example-dental.yaml`](config/businesses/example-dental.yaml)   | Dental Practice        | Dental cleaning, root canal consultations, emergency triage, and front-desk transfers.                                                                 |

---

## 🏗️ Architecture

```
[ PSTN Phone Caller ]
         │
         ▼ SIP
[ SIP Trunk (Twilio / Telnyx) ]
         │
         ▼ SIP URI
[ LiveKit Cloud / Self-Hosted Gateway ]
         │
         ▼ WebRTC Full-Duplex Audio (<500ms)
[ Python Agent Worker (LiveKit Agents SDK 1.8) ]
   ├── Google Gemini Live API / OpenAI Realtime (Speech-to-Speech)
   ├── Domain ASR Adaptation Engine (hi-IN / en-IN / en-US)
   ├── Token-Overlap FAQ Grounding Matcher
   └── Autonomous Tool Dispatcher
         ├── Google Calendar API (IST Appointment Scheduling)
         ├── LiveKit SIP Transfer (Front Desk / Staff Routing)
         ├── DTMF Keypad Decoder (Caller PIN / Case Intake)
         └── Email & Webhook Dispatcher (SMTP / Resend / Disk)
```

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
