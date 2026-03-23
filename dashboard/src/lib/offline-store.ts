// IndexedDB wrapper for offline drug data caching.
// Stores drug records, interactions, and sync metadata for offline use.

const DB_NAME = "medgraph-offline";
const DB_VERSION = 1;

const STORE_DRUGS = "drugs";
const STORE_INTERACTIONS = "interactions";
const STORE_META = "meta";

export interface OfflineDrug {
  id: string;
  name: string;
  drug_class: string;
  enzymes: { enzyme_id: string; relation_type: string; strength: string }[];
}

export interface OfflineInteraction {
  id: string;
  drug_a_id: string;
  drug_b_id: string;
  severity: string;
  description: string;
}

export class OfflineStore {
  private db: IDBDatabase | null = null;

  async init(): Promise<void> {
    return new Promise((resolve, reject) => {
      const req = indexedDB.open(DB_NAME, DB_VERSION);

      req.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;

        if (!db.objectStoreNames.contains(STORE_DRUGS)) {
          const drugStore = db.createObjectStore(STORE_DRUGS, { keyPath: "id" });
          drugStore.createIndex("name", "name", { unique: false });
        }
        if (!db.objectStoreNames.contains(STORE_INTERACTIONS)) {
          const intStore = db.createObjectStore(STORE_INTERACTIONS, { keyPath: "id" });
          intStore.createIndex("drug_a_id", "drug_a_id", { unique: false });
          intStore.createIndex("drug_b_id", "drug_b_id", { unique: false });
        }
        if (!db.objectStoreNames.contains(STORE_META)) {
          db.createObjectStore(STORE_META, { keyPath: "key" });
        }
      };

      req.onsuccess = (event) => {
        this.db = (event.target as IDBOpenDBRequest).result;
        resolve();
      };

      req.onerror = () => reject(req.error);
    });
  }

  async syncFromServer(): Promise<void> {
    if (!this.db) await this.init();

    const [drugsRes, statsRes] = await Promise.all([
      fetch("/api/drugs/search?q=&limit=500"),
      fetch("/api/stats"),
    ]);

    if (!drugsRes.ok) throw new Error(`Sync failed: drugs ${drugsRes.status}`);

    const drugs: OfflineDrug[] = await drugsRes.json();

    await this._bulkPut(STORE_DRUGS, drugs);
    await this._putMeta("last_sync", new Date().toISOString());
    await this._putMeta("drug_count", drugs.length);

    // Sync stats for display
    if (statsRes.ok) {
      const stats = await statsRes.json();
      await this._putMeta("stats", JSON.stringify(stats));
    }
  }

  async searchDrugs(query: string): Promise<OfflineDrug[]> {
    if (!this.db) await this.init();

    return new Promise((resolve, reject) => {
      const tx = this.db!.transaction(STORE_DRUGS, "readonly");
      const store = tx.objectStore(STORE_DRUGS);
      const req = store.getAll();

      req.onsuccess = () => {
        const all: OfflineDrug[] = req.result;
        if (!query.trim()) {
          resolve(all.slice(0, 20));
          return;
        }
        const lower = query.toLowerCase();
        const matches = all
          .filter((d) => d.name.toLowerCase().includes(lower))
          .slice(0, 20);
        resolve(matches);
      };

      req.onerror = () => reject(req.error);
    });
  }

  async getInteractions(drugIds: string[]): Promise<OfflineInteraction[]> {
    if (!this.db) await this.init();
    if (drugIds.length < 2) return [];

    const idSet = new Set(drugIds);

    return new Promise((resolve, reject) => {
      const tx = this.db!.transaction(STORE_INTERACTIONS, "readonly");
      const store = tx.objectStore(STORE_INTERACTIONS);
      const req = store.getAll();

      req.onsuccess = () => {
        const all: OfflineInteraction[] = req.result;
        // Return interactions where both drugs are in the requested set
        const matches = all.filter(
          (i) => idSet.has(i.drug_a_id) && idSet.has(i.drug_b_id)
        );
        resolve(matches);
      };

      req.onerror = () => reject(req.error);
    });
  }

  async getLastSync(): Promise<string | null> {
    if (!this.db) await this.init();
    const val = await this._getMeta("last_sync");
    return typeof val === "string" ? val : null;
  }

  // ── Private helpers ────────────────────────────────────────────────────────

  private _bulkPut(storeName: string, items: object[]): Promise<void> {
    return new Promise((resolve, reject) => {
      const tx = this.db!.transaction(storeName, "readwrite");
      const store = tx.objectStore(storeName);
      for (const item of items) {
        store.put(item);
      }
      tx.oncomplete = () => resolve();
      tx.onerror = () => reject(tx.error);
    });
  }

  private _putMeta(key: string, value: unknown): Promise<void> {
    return new Promise((resolve, reject) => {
      const tx = this.db!.transaction(STORE_META, "readwrite");
      tx.objectStore(STORE_META).put({ key, value });
      tx.oncomplete = () => resolve();
      tx.onerror = () => reject(tx.error);
    });
  }

  private _getMeta(key: string): Promise<unknown> {
    return new Promise((resolve, reject) => {
      const tx = this.db!.transaction(STORE_META, "readonly");
      const req = tx.objectStore(STORE_META).get(key);
      req.onsuccess = () => resolve(req.result?.value ?? null);
      req.onerror = () => reject(req.error);
    });
  }
}

// Singleton for app-wide use
export const offlineStore = new OfflineStore();
