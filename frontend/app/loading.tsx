export default function Loading() {
  return (
    <div className="flex h-screen items-center justify-center bg-[#121212]">
      <div className="flex flex-col items-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-[#1a1a1a] border-t-[#FF5722]" />
        <p className="mt-4 text-sm text-gray-400">Loading Forge...</p>
      </div>
    </div>
  );
}
