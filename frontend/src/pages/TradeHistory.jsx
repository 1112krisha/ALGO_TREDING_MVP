import { useEffect, useState } from 'react';
import { trades } from '../services/api';
import TradeTable from '../components/TradeTable';
import PnLCard from '../components/PnLCard';

export default function TradeHistory() {
  const [tradesList, setTradesList] = useState([]);
  const [pnl, setPnl] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetch = async () => {
    try {
      const [tRes, pRes] = await Promise.all([
        trades.list(),
        trades.pnl(),
      ]);
      setTradesList(tRes.data);
      setPnl(pRes.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetch();
    const id = setInterval(fetch, 10000); // Refresh every 10s
    return () => clearInterval(id);
  }, []);

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-bold text-slate-100">Trade History & PnL</h1>
      <PnLCard pnl={pnl} loading={loading} />
      <div>
        <h2 className="text-lg font-semibold text-slate-100 mb-4">Trade Logs</h2>
        <TradeTable trades={tradesList} loading={loading} />
      </div>
    </div>
  );
}
