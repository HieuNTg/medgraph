import { AlertTriangle } from "lucide-react";

interface MedicalDisclaimerProps {
  full?: boolean;
}

export function MedicalDisclaimer({ full = false }: MedicalDisclaimerProps) {
  return (
    <div className="flex gap-3 rounded-lg border border-amber-200 bg-amber-50 p-3 text-amber-900 dark:border-amber-800 dark:bg-amber-950 dark:text-amber-200">
      <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-amber-600 dark:text-amber-400" />
      <div className="text-sm">
        {full ? (
          <div className="space-y-2">
            <p className="font-semibold">Medical Disclaimer</p>
            <p>
              MEDGRAPH is provided for informational and educational purposes
              only. The information presented does not constitute medical advice
              and is not a substitute for professional medical judgment,
              diagnosis, or treatment.
            </p>
            <p>
              Always seek the advice of your physician, pharmacist, or other
              qualified healthcare provider with any questions you may have
              regarding drug interactions, medications, or medical conditions.
              Never disregard professional medical advice or delay seeking it
              because of something you have read on this platform.
            </p>
            <p>
              Drug interaction data is based on publicly available databases
              (DrugBank, OpenFDA, RxNorm) and may not be complete or current.
              Always verify with your healthcare provider.
            </p>
          </div>
        ) : (
          <p>
            <span className="font-semibold">For informational purposes only.</span>{" "}
            Not medical advice. Always consult your healthcare provider before
            making any medication decisions.
          </p>
        )}
      </div>
    </div>
  );
}
