export default function TricoloreLine({ className = '' }) {
  return (
    <div className={`tricolore-line ring-1 ring-black/10 ${className}`} aria-hidden="true">
      <span className="bg-rosetti-green" />
      <span className="bg-white" />
      <span className="bg-rosetti-red" />
    </div>
  );
}
