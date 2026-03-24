// Voice drug input using Web Speech API.
// Falls back gracefully if SpeechRecognition is not supported.

import { useState, useRef, useCallback, useEffect } from "react";
import { Mic, MicOff } from "lucide-react";
import { useTranslation } from "react-i18next";
import { Button } from "@/components/ui/button";

interface VoiceInputProps {
  onResult: (text: string) => void;
  disabled?: boolean;
}

// Browser SpeechRecognition API (prefixed in some browsers)
const SpeechRecognitionAPI =
  typeof window !== "undefined"
    ? window.SpeechRecognition ?? (window as unknown as Record<string, unknown>).webkitSpeechRecognition
    : null;

const isSupported = SpeechRecognitionAPI != null;

export function VoiceInput({ onResult, disabled = false }: VoiceInputProps) {
  const { t } = useTranslation();
  const [isRecording, setIsRecording] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const recognitionRef = useRef<InstanceType<typeof SpeechRecognition> | null>(null);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      recognitionRef.current?.abort();
    };
  }, []);

  const startRecording = useCallback(() => {
    if (!isSupported || disabled) return;

    setErrorMsg(null);
    const recognition = new (SpeechRecognitionAPI as typeof SpeechRecognition)();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => setIsRecording(true);

    recognition.onresult = (event: SpeechRecognitionEvent) => {
      const transcript = event.results[0]?.[0]?.transcript ?? "";
      if (transcript.trim()) {
        onResult(transcript.trim());
      }
    };

    recognition.onerror = (event: SpeechRecognitionErrorEvent) => {
      if (event.error === "not-allowed") {
        setErrorMsg(t("voice.mic_denied"));
      } else if (event.error !== "aborted") {
        setErrorMsg(t("voice.error"));
      }
      setIsRecording(false);
    };

    recognition.onend = () => setIsRecording(false);

    recognitionRef.current = recognition;
    recognition.start();
  }, [disabled, onResult, t]);

  const stopRecording = useCallback(() => {
    recognitionRef.current?.stop();
    setIsRecording(false);
  }, []);

  if (!isSupported) {
    return (
      <div className="flex items-center gap-2 text-sm text-[var(--muted-foreground)]">
        <MicOff className="h-4 w-4" aria-hidden="true" />
        <span>{t("voice.not_supported")}</span>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-1">
      <Button
        type="button"
        variant="outline"
        size="icon"
        onClick={isRecording ? stopRecording : startRecording}
        disabled={disabled}
        aria-label={isRecording ? t("voice.stop") : t("voice.start")}
        aria-pressed={isRecording}
        className={`relative h-10 w-10 transition-colors ${
          isRecording
            ? "border-red-500 text-red-500 hover:bg-red-50 dark:hover:bg-red-950"
            : "hover:border-blue-500 hover:text-blue-500"
        }`}
      >
        {isRecording ? (
          <>
            {/* Pulsing ring animation */}
            <span
              className="absolute inset-0 rounded-md animate-ping bg-red-400 opacity-30"
              aria-hidden="true"
            />
            <MicOff className="h-4 w-4 relative z-10" aria-hidden="true" />
          </>
        ) : (
          <Mic className="h-4 w-4" aria-hidden="true" />
        )}
      </Button>

      {isRecording && (
        <p className="text-xs text-red-500 animate-pulse" role="status">
          {t("voice.listening")}
        </p>
      )}

      {errorMsg && (
        <p className="text-xs text-red-500" role="alert">
          {errorMsg}
        </p>
      )}
    </div>
  );
}
