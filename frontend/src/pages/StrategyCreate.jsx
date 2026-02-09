import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { strategies } from '../services/api';
import StrategyForm from '../components/StrategyForm';

export default function StrategyCreate() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (data) => {
    setError('');
    setLoading(true);
    try {
      await strategies.create(data);
      navigate('/strategies');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create strategy');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl">
      <h1 className="text-2xl font-bold text-slate-100 mb-6">Create Strategy</h1>
      {error && (
        <div className="mb-4 p-3 rounded-lg bg-red-500/20 text-red-400 text-sm">{error}</div>
      )}
      <StrategyForm onSubmit={handleSubmit} loading={loading} />
    </div>
  );
}
