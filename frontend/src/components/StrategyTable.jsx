import { strategies as strategiesApi } from '../services/api';

export default function StrategyTable({ strategies: list, loading, onRefresh }) {
  const handleStart = async (id) => {
    try {
      await strategiesApi.start(id);
      onRefresh?.();
    } catch (e) {
      alert(e.response?.data?.detail || 'Failed to start');
    }
  };

  const handleStop = async (id) => {
    try {
      await strategiesApi.stop(id);
      onRefresh?.();
    } catch (e) {
      alert(e.response?.data?.detail || 'Failed to stop');
    }
  };

  if (loading) {
    return (
      <div className="rounded-xl border border-slate-700 bg-slate-900 p-8 text-center text-slate-400">
        Loading strategies...
      </div>
    );
  }

  if (!list?.length) {
    return (
      <div className="rounded-xl border border-slate-700 bg-slate-900 p-8 text-center text-slate-400">
        No strategies yet. Create one to get started.
      </div>
    );
  }

  return (
    <div className="overflow-x-auto rounded-xl border border-slate-700 bg-slate-900">
      <table className="w-full">
        <thead>
          <tr className="border-b border-slate-700">
            <th className="text-left py-3 px-4 text-slate-400 font-medium">Symbol</th>
            <th className="text-left py-3 px-4 text-slate-400 font-medium">Buy</th>
            <th className="text-left py-3 px-4 text-slate-400 font-medium">Sell</th>
            <th className="text-left py-3 px-4 text-slate-400 font-medium">Stop Loss</th>
            <th className="text-left py-3 px-4 text-slate-400 font-medium">Qty</th>
            <th className="text-left py-3 px-4 text-slate-400 font-medium">Status</th>
            <th className="text-left py-3 px-4 text-slate-400 font-medium">Actions</th>
          </tr>
        </thead>
        <tbody>
          {list.map((s) => (
            <tr key={s.id} className="border-b border-slate-800 hover:bg-slate-800/50">
              <td className="py-3 px-4 font-mono text-emerald-400">{s.symbol}</td>
              <td className="py-3 px-4 text-slate-300">{s.buy_price}</td>
              <td className="py-3 px-4 text-slate-300">{s.sell_price}</td>
              <td className="py-3 px-4 text-red-400">{s.stop_loss}</td>
              <td className="py-3 px-4 text-slate-300">{s.quantity}</td>
              <td className="py-3 px-4">
                <span
                  className={`inline-flex px-2 py-1 rounded text-xs font-medium ${
                    s.is_active ? 'bg-emerald-500/20 text-emerald-400' : 'bg-slate-600 text-slate-400'
                  }`}
                >
                  {s.is_active ? 'Active' : 'Stopped'}
                </span>
              </td>
              <td className="py-3 px-4">
                {s.is_active ? (
                  <button
                    onClick={() => handleStop(s.id)}
                    className="text-red-400 hover:text-red-300 text-sm"
                  >
                    Stop
                  </button>
                ) : (
                  <button
                    onClick={() => handleStart(s.id)}
                    className="text-emerald-400 hover:text-emerald-300 text-sm"
                  >
                    Start
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
