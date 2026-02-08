"use client";

import { useCallback, useState } from "react";

/**
 * Generic hook for API calls with loading and error state.
 */
export function useApi<T, Args extends unknown[]>(
  fetcher: (...args: Args) => Promise<T>
) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const run = useCallback(
    async (...args: Args) => {
      setLoading(true);
      setError(null);
      try {
        const result = await fetcher(...args);
        setData(result);
        return result;
      } catch (err) {
        const message = err instanceof Error ? err.message : "Request failed";
        setError(message);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [fetcher]
  );

  return { data, loading, error, run };
}
