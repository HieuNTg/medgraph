import { useState, useRef, useEffect, useCallback } from "react";
import { useQuery } from "@tanstack/react-query";
import { X, Search, Loader2, Plus } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { searchDrugs } from "@/lib/api";
import type { SearchResult } from "@/lib/types";

interface DrugInputProps {
  onSubmit: (drugs: string[]) => void;
  loading?: boolean;
}

export function DrugInput({ onSubmit, loading = false }: DrugInputProps) {
  const [query, setQuery] = useState("");
  const [debouncedQuery, setDebouncedQuery] = useState("");
  const [selectedDrugs, setSelectedDrugs] = useState<SearchResult[]>([]);
  const [open, setOpen] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(-1);
  const inputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Debounce query
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedQuery(query);
    }, 300);
    return () => clearTimeout(timer);
  }, [query]);

  const { data: results = [], isLoading: searching } = useQuery({
    queryKey: ["drug-search", debouncedQuery],
    queryFn: () => searchDrugs(debouncedQuery),
    enabled: debouncedQuery.trim().length >= 2,
    staleTime: 60_000,
  });

  // Filter out already-selected drugs
  const filteredResults = results.filter(
    (r) => !selectedDrugs.some((s) => s.id === r.id)
  );

  const shouldBeOpen = filteredResults.length > 0 && query.trim().length >= 2;
  useEffect(() => {
    setOpen(shouldBeOpen);
    setHighlightedIndex(-1);
  }, [shouldBeOpen]);

  // Close dropdown on outside click
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(e.target as Node) &&
        inputRef.current &&
        !inputRef.current.contains(e.target as Node)
      ) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const selectDrug = useCallback(
    (drug: SearchResult) => {
      if (selectedDrugs.length >= 10) return;
      if (selectedDrugs.some((d) => d.id === drug.id)) return;
      setSelectedDrugs((prev) => [...prev, drug]);
      setQuery("");
      setOpen(false);
      inputRef.current?.focus();
    },
    [selectedDrugs]
  );

  const removeDrug = useCallback((id: string) => {
    setSelectedDrugs((prev) => prev.filter((d) => d.id !== id));
  }, []);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (!open) return;
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setHighlightedIndex((i) => Math.min(i + 1, filteredResults.length - 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setHighlightedIndex((i) => Math.max(i - 1, 0));
    } else if (e.key === "Enter" && highlightedIndex >= 0) {
      e.preventDefault();
      selectDrug(filteredResults[highlightedIndex]);
    } else if (e.key === "Escape") {
      setOpen(false);
    }
  };

  const canSubmit = selectedDrugs.length >= 2 && !loading;

  return (
    <div className="space-y-4">
      {/* Selected drugs */}
      {selectedDrugs.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {selectedDrugs.map((drug) => (
            <Badge
              key={drug.id}
              variant="secondary"
              className="flex items-center gap-1 px-3 py-1.5 text-sm"
            >
              {drug.name}
              <button
                type="button"
                onClick={() => removeDrug(drug.id)}
                className="ml-1 rounded-full hover:bg-slate-300 dark:hover:bg-slate-600 transition-colors"
                aria-label={`Remove ${drug.name}`}
              >
                <X className="h-3 w-3" />
              </button>
            </Badge>
          ))}
        </div>
      )}

      {/* Input + dropdown */}
      <div className="relative">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--muted-foreground)]" />
          <Input
            ref={inputRef}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            onFocus={() => {
              if (filteredResults.length > 0 && query.trim().length >= 2) {
                setOpen(true);
              }
            }}
            placeholder={
              selectedDrugs.length === 0
                ? "Search for a medication (e.g. Warfarin, Aspirin)..."
                : selectedDrugs.length >= 10
                ? "Maximum 10 drugs reached"
                : "Add another medication..."
            }
            disabled={selectedDrugs.length >= 10 || loading}
            className="pl-9"
            aria-label="Search medications"
            aria-autocomplete="list"
            aria-expanded={open}
          />
          {searching && (
            <Loader2 className="absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 animate-spin text-[var(--muted-foreground)]" />
          )}
        </div>

        {/* Dropdown */}
        {open && (
          <div
            ref={dropdownRef}
            className="absolute z-50 mt-1 w-full rounded-md border border-[var(--border)] bg-[var(--popover)] shadow-lg"
            role="listbox"
          >
            {filteredResults.map((drug, index) => (
              <button
                key={drug.id}
                role="option"
                aria-selected={index === highlightedIndex}
                onClick={() => selectDrug(drug)}
                onMouseEnter={() => setHighlightedIndex(index)}
                className={`flex w-full items-center gap-3 px-4 py-3 text-left text-sm hover:bg-[var(--accent)] transition-colors ${
                  index === highlightedIndex ? "bg-[var(--accent)]" : ""
                } ${index !== 0 ? "border-t border-[var(--border)]" : ""}`}
              >
                <Plus className="h-4 w-4 shrink-0 text-[var(--muted-foreground)]" />
                <div>
                  <div className="font-medium text-[var(--foreground)]">{drug.name}</div>
                  <div className="text-xs text-[var(--muted-foreground)]">
                    {drug.drug_class && (
                      <span>{drug.drug_class}</span>
                    )}
                    {drug.brand_names.length > 0 && (
                      <span>
                        {drug.drug_class ? " · " : ""}
                        {drug.brand_names.slice(0, 3).join(", ")}
                      </span>
                    )}
                  </div>
                </div>
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="flex items-center justify-between">
        <p className="text-sm text-[var(--muted-foreground)]">
          {selectedDrugs.length === 0 && "Add at least 2 medications to check interactions."}
          {selectedDrugs.length === 1 && "Add 1 more medication to check interactions."}
          {selectedDrugs.length >= 2 && `${selectedDrugs.length} medications selected.`}
        </p>
        <Button
          onClick={() => onSubmit(selectedDrugs.map((d) => d.name))}
          disabled={!canSubmit}
          size="lg"
          className="min-w-[200px]"
        >
          {loading ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              Analyzing...
            </>
          ) : (
            "Check Interactions"
          )}
        </Button>
      </div>
    </div>
  );
}
