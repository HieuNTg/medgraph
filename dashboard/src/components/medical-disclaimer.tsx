import { AlertTriangle } from "lucide-react";
import { useTranslation } from "react-i18next";

interface MedicalDisclaimerProps {
  full?: boolean;
}

export function MedicalDisclaimer({ full = false }: MedicalDisclaimerProps) {
  const { t } = useTranslation();

  return (
    <div className="flex gap-3 rounded-lg border border-amber-200 bg-amber-50 p-3 text-amber-900 dark:border-amber-800 dark:bg-amber-950 dark:text-amber-200">
      <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-amber-600 dark:text-amber-400" />
      <div className="text-sm">
        {full ? (
          <div className="space-y-2">
            <p className="font-semibold">{t("disclaimer.title")}</p>
            <p>{t("disclaimer.full_p1")}</p>
            <p>{t("disclaimer.full_p2")}</p>
            <p>{t("disclaimer.full_p3")}</p>
          </div>
        ) : (
          <p>
            <span className="font-semibold">{t("disclaimer.title")}.</span>{" "}
            {t("disclaimer.short")}
          </p>
        )}
      </div>
    </div>
  );
}
