interface LoadingProps {
  spinning: boolean;
}

export default function Loading({ spinning }: LoadingProps) {
  return (
    spinning && (
      <div>
        <h1 className="animate-spin text-5xl">🔄</h1>
      </div>
    )
  );
}
