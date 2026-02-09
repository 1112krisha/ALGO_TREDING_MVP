import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { strategies } from '../services/api';
import StrategyTable from '../components/StrategyTable';

export default function StrategyList() {
  const [list, setList] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetch = async () => {
    try {
      const { data } = await strategies.list();
      setList(data);
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
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-100">Strategies</h1>
        <Link
          to="/strategies/new"
          className="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-medium transition"
        >
          New Strategy
        </Link>
      </div>
      <StrategyTable strategies={list} loading={loading} onRefresh={fetch} />
    </div>
  );
}
