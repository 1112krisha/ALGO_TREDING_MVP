import { Link, useNavigate } from 'react-router-dom';

export default function Navbar() {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');

  const logout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <nav className="border-b border-slate-800 bg-slate-900/80 backdrop-blur">
      <div className="container mx-auto px-4 max-w-7xl">
        <div className="flex items-center justify-between h-14">
          <Link to="/" className="text-lg font-semibold text-emerald-400">
            Algo Trading MVP
          </Link>
          <div className="flex items-center gap-6">
            {token ? (
              <>
                <Link to="/strategies" className="text-slate-300 hover:text-white transition">
                  Strategies
                </Link>
                <Link to="/strategies/new" className="text-slate-300 hover:text-white transition">
                  New Strategy
                </Link>
                <Link to="/trades" className="text-slate-300 hover:text-white transition">
                  Trades
                </Link>
                <button
                  onClick={logout}
                  className="text-slate-400 hover:text-red-400 transition text-sm"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="text-slate-300 hover:text-white transition">
                  Login
                </Link>
                <Link to="/register" className="text-emerald-400 hover:text-emerald-300 transition">
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
