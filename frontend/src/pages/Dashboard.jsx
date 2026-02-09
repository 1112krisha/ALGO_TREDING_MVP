import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { strategies, trades } from '../services/api';
import StrategyTable from '../components/StrategyTable';
import PnLCard from '../components/PnLCard';

export default function Dashboard() {
  const [strategiesList, setStrategiesList] = useState([]);
  const [pnl, setPnl] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetch = async () => {
    try {
      const [sRes, pRes] = await Promise.all([
        strategies.list(),
        trades.pnl(),
      ]);
      setStrategiesList(sRes.data);
      setPnl(pRes.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetch();
  }, []);

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-100">Dashboard</h1>
        <Link
          to="/strategies/new"
          className="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-medium transition"
        >
          New Strategy
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <PnLCard pnl={pnl} loading={loading} />
        <div className="rounded-xl border border-slate-700 bg-slate-900 p-6">
          <h3 className="text-slate-400 text-sm font-medium mb-2">Paper Trading</h3>
          <p className="text-slate-300 text-sm">
            This is a simulated environment. No real money is involved. Create strategies and
            watch the engine execute trades based on mock market prices.
          </p>
        </div>
      </div>

      <div>
        <h2 className="text-lg font-semibold text-slate-100 mb-4">Active Strategies</h2>
        <StrategyTable strategies={strategiesList} loading={loading} onRefresh={fetch} />
      </div>
    </div>
  );
}
