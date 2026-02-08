/**
 * Format date for display
 */
export function formatDate(value: string | Date | null | undefined): string {
  if (value == null) return "—";
  const d = typeof value === "string" ? new Date(value) : value;
  return d.toLocaleDateString();
}

/**
 * Format time for display (HH:mm)
 */
export function formatTime(value: string | null | undefined): string {
  if (value == null) return "—";
  if (typeof value === "string" && value.includes("T")) {
    return new Date(value).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }
  return value;
}

/**
 * Format number of days
 */
export function formatDays(days: number): string {
  return `${days} day${days !== 1 ? "s" : ""}`;
}
