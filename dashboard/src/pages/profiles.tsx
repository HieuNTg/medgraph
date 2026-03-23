import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Plus, BookMarked, AlertCircle, X, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { ProfileCard } from "@/components/profile-card";
import { useAuth } from "@/lib/auth-context";
import { getProfiles, createProfile, updateProfile, deleteProfile } from "@/lib/api";
import type { MedicationProfile } from "@/lib/types";

interface ProfileForm {
  name: string;
  drug_ids_raw: string;
  notes: string;
}

const EMPTY_FORM: ProfileForm = { name: "", drug_ids_raw: "", notes: "" };

export function ProfilesPage() {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  const [profiles, setProfiles] = useState<MedicationProfile[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [editTarget, setEditTarget] = useState<MedicationProfile | null>(null);
  const [form, setForm] = useState<ProfileForm>(EMPTY_FORM);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) return;
    setLoading(true);
    getProfiles()
      .then(setProfiles)
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load profiles."))
      .finally(() => setLoading(false));
  }, [isAuthenticated]);

  const openNewForm = () => {
    setEditTarget(null);
    setForm(EMPTY_FORM);
    setShowForm(true);
  };

  const openEditForm = (profile: MedicationProfile) => {
    setEditTarget(profile);
    setForm({
      name: profile.name,
      drug_ids_raw: profile.drug_ids.join(", "),
      notes: profile.notes ?? "",
    });
    setShowForm(true);
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    const drug_ids = form.drug_ids_raw
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);
    try {
      if (editTarget) {
        const updated = await updateProfile(editTarget.id, {
          name: form.name,
          drug_ids,
          notes: form.notes || null,
        });
        setProfiles((prev) => prev.map((p) => (p.id === updated.id ? updated : p)));
      } else {
        const created = await createProfile(form.name, drug_ids, form.notes || undefined);
        setProfiles((prev) => [created, ...prev]);
      }
      setShowForm(false);
      setForm(EMPTY_FORM);
      setEditTarget(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save profile.");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm("Delete this profile?")) return;
    try {
      await deleteProfile(id);
      setProfiles((prev) => prev.filter((p) => p.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete profile.");
    }
  };

  const handleLoad = (profile: MedicationProfile) => {
    navigate("/checker", { state: { preloadedDrugs: profile.drug_ids } });
  };

  if (!isAuthenticated) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-16 sm:px-6 text-center space-y-4">
        <BookMarked className="mx-auto h-12 w-12 text-[var(--muted-foreground)]" />
        <h1 className="text-2xl font-bold text-[var(--foreground)]">Medication Profiles</h1>
        <p className="text-[var(--muted-foreground)]">
          Sign in to save and manage your medication profiles.
        </p>
        <Button onClick={() => navigate("/login")}>Sign in</Button>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 lg:px-8 space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-[var(--primary)]">
            <BookMarked className="h-5 w-5 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-[var(--foreground)]">Medication Profiles</h1>
            <p className="text-sm text-[var(--muted-foreground)]">Save drug combinations for quick access.</p>
          </div>
        </div>
        <Button onClick={openNewForm} className="flex items-center gap-2">
          <Plus className="h-4 w-4" />
          New Profile
        </Button>
      </div>

      {error && (
        <div role="alert" className="flex items-start gap-3 rounded-lg border border-red-200 bg-red-50 p-4 text-red-800 dark:border-red-800 dark:bg-red-950 dark:text-red-300">
          <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
          <p className="text-sm">{error}</p>
        </div>
      )}

      {/* Inline form */}
      {showForm && (
        <div className="rounded-xl border border-[var(--border)] bg-[var(--card)] p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="font-semibold text-[var(--foreground)]">
              {editTarget ? "Edit Profile" : "New Profile"}
            </h2>
            <button
              type="button"
              onClick={() => { setShowForm(false); setEditTarget(null); }}
              className="rounded-md p-1 hover:bg-[var(--accent)] transition-colors"
              aria-label="Close form"
            >
              <X className="h-4 w-4 text-[var(--muted-foreground)]" />
            </button>
          </div>
          <form onSubmit={handleSave} className="space-y-4">
            <div className="space-y-1">
              <label className="text-sm font-medium text-[var(--foreground)]">Profile name</label>
              <input
                required
                value={form.name}
                onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
                placeholder="e.g. Morning medications"
                className="w-full rounded-md border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-sm text-[var(--foreground)] placeholder:text-[var(--muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
              />
            </div>
            <div className="space-y-1">
              <label className="text-sm font-medium text-[var(--foreground)]">
                Drug IDs <span className="text-[var(--muted-foreground)] font-normal">(comma-separated)</span>
              </label>
              <input
                required
                value={form.drug_ids_raw}
                onChange={(e) => setForm((f) => ({ ...f, drug_ids_raw: e.target.value }))}
                placeholder="warfarin, aspirin, metformin"
                className="w-full rounded-md border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-sm text-[var(--foreground)] placeholder:text-[var(--muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
              />
            </div>
            <div className="space-y-1">
              <label className="text-sm font-medium text-[var(--foreground)]">
                Notes <span className="text-[var(--muted-foreground)] font-normal">(optional)</span>
              </label>
              <textarea
                rows={2}
                value={form.notes}
                onChange={(e) => setForm((f) => ({ ...f, notes: e.target.value }))}
                placeholder="Any notes about this profile..."
                className="w-full rounded-md border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-sm text-[var(--foreground)] placeholder:text-[var(--muted-foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)] resize-none"
              />
            </div>
            <div className="flex justify-end gap-2">
              <Button
                type="button"
                variant="outline"
                onClick={() => { setShowForm(false); setEditTarget(null); }}
              >
                Cancel
              </Button>
              <Button type="submit" disabled={saving}>
                {saving ? (
                  <span className="flex items-center gap-2">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Saving...
                  </span>
                ) : (
                  editTarget ? "Save changes" : "Create profile"
                )}
              </Button>
            </div>
          </form>
        </div>
      )}

      {/* Profile list */}
      {loading ? (
        <div className="flex items-center gap-3 text-sm text-[var(--muted-foreground)]">
          <Loader2 className="h-4 w-4 animate-spin" />
          Loading profiles...
        </div>
      ) : profiles.length === 0 ? (
        <div className="rounded-xl border border-dashed border-[var(--border)] p-12 text-center space-y-3">
          <BookMarked className="mx-auto h-10 w-10 text-[var(--muted-foreground)]" />
          <p className="text-[var(--muted-foreground)]">No profiles yet. Create one to save your medication combinations.</p>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          {profiles.map((profile) => (
            <ProfileCard
              key={profile.id}
              profile={profile}
              onLoad={handleLoad}
              onEdit={openEditForm}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}
    </div>
  );
}
