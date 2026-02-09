import { format } from 'date-fns';

export default function TradeTable({ trades, loading }) {
  if (loading) {
    return (
      <div className="rounded-xl border border-slate-700 bg-slate-900 p-8 text-center text-slate-400">
        Loading trades...
      </div>
    );
  }

  if (!trades?.length) {
    return (
      <div className="rounded-xl border border-slate-700 bg-slate-900 p-8 text-center text-slate-400">
        No trades yet. Active strategies will execute automatically.
      </div>
    );
  }

  return (
    <div className="overflow-x-auto rounded-xl border border-slate-700 bg-slate-900">
      <table className="w-full">
        <thead>
          <tr className="border-b border-slate-700">
            <th className="text-left py-3 px-4 text-slate-400 font-medium">Time</th>
            <th className="text-left py-3 px-4 text-slate-400 font-medium">Type</th>
            <th className="text-left py-3 px-4 text-slate-400 font-medium">Symbol</th>
            <th className="text-left py-3 px-4 text-slate-400 font-medium">Qty</th>
            <th className="text-left py-3 px-4 text-slate-400 font-medium">Price</th>
            <th className="text-left py-3 px-4 text-slate-400 font-medium">PnL</th>
          </tr>
        </thead>
        <tbody>
          {trades.map((t) => (
            <tr key={t.id} className="border-b border-slate-800 hover:bg-slate-800/50">
              <td className="py-3 px-4 text-slate-400 text-sm">
                {format(new Date(t.created_at), 'MMM d, HH:mm:ss')}
              </td>
              <td className="py-3 px-4">
                <span
                  className={`font-medium ${
                    t.trade_type === 'BUY' ? 'text-emerald-400' : 'text-amber-400'
                  }`}
                >
                  {t.trade_type}
                </span>
              </td>
              <td className="py-3 px-4 font-mono text-slate-300">{t.symbol}</td>
              <td className="py-3 px-4 text-slate-300">{t.quantity}</td>
              <td className="py-3 px-4 text-slate-300">${t.price?.toFixed(2)}</td>
              <td className="py-3 px-4">
                {t.pnl != null ? (
                  <span
                    className={
                      t.pnl >= 0 ? 'text-emerald-400 font-medium' : 'text-red-400 font-medium'
                    }
                  >
                    {t.pnl >= 0 ? '+' : ''}${t.pnl?.toFixed(2)}
                    {t.pnl_percent != null && ` (${t.pnl_percent.toFixed(1)}%)`}
                  </span>
                ) : (
                  <span className="text-slate-500">—</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
