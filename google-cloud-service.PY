import os
import io
from google.cloud import speech
import pyaudio

# إدخال مسار ملف الشهادة JSON الخاص بمفتاح API
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dawd1.json"

# إعداد العميل
client = speech.SpeechClient()

# إعداد الميكروفون للتسجيل
RATE = 16000
CHUNK = int(RATE / 1)  # 100ms

def record_audio():
    """تسجيل الصوت من الميكروفون."""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
    
    print("ابدأ بالتحدث...")

    while True:
        data = stream.read(CHUNK)
        yield data

def transcribe_streaming():
    """إرسال البيانات الصوتية وتحويلها إلى نص في الوقت الفعلي."""
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="ar-SA"  # يمكنك تخصيص اللهجة هنا (مثلاً ar-EG للهجة المصرية)
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config)

    # تدفق الصوت إلى Google API
    requests = (speech.StreamingRecognizeRequest(audio_content=content) for content in record_audio())

    responses = client.streaming_recognize(streaming_config, requests)

    try:
        for response in responses:
            for result in response.results:
                print(f"لقد قلت: {result.alternatives[0].transcript}")
    except KeyboardInterrupt:
        print("تم إيقاف البرنامج")

# تنفيذ الدالة لبدء تحويل الكلام إلى نص
transcribe_streaming()
