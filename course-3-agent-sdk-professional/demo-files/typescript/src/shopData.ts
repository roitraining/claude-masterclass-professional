// Fake backend for Brightwater Outfitters: a thin accessor over data/shop.json. All data is fictional.
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const dataDir = fileURLToPath(new URL("../../data/", import.meta.url));
const shop = JSON.parse(readFileSync(dataDir + "shop.json", "utf-8"));
const notes = JSON.parse(readFileSync(dataDir + "order_notes.json", "utf-8"));

export const AS_OF: string = shop.as_of;
export const POLICY_TOPICS: string[] = Object.keys(shop.policies).sort();

// The record carries as_of so date questions ("can I still return this?") are
// answered against the fixture's own date rather than whatever the model believes
// today is. Without it the return-window answers drift as real time passes the window.
export function getOrder(orderId: string): Record<string, unknown> | null {
  const key = (orderId ?? "").trim().toUpperCase();
  const rec = shop.orders[key];
  return rec ? { order_id: key, as_of: AS_OF, ...rec } : null;
}

export function getCustomer(email: string): Record<string, unknown> | null {
  const key = (email ?? "").trim().toLowerCase();
  const rec = shop.customers[key];
  return rec ? { email: key, ...rec } : null;
}

export function getPolicy(topic: string): string | null {
  return shop.policies[(topic ?? "").trim()] ?? null;
}

export function getNotes(orderId: string): string[] | null {
  const key = (orderId ?? "").trim().toUpperCase();
  if (!shop.orders[key]) return null;
  return [...(notes[key] ?? [])];
}
