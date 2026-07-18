import TricoloreLine from './TricoloreLine.jsx';

export default function Header() {
  return (
    <header className="relative bg-rosetti-black text-rosetti-white">
      <TricoloreLine />
      <div className="mx-auto max-w-5xl px-4 py-8 text-center sm:py-10">
        <p className="text-xs uppercase tracking-[0.35em] text-rosetti-red">Ristorante Italiano</p>
        <h1 className="mt-2 font-serif text-4xl font-semibold tracking-wide sm:text-5xl">
          Rosetti
        </h1>
        <p className="mt-3 font-serif text-base italic text-rosetti-white/80 sm:text-lg">
          "Benvenuti alla nostra tavola"
        </p>
      </div>
      <TricoloreLine />
    </header>
  );
}
