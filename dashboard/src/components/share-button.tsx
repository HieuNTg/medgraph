import { useState } from "react";
import { Share2, Check, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { shareResult } from "@/lib/api";

interface ShareButtonProps {
  analysisId: string;
}

export function ShareButton({ analysisId }: ShareButtonProps) {
  const [state, setState] = useState<"idle" | "loading" | "copied" | "error">("idle");

  const handleShare = async () => {
    setState("loading");
    try {
      const { url } = await shareResult(analysisId);
      await navigator.clipboard.writeText(url);
      setState("copied");
      setTimeout(() => setState("idle"), 2500);
    } catch {
      // Fallback: copy current URL with analysisId query param
      try {
        const fallback = `${window.location.origin}/shared/${analysisId}`;
        await navigator.clipboard.writeText(fallback);
        setState("copied");
        setTimeout(() => setState("idle"), 2500);
      } catch {
        setState("error");
        setTimeout(() => setState("idle"), 2500);
      }
    }
  };

  return (
    <Button
      variant="outline"
      size="sm"
      onClick={handleShare}
      disabled={state === "loading"}
      className="flex items-center gap-2"
      aria-label="Share this result"
    >
      {state === "loading" && <Loader2 className="h-4 w-4 animate-spin" />}
      {state === "copied" && <Check className="h-4 w-4 text-green-500" />}
      {(state === "idle" || state === "error") && <Share2 className="h-4 w-4" />}
      {state === "copied" ? "Link copied!" : state === "error" ? "Copy failed" : "Share"}
    </Button>
  );
}
