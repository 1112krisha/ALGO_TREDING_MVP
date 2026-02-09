export default function PnLCard({ pnl, loading }) {
  if (loading) {
    return (
      <div className="rounded-xl border border-slate-700 bg-slate-900 p-6 animate-pulse">
        <div className="h-8 bg-slate-700 rounded w-1/2 mb-4" />
        <div className="h-12 bg-slate-700 rounded w-1/3" />
      </div>
    );
  }

  const isProfit = pnl?.total_pnl >= 0;

  return (
    <div className="rounded-xl border border-slate-700 bg-slate-900 p-6">
      <h3 className="text-slate-400 text-sm font-medium mb-2">Simulated PnL</h3>
      <p
        className={`text-3xl font-bold ${
          isProfit ? 'text-emerald-400' : 'text-red-400'
        }`}
      >
        {pnl?.total_pnl >= 0 ? '+' : ''}${pnl?.total_pnl?.toFixed(2) ?? '0.00'}
      </p>
      <div className="mt-4 flex gap-4 text-sm text-slate-500">
        <span>{pnl?.total_trades ?? 0} trades</span>
        <span className="text-emerald-500">{pnl?.winning_trades ?? 0} wins</span>
        <span className="text-red-500">{pnl?.losing_trades ?? 0} losses</span>
      </div>
    </div>
  );
}
