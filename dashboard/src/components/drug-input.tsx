import { useState, useRef, useEffect, useCallback, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { X, Search, Loader2, Plus } from "lucide-react";
import { useTranslation } from "react-i18next";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { searchDrugs } from "@/lib/api";
import type { SearchResult } from "@/lib/types";
import { VoiceInput } from "./voice-input";

interface DrugInputProps {
  onSubmit: (drugs: string[]) => void;
  loading?: boolean;
}

export function DrugInput({ onSubmit, loading = false }: DrugInputProps) {
  const { t } = useTranslation();
  const [query, setQuery] = useState("");
  const [debouncedQuery, setDebouncedQuery] = useState("");
  const [selectedDrugs, setSelectedDrugs] = useState<SearchResult[]>([]);
  const [forceClosed, setForceClosed] = useState(false);
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
  const filteredResults = useMemo(
    () => results.filter((r) => !selectedDrugs.some((s) => s.id === r.id)),
    [results, selectedDrugs]
  );

  // Derive open state — no useEffect needed
  const open = filteredResults.length > 0 && query.trim().length >= 2 && !forceClosed;

  // Reset highlightedIndex when query changes
  useEffect(() => {
    setHighlightedIndex(-1);
    setForceClosed(false);
  }, [query]);

  // Close dropdown on outside click
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(e.target as Node) &&
        inputRef.current &&
        !inputRef.current.contains(e.target as Node)
      ) {
        setForceClosed(true);
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
      setForceClosed(true);
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
      setForceClosed(true);
    }
  };

  const canSubmit = selectedDrugs.length >= 2 && !loading;

  const getPlaceholder = () => {
    if (selectedDrugs.length === 0) return t("checker.search_placeholder");
    if (selectedDrugs.length >= 10) return t("checker.max_reached");
    return t("checker.search_placeholder_add");
  };

  const getHintText = () => {
    if (selectedDrugs.length === 0) return t("checker.add_hint_0");
    if (selectedDrugs.length === 1) return t("checker.add_hint_1");
    return t("checker.add_hint_n", { count: selectedDrugs.length });
  };

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
        <div className="flex items-start gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-[var(--muted-foreground)]" />
            <Input
              ref={inputRef}
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={handleKeyDown}
              onFocus={() => {
                setForceClosed(false);
              }}
              placeholder={getPlaceholder()}
              disabled={selectedDrugs.length >= 10 || loading}
              className="pl-9"
              role="combobox"
              aria-label={t("common.search")}
              aria-autocomplete="list"
              aria-expanded={open}
              aria-controls="drug-search-listbox"
              aria-activedescendant={
                open && highlightedIndex >= 0
                  ? `drug-option-${highlightedIndex}`
                  : undefined
              }
            />
            {searching && (
              <Loader2 className="absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 animate-spin text-[var(--muted-foreground)]" />
            )}
          </div>
          <VoiceInput
            onResult={(text) => {
              setQuery(text);
              setForceClosed(false);
              inputRef.current?.focus();
            }}
            disabled={selectedDrugs.length >= 10 || loading}
          />
        </div>

        {/* Dropdown */}
        {open && (
          <div
            ref={dropdownRef}
            id="drug-search-listbox"
            className="absolute z-50 mt-1 w-full rounded-md border border-[var(--border)] bg-[var(--popover)] shadow-lg"
            role="listbox"
          >
            {filteredResults.map((drug, index) => (
              <button
                key={drug.id}
                id={`drug-option-${index}`}
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
          {getHintText()}
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
              {t("checker.analyzing")}
            </>
          ) : (
            t("checker.check_button")
          )}
        </Button>
      </div>
    </div>
  );
}
