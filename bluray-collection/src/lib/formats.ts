// Formats de support disponibles pour un titre de la collection.
export const FORMATS = [
  "Blu-ray",
  "4K UHD Blu-ray",
  "Blu-ray 3D",
  "Steelbook",
  "Coffret",
  "DVD",
] as const;

export type Format = (typeof FORMATS)[number];

export const DEFAULT_FORMAT: Format = "Blu-ray";

export function isFormat(v: unknown): v is Format {
  return typeof v === "string" && (FORMATS as readonly string[]).includes(v);
}
