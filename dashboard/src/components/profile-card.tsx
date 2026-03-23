import { Pencil, Trash2, Pill } from "lucide-react";
import { Button } from "@/components/ui/button";
import type { MedicationProfile } from "@/lib/types";

interface ProfileCardProps {
  profile: MedicationProfile;
  onLoad: (profile: MedicationProfile) => void;
  onEdit: (profile: MedicationProfile) => void;
  onDelete: (id: string) => void;
}

export function ProfileCard({ profile, onLoad, onEdit, onDelete }: ProfileCardProps) {
  const updatedAt = new Date(profile.updated_at).toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });

  return (
    <div className="rounded-xl border border-[var(--border)] bg-[var(--card)] p-5 space-y-3 hover:border-[var(--primary)] transition-colors">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-3 min-w-0">
          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-[var(--primary)]/10">
            <Pill className="h-4 w-4 text-[var(--primary)]" />
          </div>
          <div className="min-w-0">
            <h3 className="font-semibold text-[var(--foreground)] truncate">{profile.name}</h3>
            <p className="text-xs text-[var(--muted-foreground)]">
              {profile.drug_ids.length} drug{profile.drug_ids.length !== 1 ? "s" : ""} · Updated {updatedAt}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-1 shrink-0">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => onEdit(profile)}
            aria-label="Edit profile"
            className="h-8 w-8"
          >
            <Pencil className="h-3.5 w-3.5" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => onDelete(profile.id)}
            aria-label="Delete profile"
            className="h-8 w-8 text-red-500 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-950"
          >
            <Trash2 className="h-3.5 w-3.5" />
          </Button>
        </div>
      </div>

      {profile.notes && (
        <p className="text-sm text-[var(--muted-foreground)] line-clamp-2">{profile.notes}</p>
      )}

      <Button
        variant="outline"
        size="sm"
        onClick={() => onLoad(profile)}
        className="w-full"
      >
        Load into Checker
      </Button>
    </div>
  );
}
