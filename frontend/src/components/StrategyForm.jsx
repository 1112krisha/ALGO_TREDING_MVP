import { useState } from 'react';

export default function StrategyForm({ onSubmit, loading = false }) {
  const [form, setForm] = useState({
    symbol: 'AAPL',
    buy_price: 100,
    sell_price: 110,
    stop_loss: 95,
    quantity: 10,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: name.match(/price|quantity/) ? parseFloat(value) || 0 : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(form);
  };

  return (
    <form onSubmit={handleSubmit} className="bg-slate-900 border border-slate-700 rounded-xl p-6 shadow-xl">
      <h2 className="text-xl font-semibold text-slate-100 mb-4">Create Strategy</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm text-slate-400 mb-1">Symbol</label>
          <input
            type="text"
            name="symbol"
            value={form.symbol}
            onChange={handleChange}
            className="w-full px-4 py-2 rounded-lg bg-slate-800 border border-slate-600 text-slate-100 focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            placeholder="AAPL"
            required
          />
        </div>
        <div>
          <label className="block text-sm text-slate-400 mb-1">Quantity</label>
          <input
            type="number"
            name="quantity"
            value={form.quantity}
            onChange={handleChange}
            step="0.01"
            min="0.01"
            className="w-full px-4 py-2 rounded-lg bg-slate-800 border border-slate-600 text-slate-100 focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            required
          />
        </div>
        <div>
          <label className="block text-sm text-slate-400 mb-1">Buy Price</label>
          <input
            type="number"
            name="buy_price"
            value={form.buy_price}
            onChange={handleChange}
            step="0.01"
            min="0"
            className="w-full px-4 py-2 rounded-lg bg-slate-800 border border-slate-600 text-slate-100 focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            required
          />
        </div>
        <div>
          <label className="block text-sm text-slate-400 mb-1">Sell Price</label>
          <input
            type="number"
            name="sell_price"
            value={form.sell_price}
            onChange={handleChange}
            step="0.01"
            min="0"
            className="w-full px-4 py-2 rounded-lg bg-slate-800 border border-slate-600 text-slate-100 focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            required
          />
        </div>
        <div>
          <label className="block text-sm text-slate-400 mb-1">Stop Loss</label>
          <input
            type="number"
            name="stop_loss"
            value={form.stop_loss}
            onChange={handleChange}
            step="0.01"
            min="0"
            className="w-full px-4 py-2 rounded-lg bg-slate-800 border border-slate-600 text-slate-100 focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            required
          />
        </div>
      </div>
      <button
        type="submit"
        disabled={loading}
        className="mt-6 px-6 py-2.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-medium transition disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? 'Creating...' : 'Create Strategy'}
      </button>
    </form>
  );
}
