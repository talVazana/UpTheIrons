'use client';

import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="flex h-screen flex-col items-center justify-center bg-[#121212] p-4 text-center">
      <h2 className="text-xl font-bold text-white">Something went wrong</h2>
      <p className="mt-2 text-gray-400">The forge encountered an error.</p>
      <button
        onClick={() => reset()}
        className="mt-6 rounded-md bg-[#FF5722] px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-orange-600 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-orange-500 focus-visible:ring-offset-2 focus-visible:ring-offset-[#121212]"
      >
        Try again
      </button>
    </div>
  );
}
